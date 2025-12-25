def run(connector, run):
    # hit database for data...
    response = [
        {
            "name": "House Down Payment",
            "goal": 80000,
            "progress": 20000,
            "monthly": 1000,
            "target_month": 7,
            "target_year": 2028
        },
        {
            "name": "Vacation Fund",
            "goal": 5000,
            "progress": 1200,
            "monthly": 300,
            "target_month": 7,
            "target_year": 2025
        },
        {
            "name": "Taycan Turbo",
            "goal": 76000,
            "progress": 760000,
            "monthly": 0,
            "target_month": 12,
            "target_year": 2025
        },
    ]
    return {
        "goal_data": response
    }