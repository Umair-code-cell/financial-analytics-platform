
with first_deposits as (

    select
        a.customer_id,
        min(f.transaction_ts) as first_deposit_ts
    from {{ ref('int_money_flows') }} f
    inner join {{ ref('stg_accounts') }} a
        on f.account_id = a.account_id
    where f.transaction_type = 'deposit'
    group by a.customer_id

)

select
    c.customer_id,
    c.registration_ts,
    d.first_deposit_ts,

    case
        when d.first_deposit_ts >= c.registration_ts
         and d.first_deposit_ts <= c.registration_ts + interval '30 days'
        then 1
        else 0
    end as activated_within_30d

from {{ ref('stg_customers') }} c
left join first_deposits d
    on c.customer_id = d.customer_id
