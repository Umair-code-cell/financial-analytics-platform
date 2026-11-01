
select
    date_trunc('month', transaction_ts)::date as reporting_month,

    count(*) filter (
        where transaction_type = 'deposit'
    ) as deposit_count,

    count(*) filter (
        where transaction_type = 'withdrawal'
    ) as withdrawal_count,

    coalesce(
        sum(amount) filter (
            where transaction_type = 'deposit'
        ), 0
    ) as gross_deposits,

    coalesce(
        sum(amount) filter (
            where transaction_type = 'withdrawal'
        ), 0
    ) as gross_withdrawals,

    sum(signed_flow_amount) as net_flows

from {{ ref('int_money_flows') }}

group by 1
