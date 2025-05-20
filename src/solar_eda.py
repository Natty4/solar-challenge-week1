"""
solar_eda.py
Reusable EDA & cleaning module for solar datasets.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import zscore
from windrose import WindroseAxes

# Constants
_ZCOLS = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
_KEYCOLS = _ZCOLS + ['Tamb', 'RH']

class SolarCleaner:
    def __init__(self, z_thresh: float = 3.0, impute: bool = True, add_features: bool = True):
        self.z_thresh = z_thresh
        self.impute = impute
        self.add_features = add_features
    
    def plot_value_distribution_summary(df: pd.DataFrame, cols=None, title="Value Distribution Summary"):
        """
        Plots count of negative, zero, and positive values in numeric columns of the DataFrame.

        Parameters:
            df (pd.DataFrame): The input DataFrame.
            cols (list or None): Subset of columns to check. If None, all numeric columns are used.
            title (str): Plot title.
        """
        if cols is None:
            cols = df.select_dtypes(include=[np.number]).columns

        neg_counts = (df[cols] < 0).sum()
        zero_counts = (df[cols] == 0).sum()
        pos_counts = (df[cols] > 0).sum()

        summary_df = pd.DataFrame({
            'Negative': neg_counts,
            'Zero': zero_counts,
            'Positive': pos_counts
        }).sort_index()

        # Drop columns with no data in any category
        summary_df = summary_df[(summary_df[['Negative', 'Zero', 'Positive']].sum(axis=1) > 0)]

        ax = summary_df.plot(kind='bar', figsize=(14, 6), stacked=True,
                            color=['blue', '#ff7f0e', '#2ca02c'])  # Red, orange, green
        plt.title(title)
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Value Type')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        return ax
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._drop_empty_columns(df.copy())
        df = self._zero_night_negatives(df)
        df = self._fix_daytime_negatives(df)
        df, _ = self._clip_outliers(df)
        if self.impute:
            df = self._impute_median(df)
        if self.add_features:
            df = self._engineer_features(df)
        return df

    def _drop_empty_columns(self, df: pd.DataFrame, thresh: float = 1.0) -> pd.DataFrame:
        to_drop = df.columns[df.isna().mean() >= thresh]
        if not to_drop.empty:
            print(f"Dropping columns: {list(to_drop)}")
        return df.drop(columns=to_drop)

    def _zero_night_negatives(self, df: pd.DataFrame, irr_cols=_ZCOLS[:3], threshold: float = 1.0) -> pd.DataFrame:
        night = (df[irr_cols] < threshold).all(axis=1)
        neg = (df[irr_cols] < 0).any(axis=1)
        fix = night & neg
        df.loc[fix, irr_cols] = df.loc[fix, irr_cols].clip(lower=0)
        return df
    
    def _fix_daytime_negatives(self, df: pd.DataFrame, irr_cols=_ZCOLS[:3], threshold: float = 1.0) -> pd.DataFrame:
        """
        Sets negative irradiance values (GHI, DNI, DHI) to 0 if they occur during daytime.
        
        Parameters:
            df: DataFrame with irradiance data and 'Hour' column.
            irr_cols: List of irradiance columns to check (default: ['GHI', 'DNI', 'DHI']).
            threshold: Minimum value to consider it "daytime" (e.g., GHI > 1).
        
        Returns:
            Cleaned DataFrame.
        """
        if 'Hour' not in df.columns:
            df['Hour'] = df['Timestamp'].dt.hour

        # Define daytime: any irradiance value above threshold
        is_daytime = (df[irr_cols] > threshold).any(axis=1)

        # Find negative values during daytime
        day_neg = is_daytime & (df[irr_cols] < 0).any(axis=1)

        # Set negatives to zero only in those rows
        df.loc[day_neg, irr_cols] = df.loc[day_neg, irr_cols].clip(lower=0)

        return df

    def _clip_outliers(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        z = df[_ZCOLS].apply(zscore, nan_policy='omit')
        mask = (np.abs(z) > self.z_thresh).any(axis=1)
        return df.loc[~mask].copy(), int(mask.sum())

    def _impute_median(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in _KEYCOLS:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        return df

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'Timestamp' in df.columns:
            df['Hour'] = df['Timestamp'].dt.hour
            df['Month'] = df['Timestamp'].dt.month
        if 'Precipitation' in df.columns:
            df['HasRain'] = (df['Precipitation'] > 0).astype(int)
        return df

class SolarEDA:
    @staticmethod
    def dtype_summary(df: pd.DataFrame) -> pd.DataFrame:
        mem = df.memory_usage(deep=True) / 1_048_576
        return pd.DataFrame({
            "dtype": df.dtypes,
            "non-null": df.notna().sum(),
            "missing": df.isna().sum(),
            "% missing": df.isna().mean().round(3),
            "memory_mb": mem.round(3)
        }).sort_values("memory_mb", ascending=False)

    @staticmethod
    def numeric_overview(df: pd.DataFrame) -> "pd.io.formats.style.Styler":
        return df.describe().T.style.format("{:.3f}")

    @staticmethod
    def cat_counts(df: pd.DataFrame, top: int = 10) -> dict:
        cats = df.select_dtypes(include=['object', 'category']).columns
        return {col: df[col].value_counts().head(top) for col in cats}

    @staticmethod
    def missing_table(df: pd.DataFrame, mv_thresh: float = 0.0) -> pd.DataFrame:
        miss = df.isna().sum()
        pct = df.isna().mean()
        tbl = pd.DataFrame({"missing": miss, "% missing": pct})
        if mv_thresh > 0:
            tbl = tbl[tbl["% missing"] >= mv_thresh]
        return tbl.sort_values("% missing", ascending=False)

    @staticmethod
    def dup_report(df: pd.DataFrame, subset: list[str] | None = None) -> tuple[int, pd.DataFrame]:
        dups = df.duplicated(subset=subset, keep=False)
        return dups.sum(), df[dups].copy()

    @staticmethod
    def corr_heatmap(df: pd.DataFrame, cols=None, only_engineered=False):
        if only_engineered:
            engineered = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'Tamb', 'RH', 'Hour', 'Month']
            cols = [c for c in engineered if c in df.columns]
        elif cols:
            engineered = cols
            cols = [c for c in engineered if c in df.columns]
        elif cols is None:
            cols = df.select_dtypes(include=[np.number]).columns
        if cols is None:
            cols = df.select_dtypes(include=[np.number]).columns
        corr = df[cols].corr()
        ax = sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, square=True)
        ax.set_title("Correlation Matrix")
        return ax    


    @staticmethod
    def line_overview(df, cols=('GHI','DNI','DHI','Tamb')):
        fig, ax = plt.subplots(figsize=(14, 4))
        for c in cols:
            if c in df.columns:
                ax.plot(df['Timestamp'], df[c], label=c, alpha=.6)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.legend(ncol=len(cols), loc='upper right')
        ax.set_title("Irradiance & Tamb (full record)")
        plt.tight_layout(); return ax

    @staticmethod
    def diurnal_curve(df):
        if 'Hour' not in df.columns:
            df['Hour'] = df['Timestamp'].dt.hour
        hourly = df.groupby('Hour')[['GHI','DNI','DHI','Tamb']].mean()
        ax = hourly[['GHI','DNI','DHI']].plot(marker='o', figsize=(10,4))
        ax2 = ax.twinx(); hourly['Tamb'].plot(ax=ax2, color='gray', marker='o')
        ax.set_xticks(range(0,24,2)); ax.set_title("Average Diurnal Pattern")
        return ax

    @staticmethod
    def monthly_facets(df):
        df_m = df.assign(Month=df['Timestamp'].dt.strftime('%b'), Day=df['Timestamp'].dt.day)
        g = sns.relplot(data=df_m, x='Day', y='GHI', col='Month', col_wrap=4, kind='line',
                        height=2.5, aspect=1.5, linewidth=.7, alpha=.8,
                        facet_kws={'sharey': False, 'sharex': False})
        for ax in g.axes.flatten():
            ax.set_xticks(range(1,32,2))
        g.set_axis_labels("Day", "GHI (W/m²)")
        g.fig.suptitle('Monthly GHI Patterns', y=1.02)
        return g

    @staticmethod
    def cleaning_impact(df):
        if 'Cleaning' not in df.columns:
            raise KeyError("Column 'Cleaning' not found.")
        imp = (df.groupby('Cleaning')[['ModA','ModB']].mean()
                 .rename(index={0:'Pre/No-Clean',1:'Post-Clean'}))
        ax = imp.plot(kind='bar', rot=0, figsize=(6,4)); ax.set_title("Cleaning Effect")
        return ax, imp.round(1)

    @staticmethod
    def wind_rose(df):
        ax = WindroseAxes.from_ax()
        ax.bar(df['WD'], df['WS'], normed=True,
               opening=.8, edgecolor='white', bins=[0,2,4,6,8,10,12])
        ax.set_title("Wind-Rose")
        return ax

    @staticmethod
    def bubble_ghi_tamb(df: pd.DataFrame, size_col: str = "RH", n: int = 20_000,
                        alpha: float = 0.35, size_scale: float = 0.9,
                        title: str | None = None) -> plt.Axes:
        if size_col not in df.columns:
            raise KeyError(f"{size_col} not in dataframe")
        sample = df.sample(min(len(df), n), random_state=42)
        fig, ax = plt.subplots(figsize=(8, 5))
        sc = ax.scatter(sample["GHI"], sample["Tamb"],
                        s=sample[size_col] * size_scale,
                        alpha=alpha, edgecolor="black", linewidths=0.3)
        ax.set_xlabel("GHI (W/m²)")
        ax.set_ylabel("Tamb (°C)")
        ax.set_title(title or f"Bubble Chart – GHI vs Tamb (bubble = {size_col})")
        for v in [20, 40, 60, 80, 100]:
            ax.scatter([], [], s=v * size_scale, c="gray", alpha=alpha,
                       edgecolor="black", linewidths=0.3,
                       label=f"{size_col} {v}")
        ax.legend(scatterpoints=1, frameon=False, title=size_col)
        ax.grid(alpha=0.3)
        return ax

# Basic CSV utility functions
def load_raw(path: str, ts_col: str = "Timestamp") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=[ts_col])
    df.sort_values(ts_col, inplace=True)
    return df

def profile(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    return df.describe().T, df.isna().mean().mul(100).round(2)
