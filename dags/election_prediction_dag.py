from __future__ import annotations

from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import pendulum
import pandas as pd

from src.paths import processed_dir, reports_dir, assets_dir
from src.prediction import baseline_winner_from_cleaned, save_prediction_outputs

TZ = pendulum.timezone("Europe/Berlin")

with DAG(
    dag_id="polling_baseline_prediction",
    description="Baseline prediction job reading cleaned polls and producing summary + plot.",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=TZ),
    catchup=False,
    tags=["baseline", "prediction", "ml-backbone"],
) as dag:

    @task
    def run_baseline() -> None:
        cleaned_path = processed_dir() / "polls_cleaned.csv"
        if not cleaned_path.exists():
            raise FileNotFoundError("Cleaned dataset not found. Run DAG `polling_intelligence_etl` first.")
        df = pd.read_csv(cleaned_path, parse_dates=["start_date", "end_date"])
        grouped, winner = baseline_winner_from_cleaned(df)
        save_prediction_outputs(
            grouped,
            winner,
            reports_dir() / "prediction_summary.csv",
            assets_dir() / "candidates_probability_visualization.png",
        )

    run_baseline()
