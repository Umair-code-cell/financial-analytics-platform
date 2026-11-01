from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
REFERENCE_DIR = PROJECT_ROOT / "data" / "reference"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "financial_analytics")
DB_USER = os.getenv("DB_USER", "finanalytics_user")
DB_PASSWORD = os.getenv("DB_PASSWORD")


if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is not set in .env")


engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


TABLES = {
    "raw": {
        "customers": RAW_DIR / "customers.csv",
        "accounts": RAW_DIR / "accounts.csv",
        "transactions": RAW_DIR / "transactions.csv",
        "portfolio_snapshots": RAW_DIR / "portfolio_snapshots.csv",
        "customer_events": RAW_DIR / "customer_events.csv",
        "market_prices": RAW_DIR / "market_prices.csv",
    },
    "reference": {
        "products": REFERENCE_DIR / "products.csv",
        "portfolios": REFERENCE_DIR / "portfolios.csv",
        "instruments": REFERENCE_DIR / "instruments.csv",
        "portfolio_holdings": REFERENCE_DIR / "portfolio_holdings.csv",
    },
}


def load_table(
    schema: str,
    table_name: str,
    file_path: Path,
) -> None:
    print(f"Loading {schema}.{table_name} ...")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=5000,
    )

    print(
        f"Loaded {schema}.{table_name}: "
        f"{len(df):,} rows"
    )


def main() -> None:
    print("Financial Analytics PostgreSQL Ingestion")
    print("---------------------------------------")

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS reference"))

    print("PostgreSQL source schemas verified.")

    for schema, tables in TABLES.items():
        for table_name, file_path in tables.items():

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Missing file: {file_path}"
                )

            load_table(
                schema,
                table_name,
                file_path,
            )

    print("---------------------------------------")
    print("All source tables loaded successfully.")


if __name__ == "__main__":
    main()
