select
sum(amount),
month,
category
from financial.bills
group by month, category