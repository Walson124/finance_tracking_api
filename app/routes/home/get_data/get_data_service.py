import random

def run(connector, data):
    # calls to database...
    widgets = {
        "safe_to_spend": 123.45,
        "income": 1234.56,
        "spent": 888.88,
        "bills_due": 3
    }
    cashflow = {
        "income": [random.random()*10000 for i in range(12)],
        "spent": [random.random()*10000 for i in range(12)],
    }
    return {
        "widgets": widgets,
        "cashflow": cashflow,
        "recents": {},
    }
