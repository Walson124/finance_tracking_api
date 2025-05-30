# Endpoint Documentation

## General /general

<details><summary>get_users</summary>

    GET: /general/get_users

    Example response:
    [
        "john",
        "cena"
    ]


</details>

## Insert /insert

<details><summary>get_data</summary>

    POST: /insert/get_data

    Example requestbody:
    {
        "month": "March",
        "year": "2025"
    }

    Example response:
    [
        {
            "amount": 122.23,
            "assigned_user": "feilan",
            "category": "Groceries",
            "name": "Wee"
        },
        {
            "amount": 21.07,
            "assigned_user": "feilan",
            "category": "Dining",
            "name": "Bomberino"
        },
        ...
    ]


</details>

<details><summary>add_rows</summary>

    POST: /insert/add_rows

    Example requestbody:
    [
        {
            "name": "testname",
            "amount": "testamont",
            "category": "testcategory",
            "month": "jan",
            "year": "1355"
        },
        {
            "name": "testname",
            "amount": "testamont",
            "category": "testcategory",
            "month": "jan",
            "year": "1355"
        }
    ]

    Example response:
    'success'

</details>

## Analysis /analysis

<details><summary>get_pi_chart</summary>

    POST: /analysis/get_pi_chart

    Example request:
    {
        "month": "March", // optional
        "year": "2025", // optional
        "assigned_user": "", // optional
        "category": "Dining" // optional
    }

    Example response:
    [
        {
            "amount": 21.07,
            "assigned_user": "feilan",
            "category": "Dining",
            "month": "March",
            "name": "Bomberino",
            "year": 2025
        },
        {
            "amount": 21.89,
            "assigned_user": "feilan",
            "category": "Dining",
            "month": "March",
            "name": "Bomberino",
            "year": 2025
        },
        ...
    ]

</details>

<details><summary>get_params</summary>

    GET: /analysis/get_params

    Example response:
    

</details>
