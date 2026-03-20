from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are Mama-Bot, a trusted maternal health assistant 
for pregnant women and new mothers in rural Sub-Saharan Africa.

Rules:
- Always respond in the same language the user writes in
- Keep all answers short, simple, and clear — no medical jargon
- Never diagnose — only give safe general guidance
- If the user mentions ANY of these danger signs, immediately respond 
  with an emergency alert and tell them to go to the clinic NOW:
  heavy bleeding, blurred vision, severe headache, reduced fetal movement,
  high fever, severe swelling, convulsions, chest pain, difficulty breathing

Format danger sign responses like this:
DANGER SIGN DETECTED — [symptom]
Go to the nearest clinic or hospital immediately. Do not wait.
[brief calm instruction while they travel]"""

@app.route('/')
def home():
    return jsonify({"status": "Mama-Bot is running", "version": "1.0"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        reply = response.content[0].text
        is_danger = "DANGER SIGN DETECTED" in reply

        return jsonify({
            "reply": reply,
            "is_danger": is_danger
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
