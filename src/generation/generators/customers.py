from datetime import timedelta

import numpy as np
import pandas as pd

from src.generation.config import (
    COUNTRY_CODES,
    END_DATE,
    N_CUSTOMERS,
    START_DATE,
)


RISK_PROFILE_MAP = {
    1: "Conservative",
    2: "Cautious",
    3: "Balanced",
    4: "Growth",
    5: "Adventurous",
}


def generate_customers() -> pd.DataFrame:
    """Generate synthetic customer master data."""

    start_date = pd.Timestamp(START_DATE)
    end_date = pd.Timestamp(END_DATE)

    registration_days = (end_date - start_date).days

    customer_ids = np.arange(1, N_CUSTOMERS + 1)

    registration_offsets = np.random.randint(
        0,
        registration_days + 1,
        size=N_CUSTOMERS,
    )

    registration_ts = (
        start_date
        + pd.to_timedelta(registration_offsets, unit="D")
        + pd.to_timedelta(
            np.random.randint(0, 24 * 60 * 60, size=N_CUSTOMERS),
            unit="s",
        )
    )

    ages = np.clip(
        np.random.normal(
            loc=42,
            scale=12,
            size=N_CUSTOMERS,
        ).round(),
        18,
        80,
    ).astype(int)

    date_of_birth = (
        registration_ts
        - pd.to_timedelta(
            ages * 365 + np.random.randint(0, 365, size=N_CUSTOMERS),
            unit="D",
        )
    ).normalize()

    countries = np.random.choice(
        COUNTRY_CODES,
        size=N_CUSTOMERS,
        p=[
            0.35,  # IT
            0.15,  # GB
            0.12,  # DE
            0.10,  # FR
            0.10,  # ES
            0.07,  # NL
            0.06,  # BE
            0.05,  # IE
        ],
    )

    nationality_codes = np.random.choice(
        COUNTRY_CODES,
        size=N_CUSTOMERS,
    )

    employment_status = np.random.choice(
        [
            "employed",
            "self_employed",
            "student",
            "retired",
            "unemployed",
            "other",
        ],
        size=N_CUSTOMERS,
        p=[
            0.55,
            0.12,
            0.08,
            0.12,
            0.06,
            0.07,
        ],
    )

    income_band = np.random.choice(
        [
            "<25k",
            "25k-50k",
            "50k-75k",
            "75k-100k",
            "100k+",
        ],
        size=N_CUSTOMERS,
        p=[
            0.20,
            0.35,
            0.23,
            0.12,
            0.10,
        ],
    )

    risk_score = np.random.choice(
        [1, 2, 3, 4, 5],
        size=N_CUSTOMERS,
        p=[
            0.12,
            0.18,
            0.32,
            0.25,
            0.13,
        ],
    )

    risk_profile = pd.Series(
        risk_score
    ).map(RISK_PROFILE_MAP).to_numpy()

    acquisition_channel = np.random.choice(
        [
            "organic",
            "paid_search",
            "referral",
            "social",
            "partnership",
            "direct",
        ],
        size=N_CUSTOMERS,
        p=[
            0.25,
            0.22,
            0.18,
            0.12,
            0.13,
            0.10,
        ],
    )

    customer_status = np.random.choice(
        [
            "registered",
            "onboarded",
            "active",
            "inactive",
            "churned",
        ],
        size=N_CUSTOMERS,
        p=[
            0.08,
            0.10,
            0.58,
            0.14,
            0.10,
        ],
    )

    marketing_consent = np.random.choice(
        [True, False],
        size=N_CUSTOMERS,
        p=[0.68, 0.32],
    )

    created_at = registration_ts



    updated_at = registration_ts + pd.to_timedelta(
        np.random.randint(
            0,
            180,
            size=N_CUSTOMERS,
        ),
        unit="D",
    )

    end_timestamp = (
        end_date
        + pd.Timedelta(days=1)
        - pd.Timedelta(seconds=1)
    )

    updated_at = np.minimum(
        updated_at.values.astype("datetime64[ns]"),
        np.datetime64(end_timestamp),
    )

    customers = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "registration_ts": registration_ts,
            "date_of_birth": date_of_birth,
            "country_code": countries,
            "nationality_code": nationality_codes,
            "employment_status": employment_status,
            "income_band": income_band,
            "risk_score": risk_score,
            "risk_profile": risk_profile,
            "acquisition_channel": acquisition_channel,
            "customer_status": customer_status,
            "marketing_consent": marketing_consent,
            "created_at": created_at,
            "updated_at": updated_at,
        }
    )

    return customers.sort_values("customer_id").reset_index(drop=True)
