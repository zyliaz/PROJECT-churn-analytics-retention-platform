# Churn Analytics Retention Platform

## Project Overview

This project provides a comprehensive analytics solution for analyzing customer churn and retention patterns in a streaming subscription service. The platform combines SQL analytics, Python-based exploratory data analysis (EDA), machine learning models, and business intelligence dashboards to deliver actionable insights for reducing churn and improving customer retention.

## Business Goal

The primary objective is to identify, analyze, and predict customer churn to enable proactive retention strategies. The platform focuses on:

- Understanding churn patterns and root causes
- Identifying at-risk customers before they churn
- Measuring retention metrics and KPIs
- Supporting data-driven decision making for retention campaigns

## Project Phases

### Phase 1: Data Familiarization & KPI Validation
- Data exploration and quality assessment
- KPI definition and validation
- Initial data profiling

### Phase 2: SQL Analytics
- Data transformation and aggregation
- KPI calculations and reporting queries
- Data quality checks and validation

### Phase 3: Exploratory Data Analysis (EDA)
- Statistical analysis and visualization
- Feature engineering
- Pattern identification and hypothesis testing

### Phase 4: Machine Learning
- Predictive churn modeling
- Feature importance analysis
- Model evaluation and validation

### Phase 5: BI Dashboard Development
- Interactive dashboard creation
- Real-time KPI monitoring
- Executive reporting

## Key Deliverables

1. **SQL Analytics**: Optimized queries for churn metrics, retention rates, and cohort analysis
2. **EDA Reports**: Comprehensive analysis notebooks with visualizations and insights
3. **ML Models**: Trained churn prediction models with performance metrics
4. **BI Dashboards**: Interactive dashboards for stakeholders and executives
5. **Documentation**: Technical documentation, data dictionary, and architecture guide

## Dataset Description

The project uses a star schema database design with the following components:

### Core Tables

**users** (Dimension Table)
- User demographic information and profile attributes
- Contains ~80% subscribed users and ~20% registered users without subscriptions
- Primary key: `user_id`

**subscriptions** (Fact Table)
- Subscription lifecycle and service details
- One record per subscribed user
- Includes: signup_date, cancel_date, plan, price, status, payment_method, total_charges
- Service flags: internet_service, phone_service, streaming services, etc.
- Foreign key: `user_id` → `users.user_id`

**user_events** (CSV File)
- Behavioral event data stored as CSV
- Event types: login, watch, click, cancel
- Fields: user_id, event_type, event_time, device_type, page_url
- Simulates streaming/event data for time-series analysis

### Data Characteristics

- **Snapshot Date**: 2024-03-31 (all date calculations based on this)
- **Schema**: Star schema (users dimension, subscriptions fact)
- **Data Quality**: Includes realistic data issues for testing (timestamp disorder, silent users, etc.)
- **Churn Patterns**: Concentrated in March and November for business storytelling

## How Components Connect

### SQL → EDA → ML → BI Pipeline

1. **SQL Analytics** (`sql/`)
   - Extracts and transforms raw data from database
   - Creates aggregated views and calculated metrics
   - Outputs processed datasets for downstream analysis

2. **Python EDA** (`python/notebooks/`)
   - Reads processed data from SQL outputs
   - Performs statistical analysis and visualization
   - Identifies features and patterns for modeling
   - Generates insights and recommendations

3. **Machine Learning** (`python/models/`)
   - Uses features identified in EDA
   - Trains predictive churn models
   - Evaluates model performance
   - Exports model artifacts and predictions

4. **BI Dashboards** (`bi/dashboards/`)
   - Connects to SQL views and ML predictions
   - Visualizes KPIs and metrics in real-time
   - Provides interactive exploration for stakeholders
   - Supports executive reporting and decision-making

### Data Flow

```
Database (users, subscriptions)
    ↓
SQL Queries (aggregation, transformation)
    ↓
Processed Data (CSV/Parquet)
    ↓
Python EDA (analysis, feature engineering)
    ↓
ML Models (training, prediction)
    ↓
BI Dashboards (visualization, reporting)
```

## Getting Started

1. Review the `ARCHITECTURE_GUIDE.md` for project structure details
2. Check `DATA_DICTIONARY.md` for data schema information
3. Start with SQL queries in `sql/queries/` for initial data exploration
4. Proceed to Python notebooks in `python/notebooks/` for EDA
5. Build ML models using scripts in `python/models/`
6. Create dashboards in `bi/dashboards/` for visualization

## Project Structure

```
churn-analytics-retention-platform/
├── sql/                    # SQL analytics queries and views
├── python/                 # Python EDA and ML code
├── bi/                     # BI dashboard configurations
├── data/                   # Data storage (raw, processed, external)
├── docs/                   # Project documentation
└── tests/                  # Test files for each component
```

See `ARCHITECTURE_GUIDE.md` for detailed folder descriptions.

