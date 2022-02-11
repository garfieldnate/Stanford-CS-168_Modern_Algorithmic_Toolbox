from pathlib import Path

import pandas as pd

MATERIALS = Path(__file__).parents[1] / "materials" / "Week 6"
SNAP_CSV = MATERIALS / "cs168mp6.csv"


def load_snap() -> pd.DataFrame:
    return pd.read_csv(SNAP_CSV, header=None)
