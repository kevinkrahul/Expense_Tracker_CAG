# 💰 Personal Expense Tracker (SQL-RAG + AI Agent)

An **AI-powered personal finance assistant** that helps you **track your expenses, calculate savings**, and manage finances smartly. Built with a modern stack including **Flask**, **Next.js**, **PostgreSQL**, and **Gemini API**, it leverages **SQL-based Retrieval-Augmented Generation (SQL-RAG)** to analyze and respond to your financial queries contextually.

---

## 🚀 Live Deployments

- **Frontend (Next.js)**: [Hosted on Vercel](https://vercel.com)
- **Backend (Flask API)**: [Hosted on Render](https://render.com)

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
├── Expense_backend/
│ ├── app.py
│ ├── routes/
│ ├── models/
│ ├── utils/
│ ├── auth/
│ ├── requirements.txt
│ └── Dockerfile
├── frontend/
│ ├── app/
│ ├── components/
│ ├── pages/
│ ├── public/
│ ├── .env.local
│ └── Dockerfile
├── docker-compose.yml
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
- 🐳 Dockerized setup for full stack deployment
- 🌍 Deployed on cloud platforms (Render + Vercel)
- 🧙 Agentic AI architecture for personalized finance recommendations

---

## 🆕 Extra Features (Planned or Optional)

- 📅 Recurring Expense Scheduling
- 🔔 Budget Limit Alerts via Email
- 📈 Export Reports (PDF/CSV)
- 📱 Mobile-Responsive UI
- 🌐 Multi-language Support

---

## 🛠️ Getting Started Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Expense_Tracker.git
cd Expense_Tracker
```

### 2. Create .env Files
Backend (Expense_backend/.env)
env
Copy
Edit
```bash
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@db:5432/expense_db
```
Frontend (frontend/.env.local)
env
Copy
Edit
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```
### 3. Run with Docker Compose
bash
Copy
Edit
```bash
docker-compose up --build
```
This will spin up:

Flask backend at http://localhost:8000

Next.js frontend at http://localhost:3000

PostgreSQL database at port 5432

🔐 Authentication Flow
User logs in via frontend

Backend returns access & refresh tokens

Tokens are stored in localStorage or HTTP-only cookies

Secured endpoints require Authorization header:
Authorization: Bearer <access_token>

### 🤖 How the AI Agent Works
User Input:
"How much did I spend on food this month?"

Backend Query:
Flask API queries PostgreSQL for expenses with category food and current month.

Context Sent to Gemini:
Expense data is embedded into the prompt.

Gemini Response:
Generates an intelligent response with insights and recommendations.

🧪 Sample Prompt & Output
Prompt:

"Where did I spend the most this month and on what?"

AI Response:

"You spent the most on Dining (₹3,250), particularly at Starbucks and Zomato. You could reduce this by meal prepping 2 days a week."

🐋 Docker Commands Reference
Build & Run:

bash
Copy
Edit
```bash
docker-compose up --build
```
Stop:

bash
Copy
Edit
```bash
docker-compose down
```
Remove volumes:

bash
Copy
Edit
```bash
docker-compose down -v
```
📬 Contact
For queries, suggestions, or collaboration, feel free to contact:
📧 kevin@example.com
🔗 LinkedIn

