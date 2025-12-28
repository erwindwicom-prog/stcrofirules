import streamlit as st
import pandas as pd
import os

# Judul aplikasi
st.set_page_config(page_title="📊 Screening Saham IHSG", layout="wide")
st.title("🚀 Sistem Screening Saham — User Friendly • Akuntabel • Disiplin")

# Load data dari CSV (di-host di GitHub)
@st.cache_data
def load_data():
    # Ganti dengan URL raw file Anda nanti
    try:
        url = "https://raw.githubusercontent.com/erwindwicom-prog/stcrofirules/main/data/raw/fundamental.csv"
        df = pd.read_csv(url, dtype=str)
        # Parse format IDX: "58,4E+12" → angka
        for col in ['MarketCap', 'ROE', 'DER', 'NPM']:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].str.replace('"', '').str.replace(',', '.'),
                    errors='coerce'
                )
        return df
    except:
        # Jika gagal, pakai data contoh
        return pd.DataFrame({
            'Ticker': ['BBRI', 'TLKM', 'UNVR'],
            'Sector': ['Bank', 'Telekomunikasi', 'Consumer'],
            'MarketCap': [150000000000000, 80000000000000, 200000000000000],
            'ROE': [18.5, 12.0, 45.0],
            'DER': [1.2, 0.8, 0.5],
            'NPM': [20.0, 15.0, 30.0]
        })

df = load_data()

# Filter: MarketCap > 10T, ROE ≥ 0, DER ≤ 2.0, NPM ≥ 0
df_filtered = df[
    (df['MarketCap'] >= 1e13) &
    (df['ROE'] >= 0) &
    (df['DER'] <= 2.0) &
    (df['NPM'] >= 0)
].copy()

# Tampilkan hasil
st.subheader(f"✅ Saham Lolos Fundamental Gate ({len(df_filtered)} saham)")
st.dataframe(df_filtered[['Ticker', 'Sector', 'MarketCap', 'ROE', 'DER', 'NPM']], use_container_width=True)

# Visualisasi sederhana
if len(df_filtered) > 0:
    st.subheader("📈 ROE vs DER (Semakin tinggi ROE & rendah DER, semakin baik)")
    st.scatter_chart(
        df_filtered,
        x='DER',
        y='ROE',
        color='Sector',
        size='MarketCap'
    )

# Info
st.markdown("---")
st.caption("Sumber data: IDX Stock Screener • Update manual bulanan")
