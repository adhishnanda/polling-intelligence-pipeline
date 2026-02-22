from __future__ import annotations
import pandas as pd

def build_candidate_level_features(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["candidate_name", "state"])
        .agg(
            mean_pct=("pct", "mean"),
            std_pct=("pct", "std"),
            polls_count=("poll_id", "nunique"),
            mean_sample_size=("sample_size", "mean"),
            mean_transparency=("transparency_score", "mean"),
            start_date_min=("start_date", "min"),
            start_date_max=("start_date", "max"),
        )
        .reset_index()
    )
    grouped["std_pct"] = grouped["std_pct"].fillna(0.0)
    return grouped
