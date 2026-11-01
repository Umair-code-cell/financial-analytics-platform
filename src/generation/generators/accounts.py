import numpy as np
import pandas as pd


def generate_accounts(
    customers: pd.DataFrame,
    portfolios: pd.DataFrame,
) -> pd.DataFrame:
    """Generate realistic investment accounts."""

    accounts = []
    account_id = 1

    end_timestamp = pd.Timestamp("2026-07-31 23:59:59")

    for _, customer in customers.iterrows():

        status = customer["customer_status"]

        # Customers who only registered may never open an account
        if status == "registered":
            if np.random.random() < 0.85:
                continue

        # Onboarded customers may still not have opened an account
        if status == "onboarded":
            if np.random.random() < 0.40:
                continue

        # Most customers have one account; some have two
        n_accounts = np.random.choice(
            [1, 2],
            p=[0.82, 0.18],
        )

        risk_score = int(customer["risk_score"])

        compatible = portfolios[
            portfolios["risk_level"].between(
                max(1, risk_score - 1),
                min(5, risk_score + 1),
            )
        ]

        for _ in range(n_accounts):

            portfolio = compatible.sample(1).iloc[0]

            registration_ts = pd.Timestamp(
                customer["registration_ts"]
            )

            days_to_open = int(
                np.random.gamma(
                    shape=2.0,
                    scale=8.0,
                )
            )

            opened_at = (
                registration_ts
                + pd.Timedelta(days=days_to_open)
                + pd.Timedelta(
                    hours=np.random.randint(0, 24)
                )
            )

            if opened_at > end_timestamp:
                opened_at = registration_ts

            account_status = "open"
            closed_at = pd.NaT

            if status == "churned":
                account_status = "closed"

                possible_close = (
                    opened_at
                    + pd.Timedelta(
                        days=np.random.randint(60, 700)
                    )
                )

                closed_at = min(
                    possible_close,
                    end_timestamp,
                )

            elif status == "inactive":
                if np.random.random() < 0.30:
                    account_status = "closed"

                    possible_close = (
                        opened_at
                        + pd.Timedelta(
                            days=np.random.randint(90, 700)
                        )
                    )

                    closed_at = min(
                        possible_close,
                        end_timestamp,
                    )

            accounts.append(
                {
                    "account_id": account_id,
                    "customer_id": customer["customer_id"],
                    "portfolio_id": portfolio["portfolio_id"],
                    "account_type": "investment",
                    "currency": "EUR",
                    "opened_at": opened_at,
                    "closed_at": closed_at,
                    "account_status": account_status,
                    "created_at": opened_at,
                    "updated_at": (
                        closed_at
                        if pd.notna(closed_at)
                        else opened_at
                    ),
                }
            )

            account_id += 1

    return (
        pd.DataFrame(accounts)
        .sort_values("account_id")
        .reset_index(drop=True)
    )
