# Polling Intelligence Pipeline  
## Data Engineering Backbone for ML Systems (Airflow + Feature Marts + Dashboard)

A production-style mini data platform built to support downstream machine learning workflows.
It ingests a FiveThirtyEight polling export snapshot, orchestrates transformations with Apache Airflow, produces curated datasets + analytical marts + an ML-ready feature table, and serves results in a Streamlit dashboard.

**Validated:** DAG runs were executed successfully in the Airflow UI (manual trigger), after iterative debugging and dependency fixes.

---

## What this demonstrates (ML-first relevance)

- **Orchestration:** Airflow DAGs coordinating ingestion → cleaning → marts/features → baseline scoring
- **Data modeling mindset:** curated layer + marts layer (analytics + ML features)
- **ML readiness:** candidate/state-level features (counts, variance, sample size, transparency)
- **Delivery:** dashboard consuming pipeline artifacts

---

## Demo

### Dashboard
![Dashboard](assets/screenshots/Streamlit_Dashboard.png)

### Example Charts
![Charts](assets/screenshots/Top_Candidates.png)
![Charts](assets/screenshots/Polling_Trends.png)
![Charts](assets/screenshots/Transparency_Score.png)

---

## Architecture
See:
- `assets/diagrams/architecture.mmd` (Mermaid)
- `assets/diagrams/data_lineage.dot` (Graphviz)
- `assets/diagrams/future_architecture.mmd` (Mermaid)

---

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Airflow
```bash
export AIRFLOW_HOME=$(pwd)/airflow
export PIPELINE_ROOT=$(pwd)
airflow db init
airflow webserver -p 8080
airflow scheduler
```

Trigger:
- `polling_intelligence_etl`
- then `polling_baseline_prediction`

### Dashboard
```bash
streamlit run dashboard/streamlit_app.py
```
