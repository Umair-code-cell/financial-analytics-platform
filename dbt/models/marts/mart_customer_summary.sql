select
    risk_segment,
    count(*) as customer_count
from {{ ref('int_customer_segments') }}
group by risk_segment
order by customer_count desc