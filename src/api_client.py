
"""
Fetch protein data from the public UniProt REST API.
Supports pagination, retries, timeouts and logging.
Author: Shaheena Shajira
"""

import logging
import time

import requests

# UniProt REST API endpoint.
API_URL = "https://rest.uniprot.org/uniprotkb/search"

# Configure a module-level logger.
logger = logging.getLogger(__name__)


def fetch_proteins(size=5, max_pages=1, max_retries=3):
    """
    Fetch reviewed human protein records from UniProt.

    Args:
        size: Number of records requested per page.
        max_pages: Maximum number of pages to fetch.
        max_retries: Number of attempts for a failed request.

    Returns:
        A list of raw UniProt protein records.

    Raises:
        ValueError: If pagination or retry settings are invalid.
        requests.RequestException: If the API request ultimately fails.
        ValueError: If the API returns invalid JSON.
    """
    if size < 1 or max_pages < 1 or max_retries < 1:
        raise ValueError("size, max_pages and max_retries must be at least 1")

    params = {
        "query": "reviewed:true AND organism_id:9606",
        "format": "json",
        "size": size,
        "fields": "accession,protein_name,gene_names,organism_name",
    }

    proteins = []
    page_url = API_URL
    page_params = params

    with requests.Session() as session:
        for page_number in range(1, max_pages + 1):
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(
                        "Fetching page %s, attempt %s",
                        page_number,
                        attempt,
                    )

                    response = session.get(
                        page_url,
                        params=page_params,
                        timeout=30,
                    )
                    response.raise_for_status()
                    data = response.json()
                    break

                except (requests.RequestException, ValueError) as exc:
                    logger.warning(
                        "Page %s failed on attempt %s: %s",
                        page_number,
                        attempt,
                        exc,
                    )

                    if attempt == max_retries:
                        raise

                    # Brief exponential backoff before retrying.
                    time.sleep(2 ** (attempt - 1))

            results = data.get("results", [])

            if not isinstance(results, list):
                raise ValueError("Unexpected UniProt API response: results is not a list")

            if not results:
                logger.info("No more records returned; stopping pagination.")
                break

            proteins.extend(results)

            logger.info(
                "Page %s returned %s records",
                page_number,
                len(results),
            )

            # Follow the API's next-page link when one is provided.
            next_link = response.links.get("next", {}).get("url")

            if not next_link or page_number == max_pages:
                break

            page_url = next_link
            page_params = None

    logger.info("Fetched %s protein records in total", len(proteins))
    return proteins


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    records = fetch_proteins(size=5, max_pages=2)

    for protein in records:
        print(protein.get("primaryAccession"))
        print("-" * 40)
