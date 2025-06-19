from flask import Flask, request, jsonify
from flask_cors import CORS
from Model.Model_Generator import generate_sql_from_query, generate_interactive_response, contextual_query_response, classify_input_type, extract_info
from Model.SQL_operations import store_transaction, execute_sql_query

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

@app.route("/", methods=["POST"])
def handle_message():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        print(f"Received input: {user_input}")

        input_type = classify_input_type(user_input)

        print(f"Classified input type: {input_type}")


        if input_type == "context":
            structured_data = extract_info(user_input)
            print(f"Extracted Info: \n{structured_data}")

            if structured_data:
                success = store_transaction(structured_data)
                reply = contextual_query_response(success)
                return jsonify({"response": reply})
            else:
                return jsonify({"response": "⚠️ Couldn't understand the context."})

        else:
            sql = generate_sql_from_query(user_input)
            result = execute_sql_query(sql)
            response_text = generate_interactive_response(user_input, result)
            return jsonify({"response": response_text})

        # else:
        #     return jsonify({"response": "❌ Could not classify input properly."})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "⚠️ Something went wrong on the server."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
