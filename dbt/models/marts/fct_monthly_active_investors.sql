
with eligible_accounts as (

    select
        v.reporting_month,
        v.snapshot_date,
        a.customer_id,
        v.account_id,
        v.market_value

    from {{ ref('int_monthly_account_valuations') }} v

    inner join {{ ref('stg_accounts') }} a
        on v.account_id = a.account_id

    where v.market_value > 0
      and a.opened_at::date <= v.snapshot_date
      and (
          a.closed_at is null
          or a.closed_at::date > v.snapshot_date
      )

)

select
    reporting_month,
    count(distinct customer_id) as active_investors,
    count(distinct account_id) as active_investment_accounts,
    sum(market_value) as active_account_aum

from eligible_accounts
group by reporting_month
