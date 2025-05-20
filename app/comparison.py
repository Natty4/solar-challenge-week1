
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from utils import load_all_countries

# Page setup
st.set_page_config(page_title="🌍 Cross-Country Comparison", layout="wide")
st.title("🌍 Cross-Country Comparison")
st.caption("Analyze and compare solar energy metrics across multiple countries.")

# Load all cleaned CSVs
DATA_DIR = Path("./data").resolve()
df_all = load_all_countries(DATA_DIR)

if df_all.empty:
    st.warning("No cleaned data found in './data'. Ensure *_clean.csv files exist.")
    st.stop()

# Summary Statistics
st.subheader("📋 Combined Summary Statistics")
st.dataframe(df_all.describe().T)

# Boxplot Comparison
st.subheader("📦 Metric Distribution by Country")
numeric_columns = df_all.select_dtypes(include='number').columns.tolist()
metric = st.selectbox("Select metric to compare:", options=numeric_columns, index=numeric_columns.index("GHI") if "GHI" in numeric_columns else 0)
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

st.markdown(f"### 📊 {metric} Summary by Country")
st.dataframe(summary_table)

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### 📈 Average GHI by Country")
    region_df = df_all.groupby("Country")["GHI"].mean().reset_index().sort_values("GHI", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=region_df, x="GHI", y="Country", palette="viridis", ax=ax)
    ax.set_xlabel("Average {GHI (W/m²)}")
    st.pyplot(fig)
with col2:
    st.markdown(f"##### 📈 {metric} Distribution by Country")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df_all, x="Country", y=metric, palette="Set2", ax=ax)
    ax.set_title(f"{metric} Distribution by Country")
    st.pyplot(fig)