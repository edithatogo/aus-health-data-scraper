# Todo List

A list of actionable tasks to achieve the goals outlined in the roadmap.

## v0.2 - Enhanced Data Collection

- [ ] **MBS Benefits:**
    - [ ] Investigate MBS website/data sources to identify where "benefits" paid data is located.
    - [ ] Update `src/scraper.py` to download benefits data.
    - [ ] Update `src/processor.py` to parse and integrate benefits data.
    - [ ] Update tests to cover benefits data processing.
- [ ] **PBS Integration:**
    - [ ] Analyze the PBS XML schema from `https://info.data.pbs.gov.au/xml-schema/`.
    - [ ] Identify the specific XML files or data dumps to be downloaded.
    - [ ] Create `src/pbs_scraper.py` to handle downloading of PBS data.
    - [ ] Create `src/pbs_processor.py` to parse the XML and structure the data into a tabular format (e.g., CSV).
    - [ ] Update `src/main.py` to include calls to the new PBS modules.
    - [ ] Add tests for PBS data scraping and processing.

## v1.0 - Unified Data Model

- [ ] Design a target schema that can accommodate both MBS and PBS data.
- [ ] Refactor `processor.py` scripts to output data conforming to the new schema.
- [ ] Create comprehensive documentation for the final dataset fields.

## v2.0 - Advanced Analysis & Insights

- [ ] Research and select an appropriate graph database technology.
- [ ] Design a graph schema to represent the entities and relationships.
- [ ] Write scripts to load the processed data into the graph database.
- [ ] ... (Further tasks to be defined)