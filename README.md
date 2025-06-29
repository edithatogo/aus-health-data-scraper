# Automated MBS Data Scraper and Processor

This project automates the scraping, processing, and analysis of Medicare Benefits Schedule (MBS) data from the official medicarestatistics.humanservices.gov.au website.

It is designed to be run automatically on a monthly schedule using GitHub Actions, ensuring the data is always up-to-date.

## Project Structure

```
.
├── .github/                # GitHub Actions workflows
│   └── workflows/
│       └── monthly_run.yml
├── data/
│   ├── processed/          # Final, cleaned datasets
│   ├── raw/                # Raw HTML files from scraping
│   │   ├── items/
│   │   └── participants/
│   └── source/               # Source files for the scraper
├── src/                    # Python source code
│   ├── scraper.py
│   ├── processor.py
│   └── main.py
├── tests/                  # Automated tests
│   ├── fixtures/
│   └── test_processor.py
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

3.  **Run the scraper and processor:**
    ```bash
    python src/main.py
    ```

## Automation

The project is configured to run automatically on the first of every month via the GitHub Actions workflow defined in `.github/workflows/monthly_run.yml`. This workflow will:

1.  Install all necessary dependencies.
2.  Run the test suite to ensure code quality.
3.  Execute the main script to scrape and process the latest data.
4.  Commit the updated data files back to the repository.