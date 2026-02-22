from __future__ import annotations

from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from datetime import datetime
import pendulum

from src.paths import raw_dir, processed_dir, marts_dir
from src.ingest import load_raw_polls
from src.transform import clean_polls, save_cleaned
from src.analytics_marts import (
    mart_candidate_state_vote_share,
    mart_key_candidates_comparison,
    mart_sample_size_variance,
    mart_polling_trends_timeseries,
    mart_pollster_transparency,
    save_table,
)
from src.feature_engineering import build_candidate_level_features

TZ = pendulum.timezone("Europe/Berlin")

with DAG(
    dag_id="polling_intelligence_etl",
    description="ETL + analytics marts + ML feature prep for FiveThirtyEight polling exports.",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=TZ),
    catchup=False,
    tags=["data-engineering", "etl", "ml-backbone"],
) as dag:

    @task
    def ingest_raw() -> str:
        path = raw_dir() / "president_polls.csv"
        _ = load_raw_polls(path)
        return str(path)

    @task
    def clean_transform(_: str) -> str:
        df = load_raw_polls(raw_dir() / "president_polls.csv")
        cleaned = clean_polls(df)
        out = processed_dir() / "polls_cleaned.csv"
        save_cleaned(cleaned, out)
        return str(out)

    @task
    def build_marts(cleaned_path: str) -> None:
        import pandas as pd
        df = pd.read_csv(cleaned_path, parse_dates=["start_date", "end_date"])
        save_table(mart_candidate_state_vote_share(df), marts_dir() / "mart_candidate_state_vote_share.csv")
        save_table(mart_key_candidates_comparison(df), marts_dir() / "mart_key_candidates_comparison.csv")
        save_table(mart_sample_size_variance(df), marts_dir() / "mart_sample_size_variance.csv")
        save_table(mart_polling_trends_timeseries(df), marts_dir() / "mart_polling_trends_timeseries.csv")
        save_table(mart_pollster_transparency(df), marts_dir() / "mart_pollster_transparency.csv")

    @task
    def build_ml_features(cleaned_path: str) -> str:
        import pandas as pd
        df = pd.read_csv(cleaned_path, parse_dates=["start_date", "end_date"])
        feats = build_candidate_level_features(df)
        out = marts_dir() / "mart_ml_features_candidate_level.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        feats.to_csv(out, index=False)
        return str(out)

    ingest = ingest_raw()
    cleaned = clean_transform(ingest)

    with TaskGroup(group_id="marts_and_features"):
        build_marts(cleaned)
        build_ml_features(cleaned)

    cleaned
