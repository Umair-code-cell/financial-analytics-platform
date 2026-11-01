
with ranked_valuations as (

    select
        account_id,
        portfolio_id,
        date_trunc('month', snapshot_date)::date as reporting_month,
        snapshot_date,
        valuation_ts,
        market_value,
        cash_value,
        invested_value,

        row_number() over (
            partition by
                account_id,
                date_trunc('month', snapshot_date)
            order by
                snapshot_date desc,
                valuation_ts desc
        ) as valuation_rank

    from {{ ref('stg_portfolio_snapshots') }}

)

select
    account_id,
    portfolio_id,
    reporting_month,
    snapshot_date,
    market_value,
    cash_value,
    invested_value

from ranked_valuations
where valuation_rank = 1
