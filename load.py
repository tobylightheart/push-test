"""Normalise SA Water's monthly reservoir CSVs (headers vary file to file) into one long table."""
from pathlib import Path
import pandas as pd

def _pick(cols, *needles):
    for c in cols:
        k = c.lower().replace("_", " ")
        if all(n in k for n in needles):
            return c
    return None

def load(folder="data"):
    frames = []
    for f in sorted(Path(folder).glob("*.csv")):
        try:
            df = pd.read_csv(f, encoding="utf-8-sig")
        except UnicodeDecodeError:
            df = pd.read_csv(f, encoding="latin-1")
        cols = list(df.columns)
        name, date = _pick(cols, "name"), _pick(cols, "date")
        cap, vol = _pick(cols, "capacity"), _pick(cols, "volume", "today")
        if not all([name, date, cap, vol]):
            continue  # e.g. the annual-report operations file
        out = pd.DataFrame({
            "reservoir": df[name].astype(str).str.strip(),
            "date": pd.to_datetime(df[date], dayfirst=True, errors="coerce", format="mixed"),
            "capacity_ml": pd.to_numeric(df[cap], errors="coerce"),
            "volume_ml": pd.to_numeric(df[vol], errors="coerce"),
        })
        frames.append(out)
    df = pd.concat(frames).dropna()
    df = df[df.reservoir.str.contains("Reservoir")]
    df["pct_full"] = 100 * df.volume_ml / df.capacity_ml
    return df.drop_duplicates(["reservoir", "date"]).sort_values("date")

if __name__ == "__main__":
    d = load()
    print(d.shape, d.date.min(), d.date.max())
    print(d.reservoir.value_counts())
