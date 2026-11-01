import numpy as np
import pandas as pd


def generate_transactions(
    accounts: pd.DataFrame,
    target_rows: int = 20_000,
) -> pd.DataFrame:
    """Generate deposits, withdrawals, fees and transfers."""

    records = []
    transaction_id = 1

    accounts = accounts.copy()
    accounts["opened_at"] = pd.to_datetime(accounts["opened_at"])
    accounts["closed_at"] = pd.to_datetime(accounts["closed_at"])

    end_date = pd.Timestamp("2026-07-31 23:59:59")

    # Every account gets an initial funding attempt
    for _, account in accounts.iterrows():

        opened = account["opened_at"]

        first_deposit_ts = opened + pd.Timedelta(
            days=np.random.randint(0, 15),
            hours=np.random.randint(0, 24),
        )

        amount = round(
            np.random.lognormal(
                mean=np.log(5000),
                sigma=0.8,
            ),
            2,
        )

        status = np.random.choice(
            ["completed", "failed"],
            p=[0.94, 0.06],
        )

        settlement_ts = (
            first_deposit_ts + pd.Timedelta(days=2)
            if status == "completed"
            else pd.NaT
        )

        records.append(
            {
                "transaction_id": transaction_id,
                "account_id": account["account_id"],
                "transaction_ts": first_deposit_ts,
                "transaction_type": "deposit",
                "amount": amount,
                "currency": "EUR",
                "status": status,
                "payment_method": np.random.choice(
                    ["bank_transfer", "card"]
                ),
                "settlement_ts": settlement_ts,
                "created_at": first_deposit_ts,
                "updated_at": settlement_ts
                if pd.notna(settlement_ts)
                else first_deposit_ts,
            }
        )

        transaction_id += 1

    remaining = max(0, target_rows - len(records))

    sampled_accounts = accounts.sample(
        n=remaining,
        replace=True,
    )

    for _, account in sampled_accounts.iterrows():

        opened = account["opened_at"]

        account_end = (
            account["closed_at"]
            if pd.notna(account["closed_at"])
            else end_date
        )

        if account_end <= opened:
            transaction_ts = opened
        else:
            seconds = int(
                (account_end - opened).total_seconds()
            )

            transaction_ts = (
                opened
                + pd.Timedelta(
                    seconds=np.random.randint(
                        0,
                        max(1, seconds),
                    )
                )
            )

        transaction_type = np.random.choice(
            [
                "deposit",
                "withdrawal",
                "fee",
                "transfer",
            ],
            p=[0.48, 0.28, 0.14, 0.10],
        )

        if transaction_type == "fee":
            amount = round(
                np.random.uniform(1, 50),
                2,
            )
        else:
            amount = round(
                np.random.lognormal(
                    mean=np.log(1500),
                    sigma=1.0,
                ),
                2,
            )

        status = np.random.choice(
            [
                "completed",
                "failed",
                "cancelled",
                "reversed",
            ],
            p=[0.92, 0.04, 0.025, 0.015],
        )

        settlement_ts = (
            transaction_ts
            + pd.Timedelta(
                days=np.random.randint(1, 4)
            )
            if status == "completed"
            else pd.NaT
        )

        records.append(
            {
                "transaction_id": transaction_id,
                "account_id": account["account_id"],
                "transaction_ts": transaction_ts,
                "transaction_type": transaction_type,
                "amount": amount,
                "currency": "EUR",
                "status": status,
                "payment_method": np.random.choice(
                    [
                        "bank_transfer",
                        "card",
                        "internal",
                    ]
                ),
                "settlement_ts": settlement_ts,
                "created_at": transaction_ts,
                "updated_at": settlement_ts
                if pd.notna(settlement_ts)
                else transaction_ts,
            }
        )

        transaction_id += 1

    return (
        pd.DataFrame(records)
        .sort_values("transaction_id")
        .reset_index(drop=True)
    )


def generate_market_prices(
    instruments: pd.DataFrame,
) -> pd.DataFrame:
    """Generate synthetic daily instrument prices."""

    dates = pd.bdate_range(
        "2023-01-02",
        "2026-07-31",
    )

    parameters = {
        "equity": (0.00030, 0.012),
        "bond": (0.00008, 0.004),
        "cash": (0.00003, 0.0002),
        "alternatives": (0.00020, 0.009),
    }

    records = []

    for _, instrument in instruments.iterrows():

        asset_class = instrument["asset_class"]

        drift, volatility = parameters[asset_class]

        start_price = np.random.uniform(
            80,
            120,
        )

        returns = np.random.normal(
            drift,
            volatility,
            len(dates),
        )

        prices = (
            start_price
            * np.exp(
                np.cumsum(returns)
            )
        )

        for date, price in zip(
            dates,
            prices,
        ):
            records.append(
                {
                    "instrument_id":
                        instrument["instrument_id"],
                    "price_date": date,
                    "asset_class": asset_class,
                    "close_price": round(
                        float(price),
                        4,
                    ),
                    "currency": "EUR",
                    "benchmark_code":
                        f"BM_{asset_class.upper()}",
                    "loaded_at":
                        date
                        + pd.Timedelta(hours=22),
                }
            )

    return pd.DataFrame(records)


