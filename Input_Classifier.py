import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import datetime
import re
from datetime import datetime,timedelta

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def classify_input_type(text: str) -> str:
    prompt = f"""
You are a classification assistant.

Classify the following input as either:
- "query" (if it’s a question, command, or user request), or
- "context" (if it’s background info, logs, documents, or factual data).

Input:
\"\"\"{text}\"\"\"

Output (only one word - 'query' or 'context'):
"""

    try:
        response = model.generate_content(prompt)
        label = response.text.strip().lower()

        if "query" in label:
            return "query"
        elif "context" in label:
            return "context"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error: {e}")
        return "error"



import psycopg2  # or import the appropriate DB-API for your database

# Initialize your database connection (update with your DB credentials)
conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    database=os.getenv("PG_NAME"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD")
)
cursor = conn.cursor()

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
    """
    cursor.execute(query)
    conn.commit()
    print("✅ Table created or already exists.")
create_table_if_not_exists()



# Function to convert time strings to 24-hour format
def convert_time_to_24hr_format(time_str):
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
from datetime import datetime, timedelta
import re

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


# Store transaction data in the database
def store_transaction(data: dict) -> None:
    source= data.get("source",None)
    raw_time = data["time"]
    parsed_time = convert_time_to_24hr_format(raw_time)
    raw_date = data["date"]
    parsed_date = parse_date(raw_date) if raw_date else datetime.now().date()


    query="""
        INSERT INTO transactions (type, amount, category, target, source, date, time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data["type"],
        data["amount"],
        data.get("category"),
        data.get("target"),
        source,
        parsed_date,
        parsed_time
    )
    cursor.execute(query, values)
    conn.commit()
    print("✅ Stored in DB")

def extract_info(text: str) -> dict:
    prompt = f"""
You are an expense tracker assistant.

Given the following input, extract the data in structured JSON format(without guessing current date/time).

Rules:
- If it's an **expense**, extract:
    - "type": "expense"
    - "amount": numeric amount
    - "category": (e.g., food, fuel, shopping)
    - "target": item or purpose (e.g., milk, petrol, shoes)
    - "date": only if explicitly present, otherwise null
    - "time": only if explicitly present, otherwise null

- If it's **income**, extract:
    - "type": "income"
    - "amount": numeric amount
    - "source": (e.g., mom, salary, refund)
    - "date": only if explicitly present, otherwise null
    - "time": only if explicitly present, otherwise null

Only return the JSON object. Input:
\"\"\"{text}\"\"\"
"""
    try:
        response = model.generate_content(prompt)
        raw_json = response.text.strip()

        json_text = re.sub(r"```json|```", "", raw_json).strip()

        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            print(f"⚠️ JSON parsing failed:\n{raw_json}")
            return {}

        # Inject system date/time if missing
        now = datetime.now()
        if not data.get("date"):
            data["date"] = now.strftime("%Y-%m-%d")
        if not data.get("time"):
            data["time"] = now.strftime("%H:%M")

        return data

    
    except Exception as e:
        print(f"Error: {e}")
        return {}

# Test examples
samples = [
    "How much did I spend on food last week?",
    "User spent 300 rupees on groceries at 5PM",
    "Give me a summary of my travel expenses",
    "Expense: Fuel - 700 INR - 12th June",
    "i got 200 rupees from my mom today",
    "Recharged my phone for 249 rupees"
]

for sample in samples:
    result = classify_input_type(sample)
    print(f"Input: {sample}\nClassified as: {result}\n")

    if result == "context": 
        Structured_data = extract_info(sample)
        print(f"Extracted Info: \n{Structured_data}")

        if Structured_data:
            store_transaction(Structured_data)