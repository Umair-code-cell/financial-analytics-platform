select
    customer_id,
    customer_name,
    country_code,
    risk_profile,
    registration_date,
    case
        when risk_profile = 'Conservative' then 'Lower Risk'
        when risk_profile = 'Balanced' then 'Medium Risk'
        when risk_profile = 'Growth' then 'Higher Risk'
        else 'Unknown'
    end as risk_segment
from {{ ref('stg_customers') }}