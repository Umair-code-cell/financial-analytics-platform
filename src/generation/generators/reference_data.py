import pandas as pd


def generate_products() -> pd.DataFrame:
    """Generate the investment product catalogue."""

    products = [
        {
            "product_id": 1,
            "product_name": "General Investment",
            "product_category": "investment",
            "min_risk_level": 1,
            "max_risk_level": 5,
            "annual_fee_pct": 0.75,
            "launch_date": "2020-01-01",
            "is_active": True,
        },
        {
            "product_id": 2,
            "product_name": "Sustainable Investment",
            "product_category": "investment",
            "min_risk_level": 2,
            "max_risk_level": 5,
            "annual_fee_pct": 0.80,
            "launch_date": "2021-06-01",
            "is_active": True,
        },
        {
            "product_id": 3,
            "product_name": "Growth Investment",
            "product_category": "investment",
            "min_risk_level": 3,
            "max_risk_level": 5,
            "annual_fee_pct": 0.70,
            "launch_date": "2022-01-01",
            "is_active": True,
        },
        {
            "product_id": 4,
            "product_name": "Conservative Investment",
            "product_category": "investment",
            "min_risk_level": 1,
            "max_risk_level": 3,
            "annual_fee_pct": 0.65,
            "launch_date": "2020-09-01",
            "is_active": True,
        },
        {
            "product_id": 5,
            "product_name": "Income Investment",
            "product_category": "investment",
            "min_risk_level": 1,
            "max_risk_level": 4,
            "annual_fee_pct": 0.70,
            "launch_date": "2021-03-01",
            "is_active": True,
        },
    ]

    df = pd.DataFrame(products)
    df["launch_date"] = pd.to_datetime(df["launch_date"])

    return df


def generate_portfolios() -> pd.DataFrame:
    """Generate managed portfolios with different risk levels."""

    portfolios = []

    portfolio_id = 1

    allocations = {
        1: (20, 70, 10, 0),
        2: (35, 55, 10, 0),
        3: (50, 40, 5, 5),
        4: (70, 20, 5, 5),
        5: (85, 5, 5, 5),
    }

    benchmark_codes = {
        1: "BM_CONSERVATIVE",
        2: "BM_CAUTIOUS",
        3: "BM_BALANCED",
        4: "BM_GROWTH",
        5: "BM_ADVENTUROUS",
    }

    risk_names = {
        1: "Conservative",
        2: "Cautious",
        3: "Balanced",
        4: "Growth",
        5: "Adventurous",
    }

    # Two portfolio families, each covering all five risk levels.
    for product_id in [1, 2]:
        for risk_level in range(1, 6):

            equity, bond, cash, alternatives = allocations[risk_level]

            portfolios.append(
                {
                    "portfolio_id": portfolio_id,
                    "product_id": product_id,
                    "portfolio_name": (
                        f"{risk_names[risk_level]} "
                        f"{'Core' if product_id == 1 else 'Sustainable'}"
                    ),
                    "risk_level": risk_level,
                    "equity_pct": equity,
                    "bond_pct": bond,
                    "cash_pct": cash,
                    "alternatives_pct": alternatives,
                    "benchmark_code": benchmark_codes[risk_level],
                    "is_active": True,
                }
            )

            portfolio_id += 1

    return pd.DataFrame(portfolios)

def generate_instruments() -> pd.DataFrame:
    """Generate the investable instrument universe."""

    instruments = []

    asset_classes = {
        "equity": 12,
        "bond": 10,
        "cash": 3,
        "alternatives": 5,
    }

    instrument_id = 1

    for asset_class, count in asset_classes.items():
        for number in range(1, count + 1):
            instruments.append(
                {
                    "instrument_id": instrument_id,
                    "instrument_code": f"{asset_class.upper()}_{number:02d}",
                    "instrument_name": (
                        f"Synthetic {asset_class.title()} Instrument {number:02d}"
                    ),
                    "asset_class": asset_class,
                    "currency": "EUR",
                    "is_active": True,
                }
            )

            instrument_id += 1

    return pd.DataFrame(instruments)


def generate_portfolio_holdings(
    portfolios: pd.DataFrame,
    instruments: pd.DataFrame,
) -> pd.DataFrame:
    """Generate portfolio-to-instrument allocation weights."""

    holdings = []

    allocation_columns = {
        "equity": "equity_pct",
        "bond": "bond_pct",
        "cash": "cash_pct",
        "alternatives": "alternatives_pct",
    }

    for _, portfolio in portfolios.iterrows():

        for asset_class, allocation_column in allocation_columns.items():

            target_weight = portfolio[allocation_column]

            if target_weight == 0:
                continue

            available = instruments[
                instruments["asset_class"] == asset_class
            ]

            # Use up to three instruments from each asset class.
            selected = available.head(min(3, len(available)))

            weight_per_instrument = target_weight / len(selected)

            for _, instrument in selected.iterrows():
                holdings.append(
                    {
                        "portfolio_id": portfolio["portfolio_id"],
                        "instrument_id": instrument["instrument_id"],
                        "asset_class": asset_class,
                        "allocation_weight": weight_per_instrument,
                        "effective_from": "2023-01-01",
                        "effective_to": None,
                    }
                )

    df = pd.DataFrame(holdings)

    df["effective_from"] = pd.to_datetime(df["effective_from"])
    df["effective_to"] = pd.to_datetime(df["effective_to"])

    return df