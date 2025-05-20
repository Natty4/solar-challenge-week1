import pandas as pd
from pathlib import Path

# Get available countries
def get_available_countries(data_dir: Path) -> list:
    csv_files = list(data_dir.glob("*_clean.csv"))
    countries = [f.name.replace("_clean.csv", "") for f in csv_files]
    return countries

# Load selected data
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
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)