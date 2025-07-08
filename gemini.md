# Project: Automated HTML Scraper and Data Processor

This project automates the process of scraping HTML files, extracting and cleaning tabular data, and generating a combined, long-form dataset. The entire process is designed to be run automatically on a monthly schedule using GitHub Actions.

## Project Structure

The project will be organized into the following directory structure:

```
.
├── .github/
│   └── workflows/
│       └── monthly_run.yml  # GitHub Actions workflow for monthly execution
├── data/
│   ├── processed/         # Stores the final, cleaned dataset
│   │   └── .gitkeep
│   └── raw/               # Stores the raw HTML files from scraping
│       └── .gitkeep
├── src/
│   ├── main.py            # Main entry point for the application
│   ├── scraper.py         # Script to scrape and download HTML files
│   └── processor.py       # Script to process HTML files and generate the dataset
├── tests/
│   ├── test_processor.py  # Tests for the data processor
│   └── fixtures/          # Test fixtures
├── .gitignore             # Specifies files for Git to ignore
├── README.md              # Project overview and instructions
└── requirements.txt       # Python dependencies
```

## File Descriptions

### `src/main.py`

-   **Purpose:** Main entry point for the application.
-   **Logic:**
    -   Orchestrates the scraping and processing of data.
    -   Calls functions from `scraper.py` and `processor.py`.

### `src/scraper.py`

-   **Purpose:** Fetches and saves the target HTML files.
-   **Logic:**
    -   Uses the `requests` library to download HTML content from specified URLs.
    -   Saves the raw HTML files into the `data/raw/` directory.
    -   Called by `src/main.py`.

### `src/processor.py`

-   **Purpose:** Extracts, cleans, and transforms data from the raw HTML files.
-   **Logic:**
    -   Reads each HTML file from the `data/raw/` directory.
    -   Uses `lxml` to parse the HTML and `pandas` to read HTML tables.
    -   Cleans and transforms the extracted tables.
    -   Joins the tables into a single, long-form DataFrame.
    -   Saves the final dataset to `data/processed/dataset.csv`.
    -   Called by `src/main.py`.

### `requirements.txt`

This file lists the necessary Python libraries for the project.

```
pandas
lxml
requests
```

### `.github/workflows/monthly_run.yml`

This GitHub Actions workflow automates the scraping and processing tasks.

-   **Trigger:** Runs automatically at 00:00 on the first day of every month, and can also be triggered manually.
-   **Jobs:**
    1.  **Setup:** Checks out the repository, sets up Python, and installs the dependencies from `requirements.txt`.
    2.  **Run Scripts:** Executes `src/main.py`.
    3.  **Commit Data:** Commits the newly generated files in `data/raw/` and `data/processed/` back to the repository.

### `.gitignore`

A standard Python `.gitignore` file will be created to ignore files like `__pycache__/`, `.env`, and other common temporary files.

## Testing

The `tests/` directory contains unit tests for the project. The tests are written using the `pytest` framework.

-   `tests/test_processor.py`: Contains tests for the data processing logic in `src/processor.py`.
-   `tests/fixtures/`: Contains sample HTML files used as test data.
