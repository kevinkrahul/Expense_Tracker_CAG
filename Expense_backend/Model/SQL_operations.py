import os
import psycopg2
from dotenv import load_dotenv
import re
from datetime import datetime, timedelta

load_dotenv()

# Initialize your database connection (update with your DB credentials)
# conn = psycopg2.connect(
#     host=os.getenv("PG_HOST"),
#     database=os.getenv("PG_NAME"),
#     user=os.getenv("PG_USER"),
#     password=os.getenv("PG_PASSWORD")
# )
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

# Function to create the transactions table if it doesn't exist
def create_table_if_not_exists():
    query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        type TEXT NOT NULL,
        amount NUMERIC NOT NULL,
        category TEXT,
        target TEXT,
        source TEXT,
        date DATE,
        time TIME
    );


    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );

    ALTER TABLE transactions
    ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);

    """
    cursor.execute(query)
    conn.commit()
    print("✅ Table created or already exists.")
create_table_if_not_exists()






# Store transaction data in the database
def store_transaction(data: dict) -> bool:
    source= data.get("source",None)
    raw_time = data["time"]
    parsed_time = convert_time_to_24hr_format(raw_time)
    raw_date = data["date"]
    parsed_date = parse_date(raw_date) if raw_date else datetime.now().date()
    user_id = data.get("user_id")

    query="""
        INSERT INTO transactions (type, amount, category, target, source, date, time,user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data["type"],
        data["amount"],
        data.get("category"),
        data.get("target"),
        source,
        parsed_date,
        parsed_time,
        user_id
    )
    try:
        cursor.execute(query, values)
        conn.commit()
        print("✅ Stored in DB")
        return True
    except Exception as e:
        print(f"❌ Failed to store transaction: {e}")
        conn.rollback()
        return False

# Function to inject user_id into SQL queries
def inject_user_filter(sql: str, user_id: int) -> str:
    sql = sql.strip().rstrip(";")  # Remove any trailing semicolon

    if "WHERE" in sql.upper():
        # Inject user_id after WHERE but before any conditions
        sql = re.sub(r"(WHERE\s+)", f"\\1user_id = {user_id} AND ", sql, flags=re.IGNORECASE)
    else:
        # No WHERE clause? Add one
        sql = re.sub(r"(FROM\s+transactions)", f"\\1 WHERE user_id = {user_id}", sql, flags=re.IGNORECASE)

    return sql + ";"



# Function to execute SQL query and fetch results
def execute_sql_query(query):
    try:
        cursor.execute(query)

        # Check if it's a SELECT query
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()

        # For DELETE/INSERT/UPDATE, return row count
        else:
            affected = cursor.rowcount
            conn.commit()
            return affected  # return number of rows affected

    except Exception as e:
        print("Error executing SQL:", e)
        return None


# Function to convert time strings to 24-hour format
def convert_time_to_24hr_format(time_str):
    time_str = time_str.strip().upper().replace(" ", "")
    try:
        # Try parsing common 12-hour formats (like 5PM, 5:30PM, etc.)
        return datetime.strptime(time_str.strip(), "%I%p").time()
    except ValueError:
        try:
            return datetime.strptime(time_str.strip(), "%I:%M%p").time()
        except ValueError:
            try:
                # Fallback: assume already in 24-hour format
                return datetime.strptime(time_str.strip(), "%H:%M").time()
            except ValueError:
                print(f"⚠️ Invalid time format: {time_str}")
                return None

# Function to parse date strings
def parse_date(date_str):
    try:
        # Normalize the string
        date_str = date_str.strip().lower()
        # Handle vague terms
        if date_str == "today":
            return datetime.now().date()
        elif date_str == "yesterday":
            return (datetime.now() - timedelta(days=1)).date()
        # If already in YYYY-MM-DD, accept it
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            pass
        # Remove ordinal suffixes (12th -> 12, 1st -> 1)
        date_str = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str)
        # Try parsing "12 June"
        try:
            parsed = datetime.strptime(date_str, "%d %B")
            return parsed.replace(year=datetime.now().year).date()
        except ValueError:
            pass
        # Try parsing "June 12"
        try:
            parsed = datetime.strptime(date_str, "%B %d")
            return parsed.replace(year=datetime.now().year).date()
        except ValueError:
            pass

        # Try fallback formats if needed
        print(f"⚠️ Could not parse date: {date_str}")
        return None
    except Exception as e:
        print(f"⚠️ Date parsing failed: {e}")
        return None