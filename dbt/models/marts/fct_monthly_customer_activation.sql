
with observation_window as (

    select
        max(transaction_ts) as observation_end
    from {{ ref('stg_transactions') }}

)

select
    date_trunc('month', c.registration_ts)::date as registration_month,

    count(*) as registered_customers,

    count(*) filter (
        where c.registration_ts + interval '30 days' <= o.observation_end
    ) as eligible_customers_30d,

    count(*) filter (
        where c.activated_within_30d = 1
          and c.registration_ts + interval '30 days' <= o.observation_end
    ) as activated_customers_30d,

    round(
        100.0 * count(*) filter (
            where c.activated_within_30d = 1
              and c.registration_ts + interval '30 days' <= o.observation_end
        )
        / nullif(
            count(*) filter (
                where c.registration_ts + interval '30 days' <= o.observation_end
            ), 0
        ),
        2
    ) as activation_rate_30d_pct

from {{ ref('int_customer_activation') }} c
cross join observation_window o
group by 1
