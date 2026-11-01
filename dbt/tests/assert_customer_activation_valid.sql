select
    registration_month,
    registered_customers,
    eligible_customers_30d,
    activated_customers_30d,
    activation_rate_30d_pct
from {{ ref('fct_monthly_customer_activation') }}
where registered_customers < 0
   or eligible_customers_30d < 0
   or activated_customers_30d < 0
   or eligible_customers_30d > registered_customers
   or activated_customers_30d > eligible_customers_30d
   or (
       eligible_customers_30d > 0
       and (
           activation_rate_30d_pct is null
           or abs(
               activation_rate_30d_pct
               - round(
                   100.0 * activated_customers_30d
                   / eligible_customers_30d, 2
               )
           ) > 0.01
       )
   )
   or (
       eligible_customers_30d = 0
       and activation_rate_30d_pct is not null
   )