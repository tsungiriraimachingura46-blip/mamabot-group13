from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are Mama-Bot, a trusted maternal health assistant 
for pregnant women and new mothers in rural Sub-Saharan Africa. 
Respond in the user's language. Keep answers simple and clear. 
If the user describes heavy bleeding, blurred vision, severe headache, 
reduced fetal movement, high fever or convulsions — immediately flag it 
as a danger sign and urge them to go to the nearest clinic right away.
Always respond with compassion and without medical jargon."""

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

if __name__ == '__main__':
    app.run(debug=True)



