from __future__ import annotations
from pathlib import Path
import pandas as pd

def load_raw_polls(raw_csv_path: Path) -> pd.DataFrame:
    """Load raw polling export snapshot (CSV)."""
    if not raw_csv_path.exists():
        raise FileNotFoundError(f"Raw dataset not found at: {raw_csv_path}")
    return pd.read_csv(raw_csv_path)
