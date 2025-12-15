import pandas as pd
from pathlib import Path

def load_transactions(csv_path):
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # 🔑 Normalize column names (fixes your error)
    df.columns = df.columns.str.strip().str.lower()

    # Accept flexible naming
    member_col = None
    item_col = None

    for col in df.columns:
        if "member" in col:
            member_col = col
        if "item" in col:
            item_col = col

    if member_col is None or item_col is None:
        raise ValueError(f"CSV must contain member and item columns, got {df.columns}")

    transactions = (
        df.groupby(member_col)[item_col]
        .apply(lambda x: set(x.dropna().astype(str).str.strip()))
        .tolist()
    )

    return [t for t in transactions if t]

