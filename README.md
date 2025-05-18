# Solar Challenge – Week 1

## Local setup
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

### 1.  Install dependencies

```bash
python -m venv .venv          # or conda create -n solar-challenge python=3.10
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt