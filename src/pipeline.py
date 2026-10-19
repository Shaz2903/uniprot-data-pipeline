
"""
Run the UniProt extraction, transformation and loading steps.
Author: Shaheena Shajira
"""

from src.api_client import fetch_proteins
from src.transform import transform_proteins
from src.storage import save_proteins


def run_pipeline():
    """Fetch, clean and save protein records."""
    # Extract protein records from the UniProt API.
    raw_records = fetch_proteins(size=5)
    print(f"Fetched {len(raw_records)} protein records.")

    # Clean the records before storing them.
    cleaned_records = transform_proteins(raw_records)
    print(f"Cleaned {len(cleaned_records)} protein records.")

    # Load the cleaned records into SQLite.
    save_proteins(cleaned_records)
    print("Protein records saved successfully.")


if __name__ == "__main__":
    run_pipeline()
