# Report & Deliverables Redesign Guide (academic → recruiter-grade)

## Rename assignment language
Replace:
- "Question 1/2/3/4/5"
With:
- "Analytics Mart A/B/C/D/E" (or use the actual mart file names)

## Suggested report sections
1. Executive Summary (why this pipeline supports ML systems)
2. Data source & ingestion (FiveThirtyEight export snapshot)
3. Orchestration (Airflow DAGs + task grouping)
4. Transformations (schema standardization + cleaning rules)
5. Data marts & ML readiness (feature table)
6. Baseline prediction (explicitly label as baseline)
7. Dashboard (how outputs are consumed)
8. Engineering challenges (debugging, idempotency, path normalization)
9. Future scalable architecture (design)

## Add screenshots
- Airflow UI DAG graph view (optional)
- Streamlit dashboard main screen (recommended)
