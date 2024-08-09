# FastAPI Application for Splitwise-like System

This FastAPI application provides APIs to manage transactions, calculate splits, and settle amounts in a Splitwise-like system.

## Features

- **Calculate Splits**: Calculate equal, percentage, or share-based splits.
- **Settle Amount**: Record settlement of amounts between users.
- **Fetch Amounts**: Retrieve amounts borrowed and lent by a user.

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL (or other supported databases)
- Pydantic

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set Up the Database**

    Update your database connection settings in `database.py` and ensure your database schema is created.

## Usage

1. **Run the Application**

    ```bash
    uvicorn main:app --reload
    ```

    The application will be available at `http://localhost:8000`.

2. **API Endpoints**

    ### `POST /splitwise/calculate`

    Calculate the amount each user owes or is owed based on the type of split.

    **Request Body**

    ```json
    {
    "type": "equal",
    "transaction_type": "group",
    "group_name": "BBQ",
    "data": {
        "amount": 4058,
        "people": [
            "Alice Johnson",
            "Mia Adams",
            "Leo Robinson"
        ],
        "paid_by": "Leo Robinson"
    }
    }
    ```

    **Response**

    ```json
    {
    "splits": {
        "Alice Johnson": 1352.6666666666667,
        "Mia Adams": 1352.6666666666667,
        "Leo Robinson": 1352.6666666666667
    },
    "paid_by": "Leo Robinson",
    "total_amount_lent": 2705.3333333333335
    }
    ```

    **Request Body**
   
    ```json
    {
    "type": "percentage",
    "transaction_type": "group",
    "group_name": "NightOut",
    "data": {
        "amount": 10120,
        "percentages": {
            " Alice Johnson": 10,
            "Mia Adams": 30,
            "Bob Smith": 20,
            "Leo Robinson": 40
        },
        "paid_by": "Mia Adams"
    }
    }
    ```

    **Response**

    ```json
    {
    "splits": {
        " Alice Johnson": 1012.0,
        "Mia Adams": 3036.0,
        "Bob Smith": 2024.0,
        "Leo Robinson": 4048.0
    },
    "paid_by": "Mia Adams",
    "total_amount_lent": 7084.0
    }
    ```

    **Request Body**
   
    ```json
    {
    "type": "share",
    "transaction_type": "group",
    "group_name": "NightOut",
    "data": {
        "amount": 10450,
        "shares": {
            " Alice Johnson": 2,
            "Mia Adams": 3,
            "Bob Smith": 2,
            "Leo Robinson": 3
        },
        "paid_by": "Bob Smith"
    }
    }
    ```

    **Response**

    ```json
    {
    "splits": {
        " Alice Johnson": 2090.0,
        "Mia Adams": 3135.0,
        "Bob Smith": 2090.0,
        "Leo Robinson": 3135.0
    },
    "paid_by": "Bob Smith",
    "total_amount_lent": 8360.0
    }
    ```
    
    ### `POST /splitwise/settle`

    Record the settlement of an amount between users.

    **Request Body**

    ```json
    {
    "transaction_id": "5736442b-bc48-4a10-9424-5cfcf75785af",
    "lender_user_id": "c1e6f2f0-0c3e-4bfa-b769-2d8e4d5c1b99",
    //   "group_id": "group789", optional
    "settled_amount": 3135.00,
    "settled_by": "Leo Robinson"
    }
    ```

    **Response**

    ```json
    {
        "status": "success",
        "message": "Amount settled successfully"
    }
    ```

    ### `GET /splitwise/amounts/{user_name}`

    Fetch amounts borrowed and lent by a user.

    **Request Parameters**

    - `user_name`: The name of the user

    **Response**

    ```json
    {
    "borrowed_amount": 3135.0,
    "amount_lended": 57953.0
    }
    ```

## Database Schema
Run Create Queries.sql file for database setup

## Contributing

Feel free to submit pull requests or open issues for any bugs or enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
