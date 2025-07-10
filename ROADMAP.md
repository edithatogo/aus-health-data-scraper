# Roadmap

This document outlines the future goals and planned features for the project.

## v0.1 - Initial Scraper (Current)

- [x] Scrape MBS item and participant data (counts).
- [x] Process raw HTML into structured CSV files.
- [x] Set up automated monthly runs with GitHub Actions.

## v0.2 - Enhanced Data Collection

- [ ] **MBS:** Enhance scraper to collect "benefits" data (e.g., monetary value) in addition to service counts.
- [ ] **PBS:** Add new capability to scrape and process data from the Pharmaceutical Benefits Scheme (PBS).
    - [ ] Parse XML data from PBS data source.
    - [ ] Integrate PBS data into the processing pipeline.

## v1.0 - Unified Data Model

- [ ] Consolidate MBS and PBS data into a unified, well-documented schema.
- [ ] Implement robust data cleaning and validation processes.
- [ ] Refactor processing scripts for better scalability and maintainability.

## v2.0 - Advanced Analysis & Insights

- [ ] **Graph Database:** Model the interconnected data (doctors, patients, items, benefits, prescriptions) in a graph database (e.g., Neo4j).
- [ ] **NLP:** Apply Natural Language Processing to extract structured information from unstructured text in handbooks and item descriptions.
- [ ] **Causal Analysis:** Develop and apply causal inference models to generate insights from the data.
- [ ] **API/Dashboard:** (Optional) Create an API or a simple dashboard to explore the data and insights.