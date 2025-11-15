## Overview

This project demonstrates a modern, real-time data pipeline implemented using the **Medallion Architecture** (Bronze → Silver → Gold) and built on top of **Apache Spark**, **Delta Lake**, **Python**, and **dbt**.

**It processes streaming CSV data using PySpark**: handles raw data ingestion from CSV files and  writes the data incrementally into **Delta Lake** format.

**Applied Silver Layer transformation using PySpark**: performed deduplication, data enrichment, and upserts into Delta Lake tables using modular class-based processing with timestamp-based merge logic.

**Gold Layer modeled using dbt**: includes SCD Type 2 implementation via snapshots and an incremental model for trips, pulling from Silver Layer sources.

The overall pipeline is scalable, cloud-native, and production-ready, following best practices for modular and reliable data engineering workflows.

---

## Architecture Overview

This pipeline follows the **Medallion Architecture**, separating raw, cleaned, and curated data into Bronze, Silver, and Gold layers:

1. **Bronze Layer** – Raw data ingestion from CSV using Spark Structured Streaming
2. **Silver Layer** – Cleansed and deduplicated data with enrichment and upsert logic using PySpark
3. **Gold Layer** – Business-ready analytics layer modeled using dbt (with SCD Type 2 and incremental models)

---

## 🥉 Bronze Layer – Streaming Ingestion using PySpark & Delta Lake

The Bronze Layer handles raw data ingestion from CSV files using **Apache Spark Structured Streaming** and writes the data incrementally into **Delta Lake** format.

### Key Features:

- **Schema Inference**: Automatically detects data types during initial load.
- **Incremental Streaming**: Uses Spark Structured Streaming to load data as it arrives.
- **Parallel Processing**: Utilizes `ThreadPoolExecutor` to ingest multiple data sources concurrently.
- **Delta Lake Integration**: Writes data with ACID support and schema evolution.
- **Checkpointing**: Ensures streaming job fault tolerance and recovery.


---

## 🥈 Silver Layer – Applied Silver Layer transformation using PySpark

The Silver Layer transforms Bronze data into structured,performed deduplication, data enrichment, and upserts into Delta Lake tables using modular class-based processing with timestamp-based merge logic 
by applying custom business logic and data quality improvements.

### Key Steps:

- **Deduplication**: Keeps the latest record per entity using window functions.
- **Data Enrichment**:
  - Applies necessary cleansing, standardization, and feature engineering to improve data quality and usability.
- **Timestamp Tracking**: Adds `process_date` to monitor pipeline activity.
- **Upsert with Delta Lake**:
  - Uses `MERGE` to update existing records or insert new ones based on timestamps.
- **Modular Python Code**: All transformations are encapsulated in a reusable `transformation` class.
- **Applied To**: All domain tables – `customer`, `location`, `payment`, `driver`, `vehicle` excluding `trips`.

---

## 🥇 Gold Layer – Data Modeling with dbt (SCD Type 2 and Incremental Models)

The Gold Layer is powered by **dbt**, enabling structured modeling of analytical datasets from Silver Layer sources.

### Key Features:

- **SCD Type 2 with Snapshots**:
  - Historical tracking of dimensional changes.
  - Maintains versioned records for time-based analysis.
- **Incremental Fact Table (Trips)**:
  - Uses `is_incremental()` logic in dbt to efficiently load only new/updated records.
- **Source Definitions**:
  - dbt sources pull from Silver Layer Delta tables for traceability.
- **Star Schema Output**:
  - Models are organized under `silver` and `gold` folders for clear logical separation.

This layer produces high-quality, business-ready tables optimized for analytics, dashboards, and reporting tools.

---

## 💻 Technologies Used

- **Apache Spark (Structured Streaming)**
- **Delta Lake (ACID tables, schema evolution)**
- **Python (PySpark)**
- **dbt (Data modeling and SCD logic)**
- **ThreadPoolExecutor** for parallel ingestion

---

## 📁 Project Structure

```plaintext
Project2/
│
├── bronze/
│   └── Ingest raw CSVs using Spark streaming
│
├── silver/
│   └── Apply transformations (deduplication, enrichment, upsert)
│
├── dbt/
│   ├── models/
│   │   ├── silver/
│   │   └── gold/
│   ├── snapshots/
│   └── sources.yml
```

## 📊 Dashboard – Business Insights Layer

The final output of the Gold Layer feeds into a dashboard that delivers real-time, actionable insights for stakeholders.
Key Features:
- Data Source: Connects directly to Gold Layer Delta tables.
- KPIs Tracked:
- Total Trips, Revenue, and Active Drivers
- Payment Method Distribution

<img width="1602" height="711" alt="image" src="https://github.com/user-attachments/assets/8185a388-e34d-453f-8c85-9360df807b64" />



