import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.paths import processed_dir, marts_dir, reports_dir

st.set_page_config(page_title="Polling Intelligence Dashboard", layout="wide")
st.title("Polling Intelligence Dashboard")
st.caption("Airflow-orchestrated pipeline outputs (FiveThirtyEight export snapshot).")

cleaned_path = processed_dir() / "polls_cleaned.csv"
if not cleaned_path.exists():
    st.warning("Cleaned dataset not found. Run Airflow DAG `polling_intelligence_etl` first.")
    st.stop()

data = pd.read_csv(cleaned_path)
data = data.loc[:, ~data.columns.duplicated()]

st.sidebar.title("Filters")
states = sorted(data["state"].dropna().unique())
cands = sorted(data["candidate_name"].dropna().unique())
selected_states = st.sidebar.multiselect("State(s)", options=states, default=states)
selected_candidates = st.sidebar.multiselect("Candidate(s)", options=cands, default=cands)

df = data[data["state"].isin(selected_states) & data["candidate_name"].isin(selected_candidates)].copy()

c1, c2 = st.columns([2, 1])
with c1:
    st.subheader("Dataset Preview")
    st.dataframe(df.head(50), use_container_width=True)
with c2:
    st.subheader("Quick Stats")
    st.write(df[["pct", "sample_size", "transparency_score"]].describe(include="all"))

st.divider()
st.subheader("Visualizations")

top_candidates = df.groupby("candidate_name")["pct"].mean().sort_values(ascending=False).head(5).index
top_df = df[df["candidate_name"].isin(top_candidates)]

st.plotly_chart(
    px.bar(top_df, x="state", y="pct", color="candidate_name", barmode="group", title="Top Candidates: Polling % by State"),
    use_container_width=True,
)

pivot = df.pivot_table(values="transparency_score", index="state", columns="candidate_name", aggfunc="mean", fill_value=0)
st.plotly_chart(px.imshow(pivot, title="Transparency Score by State x Candidate"), use_container_width=True)

trend = df[df["candidate_name"].isin(top_candidates)][["start_date", "candidate_name", "pct"]].copy()
trend["start_date"] = pd.to_datetime(trend["start_date"], errors="coerce")
trend = trend.dropna(subset=["start_date"])
trend = trend.groupby([pd.Grouper(key="start_date", freq="M"), "candidate_name"])["pct"].mean().reset_index()
st.plotly_chart(px.line(trend, x="start_date", y="pct", color="candidate_name", title="Polling Trends (Monthly Mean)"), use_container_width=True)

st.divider()
st.subheader("Pipeline Outputs")

pred = reports_dir() / "prediction_summary.csv"
if pred.exists():
    st.markdown("**Baseline Prediction Summary**")
    st.dataframe(pd.read_csv(pred), use_container_width=True)
else:
    st.info("Run Airflow DAG `polling_baseline_prediction` to generate prediction outputs.")

marts = sorted(marts_dir().glob("mart_*.csv"))
if marts:
    st.markdown("**Analytics / Feature Marts**")
    for p in marts:
        with st.expander(p.name):
            st.dataframe(pd.read_csv(p).head(50), use_container_width=True)
