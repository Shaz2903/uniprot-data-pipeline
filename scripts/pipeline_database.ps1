
# UniProt ETL Pipeline and Database Commands
# Author: Shaheena Shajira

Write-Host "`n=== 1. Run the UniProt ETL Pipeline ===" -ForegroundColor Cyan
python -m src.pipeline

if ($LASTEXITCODE -ne 0) {
    Write-Host "Pipeline failed. Check the error above." -ForegroundColor Red
    exit 1
}

Write-Host "`n=== 2. Check Database Row Count ===" -ForegroundColor Cyan
python -c "import sqlite3; c=sqlite3.connect('data/uniprot.db'); print('Total proteins:', c.execute('SELECT COUNT(*) FROM proteins').fetchone()[0]); c.close()"

Write-Host "`n=== 3. Check Unique Protein Accessions ===" -ForegroundColor Cyan
python -c "import sqlite3; c=sqlite3.connect('data/uniprot.db'); print('Unique accessions:', c.execute('SELECT COUNT(DISTINCT accession) FROM proteins').fetchone()[0]); c.close()"

Write-Host "`n=== 4. Display All Stored Proteins ===" -ForegroundColor Cyan
python -c "import sqlite3; c=sqlite3.connect('data/uniprot.db'); [print(row) for row in c.execute('SELECT accession, protein_name, organism FROM proteins ORDER BY accession')]; c.close()"

Write-Host "`n=== 5. Check for Duplicate Accessions ===" -ForegroundColor Cyan
python -c "import sqlite3; c=sqlite3.connect('data/uniprot.db'); print('Duplicate accessions:', c.execute('SELECT COUNT(*) FROM (SELECT accession FROM proteins GROUP BY accession HAVING COUNT(*) > 1)').fetchone()[0]); c.close()"

Write-Host "`nDatabase checks completed." -ForegroundColor Green
