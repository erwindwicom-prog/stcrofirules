from src.utils import setup_logger
from src import data_ingestion as di

logger = setup_logger()

def main():
    logger.info("🚀 Memulai screening...")
    df = di.load_fundamental_data()
    logger.info(f"📈 Data siap: {len(df)} saham")
    logger.info("🎉 Selesai (versi dasar).")

if __name__ == "__main__":
    main()
