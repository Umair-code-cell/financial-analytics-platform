select
    customer_id,
    customer_name,
    upper(country_code) as country_code,
    risk_profile,
    registration_date
from {{ source('raw', 'customers') }}