# ☀️ Solar Data Discovery Dashboard

An interactive Streamlit dashboard to explore, analyze, and compare solar energy metrics across different countries using cleaned irradiance datasets.


---

## 🚀 Features

- **Country-Level Insights**  
  View summary statistics, boxplots, time series, and scatter plots for a selected country.

- **Regional Comparison**  
  Compare solar metrics (e.g., GHI) across all available countries with visual summaries.

- **Interactive Widgets**  
  - Sidebar country selector  
  - Metric dropdown  
  - Expandable panels

---

## 🛠️ Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Natty4/solar-challenge-week1.git
   cd solar-solar-challenge-week1
   ``` 

2. **Install dependencies:**

    It’s recommended to use a virtual environment:
        python -m venv .venv
        source .venv/bin/activate  # On Windows: .venv\Scripts\activate
        pip install -r requirements.txt

3. **Add cleaned data:**

    Place your cleaned CSV files in the data/ folder.
    File names should follow this pattern: COUNTRY_clean.csv, e.g., benin_clean.csv.

4. **Run the dashboard:**

    From the root directory:

    streamlit run app/main.py

    The dashboard will open in your browser.

---
## 📊 Visualizations

    Boxplot of GHI by country

    Time series of irradiance

    Scatter plots (e.g., RH vs Tamb)

    Regional average GHI bar chart

---
