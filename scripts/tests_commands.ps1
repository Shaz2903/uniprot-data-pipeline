# Run automated tests
python -m pytest -v

# Run the ETL pipeline
python -m src.pipeline

# Check stored protein records
python -c "import sqlite3; c=sqlite3.connect('data/uniprot.db'); print(c.execute('SELECT accession, protein_name, organism FROM proteins').fetchall()); c.close()"