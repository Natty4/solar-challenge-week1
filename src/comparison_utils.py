from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, kruskal
import os

class ComparisonManager:
    def __init__(self, data_dir="data", countries=None, metrics=None):
        self.data_dir = Path(data_dir)
        self.countries = countries or ["benin", "sierraleone", "togo"]
        self.metrics = metrics or ["GHI", "DNI", "DHI"]
        self.data = {}
        self.summary = None

    def load_data(self):
        for country in self.countries:
            file_path = self.data_dir / f"{country}_clean.csv"
            try:
                df = pd.read_csv(file_path)
                self.data[country] = df
            except FileNotFoundError:
                print(f"⚠️ File not found: {file_path}")
            except pd.errors.ParserError:
                print(f"⚠️ Parsing error: {file_path}")
    
    def generate_summary_table(self):
        combined = pd.concat([
            df.assign(Country=country.capitalize()) 
            for country, df in self.data.items()
        ])
        summary = combined.groupby("Country")[self.metrics].agg(["mean", "median", "std"]).round(2)
        return summary
    
    def generate_country_ranking(self, metric="GHI", ascending=False, plot=True):
        ranking_data = []
        for country, df in self.data.items():
            if metric in df.columns:
                ranking_data.append({
                    "Country": country.capitalize(),
                    f"Mean {metric}": df[metric].mean()
                })
        ranking_df = pd.DataFrame(ranking_data)
        ranking_df.sort_values(by=f"Mean {metric}", ascending=ascending, inplace=True)
        ranking_df.reset_index(drop=True, inplace=True)
        ranking_df.index += 1  # start ranks from 1
        ranking_df.insert(0, "Rank", ranking_df.index)

        if plot:
            plt.figure(figsize=(8, 5))
            sns.barplot(
                data=ranking_df, 
                y=f"Mean {metric}", 
                x="Country", 
                palette="viridis" if not ascending else "magma"
            )
            plt.title(f"{metric} Ranking by Country")
            plt.xlabel(f"Mean {metric}")
            plt.ylabel("Country")
            plt.tight_layout()
            plt.show()

        return ranking_df
    
    def plot_metric_boxplots(self, save=False, save_dir="dashboard_screenshot"):
        if save:
            Path(save_dir).mkdir(exist_ok=True)

        for metric in self.metrics:
            records = []
            for country, df in self.data.items():
                if metric in df.columns:
                    for value in df[metric].dropna():
                        records.append({"Country": country.capitalize(), metric: value})
            plot_df = pd.DataFrame(records)

            plt.figure(figsize=(8, 5))
            sns.boxplot(data=plot_df, x="Country", y=metric, palette="Set2")
            plt.title(f"{metric} Comparison Across Countries")
            plt.ylabel(f"{metric} (W/m²)")
            plt.xlabel("Country")
            plt.tight_layout()

            if save:
                save_path = Path(save_dir) / f"{metric.lower()}_boxplot.png"
                try:
                    plt.savefig(save_path)
                except Exception as e:
                    print(f"❌ Failed to save {metric} boxplot: {e}")
            else:
                plt.show()

            plt.close()
            
    
    def run_statistical_tests(self, metric="GHI"):
        values = [df[metric].dropna() for df in self.data.values() if metric in df.columns]
        if len(values) < 2:
            print("⚠️ Not enough data for statistical testing.")
            return None
        try:
            anova_result = f_oneway(*values)
            kruskal_result = kruskal(*values)
            return {
                "ANOVA p-value": f"{anova_result.pvalue:.4f}",
                "Kruskal–Wallis p-value": f"{kruskal_result.pvalue:.4f}"
            }
        except Exception as e:
            print(f"❌ Statistical test failed: {e}")
            return None