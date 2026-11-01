
select
    transaction_id,
    account_id,
    transaction_ts::timestamp as transaction_ts,
    lower(trim(transaction_type)) as transaction_type,
    round(amount::numeric, 2) as amount,
    upper(trim(currency)) as currency,
    lower(trim(status)) as status,
    payment_method,
    settlement_ts::timestamp as settlement_ts,
    created_at::timestamp as created_at,
    updated_at::timestamp as updated_at
from {{ source('raw', 'transactions') }}
