
"""
Tests for the UniProt API client.
Author: Shaheena Shajira
"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from src.api_client import fetch_proteins


def make_response(results, links=None):
    """Prepare a fake API response so tests don't need a real API call."""
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"results": results}
    response.links = links or {}
    return response


def make_session(responses):
    """Set up a fake session that returns the responses we want to test."""
    session = MagicMock()
    session.__enter__.return_value = session
    session.get.side_effect = responses
    return session


def test_fetch_proteins_successfully():
    """Check that the client returns protein records from the API."""
    response = make_response([
        {"primaryAccession": "P12345"},
        {"primaryAccession": "Q12345"},
    ])
    session = make_session([response])

    # Use a fake session so the test doesn't depend on the live UniProt API.
    with patch("src.api_client.requests.Session", return_value=session):
        records = fetch_proteins(size=2)

    assert len(records) == 2
    assert records[0]["primaryAccession"] == "P12345"


def test_fetch_proteins_follows_next_page():
    """Check that records from multiple pages are combined."""
    first_response = make_response(
        [{"primaryAccession": "P12345"}],
        links={"next": {"url": "https://example.com/next-page"}},
    )
    second_response = make_response([
        {"primaryAccession": "Q12345"}
    ])
    session = make_session([first_response, second_response])

    # Simulate two pages to check that pagination works as expected.
    with patch("src.api_client.requests.Session", return_value=session):
        records = fetch_proteins(size=1, max_pages=2)

    assert len(records) == 2
    assert session.get.call_count == 2


def test_fetch_proteins_retries_after_temporary_failure():
    """Check that the client retries when a request fails temporarily."""
    response = make_response([{"primaryAccession": "P12345"}])
    session = make_session([
        requests.ConnectionError("Temporary connection failure"),
        response,
    ])

    # Skip the waiting period so the test runs quickly.
    with (
        patch("src.api_client.requests.Session", return_value=session),
        patch("src.api_client.time.sleep"),
    ):
        records = fetch_proteins(max_retries=2)

    assert len(records) == 1
    assert session.get.call_count == 2


def test_fetch_proteins_raises_after_all_retries_fail():
    """Check that the error is raised when every retry fails."""
    session = make_session([
        requests.ConnectionError("Connection failed"),
        requests.ConnectionError("Connection failed again"),
    ])

    with (
        patch("src.api_client.requests.Session", return_value=session),
        patch("src.api_client.time.sleep"),
    ):
        # The client should stop retrying and report the final error.
        with pytest.raises(requests.RequestException):
            fetch_proteins(max_retries=2)

    assert session.get.call_count == 2


def test_fetch_proteins_rejects_invalid_results_structure():
    """Check that an unexpected API response is handled correctly."""
    response = make_response("not-a-list")
    session = make_session([response])

    with patch("src.api_client.requests.Session", return_value=session):
        # The results field must be a list of protein records.
        with pytest.raises(ValueError, match="results is not a list"):
            fetch_proteins()


def test_fetch_proteins_rejects_invalid_settings():
    """Check that invalid settings are rejected before making a request."""
    # Page size, number of pages and retry count must all be positive.
    with pytest.raises(ValueError):
        fetch_proteins(size=0)

    with pytest.raises(ValueError):
        fetch_proteins(max_pages=0)

    with pytest.raises(ValueError):
        fetch_proteins(max_retries=0)
