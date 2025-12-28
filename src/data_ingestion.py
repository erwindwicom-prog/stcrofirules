import pandas as pd
import re

def parse_idx_scientific(x):
    if pd.isna(x) or x == "" or x == '""':
        return None
    x = str(x).replace('"', '').replace("'", "").strip()
    if not x:
        return None
    x = x.replace(',', '.')
    try:
        return float(x)
    except:
        match = re.match(r"([+-]?\d*\.?\d+)E([+-]?\d+)", x, re.IGNORECASE)
        if match:
            return float(match.group(1)) * (10 ** int(match.group(2)))
        return None

def load_fundamental_data(filepath="data/raw/fundamental.csv"):
    print("📥 Loading fundamental.csv...")
    df = pd.read_csv(filepath, dtype=str, keep_default_na=False)
    for col in ['MarketCap', 'ROE', 'DER', 'NPM']:
        if col in df.columns:
            df[col] = df[col].apply(parse_idx_scientific)
    print(f"✅ Loaded {len(df)} stocks.")
    return df
