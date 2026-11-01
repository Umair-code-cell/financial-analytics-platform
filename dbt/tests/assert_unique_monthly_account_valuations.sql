
select
    account_id,
    reporting_month,
    count(*) as record_count
from {{ ref('int_monthly_account_valuations') }}
group by account_id, reporting_month
having count(*) > 1
