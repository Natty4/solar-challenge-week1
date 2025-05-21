from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, kruskal


def get_available_countries(data_dir: Path) -> list:
    csv_files = list(data_dir.glob("*_clean.csv"))
    return [f.name.replace("_clean.csv", "") for f in csv_files]

def load_clean_data(data_dir: Path, country: str) -> pd.DataFrame:
    file_path = data_dir / f"{country}_clean.csv"
    if file_path.exists():
        return pd.read_csv(file_path, parse_dates=["Timestamp"])
    return pd.DataFrame()

def load_all_countries(data_dir: Path) -> pd.DataFrame:
    dfs = []
    for file in data_dir.glob("*_clean.csv"):
        country = file.stem.replace("_clean", "").capitalize()
        df = pd.read_csv(file, parse_dates=["Timestamp"])
        df["Country"] = country
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()



def generate_summary(df: pd.DataFrame, metrics: list) -> pd.DataFrame:
    return df.groupby("Country")[metrics].agg(["mean", "median", "std"]).round(2)


def plot_country_ranking(df: pd.DataFrame, metric: str, ascending=False):
    avg_df = df.groupby("Country")[metric].mean().reset_index()
    avg_df.sort_values(metric, ascending=ascending, inplace=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=avg_df, y="Country", x=metric, palette="viridis" if not ascending else "magma", ax=ax)
    ax.set_title(f"{metric} Ranking by Country")
    ax.set_xlabel(f"Average {metric}")
    ax.set_ylabel("Country")
    return fig

def plot_metric_boxplot(df: pd.DataFrame, metric: str):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x="Country", y=metric, palette="Set2", ax=ax)
    ax.set_title(f"{metric} Distribution by Country")
    return fig


def run_statistical_tests(df: pd.DataFrame, metric: str) -> dict:
    groups = [group[metric].dropna() for _, group in df.groupby("Country") if metric in group.columns]
    if len(groups) < 2:
        return {"error": "Not enough groups for statistical testing."}
    try:
        return {
            "ANOVA p-value": f"{f_oneway(*groups).pvalue:.4f}",
            "Kruskal–Wallis p-value": f"{kruskal(*groups).pvalue:.4f}"
        }
    except Exception as e:
        return {"error": str(e)}


class ComparisonManager:
    def __init__(self, data_dir="data", metrics=None):
        self.data_dir = Path(data_dir)
        self.metrics = metrics or ["GHI", "DNI", "DHI"]
        self.df_all = load_all_countries(self.data_dir)

    def summary(self):
        return generate_summary(self.df_all, self.metrics)

    def ranking(self, metric="GHI", ascending=False):
        return self.df_all.groupby("Country")[metric].mean().sort_values(ascending=ascending)

    def plot_ranking(self, metric="GHI", ascending=False):
        return plot_country_ranking(self.df_all, metric, ascending)

    def plot_box(self, metric="GHI"):
        return plot_metric_boxplot(self.df_all, metric)

    def stats(self, metric="GHI"):
        return run_statistical_tests(self.df_all, metric)