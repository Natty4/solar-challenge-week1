# # Solar Challenge – W0 ( 🌞 Solar Site Data Analysis & Region Ranking )

This repository contains a data pipeline and EDA framework to clean, explore, and compare solar sensor datasets from multiple West African countries. The goal is to enable data-driven region ranking for solar farm expansion.

---

## 🧭 Project Structure

├──.github
├── notebooks/ # Country-specific EDA notebooks
│ ├── benin_eda.ipynb
│ ├── sierraleone_eda.ipynb
│ └── togo_eda.ipynb
├── src/
│ └── solar_eda.py # Shared cleaning utilities
├── data/ # Local-only cleaned data (gitignored)
│ ├── benin_clean.csv
│ ├── sierraleone_clean.csv
│ └── togo_clean.csv
├── tests/
├── .gitignore
├── requirements.txt # Dependencies
└── README.md # You're here


---

## 📌 Project Objectives

**Main goal:** Profile, clean, and explore solar datasets from different countries to support region ranking for solar development.

### Task 2 – Profiling, Cleaning, and EDA

For each country's dataset:

- ✅ Perform **summary stats** and null checks
- ✅ Clean via **outlier clipping** and **median imputation**
- ✅ Generate cleaned dataset: `data/<country>_clean.csv`
- ✅ Produce exploratory charts for trends and correlation analysis
- ✅ Enable **notebook reproducibility** and versioned cleaning code

---

## 🚀 Run the EDA Notebooks

### 1. Setup environment

```bash
git clone https://github.com/Natty4/solar-challenge-week1.git
cd solar-challenge-week1
python -m venv .venv && source .venv/bin/activate        # or conda env create -f environment.yml
pip install -r requirements.txt

## 🚀  Run the EDA notebooks

The repository now contains a dedicated exploratory notebook for each country:

| Country | Notebook | Clean CSV output* |
|---------|----------|------------------|
| Benin          | `notebooks/benin_eda.ipynb`         | `data/benin_clean.csv` |
| Sierra Leone   | `notebooks/sierraleone_eda.ipynb`  | `data/sierraleone_clean.csv` |
| Togo           | `notebooks/togo_eda.ipynb`          | `data/togo_clean.csv` |

> \* CSVs are **git‑ignored** (see `.gitignore`) and generated locally when you run the notebook.
```
---

### 2. Launch Jupyter

jupyter lab      # or jupyter notebook

### 3. Open and run a country notebook

| Country           | Notebook Path                      | Output CSV                    |
| ----------------- | ---------------------------------- | ----------------------------- |
| 🇧🇯 Benin        | `notebooks/benin_eda.ipynb`        | `data/benin_clean.csv`        |
| 🇸🇱 Sierra Leone | `notebooks/sierraleone_eda.ipynb` | `data/sierraleone_clean.csv` |
| 🇹🇬 Togo         | `notebooks/togo_eda.ipynb`         | `data/togo_clean.csv`         |

*CSV outputs are automatically generated locally and not committed (see .gitignore).*


## 🔧 Cleaning Pipeline

Implemented in src/solar_eda.py:

| Step                               | Description                               |
| ---------------------------------- | ----------------------------------------- |
| Drop fully-null columns            | Removes columns like `Comments`           |
| Fix negative night-time irradiance | Sets negative GHI/DNI/DHI to 0 at night   |
| Z-score filtering                  | Drops rows with sensor Z > 3              |
| Median imputation                  | Fills missing values in core fields       |
| Feature engineering                | Adds `Hour`, `Month`, and `HasRain` flags |

Callable via:
from src.solar_eda import clean_solar_df
df_clean = clean_solar_df(df)


## 📊 EDA Highlights

Each notebook contains:

    Summary statistics + null audit

    Irradiance/temperature time series

    Diurnal and monthly patterns

    Outlier and missing-value handling

    Wind rose and histograms

    Correlation heatmaps

    Bubble chart (GHI vs Tamb, size = RH or BP)


## 📈 Contribution Summary

| Feature                          | Implemented                           |
| -------------------------------- | ------------------------------------- |
| Cleaning pipeline                | ✅ `clean_solar_df()` with helpers     |
| Country EDA notebooks            | ✅ 3 complete notebooks                |
| Bubble plots / Wind roses        | ✅ Included                            |
| CSV export and ignore policy     | ✅ via `data/` and `.gitignore`        |
| Visuals for trends and anomalies | ✅ All Task 2 visuals                  |
| Git commits & PR hygiene         | ✅ Commit messages + PR templates used |




## ✅ Next Steps

Add Task 3: cross-region comparison

Define region-ranking metrics

Summarize insights in dashboard or final report


## 🙌 Acknowledgments

Built as part of a data engineering challenge.
Thanks to the organizing team and coordinators.
