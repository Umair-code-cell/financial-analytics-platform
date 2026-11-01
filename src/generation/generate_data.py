import random

import numpy as np

from src.generation.generators.reference_data import (
    generate_products,
    generate_portfolios,
    generate_instruments,
    generate_portfolio_holdings,
)

from src.generation.config import (
    RANDOM_SEED,
    START_DATE,
    END_DATE,
    N_CUSTOMERS,
    RAW_DATA_DIR,
    REFERENCE_DATA_DIR,
)
from src.generation.generators.activity_data import (
    generate_transactions,
    generate_market_prices,
    generate_portfolio_snapshots,
    generate_customer_events,
)

from src.generation.generators.customers import generate_customers
from src.generation.generators.accounts import generate_accounts


def set_random_seeds() -> None:
    """Set deterministic seeds for reproducible synthetic data."""
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)


def create_output_directories() -> None:
    """Create output directories if they do not already exist."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DATA_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    # 1. Initialize environment
    set_random_seeds()
    create_output_directories()

    # 2. Generate reference data
    products = generate_products()
    portfolios = generate_portfolios()
    instruments = generate_instruments()
    customers = generate_customers()

    portfolio_holdings = generate_portfolio_holdings(
        portfolios,
        instruments,
    )
    accounts = generate_accounts(
        customers,
        portfolios,
    )

    transactions = generate_transactions(
        accounts,
    )

    market_prices = generate_market_prices(
        instruments,
    )

    portfolio_snapshots = generate_portfolio_snapshots(
        accounts,
        portfolios,
        transactions,
    )

    customer_events = generate_customer_events(
        customers,
    )

    # 3. Save reference data
    products.to_csv(
        REFERENCE_DATA_DIR / "products.csv",
        index=False,
    )

    portfolios.to_csv(
        REFERENCE_DATA_DIR / "portfolios.csv",
        index=False,
    )

    instruments.to_csv(
        REFERENCE_DATA_DIR / "instruments.csv",
        index=False,
    )

    portfolio_holdings.to_csv(
        REFERENCE_DATA_DIR / "portfolio_holdings.csv",
        index=False,
    )
    customers.to_csv(
        RAW_DATA_DIR / "customers.csv",
        index=False,
    )

    accounts.to_csv(
        RAW_DATA_DIR / "accounts.csv",
        index=False,
    )

    transactions.to_csv(
        RAW_DATA_DIR / "transactions.csv",
        index=False,
    )

    market_prices.to_csv(
        RAW_DATA_DIR / "market_prices.csv",
        index=False,
    )

    portfolio_snapshots.to_csv(
        RAW_DATA_DIR / "portfolio_snapshots.csv",
        index=False,
    )

    customer_events.to_csv(
        RAW_DATA_DIR / "customer_events.csv",
        index=False,
    )


    # 4. Verification output
    print("Financial Analytics synthetic data generator")
    print("------------------------------------------")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Simulation period: {START_DATE} to {END_DATE}")
    print(f"Development customers: {N_CUSTOMERS}")
    print(f"Generated products: {len(products):,}")
    print(f"Generated portfolios: {len(portfolios):,}")
    print(f"Generated instruments: {len(instruments):,}")
    print(f"Generated customers: {len(customers):,}")
    print(f"Generated accounts: {len(accounts):,}")
    print(
        f"Generated transactions: "
        f"{len(transactions):,}"
    )

    print(
        f"Generated market prices: "
        f"{len(market_prices):,}"
    )

    print(
        f"Generated portfolio snapshots: "
        f"{len(portfolio_snapshots):,}"
    )

    print(
        f"Generated customer events: "
        f"{len(customer_events):,}"
    )

    print(
        f"Generated portfolio holdings: "
        f"{len(portfolio_holdings):,}"
    )
    print(f"Raw data directory: {RAW_DATA_DIR}")
    print(f"Reference data directory: {REFERENCE_DATA_DIR}")
    print("Generator initialization successful.")


if __name__ == "__main__":
    main()
