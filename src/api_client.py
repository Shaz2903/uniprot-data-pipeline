
"""
Fetch protein data from the public UniProt REST API.
Author: Shaheena Shajira
"""

import requests

# Use the UniProt API to search for protein records.
API_URL = "https://rest.uniprot.org/uniprotkb/search"


def fetch_proteins(size=5):
    """Fetch a small set of reviewed human protein records."""
    params = {
        "query": "reviewed:true AND organism_id:9606",
        "format": "json",
        "size": size,
        "fields": "accession,protein_name,gene_names,organism_name"
    }

    # Send the search request and check for HTTP errors.
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    # Convert the JSON response into a Python dictionary.
    data = response.json()

    return data.get("results", [])


if __name__ == "__main__":
    # Print a few records to check that the API works.
    for protein in fetch_proteins():
        print(protein["primaryAccession"])
        print(protein.get("proteinDescription", {}))
        print("-" * 40)
