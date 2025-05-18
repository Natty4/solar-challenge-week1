"""
Reusable helpers for solar-farm EDA & cleaning
Author: <you>
"""

import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
from scipy.stats import zscore

#  1. LOAD & PROFILE -
def load_raw(path, ts_col="Timestamp"):
    """Read CSV, parse timestamp, return DataFrame."""
    df = pd.read_csv(path, parse_dates=[ts_col])
    df.sort_values(ts_col, inplace=True)
    return df

def profile(df):
    """Return numeric describe & % missing."""
    desc = df.describe().T
    null_pct = df.isna().mean().mul(100).round(2)
    return desc, null_pct



# 1. Data-type & distribution helpers
def dtype_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a dataframe summarising column dtypes and memory usage."""
    mem = df.memory_usage(deep=True) / 1_048_576  # → MB
    out = (
        pd.DataFrame({
            "dtype": df.dtypes,
            "non-null": df.notna().sum(),
            "missing": df.isna().sum(),
            "% missing": df.isna().mean().round(3),
            "memory_mb": mem.round(3)
        })
        .sort_values("memory_mb", ascending=False)
    )
    return out


def numeric_overview(df: pd.DataFrame) -> pd.DataFrame:
    """Describe numeric columns with nicer formatting."""
    desc = df.describe().T
    return desc.style.format("{:.3f}")

def cat_counts(df: pd.DataFrame, top: int = 10) -> dict[str, pd.Series]:
    """
    Return a dict where keys are categorical/object columns and
    values are their value-counts (top N).
    """
    cats = df.select_dtypes(include=["object", "category"]).columns
    return {col: df[col].value_counts().head(top) for col in cats}



# 2. Missing-value & duplicate helpers
def missing_table(df: pd.DataFrame, mv_thresh: float = 0.0) -> pd.DataFrame:
    """
    Table of missing counts/percentages.
    mv_thresh=0 leaves everything; set >0 to filter cols whose %missing ≤ thresh.
    """
    miss = df.isna().sum()
    pct = df.isna().mean()
    tbl = pd.DataFrame({"missing": miss, "% missing": pct}).sort_values("% missing", ascending=False)
    if mv_thresh > 0:
        tbl = tbl[tbl["% missing"] >= mv_thresh]
    return tbl


def dup_report(df: pd.DataFrame, subset: list[str] | None = None) -> tuple[int, pd.DataFrame]:
    """
    Return (# duplicate rows, dataframe of duplicates).
    Use subset to check only specific columns.
    """
    dups = df.duplicated(subset=subset, keep=False)
    dup_df = df[dups].copy()
    return dups.sum(), dup_df



# 3. Correlation heatmap
def corr_heatmap(df: pd.DataFrame, method: str = "pearson", annot: bool = False, figsize=(10, 8)) -> None:
    """Plot a correlation heatmap for numeric columns."""
    corr = df.select_dtypes(include=[np.number]).corr(method=method)
    plt.figure(figsize=figsize)
    sns.heatmap(corr, cmap="coolwarm", center=0, annot=annot, fmt=".2f", linewidths=.5)
    plt.title(f"{method.title()} Correlation")
    plt.show()
    
    



# 1. CONSTANTS
_ZCOLS   = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
_KEYCOLS = _ZCOLS + ['Tamb', 'RH']

# 2. LOW-LEVEL HELPERS
def _drop_empty_columns(df: pd.DataFrame, thresh: float = 1.0) -> pd.DataFrame:
    """Remove columns whose non-null ratio is below (1-thresh)."""
    to_drop = df.columns[df.isna().mean() >= thresh].tolist()
    if to_drop:
        print(f"Dropping columns (≥{int(thresh*100)} % null): {to_drop}")
    return df.drop(columns=to_drop)

def _zero_night_negatives(df: pd.DataFrame,
                          irr_cols=('GHI', 'DNI', 'DHI'),
                          dawn_dusk_threshold: float = 1.0) -> pd.DataFrame:
    """Clamp negative irradiance to 0 on rows that are clearly night-time."""
    night = (df[list(irr_cols)] < dawn_dusk_threshold).all(axis=1)
    neg   = (df[list(irr_cols)] < 0).any(axis=1)
    fix   = night & neg
    if fix.any():
        print(f"Setting {fix.sum()} negative irradiance readings to 0 (night-time rows).")
        df.loc[fix, irr_cols] = df.loc[fix, irr_cols].clip(lower=0)
    return df

def _clip_outliers(df: pd.DataFrame, zcols=_ZCOLS, z_thresh: float = 3) -> tuple[pd.DataFrame, int]:
    """Drop rows whose absolute z-score > z_thresh on *any* monitored column."""
    z     = df[zcols].apply(zscore, nan_policy='omit')
    mask  = (np.abs(z) > z_thresh).any(axis=1)
    return df.loc[~mask].copy(), int(mask.sum())

def _impute_median(df: pd.DataFrame, cols=_KEYCOLS) -> pd.DataFrame:
    for c in cols:
        df[c] = df[c].fillna(df[c].median())
    return df

def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df['HasRain'] = (df['Precipitation'] > 0).astype(int)
    df['Hour']    = df['Timestamp'].dt.hour
    df['Month']   = df['Timestamp'].dt.month
    return df

# 3. PUBLIC API
def clean_solar_df(raw: pd.DataFrame,
                   *,
                   z_thresh: float = 3,
                   impute: bool = True,
                   add_features: bool = True,
                   save_path: str | None = None) -> pd.DataFrame:
    """
    Full cleaning pipeline:

        1. Drop 100% null columns.
        2. Set negative irradiance to 0 during night-time.
        3. Remove outlier rows (z-score > `z_thresh` on monitored columns).
        4. Median-impute remaining NaNs on key sensors (optional).
        5. Add convenience features (optional).

    Parameters
    
    raw : pd.DataFrame
        The unprocessed dataframe.
    z_thresh : float, default 3
        Z-score cut-off for outlier removal.
    impute : bool, default True
        If True, median-fill the key sensor columns.
    add_features : bool, default True
        If True, add HasRain / Hour / Month columns.
    save_path : str or None
        If provided, write the final dataframe to CSV.

    Returns
    ---
    pd.DataFrame
        The cleaned (and optionally enriched) dataframe.
    """
    # --- 1 & 2: mandatory hygiene steps 
    df = _drop_empty_columns(raw.copy(), thresh=1.0)
    df = _zero_night_negatives(df)

    # --- 3: outlier clipping 
    df, n_out = _clip_outliers(df, z_thresh=z_thresh)
    if n_out:
        print(f"Dropped outliers: {n_out}")

    # --- 4: median impute 
    if impute:
        df = _impute_median(df)

    # --- 5: feature engineering 
    if add_features:
        df = _engineer_features(df)

    # --- optional save 
    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Saved cleaned dataframe → {save_path}")

    return df

#  3. PLOTTING HELPERS 
import matplotlib.pyplot as plt, seaborn as sns, matplotlib.dates as mdates
from windrose import WindroseAxes

sns.set_style("whitegrid")

def line_overview(df, cols=('GHI','DNI','DHI','Tamb')):
    fig, ax = plt.subplots(figsize=(14,4))
    for c in cols:
        ax.plot(df['Timestamp'], df[c], label=c, alpha=.6)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.legend(ncol=len(cols))
    ax.set_title("Irradiance & Tamb (full record)")
    plt.tight_layout(); return ax

def diurnal_curve(df):
    hourly = df.groupby('Hour')[['GHI','DNI','DHI','Tamb']].mean()
    ax = hourly[['GHI','DNI','DHI']].plot(marker='o', figsize=(10,4))
    ax2 = ax.twinx(); hourly['Tamb'].plot(ax=ax2, color='gray', marker='o')
    ax.set_xticks(range(0,24,2)); ax.set_title("Average Diurnal Pattern")
    return ax

def monthly_facets(df):
    df_m = df.assign(Month=df['Timestamp'].dt.strftime('%b'),
                     Day=df['Timestamp'].dt.day)
    g = sns.relplot(data=df_m, x='Day', y='GHI',
                    col='Month', col_wrap=4, kind='line',
                    height=2.5, aspect=1.5, linewidth=.7, alpha=.8,
                    facet_kws={'sharey': False, 'sharex': False})
    for ax in g.axes.flatten():
        ax.set_xticks(range(1,32,2)); ax.set_xticklabels(range(1,32,2))
    g.set_axis_labels("Day", "GHI (W/m²)")
    g.fig.suptitle('Monthly GHI Patterns', y=1.02)
    return g

def cleaning_impact(df):
    imp = (df.groupby('Cleaning')[['ModA','ModB']].mean()
             .rename(index={0:'Pre/No-Clean',1:'Post-Clean'}))
    ax = imp.plot(kind='bar', rot=0, figsize=(6,4)); ax.set_title("Cleaning Effect")
    return ax, imp.round(1)

def corr_heatmap(df, cols=('GHI','DNI','DHI','TModA','TModB')):
    corr = df[list(cols)].corr()
    ax = sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, square=True)
    ax.set_title("Correlation Matrix"); return ax

def wind_rose(df):
    ax = WindroseAxes.from_ax()
    ax.bar(df['WD'], df['WS'], normed=True,
           opening=.8, edgecolor='white', bins=[0,2,4,6,8,10,12])
    ax.set_title("Wind-Rose"); return ax
    


def bubble_ghi_tamb(df: pd.DataFrame,
                    size_col: str = "RH",
                    n: int = 20_000,
                    alpha: float = 0.35,
                    size_scale: float = 0.9,
                    ax: plt.Axes | None = None,
                    title: str | None = None) -> plt.Axes:
    """
    Return an Axes object with a bubble plot:
        x = GHI, y = Tamb, bubble area ∝ `size_col` (RH or BP).

    Parameters
    ----------
    df : DataFrame with 'GHI', 'Tamb', size_col
    size_col : str, default "RH"      Column controlling bubble size
    n : int,  default 20_000          Sub‑sample for clarity
    alpha : float, default 0.35       Bubble transparency
    size_scale : float, default 0.9   Linear scale factor → marker area
    ax : matplotlib Axes or None      Pass an existing axis or create new
    title : str or None               Custom title

    Returns
    -------
    ax : matplotlib Axes
    """
    if size_col not in df.columns:
        raise KeyError(f"{size_col!r} not found in dataframe.")

    sample = df.sample(min(len(df), n), random_state=42)

    # Use provided axis or make one
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    sc = ax.scatter(sample["GHI"],
                    sample["Tamb"],
                    s=sample[size_col] * size_scale,
                    alpha=alpha,
                    edgecolor="black",
                    linewidths=0.3)

    ax.set_xlabel("GHI (W/m²)")
    ax.set_ylabel("Tamb (°C)")
    ax.set_title(title or f"Bubble Chart – GHI vs Tamb (bubble = {size_col})")
    ax.grid(alpha=0.3)

    # -- size legend -------------------------------------------------------
    for v in [20, 40, 60, 80, 100]:
        ax.scatter([], [], s=v * size_scale, c="gray", alpha=alpha,
                   edgecolor="black", linewidths=0.3,
                   label=f"{size_col} {v}")
    ax.legend(scatterpoints=1, frameon=False, title=size_col)

    return ax