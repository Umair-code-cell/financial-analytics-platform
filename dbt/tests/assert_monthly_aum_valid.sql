
select
    reporting_month,
    valued_accounts,
    accounts_with_positive_aum,
    total_aum
from {{ ref('fct_monthly_aum') }}
where reporting_month is null
   or total_aum is null
   or total_aum < 0
   or valued_accounts < accounts_with_positive_aum
   or accounts_with_positive_aum < 0
