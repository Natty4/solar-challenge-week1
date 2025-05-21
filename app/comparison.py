import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

from utils import (
    load_all_countries,
    generate_summary,
    plot_country_ranking,
    plot_metric_boxplot,
    run_statistical_tests,
)

# Page setup
st.set_page_config(page_title="🌍 Cross-Country Comparison", layout="wide")
st.title("🌍 Cross-Country Comparison")
st.caption("Analyze and compare solar energy metrics across multiple countries.")

# Load all cleaned data
DATA_DIR = Path("./data").resolve()
df_all = load_all_countries(DATA_DIR)

if df_all.empty:
    st.warning("No cleaned data found in './data'. Ensure *_clean.csv files exist.")
    st.stop()

# Select metric
numeric_columns = df_all.select_dtypes(include='number').columns.tolist()
metric = st.selectbox("📊 Select metric to compare:", options=numeric_columns, index=numeric_columns.index("GHI") if "GHI" in numeric_columns else 0)

# Summary Table
st.subheader(f"📋 {metric} Summary Statistics by Country")
summary_table = (
    df_all.groupby("Country")[metric]
    .agg(
        Count="count",
        Mean="mean",
        StdDev="std",
        Min="min",
        Max="max"
    )
    .round(2)
    .sort_values("Mean", ascending=False)
)
st.dataframe(summary_table)

# Layout for Visuals
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"##### 📈 {metric} Mean Ranking by Country")
    fig = plot_country_ranking(df_all, metric)
    st.pyplot(fig)

with col2:
    st.markdown(f"##### 📦 {metric} Distribution by Country")
    fig = plot_metric_boxplot(df_all, metric)
    st.pyplot(fig)
    
# Statistical Tests
st.subheader("🧪 Statistical Comparison")
test_results = run_statistical_tests(df_all, metric)
if "error" in test_results:
    st.warning(f"⚠️ {test_results['error']}")
else:
    st.json(test_results)