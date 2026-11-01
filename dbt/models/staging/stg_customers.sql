
select
    customer_id,
    registration_ts::timestamp as registration_ts,
    date_of_birth::date as date_of_birth,
    upper(trim(country_code)) as country_code,
    upper(trim(nationality_code)) as nationality_code,
    employment_status,
    income_band,
    risk_score,
    risk_profile,
    acquisition_channel,
    lower(trim(customer_status)) as customer_status,
    marketing_consent,
    created_at::timestamp as created_at,
    updated_at::timestamp as updated_at
from {{ source('raw', 'customers') }}
