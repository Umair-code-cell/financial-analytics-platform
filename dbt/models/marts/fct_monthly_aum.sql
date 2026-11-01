
select
    reporting_month,

    count(*) as valued_accounts,

    count(*) filter (
        where market_value > 0
    ) as accounts_with_positive_aum,

    sum(market_value) as total_aum,

    sum(cash_value) as total_cash_value,

    sum(invested_value) as total_invested_value,

    max(snapshot_date) as latest_snapshot_date

from {{ ref('int_monthly_account_valuations') }}

group by reporting_month
