
select
    reporting_month,
    gross_deposits,
    gross_withdrawals,
    net_flows
from {{ ref('fct_monthly_money_flows') }}
where abs(
    net_flows - (gross_deposits - gross_withdrawals)
) > 0.01
