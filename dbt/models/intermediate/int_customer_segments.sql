
select
    customer_id,
    country_code,
    risk_profile,
    registration_ts,
    case
        when lower(trim(risk_profile)) in ('conservative', 'cautious')
            then 'Lower Risk'
        when lower(trim(risk_profile)) = 'balanced'
            then 'Medium Risk'
        when lower(trim(risk_profile)) in ('growth', 'adventurous')
            then 'Higher Risk'
        else 'Unknown'
    end as risk_segment
from {{ ref('stg_customers') }}
