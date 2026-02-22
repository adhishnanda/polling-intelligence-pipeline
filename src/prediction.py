from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def baseline_winner_from_cleaned(cleaned_df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    grouped = cleaned_df.groupby("candidate_name", as_index=False)["pct"].mean()
    grouped = grouped.sort_values("pct", ascending=False)
    winner = str(grouped.iloc[0]["candidate_name"])
    return grouped, winner

def save_prediction_outputs(grouped: pd.DataFrame, winner: str, out_csv: Path, plot_path: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    plot_path.parent.mkdir(parents=True, exist_ok=True)

    grouped.to_csv(out_csv, index=False)

    plt.figure(figsize=(12, 6))
    plt.bar(grouped["candidate_name"], grouped["pct"])
    plt.xlabel("Candidates")
    plt.ylabel("Mean Polling Percentage")
    plt.title("Baseline Win Likelihood (Mean Polling %)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    (out_csv.parent / "winner.txt").write_text(f"Baseline predicted winner: {winner}\n", encoding="utf-8")
