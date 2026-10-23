
"""
Tests for the UniProt data pipeline.
Author: Shaheena Shajira
"""

from unittest.mock import patch

import pytest

from src.pipeline import run_pipeline


def test_pipeline_runs_successfully():
    """Check that the pipeline fetches, transforms and saves records."""
    raw_records = [{"primaryAccession": "P12345"}]
    cleaned_records = [
        {
            "accession": "P12345",
            "protein_name": "Example protein",
            "organism": "Homo sapiens",
        }
    ]

    # Replace the real functions so we can test the pipeline flow in isolation.
    with (
        patch("src.pipeline.fetch_proteins", return_value=raw_records) as fetch,
        patch(
            "src.pipeline.transform_proteins",
            return_value=cleaned_records,
        ) as transform,
        patch("src.pipeline.save_proteins") as save,
    ):
        run_pipeline()

    # Make sure each step received the expected input.
    fetch.assert_called_once_with(size=5)
    transform.assert_called_once_with(raw_records)
    save.assert_called_once_with(cleaned_records)


def test_pipeline_stops_if_fetch_fails():
    """Check that a fetch failure prevents later steps from running."""
    with (
        patch(
            "src.pipeline.fetch_proteins",
            side_effect=RuntimeError("API unavailable"),
        ),
        patch("src.pipeline.transform_proteins") as transform,
        patch("src.pipeline.save_proteins") as save,
    ):
        # The pipeline should report the failure instead of hiding it.
        with pytest.raises(RuntimeError, match="API unavailable"):
            run_pipeline()

    transform.assert_not_called()
    save.assert_not_called()


def test_pipeline_stops_if_database_save_fails():
    """Check that a database failure is raised to the caller."""
    raw_records = [{"primaryAccession": "P12345"}]
    cleaned_records = [{"accession": "P12345"}]

    with (
        patch("src.pipeline.fetch_proteins", return_value=raw_records),
        patch(
            "src.pipeline.transform_proteins",
            return_value=cleaned_records,
        ),
        patch(
            "src.pipeline.save_proteins",
            side_effect=RuntimeError("Database unavailable"),
        ),
    ):
        with pytest.raises(RuntimeError, match="Database unavailable"):
            run_pipeline()
