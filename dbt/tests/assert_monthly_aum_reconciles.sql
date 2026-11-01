
with expected as (
    select
        reporting_month,
        count(*) as expected_accounts,
        sum(market_value) as expected_aum
    from {{ ref('int_monthly_account_valuations') }}
    group by reporting_month
)

select
    m.reporting_month,
    m.total_aum,
    e.expected_aum
from {{ ref('fct_monthly_aum') }} m
full outer join expected e
    on m.reporting_month = e.reporting_month
where m.reporting_month is null
   or e.reporting_month is null
   or m.valued_accounts <> e.expected_accounts
   or m.total_aum is distinct from e.expected_aum
