# UniProt Protein Data Pipeline

A Python-based ETL (Extract, Transform, Load) project that retrieves protein records from the public UniProt REST API, cleans and validates the data, and stores the results in a SQLite database.

**Author:** Shaheena Shajira

## Project Overview

UniProt is a comprehensive resource for protein sequence and functional information. This project demonstrates how to build a structured data pipeline that retrieves protein records from UniProt, transforms the API responses into a consistent format, and loads the processed data into a relational database.

The project focuses on modular Python development, data quality, database operations, and automated testing.

## Architecture

```text
UniProt REST API
       |
       v
   Extraction
   api_client.py
       |
       v
 Transformation
   transform.py
       |
       v
     Loading
    storage.py
       |
       v
   SQLite Database
   data/uniprot.db
```

The `pipeline.py` module coordinates the extraction, transformation, and loading stages.

## Project Structure

```text
uniprot-data-pipeline/
├── src/
│   ├── __init__.py
│   ├── api_client.py
│   ├── transform.py
│   ├── storage.py
│   └── pipeline.py
├── tests/
│   ├── __init__.py
│   └── test_transform.py
├── docs/
│   ├── module_documentation.md
│   └── test_documentation.md
├── data/
│   └── .gitkeep
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies

- **Python** — pipeline implementation and data processing
- **UniProt REST API** — protein data retrieval
- **Requests** — HTTP requests and API integration
- **SQLite** — relational data storage
- **pytest** — automated unit testing
- **Git and GitHub** — version control and project hosting

## Modules

### `api_client.py`

- Connects to the public UniProt REST API.
- Retrieves reviewed human protein records.
- Parses JSON responses and checks HTTP errors.

### `transform.py`

- Extracts relevant protein attributes.
- Removes duplicate protein accessions.
- Skips records without accession identifiers.
- Standardises records for database loading.

### `storage.py`

- Creates the SQLite protein table when required.
- Inserts new protein records.
- Updates existing records using accession identifiers.

### `pipeline.py`

- Coordinates the ETL workflow.
- Passes data between the extraction, transformation, and storage modules.
- Reports basic processing results.

### `tests/test_transform.py`

- Tests duplicate-accession handling.
- Tests the handling of records without accession identifiers.
- Verifies expected transformation results.

## Data Source

The project uses the official UniProt REST API.

- API documentation: https://www.uniprot.org/api-documentation
- Example protein entry: https://rest.uniprot.org/uniprotkb/P01308.json

The initial implementation retrieves a small number of reviewed human protein records for development and testing.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- Internet access for API requests

### 1. Clone the repository

```bash
git clone https://github.com/Shaz2903/uniprot-data-pipeline.git
cd uniprot-data-pipeline
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the pipeline

```bash
python -m src.pipeline
```

The pipeline retrieves protein records, transforms them, and saves them to the SQLite database at `data/uniprot.db`.

### 5. Run the tests

```bash
python -m pytest -v
```

The test suite checks the implemented transformation logic.

## Current Scope

The initial version focuses on a small dataset and the core ETL workflow.

Planned improvements include:

- API pagination and larger dataset processing
- Retry handling and structured logging
- Stronger validation and data-quality checks
- Integration tests for database operations
- Incremental imports and idempotent processing
- Continuous integration using GitHub Actions
- Scalable processing for larger protein datasets

## Learning Objectives

This project provides practical experience in:

- Integrating external REST APIs
- Designing modular Python applications
- Transforming nested JSON data
- Handling duplicates and missing values
- Loading records into a relational database
- Writing automated tests
- Managing code through Git and GitHub

## Disclaimer

This is an independent portfolio project using publicly accessible UniProt data. It is not an official UniProt software component.
