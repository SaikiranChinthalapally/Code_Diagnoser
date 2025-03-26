from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Use environment variable for API key
# Load environment variables from key.env
load_dotenv("key.env")

# Read API key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def analyze_code(code):
    """Send the code to OpenAI API for analysis"""
    prompt = f"""
    Consider You are an Automated Code Analysis and Evaluation System. 
    Only respond to programming language-related queries.
    Analyze the following code snippet and generate a report covering these points:
    1. Readability test
    2. Complexity
    3. Naming conventions
    4. Error handling
    5. Duplication
    6. Formatting
    7. Private key detection
    Provide suggestions for improvement.

    Code snippet:
    ```{code}```

    Also, provide a refactored version of the code.
    """

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(OPENAI_URL, headers=headers, json=data)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except KeyError:
            return "Unexpected response format from OpenAI API."
    else:
        return f"OpenAI API Error ({response.status_code}): {response.text}"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    code = data.get("code", "")

    if not code.strip():
        return jsonify({"error": "No code provided"}), 400

    report = analyze_code(code)
    return jsonify({"report": report})

if __name__ == "__main__":
    app.run(debug=True)
