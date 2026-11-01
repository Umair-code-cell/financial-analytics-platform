
select
    account_id,
    customer_id,
    portfolio_id,
    lower(trim(account_type)) as account_type,
    upper(trim(currency)) as currency,
    opened_at::timestamp as opened_at,
    closed_at::timestamp as closed_at,
    lower(trim(account_status)) as account_status,
    created_at::timestamp as created_at,
    updated_at::timestamp as updated_at
from {{ source('raw', 'accounts') }}
