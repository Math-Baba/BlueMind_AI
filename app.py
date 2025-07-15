from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/')
def home():
    return render_template("App.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']

    conversation_history = [
        {"role": "system", "content": (
            "Tu es un éducateur expert en biodiversité marine qui parle à des enfants de 8 à 14 ans. "
            "Tu expliques avec des mots simples et toujours de façon pédagogique. "
            "Tu ne réponds que sur la vie marine (océans, poissons, coraux, pollution, écosystèmes marins, etc.). "
            "Si la question sort du sujet, tu réponds gentiment que tu ne peux parler que de biodiversité marine."
            "Tes réponses doivent être simples, claires, sans mise en forme : "
            "pas de texte en gras, pas d'italique, pas de points de liste mais tu peux garder les emojis. "
            "Exprime-toi en phrases naturelles, sans utiliser de code Markdown ni de symboles décoratifs. "
        )},
        {"role": "user", "content": user_message}
    ]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",  # DeepSeek R1
        "messages": conversation_history
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
    else:
        reply = f"Erreur {response.status_code} : {response.text}"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
