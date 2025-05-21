# Solar Challenge - W0 ( 🌞 Solar Site Data Analysis & Region Ranking )


This repository contains a data pipeline and EDA framework to clean, explore, and compare solar sensor datasets from multiple West African countries. The goal is to enable data-driven region ranking for solar farm expansion.

---

## 🧭 Project Structure

<pre>
├── .github/
├── app/                       # Streamlit Dashboard app
│   ├── main.py                # Country-specific insights
│   ├── comparison.py          # Regional metric comparison
│   └── utils.py
│   └── README.md
├── dashboard_screenshot/      # Static images of dashboard pages
├── notebooks/                 # Country-specific EDA notebooks
│   ├── benin_eda.ipynb
│   ├── compare_countries.ipynb
│   ├── sierraleone_eda.ipynb
│   └── togo_eda.ipynb
│   └── README.md 
├── src/
│   └── comparison_utils.py           # Shared cleaning utilities
│   └── solar_eda.py           # Shared cleaning utilities
├── data/                      # Local-only cleaned data (gitignored)
│   ├── benin_clean.csv
│   ├── sierraleone_clean.csv
│   └── togo_clean.csv
├── tests/
├── .gitignore
├── requirements.txt           # Dependencies
└── README.md                  # You're here
</pre>


---

## 📌 Project Objectives

**Main goal:** Profile, clean, and explore solar datasets from different countries to support region ranking for solar development.

### - Initial Setup and Project Structure

- ☑️ Set up GitHub repository with clear folder structure
- ☑️ Define modular code layout (`src/`, `notebooks/`, `data/`, `tests/`)
- ☑️ Add `.gitignore` to exclude local artifacts
- ☑️ Create and document environment dependencies (`requirements.txt`)
- ☑️ Create a shared data cleaning script for reuse across notebooks

### - Profiling, Cleaning, and EDA

For each country's dataset:

- ☑️ Perform **summary statistics** and null checks  
- ☑️ Clean via **outlier clipping** and **median imputation**  
- ☑️ Generate cleaned dataset: `data/<country>_clean.csv`  
- ☑️ Produce exploratory charts for trends and correlation analysis  
- ☑️ Enable **notebook reproducibility** and versioned cleaning code  

### - Cross-Country Comparison

- ☑️ Load cleaned datasets for Benin, Sierra Leone, and Togo  
- ☑️ Plot **boxplots** of GHI, DNI, and DHI across countries  
- ☑️ Generate a **summary statistics table** (mean, median, std)  
- ☑️ Run **ANOVA statistical test** on GHI values  
- ☑️ Add 3 key markdown observations about country differences  
- ☑️ (Bonus) Include a **bar chart** ranking average GHI by country  

### Bonus Task - Streamlit Dashboard

- ☑️ Build an interactive dashboard using **Streamlit**
- ☑️ Enable **multipage layout**:
  - `main.py` → country-specific solar insights
  - `comparison.py` → cross-country metric analysis
- ☑️ Visualize EDA summaries with:
  - GHI boxplots
  - Time series plots
  - Scatter charts
  - Summary tables
- ☑️ Add interactive widgets:
  - Country selector
  - Metric dropdown
- ☑️ Store code under `app/` folder
- ☑️ Document dashboard usage in [`app/README.md`](app/README.md)
- ☑️ Added screenshots in `dashboard_screenshot/`

---


### 1. Setup environment

```bash
git clone https://github.com/Natty4/solar-challenge-week1.git
cd solar-challenge-week1
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

```
---

### 2. Launch Jupyter

jupyter lab      # or jupyter notebook

### 3. Open and run a country notebook


| Notebook Type     | Country / Topic     | Path                                      | Output CSV                  |
| ----------------- | --------------------| ----------------------------------------- |-----------------------------|
| Country EDA       | 🇧🇯 Benin             | 'notebooks/benin_eda.ipynb'              | 'data/benin_clean.csv'       |
| Country EDA       | 🇸🇱 Sierra Leone      | 'notebooks/sierraleone_eda.ipynb'        | 'data/sierraleone_clean.csv' |
| Country EDA       | 🇹🇬 Togo              | 'notebooks/togo_eda.ipynb'               | 'data/togo_clean.csv'        |
| 🔁 Cross-Country  | Comparison (All)    | 'notebooks/compare_countries.ipynb'      |   —                          |



*CSV outputs are automatically generated locally and not committed (see .gitignore).*

## 🌍 Launch the Dashboard

1. Make sure the cleaned CSVs are present in the `data/` directory.

2. From the project root, run:

```bash
streamlit run app/main.py
```

3. Use the **sidebar** to:

- ☑️ **Select a country** (Country Insights page)
- ☑️ Switch to "Cross-Country Comparison" page from the sidebar



## 🔧 Cleaning Pipeline

Implemented in src/solar_eda.py:

| Step                               | Description                               |
| ---------------------------------- | ----------------------------------------- |
| Drop fully-null columns            | Removes columns like 'Comments'           |
| Fix negative night-time irradiance | Sets negative GHI/DNI/DHI to 0 at night   |
| Z-score filtering                  | Drops rows with sensor Z > 3              |
| Median imputation                  | Fills missing values in core fields       |
| Feature engineering                | Adds 'Hour', 'Month', and 'HasRain' flags |

#### Callable via:
from src.solar_eda import SolarCleaner

cleaner = SolarCleaner()
df_clean = cleaner.clean(df)


## 📊 EDA Highlights

Each notebook contains:

- ☑️ Summary statistics + null audit
- ☑️ Irradiance/temperature time series
- ☑️ Diurnal and monthly patterns
- ☑️ Outlier and missing-value handling
- ☑️ Wind rose and histograms
- ☑️ Correlation heatmaps
- ☑️ Bubble charts (e.g. GHI vs Tamb)
- ☑️ 📊 Cross-country boxplots and summary stats *(Task 3)*
- ☑️ 📈 GHI country ranking bar chart *(Task 3)*
- ☑️ 🧪 ANOVA test results for GHI *(Task 3)*


## 📈 Contribution Summary


| Feature                          | Implemented                           |
| -------------------------------- | ------------------------------------- |
| Cleaning pipeline                | ☑️ 'SolarCleaner' in **solar_eda.py**   |
| Country EDA notebooks            | ☑️ 3 countries + comparison           |
| Cross-country comparison         | ☑️ **compare_countries.ipynb** added     |
| Modular code design              | ☑️ **utils.py** shared logic    |
| Statistical tests                | ☑️ One-way ANOVA for GHI               |
| Dashboard + visual summaries     | ☑️ Interactive Streamlit app shared utils|
| Git commits & PR hygiene         | ☑️ Followed Git feature branching      |



## 🙌 Acknowledgments

Built as part of a data engineering challenge.
Thanks to the organizing team and coordinators.
