select
year,
month,
category,
sum(amount)
from financial.bills
group by year, month, category
order by year, month, category