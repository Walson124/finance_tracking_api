select 
name,
amount,
category,
assigned_user
from financial.bills
where
    month = '{month}'
    and year = {year}