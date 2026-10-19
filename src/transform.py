
"""
Clean and standardise protein records from UniProt.
Author: Shaheena Shajira
"""


def transform_proteins(records):
    """Keep useful fields and remove duplicate protein accessions."""
    cleaned_records = []
    seen_accessions = set()

    for record in records:
        # Skip records without an accession number.
        accession = record.get("primaryAccession")
        if not accession or accession in seen_accessions:
            continue

        # Extract the protein name from the nested API response.
        description = record.get("proteinDescription", {})
        recommended_name = description.get(
            "recommendedName", {}
        )
        protein_name = recommended_name.get(
            "fullName", {}
        ).get("value")

        # Store only the fields needed for the pipeline.
        cleaned_records.append({
            "accession": accession,
            "protein_name": protein_name,
            "organism": record.get("organism", {}).get("scientificName")
        })

        seen_accessions.add(accession)

    return cleaned_records
