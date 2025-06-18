from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.route("/embed", methods=["POST"])
def embed():
    try:
        data = request.json
        texts = data.get("texts")
        if not texts:
            return jsonify({"error": "Missing 'texts' in request body"}), 400

        embeddings = model.encode(texts).tolist()

        return jsonify({
            "embeddings": embeddings,
            "dimensions": len(embeddings[0]) if embeddings else 0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
