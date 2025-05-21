import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

from utils import load_clean_data, get_available_countries

# Page setup
st.set_page_config(page_title="☀️ Solar Data Discovery Dashboard", layout="wide")
st.title("☀️ Solar Data Discovery Dashboard")
st.caption("Explore solar energy metrics for individual countries.")

# Constants
DATA_DIR = Path("./data").resolve()

# Sidebar: Country selector
available_countries = get_available_countries(DATA_DIR)
selected_country = st.sidebar.selectbox("Select a country", available_countries if available_countries else [None])

if selected_country:
    df = load_clean_data(DATA_DIR, selected_country)

    if df.empty:
        st.warning(f"No data available for {selected_country}.")
        st.stop()

    st.subheader(f"📊 Summary Statistics: {selected_country.title()}")
    st.dataframe(df.describe())

    # Layout: Boxplot & KPIs
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### GHI Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, y="GHI", ax=ax)
        st.pyplot(fig)

    with col2:
        st.markdown("#### Key Metrics")
        kpi_cols = st.columns(2)
        kpi_cols[0].metric("Avg GHI", f"{df['GHI'].mean():.1f} W/m²")
        kpi_cols[1].metric("Avg DNI", f"{df['DNI'].mean():.1f} W/m²")

    # Monthly Trend (if Month column exists)
    if "Month" in df.columns:
        st.subheader("📆 Monthly GHI Trend")
        monthly = df.groupby("Month")["GHI"].mean().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(data=monthly, x="Month", y="GHI", palette="viridis", ax=ax)
        ax.set_ylabel("Avg GHI")
        ax.set_title("Monthly Average GHI")
        st.pyplot(fig)

    # Scatter Plots
    st.subheader("🔍 Feature Relationships")
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
        st.subheader("📈 GHI Over Time")
        fig, ax = plt.subplots(figsize=(10, 4))
        df_sorted = df.sort_values("Timestamp")
        ax.plot(df_sorted["Timestamp"], df_sorted["GHI"], alpha=0.6)
        ax.set_xlabel("Time")
        ax.set_ylabel("GHI (W/m²)")
        ax.set_title("GHI Time Series")
        st.pyplot(fig)

else:
    st.warning("Please select a valid country from the dropdown.")