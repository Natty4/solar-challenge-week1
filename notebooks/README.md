# 🌞 Solar Data - EDA & Cleaning: Benin

* Goal: Profile, clean, and explore Benin's solar dataset so it's ready for comparison and ranking across countries.
## 🛠️ Setup & Imports

We load the necessary packages and prepare the notebook for data profiling and EDA.  
The solar data for **Benin** is loaded from the raw dataset folder.
## 📊 1. Data Profiling

We begin by inspecting the structure and quality of the dataset:

- `df.info()` provides an overview of column types and nulls.
- `df.describe()` gives summary statistics for all numerical features.
- `missing_table()` highlights features with >5% missing values.
- `dtype_summary()` summarizes data types by frequency.
- We visualize the distribution of values (negative, zero, positive) to guide cleaning decisions.
## 🧹 2. Cleaning Pipeline

We apply the custom cleaning logic using `SolarCleaner`, which includes:

- Removing or fixing negative irradiance values at night.
- Handling outliers (e.g. Z-score filtering for solar/wind sensors).
- Imputing missing values using median (if needed).
- Engineering features like `Hour`, `Month`, and `HasRain`.

The cleaned dataset is then saved locally.
## 📈 3. Time Series Analysis

We explore the temporal behavior of key variables:

- `line_overview()` shows overall trends over time.
- `diurnal_curve()` captures solar performance across the day.
- `monthly_facets()` highlights seasonal or monthly variations.

These insights help identify time-based patterns and anomalies.
## 🧼 4. Cleaning Impact

We evaluate how the `Cleaning` flag (e.g., physical panel cleaning) affects power output:

- Average values of `ModA` and `ModB` are compared before vs. after cleaning events.
- This analysis helps understand operational effects on performance.
## 🔗 5. Correlation & Relationships

We examine the correlation matrix between key engineered features:

- Focused on solar irradiance, module temperature, humidity, and time features.
- Includes both heatmap and optional scatter plots (e.g., wind speed vs. GHI).

This helps us identify linear relationships and potential multicollinearity.
## 💨 6. Wind & Distribution

We visualize wind conditions and general variable distributions:

- Wind rose plot summarizes direction and intensity.
- Histograms show distribution of key variables like `GHI` and `WS`.

These insights are useful for both energy yield and system design decisions.
## 🌡️ 7. Temperature & Humidity Interactions

We analyze how relative humidity (`RH`) correlates with:

- Ambient temperature (`Tamb`)
- Global Horizontal Irradiance (`GHI`)

This helps explain atmospheric influences on solar generation and heat buildup.
## 🔵 8. Bubble Chart: GHI vs Temperature

We visualize a multi-variable relationship:

- X-axis: Ambient Temperature (`Tamb`)
- Y-axis: Solar Irradiance (`GHI`)
- Bubble Size: Relative Humidity (`RH`)

This gives a compact overview of how climate affects solar output.
## 🧮 9. Value Distribution After Cleaning

We revisit the value distribution plot:

- Shows how many values in each column are negative, zero, or positive.
- Helps verify that cleaning steps were effective and no unexpected values remain.
## 💾 10. Save Cleaned Data

The cleaned dataset is saved for use in regional comparison and ranking tasks.  
Ensure the `data/` folder is included in `.gitignore` to avoid committing large CSV files.
