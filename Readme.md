## Prerequisites
Ensure you have the following installed:
- Python 3.7+
- MySQL Server
- pip (Python package installer)
-Virtual Environment (optional but recommended)
- Create a Virtual Environment (Optional but Recommended):

```python3 -m venv lms_env
source lms_env/bin/activate  # On Windows: lms_env\Scripts\activate```
#### Install Required Packages:
```pip install mysql-connector-python```

## Connecting to Database
Make a .env file in the same folder as main.py
Add the following info
```
DB_HOST=<Your DB HOST>
DB_USER=<Your DB Username>
DB_PASSWORD=<Your DB Password>
```

## Intialising the database.
Run table-creation.sql

## Running the program
Run `python3 main.py`