import pandas as pd
from src.paths import raw_dir, processed_dir, marts_dir, reports_dir, assets_dir
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
from src.prediction import baseline_winner_from_cleaned, save_prediction_outputs

# 1) Load raw
df = load_raw_polls(raw_dir() / "president_polls.csv")

# 2) Clean
cleaned = clean_polls(df)
cleaned_path = processed_dir() / "polls_cleaned.csv"
save_cleaned(cleaned, cleaned_path)

# 3) Marts
save_table(mart_candidate_state_vote_share(cleaned), marts_dir() / "mart_candidate_state_vote_share.csv")
save_table(mart_key_candidates_comparison(cleaned), marts_dir() / "mart_key_candidates_comparison.csv")
save_table(mart_sample_size_variance(cleaned), marts_dir() / "mart_sample_size_variance.csv")
save_table(mart_polling_trends_timeseries(cleaned), marts_dir() / "mart_polling_trends_timeseries.csv")
save_table(mart_pollster_transparency(cleaned), marts_dir() / "mart_pollster_transparency.csv")

# 4) ML features
feats = build_candidate_level_features(cleaned)
feats.to_csv(marts_dir() / "mart_ml_features_candidate_level.csv", index=False)

# 5) Baseline prediction outputs
grouped, winner = baseline_winner_from_cleaned(cleaned)
save_prediction_outputs(
    grouped,
    winner,
    reports_dir() / "prediction_summary.csv",
    assets_dir() / "candidates_probability_visualization.png",
)

print("Done ✅ Generated processed data, marts, features, and prediction outputs.")