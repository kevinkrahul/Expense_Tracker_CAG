import requests

data = {
    "texts": ["User input sentence here hello world", "Another sentence for embedding"]
}

response = requests.post("http://localhost:5000/embed", json=data)

print(response.json())
