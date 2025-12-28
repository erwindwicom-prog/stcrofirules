import sys
import os
import pandas as pd
import yaml
import logging

# Setup path & logger
sys.path.insert(0, os.path.abspath('.'))
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def load_config():
    with open('config/rules.yaml') as f:
        return yaml.safe_load(f)

def parse_idx_scientific(x):
    if pd.isna(x) or x == "" or x == '""':
        return None
    x = str(x).replace('"', '').replace("'", "").strip()
    x = x.replace(',', '.')
    try:
        return float(x)
    except:
        import re
        match = re.match(r"([+-]?\d*\.?\d+)E([+-]?\d+)", x, re.IGNORECASE)
        if match:
            return float(match.group(1)) * (10 ** int(match.group(2)))
        return None

def load_fundamental_data(filepath="data/raw/fundamental.csv"):
    logger.info("📥 Loading fundamental.csv...")
    df = pd.read_csv(filepath, dtype=str, keep_default_na=False)
    for col in ['MarketCap', 'ROE', 'DER', 'NPM']:
        if col in df.columns:
            df[col] = df[col].apply(parse_idx_scientific)
    logger.info(f"✅ Loaded {len(df)} stocks.")
    return df

def apply_fundamental_gate(df, rules):
    config = rules['fundamental']
    passed = (
        (df['MarketCap'] >= config['market_cap_min']) &
        (df['ROE'] >= config['roe_min']) &
        (df['DER'] <= config['der_max']) &
        (df['NPM'] >= config['npm_min'])
    )
    return df[passed].copy()

def main():
    logger.info("🚀 Memulai screening sistem...")

    # Load data & config
    df = load_fundamental_data()
    rules = load_config()

    # Filter fundamental
    df_pass = apply_fundamental_gate(df, rules)
    logger.info(f"✅ Fundamental PASS: {len(df_pass)} saham")

    # Simpan hasil
    os.makedirs("output", exist_ok=True)
    if len(df_pass) > 0:
        # Format untuk UI Streamlit
        df_pass['MarketCap'] = df_pass['MarketCap'].apply(lambda x: f"Rp{x:,.0f}".replace(",", "."))
        df_pass['ROE'] = df_pass['ROE'].apply(lambda x: f"{x:.1f}%")
        df_pass['DER'] = df_pass['DER'].apply(lambda x: f"{x:.2f}")
        df_pass['NPM'] = df_pass['NPM'].apply(lambda x: f"{x:.1f}%")
        
        df_pass[['Ticker', 'Sector', 'MarketCap', 'ROE', 'DER', 'NPM']].to_csv(
            "output/watchlist.csv", index=False, encoding='utf-8'
        )
        logger.info("✅ Watchlist disimpan di output/watchlist.csv")
    else:
        pd.DataFrame(columns=['Ticker','Sector','MarketCap','ROE','DER','NPM']).to_csv(
            "output/watchlist.csv", index=False
        )
        logger.warning("❌ Tidak ada saham lolos — file kosong dibuat.")

    logger.info("🎉 Screening selesai.")

if __name__ == "__main__":
    main()
