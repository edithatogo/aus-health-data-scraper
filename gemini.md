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
│   ├── scraper.py         # Script to scrape and download HTML files
│   └── processor.py       # Script to process HTML files and generate the dataset
├── .gitignore             # Specifies files for Git to ignore
├── README.md              # Project overview and instructions
└── requirements.txt       # Python dependencies
```

## File Descriptions

### `src/scraper.py`

-   **Purpose:** Fetches and saves the target HTML files.
-   **Logic:**
    -   Uses the `requests` library to download HTML content from specified URLs.
    -   Saves the raw HTML files into the `data/raw/` directory.

### `src/processor.py`

-   **Purpose:** Extracts, cleans, and transforms data from the raw HTML files.
-   **Logic:**
    -   Reads each HTML file from the `data/raw/` directory.
    -   Uses `lxml` to parse the HTML and `pandas` to read HTML tables.
    -   Cleans and transforms the extracted tables.
    -   Joins the tables into a single, long-form DataFrame.
    -   Saves the final dataset to `data/processed/dataset.csv`.

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
    2.  **Run Scripts:** Executes `scraper.py` and then `processor.py`.
    3.  **Commit Data:** Commits the newly generated files in `data/raw/` and `data/processed/` back to the repository.

### `.gitignore`

A standard Python `.gitignore` file will be created to ignore files like `__pycache__/`, `.env`, and other common temporary files.
