
"""
Store cleaned UniProt records in a SQLite database.
Author: Shaheena Shajira
"""

import sqlite3

DATABASE_PATH = "data/uniprot.db"


def save_proteins(records):
    """Create the protein table and insert new or updated records."""
    # Open a connection to the local database.
    with sqlite3.connect(DATABASE_PATH) as connection:
        # Create the table if it does not already exist.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS proteins (
                accession TEXT PRIMARY KEY,
                protein_name TEXT,
                organism TEXT
            )
        """)

        # Insert each protein or update its details if it exists.
        connection.executemany("""
            INSERT INTO proteins (accession, protein_name, organism)
            VALUES (?, ?, ?)
            ON CONFLICT(accession) DO UPDATE SET
                protein_name = excluded.protein_name,
                organism = excluded.organism
        """, [
            (
                protein["accession"],
                protein["protein_name"],
                protein["organism"]
            )
            for protein in records
        ])
