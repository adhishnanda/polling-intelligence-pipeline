from __future__ import annotations
from pathlib import Path
import pandas as pd

def mart_candidate_state_vote_share(df: pd.DataFrame) -> pd.DataFrame:
    res = df.groupby(["state", "candidate_name"], as_index=False)["pct"].mean()
    return res.sort_values(["state", "pct"], ascending=[True, False])

def mart_key_candidates_comparison(df: pd.DataFrame, key_candidates=None) -> pd.DataFrame:
    if key_candidates is None:
        key_candidates = ["Donald Trump", "Kamala Harris"]
    filtered = df[df["candidate_name"].isin(key_candidates)]
    res = filtered.groupby(["state", "candidate_name"])["pct"].mean().unstack().reset_index()
    return res

def mart_sample_size_variance(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("sample_size")["pct"].agg(["mean", "std"]).reset_index()

def mart_polling_trends_timeseries(df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    top_candidates = df.groupby("candidate_name")["pct"].mean().nlargest(top_n).index
    filtered = df[df["candidate_name"].isin(top_candidates)].copy()
    res = filtered.groupby(["candidate_name", "start_date"], as_index=False)["pct"].mean()
    return res.sort_values(["candidate_name", "start_date"])

def mart_pollster_transparency(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("pollster", as_index=False)["transparency_score"].mean()

def save_table(df: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
