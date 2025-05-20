
# 🌍 Interim Report - Solar Data Discovery: Week 0 Challenge  
**Submission Date:** 18 May, 2025 
**Name:** Natnael K.  
**Repository:** [https://github.com/Natty4/solar-challenge-week1.git]  

---

## ✅ Week 0 (W0) Plan Overview  

**Objective:**  
Establish a robust foundation for analyzing solar datasets for multiple countries, enabling effective comparisons and insights.

**Tasks Completed:**

### 🔧 Task 1 - Git & Environment Setup  
- Created dedicated GitHub repository with clear folder structure:
  - 'notebooks/' for per-country Jupyter Notebooks
  - 'src/' for reusable helper functions and pipelines
  - 'data/' (excluded via '.gitignore') for raw and cleaned data
- Developed 'solar_eda.py' as a reusable EDA & cleaning toolkit
- Ensured consistent Python environment via:
  - 'requirements.txt' for dependencies
  - Use of Jupyter Notebooks in VS Code

---

## 🔍 Task 2 - Data Profiling, Cleaning & EDA  

### 📦 Country Notebooks  
- Benin: 'notebooks/benin_eda.ipynb'
- Sierra Leone: 'notebooks/sierraleone_eda.ipynb'
- Togo: 'notebooks/togo_eda.ipynb'

### 🔬 EDA & Cleaning Approach  

Each notebook includes:

1. **Summary Statistics & Missing Value Report**  
   - 'df.describe()', 'df.isna().sum()', columns with >5% nulls flagged  
   - Dropped fully null columns (e.g., 'Comments')

2. **Outlier Detection**  
   - Computed Z-scores on key columns: GHI, DNI, DHI, ModA, ModB, WS, WSgust  
   - Rows with |Z| > 3 flagged and removed

3. **Cleaning Pipeline**  
   - Negative night-time irradiance values set to zero  
   - Missing values imputed using median for key columns  
   - New features: 'HasRain', 'Hour', 'Month'  
   - Cleaned data exported to 'data/<country>_clean.csv' (not committed/ignored)

4. **Visual Explorations**  
   - Time Series: Line charts of irradiance and temperature vs. time  
   - Cleaning Impact: Grouped by cleaning flag and analyzed changes  
   - Correlation Heatmaps and Scatter Plots  
   - Wind Rose plots  
   - Histograms for GHI and wind speed  
   - Bubble chart (GHI vs. Tamb with RH/BP as bubble size)  

---

## 🧠 Insights Gained So Far  
- Major share of irradiance data at night shows zero or negative values  
- Sensor outliers removed significantly improved data quality  
- Cleaning visibly improves irradiance-to-module correlation  
- Variation in humidity and wind patterns across countries is notable  

---

## 📌 Next Steps for Final Submission  
- Complete EDA for all the given countries  
- Begin ranking regions based on solar potential  
- Build comparative dashboards and statistical summaries  
- Ensure visualizations are polished and storytelling is tight  
