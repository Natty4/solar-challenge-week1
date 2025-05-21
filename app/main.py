import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

from utils import load_clean_data, get_available_countries


DATA_DIR = Path("./data").resolve()

st.set_page_config(page_title="☀️ Solar Data Discovery Dashboard", layout="wide")
st.title("☀️ Solar Data Discovery Dashboard")
st.caption("Explore solar energy metrics for individual countries.")


available_countries = get_available_countries(DATA_DIR)
selected_country = st.sidebar.selectbox("Select a country", available_countries if available_countries else [None])


if selected_country:
    df = load_clean_data(DATA_DIR, selected_country)

    # Summary Stats
    st.subheader(f"{selected_country.title()} Summary Statistics")
    st.dataframe(df.describe())

    # Layout: Boxplot & KPIs
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("GHI Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=df, y="GHI", ax=ax)
        st.pyplot(fig)

    with col2:
        st.markdown("#### Key Metrics")
        kpi_cols = st.columns(2)
        kpi_cols[0].metric("Avg GHI", f"{df['GHI'].mean():.1f} W/m²")
        kpi_cols[1].metric("Avg DNI", f"{df['DNI'].mean():.1f} W/m²")

    # Monthly Trend
    st.subheader("Monthly GHI Trend")
    if "Month" in df.columns:
        monthly = df.groupby("Month")["GHI"].mean().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(data=monthly, x="Month", y="GHI", palette="viridis", ax=ax)
        ax.set_ylabel("Avg GHI")
        st.pyplot(fig)

    # Scatter Plots
    st.subheader("Scatter Plots")
    scatter_col = st.columns(2)

    with scatter_col[0]:
        st.markdown("##### WS vs GHI")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x="WS", y="GHI", alpha=0.3, ax=ax)
        st.pyplot(fig)

    with scatter_col[1]:
        st.markdown("##### RH vs Tamb")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x="RH", y="Tamb", alpha=0.3, ax=ax)
        st.pyplot(fig)

    # Time Series Plot
    if "Timestamp" in df.columns:
        st.subheader("GHI Time Series")
        fig, ax = plt.subplots(figsize=(10, 4))
        df_sorted = df.sort_values("Timestamp")
        ax.plot(df_sorted["Timestamp"], df_sorted["GHI"], alpha=0.6)
        ax.set_xlabel("Time")
        ax.set_ylabel("GHI (W/m²)")
        st.pyplot(fig)

else:
    st.warning("No data found for the selected country.")