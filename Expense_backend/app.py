from flask import Flask, request, jsonify
from flask_cors import CORS
from Model.Model_Generator import generate_sql_from_query, generate_interactive_response, contextual_query_response, classify_input_type, extract_info
from Model.SQL_operations import store_transaction, execute_sql_query, inject_user_filter
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
import bcrypt
import psycopg2
import os
from datetime import timedelta
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app,
    supports_credentials=True,
    #  resources={r"/*": {"origins": ["http://localhost:3000"]}},
    resources={r"/*": {"origins": "*"}},
    expose_headers=["Authorization"],
    allow_headers=["Content-Type", "Authorization"]
)


load_dotenv()
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)


# Initialize your database connection (update with your DB credentials)
# conn = psycopg2.connect(
#     host=os.getenv("PG_HOST"),
#     database=os.getenv("PG_NAME"),
#     user=os.getenv("PG_USER"),
#     password=os.getenv("PG_PASSWORD")
# )
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()



# Signup Router

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
                       (username, email, hashed_pw))
        user_id = cursor.fetchone()[0]
        conn.commit()
        token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return jsonify({"token": token,"refresh_token":refresh_token ,"success": "User registered successfully!"}), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400


# Login Router

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode(), user[1].encode()):
        token = create_access_token(identity=str(user[0]))
        refresh_token=create_refresh_token(identity=str(user[0]))
        return jsonify({"token": token,"refresh_token":refresh_token})
    return jsonify({"error": "Invalid credentials"}), 401



@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token})





# Main Model
@app.route("/", methods=["POST"])
@jwt_required()
def handle_message():
    try:
        user_id = int(get_jwt_identity())
        print(f"User ID: {user_id}")
        data = request.get_json()
        user_input = data.get("message", "")
        print(f"Received input: {user_input}")

        input_type = classify_input_type(user_input)

        print(f"Classified input type: {input_type}")


        if input_type == "context":
            structured_data = extract_info(user_input)
            print(f"Extracted Info: \n{structured_data}")

            if structured_data:
                structured_data["user_id"] = user_id
                success = store_transaction(structured_data)
                reply = contextual_query_response(success)
                return jsonify({"response": reply})
            else:
                return jsonify({"response": "⚠️ Couldn't understand the context."})

        else:
            sql = generate_sql_from_query(user_input)
            sql = inject_user_filter(sql, user_id)
            result = execute_sql_query(sql)
            response_text = generate_interactive_response(user_input, result)
            return jsonify({"response": response_text})

    
    except Exception as e:
        print(f"❌ Error in handle message: {e}")
        return jsonify({"response": "⚠️ Something went wrong on the server."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
