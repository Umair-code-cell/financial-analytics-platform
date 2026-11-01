select
    reporting_month,
    active_investors,
    active_investment_accounts,
    active_account_aum
from {{ ref('fct_monthly_active_investors') }}
where active_investors <= 0
   or active_investment_accounts < active_investors
   or active_account_aum < 0
