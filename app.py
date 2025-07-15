from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests

# Charge les variables d'environnement depuis un fichier .env
load_dotenv()

# Initialise l'application Flask
app = Flask(__name__)

# Récupère la clé API OpenRouter depuis les variables d'environnement
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Route pour la page d'accueil, affiche le template HTML "App.html"
@app.route('/')
def home():
    return render_template("App.html")

# Route pour gérer la conversation chatbot via POST
@app.route('/chat', methods=['POST'])
def chat():
    # Récupère les données JSON envoyées par le client
    data = request.get_json()
    user_message = data['message'] # Message envoyé par l'utilisateur

    # Prépare l'historique de la conversation, avec un message système qui fixe le contexte
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

    # Prépare les en-têtes HTTP, avec la clé API pour l'authentification
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prépare la charge utile (payload) pour l'API OpenRouter
    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",  # DeepSeek R1
        "messages": conversation_history
    }

    # Envoie la requête POST à l'API OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    # Vérifie si la requête a réussi
    if response.status_code == 200:
        # Extrait la réponse du chatbot dans le JSON renvoyé
        reply = response.json()['choices'][0]['message']['content']
    else:
        # En cas d'erreur, renvoie le code et le message d'erreur
        reply = f"Erreur {response.status_code} : {response.text}"
    # Renvoie la réponse sous format JSON au client
    return jsonify({'reply': reply})

# Point d'entrée de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
