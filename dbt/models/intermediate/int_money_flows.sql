
select
    transaction_id,
    account_id,
    transaction_ts,
    settlement_ts,
    transaction_type,
    currency,
    amount,
    case
        when transaction_type = 'deposit' then amount
        when transaction_type = 'withdrawal' then -amount
    end as signed_flow_amount
from {{ ref('stg_transactions') }}
where status = 'completed'
  and transaction_type in ('deposit', 'withdrawal')
  and amount > 0
