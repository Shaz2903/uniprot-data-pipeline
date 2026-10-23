
"""
Run the UniProt extraction, transformation and loading steps.
Author: Shaheena Shajira
"""

import logging

from src.api_client import fetch_proteins
from src.transform import transform_proteins
from src.storage import save_proteins


# Track pipeline progress and errors using a logger.
logger = logging.getLogger(__name__)


def run_pipeline():
    """Fetch, clean and save protein records."""
    try:
        # Extract protein records from the UniProt API.
        raw_records = fetch_proteins(size=5)

        # Original print statement:
        # print(f"Fetched {len(raw_records)} protein records.")
        logger.info("Fetched %s protein records.", len(raw_records))

        # Clean the records before storing them.
        cleaned_records = transform_proteins(raw_records)

        # Original print statement:
        # print(f"Cleaned {len(cleaned_records)} protein records.")
        logger.info("Cleaned %s protein records.", len(cleaned_records))

        # Load the cleaned records into the SQLite database.
        save_proteins(cleaned_records)

        # Original print statement:
        # print("Protein records saved successfully.")
        logger.info("Protein records saved successfully.")

    except Exception:
        # Log the full error details and let the failure reach the caller.
        logger.exception("The UniProt data pipeline failed.")
        raise


if __name__ == "__main__":
    # Display informational messages and errors in the terminal.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    run_pipeline()
