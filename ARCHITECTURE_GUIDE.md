# Architecture Guide

This document explains the project folder structure and how the architecture supports development workflows.

## Folder Structure

### `sql/`
**Purpose**: SQL analytics, data transformation, and reporting queries

- **`queries/`**: Ad-hoc analysis queries, KPI calculations, and exploratory SQL
- **`views/`**: Reusable database views for common aggregations and metrics
- **`stored_procedures/`**: Automated data processing procedures and scheduled reports

**Usage**: Start here for data extraction and initial analysis. Queries feed into Python EDA and BI dashboards.

### `python/`
**Purpose**: Exploratory data analysis, machine learning, and data processing

- **`notebooks/`**: Jupyter notebooks for EDA, visualization, and iterative analysis
- **`scripts/`**: Reusable Python scripts for data processing and automation
- **`models/`**: Machine learning model training, evaluation, and prediction code
- **`utils/`**: Shared utilities, helper functions, and common data processing modules

**Usage**: Primary workspace for statistical analysis, feature engineering, and ML model development.

### `bi/`
**Purpose**: Business intelligence dashboards and reporting

- **`dashboards/`**: Dashboard configuration files and visualization definitions
- **`reports/`**: Static reports and scheduled report templates
- **`config/`**: Connection settings, data source configurations, and dashboard metadata

**Usage**: Final output layer for stakeholder consumption. Connects to SQL views and ML predictions.

### `data/`
**Purpose**: Data storage organized by processing stage

- **`raw/`**: Original, unprocessed data files (CSV, database dumps)
- **`processed/`**: Cleaned and transformed data ready for analysis
- **`external/`**: Third-party data sources and reference datasets

**Usage**: Centralized data storage following data pipeline best practices. Supports version control for processed datasets.

### `docs/`
**Purpose**: Project documentation and specifications

- **`requirements/`**: Business requirements, user stories, and acceptance criteria
- **`design/`**: Technical design documents, architecture decisions, and data models
- **`api/`**: API documentation if applicable

**Usage**: Reference documentation for project understanding and onboarding.

### `tests/`
**Purpose**: Testing code for quality assurance

- **`sql/`**: SQL query validation and data quality tests
- **`python/`**: Unit tests, integration tests for Python code
- **`bi/`**: Dashboard validation and data accuracy tests

**Usage**: Ensures code quality and data accuracy across all components.

## Architecture Benefits

### Modularity
Each component (SQL, Python, BI) operates independently while sharing data through well-defined interfaces. This allows parallel development and easy maintenance.

### Scalability
The structure supports incremental development. Start with SQL queries, add Python analysis, then build ML models and dashboards without restructuring.

### Reproducibility
Clear separation of raw, processed, and output data enables reproducible workflows. Each stage can be re-executed independently.

### Collaboration
Distinct folders for different technologies allow team members to work in their preferred tools while maintaining project coherence.

### Data Pipeline
The architecture follows a standard ETL/ELT pattern:
1. Extract: SQL queries pull from database
2. Transform: Python scripts process and enrich data
3. Load: Processed data feeds into BI dashboards

### Future Development Support

- **New Data Sources**: Add to `data/external/` and create ingestion scripts in `python/scripts/`
- **Additional Metrics**: Extend SQL views and update BI dashboards
- **Model Improvements**: Iterate in `python/models/` without affecting other components
- **New Dashboards**: Add configurations to `bi/dashboards/` using existing data sources
- **Documentation**: Expand `docs/` as project evolves

## Development Workflow

1. **Data Exploration**: Start in `sql/queries/` to understand data structure
2. **Analysis**: Move to `python/notebooks/` for deeper statistical analysis
3. **Modeling**: Develop ML models in `python/models/`
4. **Visualization**: Create dashboards in `bi/dashboards/`
5. **Documentation**: Update `docs/` throughout the process

This structure supports both iterative development and production deployment.

