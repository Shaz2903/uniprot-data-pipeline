
"""
Test protein data cleaning and duplicate handling.
Author: Shaheena Shajira
"""

from src.transform import transform_proteins


def test_duplicate_accessions_are_removed():
    """Keep only one record for each protein accession."""
    records = [
        {
            "primaryAccession": "P01308",
            "proteinDescription": {
                "recommendedName": {
                    "fullName": {"value": "Insulin"}
                }
            },
            "organism": {"scientificName": "Homo sapiens"}
        },
        {
            "primaryAccession": "P01308",
            "proteinDescription": {},
            "organism": {"scientificName": "Homo sapiens"}
        }
    ]

    # Only one record should remain for the repeated accession.
    result = transform_proteins(records)

    assert len(result) == 1
    assert result[0]["accession"] == "P01308"
    assert result[0]["protein_name"] == "Insulin"


def test_records_without_accession_are_skipped():
    """Ignore records that do not have an accession number."""
    result = transform_proteins([{"proteinDescription": {}}])

    assert result == []
