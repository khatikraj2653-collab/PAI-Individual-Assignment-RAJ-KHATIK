import os
import pandas as pd

def export_to_csv(df: pd.DataFrame, filepath: str):
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    df.to_csv(filepath, index=False)
