# UniProt Protein Data Pipeline

A Python-based ETL (Extract, Transform, Load) project that retrieves protein records from the public UniProt REST API, transforms and validates the data, and stores the results in a SQLite database.

**Author:** Shaheena Shajira

## Project Overview

UniProt is a comprehensive resource for protein sequence and functional information. This project demonstrates how to build a modular data pipeline that retrieves protein records from UniProt, transforms API responses into a consistent format, and loads the processed data into a relational database.

The project focuses on API integration, data quality, database operations, error handling, logging, and automated testing.

## Architecture

```text
UniProt REST API
       |
       v
  Extraction
  api_client.py
  - API requests
  - Pagination
  - Retry handling
       |
       v
  Transformation
  transform.py
  - Data cleaning
  - Duplicate removal
  - Missing-value handling
       |
       v
     Loading
     storage.py
     - SQLite operations
     - Insert and update
       |
       v
  SQLite Database
  data/uniprot.db
```

The `pipeline.py` module coordinates the extraction, transformation, and loading stages. It logs processing information and reports failures without silently hiding them.

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
│   ├── test_transform.py
│   ├── test_api_client.py
│   └── test_pipeline.py
├── data/
├── requirements.txt
├── README.md
```

The SQLite database is generated when the pipeline runs and is excluded from version control.

## Technologies

- **Python** — pipeline implementation and data processing
- **UniProt REST API** — protein data retrieval
- **Requests** — HTTP requests and API integration
- **SQLite** — relational data storage
- **pytest** — automated testing
- **unittest.mock** — isolating components during tests
- **Logging** — recording pipeline progress and errors
- **Git and GitHub** — version control and project hosting

## Modules

### `api_client.py`

- Connects to the public UniProt REST API.
- Retrieves reviewed human protein records.
- Supports configurable page sizes and pagination.
- Uses request timeouts and retries failed requests.
- Logs request progress and errors.
- Checks HTTP responses and validates the structure of returned results.

### `transform.py`

- Extracts relevant protein attributes.
- Removes duplicate protein accessions.
- Skips records without accession identifiers.
- Standardises records for database loading.

### `storage.py`

- Creates the SQLite protein table when required.
- Inserts new protein records.
- Updates existing records using accession identifiers.
- Supports repeatable loads through accession-based conflict handling.

### `pipeline.py`

- Coordinates extraction, transformation, and loading.
- Passes data between the pipeline modules.
- Logs record counts and successful completion.
- Logs exceptions and re-raises failures so they are not silently ignored.

## Automated Testing

The project uses pytest to verify individual modules and the overall pipeline.

Current test coverage includes:

- Successful API responses.
- Pagination across multiple API pages.
- Retrying after a temporary request failure.
- Raising an error after all retries fail.
- Handling unexpected API response structures.
- Rejecting invalid pagination and retry settings.
- Removing duplicate accessions.
- Skipping records without accessions.
- Successful execution of the pipeline workflow.
- Stopping subsequent steps when extraction fails.
- Reporting database-save failures.

**Current status:** 11 automated tests passing.

Run the complete test suite:

```bash
python -m pytest -v
```

Run only the API-client tests:

```bash
python -m pytest -v tests/test_api_client.py
```

Run only the transformation tests:

```bash
python -m pytest -v tests/test_transform.py
```

Run only the pipeline tests:

```bash
python -m pytest -v tests/test_pipeline.py
```

The API-client and pipeline tests use mocked dependencies where appropriate, avoiding unnecessary external API calls and database changes.

## Data Source

The project uses the official UniProt REST API.

- API documentation: https://www.uniprot.org/api-documentation
- Example protein entry: https://rest.uniprot.org/uniprotkb/P01308.json

The pipeline retrieves a configurable, limited number of reviewed human protein records for development and testing. The default pipeline run fetches five records.

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
.venv\Scripts\Activate.ps1
```

On Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the pipeline

```bash
python -m src.pipeline
```

The pipeline retrieves protein records, transforms them, and saves them to `data/uniprot.db`. Progress and errors are reported through logging.

### 5. Run the tests

```bash
python -m pytest -v
```

## Current Scope and Future Improvements

The current implementation demonstrates the core ETL workflow, API pagination and retries, SQLite persistence, logging, error handling, and automated tests.

Potential next improvements include:

- Stronger validation of API responses and protein records.
- Dedicated database integration tests.
- Incremental imports and improved handling of larger datasets.
- Respecting API rate limits and retry guidance.
- Continuous integration using GitHub Actions.
- More comprehensive monitoring and operational reporting.
- Exploring scalable processing tools such as PySpark where appropriate.

## Learning Objectives

This project provides practical experience in:

- Integrating external REST APIs.
- Designing modular Python applications.
- Processing nested JSON data.
- Handling duplicates and missing values.
- Loading records into a relational database.
- Implementing pagination, retries, and logging.
- Writing automated tests with mocks.
- Managing code through Git and GitHub.

## Disclaimer

This is an independent portfolio project using publicly accessible UniProt data. It is not an official UniProt software component.
