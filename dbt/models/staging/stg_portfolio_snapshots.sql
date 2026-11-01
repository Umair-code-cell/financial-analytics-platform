
select
    account_id,
    portfolio_id,
    snapshot_date::date as snapshot_date,
    round(market_value::numeric, 2) as market_value,
    round(cash_value::numeric, 2) as cash_value,
    round(invested_value::numeric, 2) as invested_value,
    daily_return,
    cumulative_return,
    benchmark_return,
    valuation_ts::timestamp as valuation_ts,
    loaded_at::timestamp as loaded_at
from {{ source('raw', 'portfolio_snapshots') }}