def generate_portfolio_snapshots(
    accounts: pd.DataFrame,
    portfolios: pd.DataFrame,
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    """Generate periodic account portfolio valuations."""

    accounts = accounts.copy()
    portfolios = portfolios.copy()
    transactions = transactions.copy()

    accounts["opened_at"] = pd.to_datetime(
        accounts["opened_at"]
    )

    accounts["closed_at"] = pd.to_datetime(
        accounts["closed_at"]
    )

    transactions["transaction_ts"] = pd.to_datetime(
        transactions["transaction_ts"]
    )

    portfolio_risk = (
        portfolios
        .set_index("portfolio_id")["risk_level"]
        .to_dict()
    )

    completed = transactions[
        transactions["status"] == "completed"
    ].copy()

    completed["signed_amount"] = np.select(
        [
            completed["transaction_type"] == "deposit",
            completed["transaction_type"] == "withdrawal",
            completed["transaction_type"] == "fee",
        ],
        [
            completed["amount"],
            -completed["amount"],
            -completed["amount"],
        ],
        default=0.0,
    )

    end_date = pd.Timestamp("2026-07-31")

    records = []

    for _, account in accounts.iterrows():

        account_id = account["account_id"]
        portfolio_id = account["portfolio_id"]

        opened = account["opened_at"].normalize()

        closed = (
            account["closed_at"].normalize()
            if pd.notna(account["closed_at"])
            else end_date
        )

        # Weekly valuations keeps development dataset manageable
        dates = pd.date_range(
            opened,
            closed,
            freq="7D",
        )

        if len(dates) == 0:
            continue

        account_tx = completed[
            completed["account_id"] == account_id
        ].sort_values(
            "transaction_ts"
        )

        risk_level = int(
            portfolio_risk[portfolio_id]
        )

        daily_mu = {
            1: 0.00008,
            2: 0.00012,
            3: 0.00018,
            4: 0.00024,
            5: 0.00030,
        }[risk_level]

        daily_sigma = {
            1: 0.002,
            2: 0.003,
            3: 0.0045,
            4: 0.006,
            5: 0.008,
        }[risk_level]

        market_value = 0.0
        cumulative_return = 0.0
        previous_date = opened

        for snapshot_date in dates:

            tx_until_date = account_tx[
                (
                    account_tx["transaction_ts"]
                    > previous_date
                )
                & (
                    account_tx["transaction_ts"]
                    <= snapshot_date
                    + pd.Timedelta(days=1)
                )
            ]

            net_flow = tx_until_date[
                "signed_amount"
            ].sum()

            days = max(
                1,
                (snapshot_date - previous_date).days,
            )

            period_return = np.random.normal(
                daily_mu * days,
                daily_sigma * np.sqrt(days),
            )

            benchmark_return = (
                period_return
                + np.random.normal(
                    0,
                    0.002,
                )
            )

            market_value = max(
                0.0,
                market_value
                * (1 + period_return)
                + net_flow,
            )

            cumulative_return = (
                (1 + cumulative_return)
                * (1 + period_return)
                - 1
            )

            cash_value = (
                market_value
                * np.random.uniform(
                    0.01,
                    0.08,
                )
            )

            invested_value = (
                market_value
                - cash_value
            )

            records.append(
                {
                    "account_id": account_id,
                    "portfolio_id": portfolio_id,
                    "snapshot_date":
                        snapshot_date,
                    "market_value":
                        round(
                            market_value,
                            2,
                        ),
                    "cash_value":
                        round(
                            cash_value,
                            2,
                        ),
                    "invested_value":
                        round(
                            invested_value,
                            2,
                        ),
                    "daily_return":
                        round(
                            period_return,
                            8,
                        ),
                    "cumulative_return":
                        round(
                            cumulative_return,
                            8,
                        ),
                    "benchmark_return":
                        round(
                            benchmark_return,
                            8,
                        ),
                    "valuation_ts":
                        snapshot_date
                        + pd.Timedelta(hours=21),
                    "loaded_at":
                        snapshot_date
                        + pd.Timedelta(hours=23),
                }
            )

            previous_date = snapshot_date

    return pd.DataFrame(records)


def generate_customer_events(
    customers: pd.DataFrame,
    target_rows: int = 40_000,
) -> pd.DataFrame:
    """Generate digital customer behaviour events."""

    customers = customers.copy()

    customers["registration_ts"] = pd.to_datetime(
        customers["registration_ts"]
    )

    end_date = pd.Timestamp(
        "2026-07-31 23:59:59"
    )

    sampled = customers.sample(
        n=target_rows,
        replace=True,
    )

    records = []

    event_names = [
        "app_open",
        "login",
        "onboarding_started",
        "onboarding_completed",
        "portfolio_viewed",
        "deposit_started",
        "deposit_completed",
        "withdrawal_started",
        "risk_questionnaire_completed",
    ]

    event_probs = [
        0.20,
        0.19,
        0.07,
        0.06,
        0.16,
        0.09,
        0.08,
        0.05,
        0.10,
    ]

    for event_id, (_, customer) in enumerate(
        sampled.iterrows(),
        start=1,
    ):

        registration = customer[
            "registration_ts"
        ]

        seconds_available = max(
            1,
            int(
                (
                    end_date
                    - registration
                ).total_seconds()
            ),
        )

        event_ts = (
            registration
            + pd.Timedelta(
                seconds=np.random.randint(
                    0,
                    seconds_available,
                )
            )
        )

        records.append(
            {
                "event_id": event_id,
                "customer_id":
                    customer["customer_id"],
                "event_ts": event_ts,
                "event_name":
                    np.random.choice(
                        event_names,
                        p=event_probs,
                    ),
                "session_id":
                    f"S{np.random.randint(1, 15000):08d}",
                "platform":
                    np.random.choice(
                        [
                            "ios",
                            "android",
                            "web",
                        ],
                        p=[
                            0.42,
                            0.38,
                            0.20,
                        ],
                    ),
                "event_source":
                    np.random.choice(
                        [
                            "mobile_app",
                            "website",
                            "backend",
                        ],
                        p=[
                            0.55,
                            0.30,
                            0.15,
                        ],
                    ),
                "properties_json":
                    "{}",
            }
        )

    return pd.DataFrame(records)