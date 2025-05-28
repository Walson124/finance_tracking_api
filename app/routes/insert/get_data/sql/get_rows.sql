select 
name,
amount,
category,
month,
year
from financial.bills
where
    month = '{month}'
    and year = {year}