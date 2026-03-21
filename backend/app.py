from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

SYSTEM_PROMPT = """You are Mama-Bot, a trusted maternal 
health assistant for pregnant women and new mothers in 
rural Sub-Saharan Africa. Respond in the user's language. 
Keep answers short, simple and clear — no medical jargon.
If the user mentions heavy bleeding, blurred vision, 
severe headache, reduced fetal movement, high fever or 
convulsions — immediately say this is a DANGER SIGN and 
tell them to go to the nearest clinic right away."""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return jsonify({"reply": response.content[0].text})

@app.route('/')
def home():
    return jsonify({"status": "Mama-Bot is running"})

if __name__ == '__main__':
    app.run(debug=True)
