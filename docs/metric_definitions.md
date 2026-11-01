# Financial KPI Definitions

## Overview

This document defines the core financial and customer metrics produced by the Financial Analytics Platform.

The reporting layer is implemented in PostgreSQL using dbt. Metrics are calculated from synthetic customer, account, transaction and portfolio valuation data.

## 1. Assets Under Management (AUM)

**dbt model:** `fct_monthly_aum`

**Definition:** The sum of portfolio market values across investment accounts represented in the selected monthly valuation snapshots.

**Calculation:**

AUM = Sum of selected account-level market values

For each account and calendar month, the platform selects the latest available snapshot within that month.

**Reporting grain:** One row per calendar month.

**Limitations:**
- Represents the latest available in-month valuation, not necessarily the exact calendar month-end.
- Missing account valuations are not automatically carried forward.
- Historical valuations are based on synthetic market data.

## 2. Net Money Flows

**dbt model:** `fct_monthly_money_flows`

**Definition:** Net cash contributed to or withdrawn from investment accounts through completed deposit and withdrawal transactions.

**Calculation:**

Net Money Flows = Gross Deposits − Gross Withdrawals

Only completed deposits and withdrawals are included. Failed, cancelled and reversed transactions, fees and transfers are excluded.

Transactions are allocated to reporting months using their transaction timestamps.

**Reporting grain:** One row per calendar month containing qualifying money-flow activity.

**Limitations:**
- Net flows should not be interpreted as investment performance.
- Valuation changes and market returns are not part of the net-flow calculation.

## 3. Monthly Active Investors

**dbt model:** `fct_monthly_active_investors`

**Definition:** The number of distinct customers holding at least one eligible investment account with positive market value in the monthly valuation snapshot.

**Calculation:**

Monthly Active Investors = Count of distinct customers with at least one qualifying positive-value account

Account eligibility considers the account opening and closing dates relative to the selected snapshot.

**Reporting grain:** One row per calendar month.

**Limitations:**
- Activity represents invested-account status, not proof of trading or application engagement.
- Counts reflect available valuation snapshots rather than continuous daily account activity.

## 4. Customer Activation Rate

**dbt model:** `fct_monthly_customer_activation`

**Definition:** The proportion of eligible newly registered customers who complete their first deposit within 30 days of registration.

**Calculation:**

30-Day Activation Rate = Customers activated within 30 days / Eligible registered customers

A customer is activated by their first completed deposit associated with an investment account.

The eligible denominator excludes registrations whose entire 30-day observation window has not yet elapsed by the available transaction-data cutoff.

**Reporting grain:** One row per customer registration month.

**Limitations:**
- Recent cohorts may be incomplete.
- The current observation cutoff is derived from the latest transaction timestamp, rather than a separately governed reporting date.
- Activation does not imply long-term customer retention.

## 5. Data Quality and Validation

The platform uses dbt tests to validate source relationships, transformations, reporting constraints and financial calculations.

Validation includes:

- Primary-key uniqueness and non-null checks.
- Referential integrity across core entities.
- Unique account-month valuation selection.
- Monthly net-flow reconciliation.
- Monthly AUM reconciliation and validity.
- Active-investor and customer-activation consistency.

**Validation baseline:** On 1 November 2026, the complete dbt build passed 46 operations, including 33 automated data tests, without errors or warnings.

## 6. Reporting Considerations

The metrics are designed for analytical reporting on synthetic data. They are not production financial accounting measures.

AUM, net flows, investor activity and customer activation represent different business concepts and should not be used interchangeably.

Any production implementation would require governed reporting cutoffs, explicit valuation staleness policies, appropriate financial precision, monitoring and reconciliation against authoritative financial systems.