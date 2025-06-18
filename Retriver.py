import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import datetime
import re
from datetime import datetime,timedelta
import psycopg2  # or import the appropriate DB-API for your database


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")



conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    database=os.getenv("PG_NAME"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD")
)
cursor = conn.cursor()


def generate_sql_from_query(natural_query: str) -> str:
    prompt = f"""
You are an assistant that helps convert user questions into SQL.

The database has a table called `transactions` with columns:
- type (expense/income)
- amount (integer)
- category (text)
- target (text)
- source (text)
- date (date in YYYY-MM-DD)
- time (time in HH:MM)

Use appropriate aggregate functions like SUM when the query asks for totals.
when both income and expense are asked always return income first, then expenses in the same order:
Convert the following user request into an SQL query that can be run on a PostgreSQL database. Return only the SQL query without markdown or extra text.

User request: "{natural_query}"

SQL:
"""
    response = model.generate_content(prompt)
    sql = re.sub(r"```sql|```", "", response.text.strip()).strip()
    return sql



def interpret_results(row):
    income, expenses = row
    savings = income - expenses
    print(f"💰 Total Income: ₹{income}")
    print(f"💸 Total Expenses: ₹{expenses}")
    if savings > 0:
        print(f"✅ You saved ₹{savings}. Great job!")
    else:
        print(f"⚠️ You overspent by ₹{-savings}. Try to reduce your expenses.")





def execute_sql_query(query):
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
        # for row in results:
            # print(row)
    except Exception as e:
        print("Error executing SQL:", e)


# # Generate interactive result
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


# sample_query = "how my income going today"
sample_query = "can u tell me the difference between my income and expenses for this today"
# sample_query = "have any idea about how i have to save my money from this month expenses and income"
sql_query = generate_sql_from_query(sample_query)
# print(f"Generated SQL Query: {sql_query}")
result=execute_sql_query(sql_query)
if result:
    response=generate_interactive_response(sample_query, result)
    print(response)
    # interpret_results(result[0])






