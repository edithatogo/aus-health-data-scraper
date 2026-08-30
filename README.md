> **Successor development:** See [the GMA compatibility notice](SUCCESSOR.md).
> Consolidation is in progress; this repository remains unarchived.

# Automated Health Data Scraper and Processor

This project automates the scraping, processing, and analysis of public health data from Australia's **Medicare Benefits Schedule (MBS)** and **Pharmaceutical Benefits Scheme (PBS)**.

The goal is to create a clean, unified, and analysis-ready dataset from these disparate sources. The entire pipeline is designed to be run automatically on a monthly schedule using GitHub Actions, ensuring the data is always up-to-date.

## Data Sources

-   **MBS (Medicare Benefits Schedule):** Data is sourced from the official [MBS XML files](https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/Content/Downloads). This provides a catalogue of medical services subsidized by the Australian government.
-   **PBS (Pharmaceutical Benefits Scheme):** Data is sourced from the [PBS XML data](https://info.data.pbs.gov.au/xml-schema/). This provides a catalogue of subsidized medicines.

## Project Structure

```
.
├── .github/                # GitHub Actions workflows
│   └── workflows/
│       └── monthly_run.yml
├── data/
│   ├── processed/          # Final, cleaned datasets
│   ├── raw/                # Raw data files from scraping
│   └── source/             # Source files for the scraper
├── src/                    # Python source code
│   ├── scraper.py          # Scripts to download data
│   ├── processor.py        # Scripts to clean and structure data
│   └── main.py             # Main application entry point
├── tests/                  # Automated tests
├── .gitignore
├── README.md
└── requirements.txt
```

## Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/doughnuted/html-scraper-project.git
    cd html-scraper-project
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python src/main.py
    ```
    This will initiate the full scraping and processing pipeline as defined in `src/main.py`.

## Automation

The project is configured to run automatically on the first of every month via the GitHub Actions workflow defined in `.github/workflows/monthly_run.yml`. This workflow will:

1.  Install all necessary dependencies.
2.  Run the test suite to ensure code quality.
3.  Execute the main script to scrape and process the latest data.
4.  Commit the updated data files back to the repository.
