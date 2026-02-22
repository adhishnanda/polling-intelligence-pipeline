from __future__ import annotations
from pathlib import Path
import pandas as pd

RELEVANT_COLUMNS = [
    "poll_id",
    "state",
    "start_date",
    "end_date",
    "sample_size",
    "party",
    "candidate_name",
    "pct",
    "pollster",
    "transparency_score",
]

def clean_polls(df: pd.DataFrame) -> pd.DataFrame:
    """Minimal, interview-safe cleaning matching the original project logic."""
    missing = [c for c in RELEVANT_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")

    out = df[RELEVANT_COLUMNS].copy()

    out["start_date"] = pd.to_datetime(out["start_date"], errors="coerce")
    out["end_date"] = pd.to_datetime(out["end_date"], errors="coerce")
    out["sample_size"] = pd.to_numeric(out["sample_size"], errors="coerce")
    out["pct"] = pd.to_numeric(out["pct"], errors="coerce")
    out["transparency_score"] = pd.to_numeric(out["transparency_score"], errors="coerce")

    out = out.dropna(subset=["state", "candidate_name", "pct", "start_date"])

    out["state"] = out["state"].astype(str).str.strip()
    out["candidate_name"] = out["candidate_name"].astype(str).str.strip()
    out["pollster"] = out["pollster"].astype(str).str.strip()
    return out

def save_cleaned(df_cleaned: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)
