import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import datetime
import re
from datetime import datetime


# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")



# Function to classify input as "query" or "context"
def classify_input_type(text: str) -> str:
    prompt = f"""
You are an assistant for a personal finance tracker.

Classify the user's input into one of two categories:

1. **"context"** – if the message contains financial information to be **stored**, such as:
   - past or present expenses or income
   - what the user spent, paid, earned, got, or bought
   - transactions that include date, time, amount, category, etc.
   - even if the tone is casual or starts with "add", "note", "log", "save", etc.

2. **"query"** – if the message asks a question or requests a report/summary, such as:
   - "how much did I spend today?"
   - "what is my income this month?"
   - "show me expenses for groceries last week
   - instructions like "delete today's records", "clear all income", "show me groceries last week"

Input:
\"\"\"{text}\"\"\"

Output (only one word - "context" or "query"):
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



# Function to extract structured information from text
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
# samples = [
#     "i spent 500 on groceries yesterday",

# ]







# Retriever Functions

# Sql query generation function
def generate_sql_from_query(natural_query: str) -> str:
    prompt = f"""
You are an assistant that converts natural language questions and commands into PostgreSQL SQL queries.

The database has one table called `transactions` with the following columns:
- type (TEXT) — either 'income' or 'expense'
- amount (NUMERIC)
- category (TEXT)
- target (TEXT)
- source (TEXT)
- date (DATE, in YYYY-MM-DD format)
- time (TIME, in HH:MM format)

Here’s what you must support:
1. Analytical queries (e.g., "total income this week", "expenses yesterday"):
   - Use appropriate aggregate functions (like `SUM`).
   - Always return `income` before `expense` when both are requested.
   - Use PostgreSQL syntax only.
   - Use `CURRENT_DATE`, `CURRENT_DATE - INTERVAL '7 days'`, etc., to filter by date.
   - Example: `WHERE date = CURRENT_DATE - INTERVAL '1 day'`

2. Data manipulation commands (e.g., "delete all expenses", "clear yesterday's income"):
   - Generate a valid `DELETE FROM transactions ...` SQL query.
   - Use correct filters to match the intent (e.g., `WHERE type='expense' AND date=CURRENT_DATE - INTERVAL '1 day'`).

Rules:
- Always output **only the SQL query** — no markdown, explanation, or extra text.
- Be precise and minimal.

User request: "{natural_query}"

SQL:
"""
    response = model.generate_content(prompt)
    sql = re.sub(r"```sql|```", "", response.text.strip()).strip()
    return sql



    

# Generate interactive result
def generate_interactive_response(natural_query: str, sql_output: list):
    prompt = f"""
You are a personal expense tracker and advisor that speaks casually and helps users understand their finances.

The user asked: "{natural_query}"

SQL output: {sql_output}

Instructions:
- Speak in a friendly and casual tone.
- If the user’s question is about advice, suggestion, or insights, give helpful feedback based on the data — like comparison with previous results if available.
- If the SQL result is empty or null, reply that you couldn’t find any data but still offer a helpful or motivational message based on the user's question.
- Don’t answer unrelated questions.
- Be encouraging and supportive.
- just give the final response without any extra text or markdown.
- Use only rupee symbol for currency.
- When you compare income and expenses, always show income first, then expenses.


Now generate a natural, conversational reply based on the above.
"""
    response = model.generate_content(prompt)
    return response.text.strip()




# Function to handle contextual responses based on stored data
def contextual_query_response(response:bool):
    status = "successfully saved" if response else "failed to save"
    prompt =  f"""
You are a friendly and casual personal expense tracker assistant.

A user just submitted a transaction.

It was **{status}**.

Now, respond with **one short, friendly, and varied sentence** to the user:

- If it was saved: confirm cheerfully that it’s added.
- If it failed: gently inform them and suggest trying again.
- Never mention the system status like “saved” or “failed” literally.
- Don’t be repetitive — no “Noted” or “It’s in your records”.
- Sound like a natural, helpful assistant — maybe throw in an emoji or light tone.

Respond now:
"""
    response  = model.generate_content(prompt)
    return response.text.strip()


# for sample in samples:
#     result = classify_input_type(sample)
#     print(f"Input: {sample}\nClassified as: {result}\n")
#     if result == "context": 
#         Structured_data = extract_info(sample)
#         print(f"Extracted Info: \n{Structured_data}")
#         if Structured_data:
#             response = store_transaction(Structured_data)
#             if response:
#                 print(contextual_query_response(response))
#     else:
#         sql_query = generate_sql_from_query(sample)
#         result=execute_sql_query(sql_query)
#         if result:
#             response=generate_interactive_response(sample, result)
#             print(response)