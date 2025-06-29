# 💰 Personal Expense Tracker (SQL-RAG + AI Agent)

An **AI-powered personal finance assistant** that helps you **track your expenses, calculate savings**, and manage finances smartly. Built with a modern stack including **Flask**, **Next.js**, **PostgreSQL**, and **Gemini API**, it leverages **SQL-based Retrieval-Augmented Generation (SQL-RAG)** to analyze and respond to your financial queries contextually.

---

## 🚀 Live Deployments

- **Frontend (Next.js)**: [Hosted on Vercel]
- **Backend (Flask API)**: [Hosted on Render](https://render.com)
- **[Test a Demo](https://expense.kevinrahul.me/)**
---

## 🧠 Architecture

> **Type:** Context-Augmented Generation (via SQL-based Retrieval)  
> **Formal Name:** SQL-Retrieval-Augmented Generation (**SQL-RAG**) using Gemini API.

The agent processes user prompts (like `"Where did I spend the most this month?"`) by retrieving relevant expense records via SQL from PostgreSQL, then generating contextual answers with Gemini API.

---

## 🔧 Tech Stack

| Layer         | Technology                      |
|---------------|----------------------------------|
| Frontend      | [Next.js 15 (App Router)](https://nextjs.org) + TypeScript |
| Backend       | [Python Flask](https://flask.palletsprojects.com/) + [Flask-JWT](https://flask-jwt-extended.readthedocs.io/) |
| Database      | [PostgreSQL](https://www.postgresql.org/) |
| AI Agent      | [Gemini API](https://deepmind.google/technologies/gemini/) |
| Deployment    | Docker + Docker Compose |
| Hosting       | Frontend: Vercel<br>Backend: Render |
| Auth          | JWT (Access & Refresh Tokens) |

---

## 📁 Project Structure

Expense_Tracker/
├─ Expense_backend/
│   ├── app.py
│   ├── models/
│     ├── Model_Generator.py
│     └── SQL_operations.py
│   ├── .env
│   ├── requirements.txt
│   └── Dockerfile
├── Expense_frontend/
│   ├── .github/
│   ├── app/
│   ├── components/
│   ├── pages/
│   ├── public/
│   ├── .env.local
│   └── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md


---

## ✨ Features

- 🔐 Secure JWT Authentication (Login & Signup)
- 📥 Add income and expenses by natural language prompts
- 📊 Expense breakdowns by category & date
- 🧠 AI-driven answers using Gemini for prompts like:
  - “Where did I spend the most this week?”
  - “How can I save more based on my spending habits?”
- 🧾 Stores all data securely in PostgreSQL
- 📱 Mobile-Responsive UI
- 🐳 Dockerized setup for full stack deployment
- 🌍 Deployed on cloud platforms (Render + Vercel)
- 🧙 Agentic AI architecture for personalized finance recommendations


---

## 🛠️ Getting Started Locally

### 1. Clone the Repository

```bash
git clone https://github.com/kevinkrahul/Expense_Tracker_CAG.git
```


---

### 2. Create .env Files

Backend (Expense_backend/.env)

```bash
GEMINI_API_KEY="YOUR_API_KEY"
PG_HOST="HOST_NAME"
PG_PORT=PORT_NUMBER
PG_DATABASE="DATABSE_NAME"
PG_USER="USER_NAME"
PG_PASSWORD="DATABASE_PASSWORD"
JWT_SECRET_KEY="ENTER_RANDOM_KEY"
DATABASE_URL="DATABASE_URL--NEED-ONLY-YOUR-DEPLOYING-BACKEND-INDIVIDUALLY"
```
Frontend (frontend/.env.local)

```bash
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

🐋 Docker Compose file (.env)
```bash
GEMINI_API_KEY="YOUR_API_KEY"
PG_HOST="HOST_NAME"
PG_PORT=PORT_NUMBER
PG_DATABASE="DATABSE_NAME"
PG_USER="USER_NAME"
PG_PASSWORD="DATABASE_PASSWORD"
JWT_SECRET_KEY="ENTER_RANDOM_KEY"
DATABASE_URL="DATABASE_URL--NEED-ONLY-YOUR-DEPLOYING-BACKEND-INDIVIDUALLY"
NEXT_PUBLIC_API_URL="http://localhost:8000"
BACKEND_PORT=8000
FRONTEND_PORT=3000
```


---

### 3. 🐋 Built and run your docker files seperatly for **Backend** & **Frontend**

```bash
docker build -t "image_name" .
docker run "image_name"
```

---

### 4. Run your **Backend** 

```bash
cd Expense_backend
python app.py
```

---

### 5. Run your **Frontend**

```bash
cd Expense_frontend
npm run dev
```

---

### 6. 🐋 Docker Compose **EASY TO RUN**

```bash
docker compose up --build
```

**To stop:**

```bash
docker compose down
```


---

## This will spin up:

**Flask backend** at [http://localhost:8000](http://localhost:8000)

**Next.js frontend** at [http://localhost:3000](http://localhost:8000)


---

## 🔐 Authentication Flow

  - User logs in via frontend
  - Backend returns access & refresh tokens
  - Tokens are stored in localStorage or HTTP-only cookies
  - Secured endpoints require Authorization header: Authorization: Bearer <access_token>


---

### 🤖 How the AI Agent Works

**User Input:**
"How much did I spend on food this month?"

**Intent Separation (Gemini API):**
The Gemini API first analyzes the user input and separates it into either:
  - A contextual statement (e.g., an expense/income to be saved)
  - A query (e.g., a question requiring a response)

**Contextual Data Handling:**
If the input is contextual, the extracted data (category, target, amount, date, etc.) is stored into the PostgreSQL database via the Flask API.

**Query Data Handling:**
  - If the input is identified as a query, the Gemini agent generates an appropriate SQL query based on the user's prompt.
  - The Flask API executes the SQL query, retrieves the relevant records from PostgreSQL.

**Context Augmentation & Response Generation:**
The retrieved data is sent back into the Gemini API as part of a structured prompt.
Gemini then generates an intelligent, personalized response with insights and recommendations.


---

## 🧪 Sample Prompt & Output

## Prompt:
  - "I spent 1750 on starbucks today"
  - "I spent 1294 on dress shopping yesterday"
  - "I spent 10 for tea today"
  - "How much I spend this month and on what?"
  - "How much I sent this month and on which target?"
    
## AI Response:
  - "Got it, that expense is added to your ledger! 🎉"
  - "Got it, I've added that transaction to your list! 🎉"
  - "Got it, that expense is added to your list! 🎉"
  - "Okay, so this month you spent ₹1760 on food and ₹1294 on shopping."
  - "Okay, so this month you've spent ₹1294 on that dress, ₹1750 at Starbucks (treat yourself!), and just ₹10 on tea."


---

## 📬 Contact
For queries, suggestions, or collaboration, feel free to contact:
📧 senkuresearch@gmail.com
[🔗 LinkedIn](https://www.linkedin.com/in/kevinkrahul)

