const themeToggle = document.querySelector(".theme-toggle");
const body = document.body;
const chatContainer = document.getElementById("chatBox");
const messageInput = document.querySelector(".message-input");
const sendButton = document.querySelector(".send-button");
const typingIndicator = document.querySelector(".typing-indicator");

// Theme toggling
let isDarkTheme = false;
themeToggle.addEventListener("click", () => {
  isDarkTheme = !isDarkTheme;
  body.setAttribute("data-theme", isDarkTheme ? "dark" : "light");
  themeToggle.innerHTML = isDarkTheme
    ? '<i class="fas fa-sun"></i>'
    : '<i class="fas fa-moon"></i>';
});

// Crée une bulle de message
function createMessageElement(content, isUser = false) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${isUser ? "user-message" : "bot-message"}`;

  messageDiv.innerHTML = `
            <div class="avatar">${isUser ? "👦" : "🤖"}</div>
            <div class="message-bubble">${content}</div>
        `;

  return messageDiv;
}

// Ajoute le message dans la boîte de discussion
function addMessage(content, isUser = false) {
  const messageElement = createMessageElement(content, isUser);
  chatContainer.appendChild(messageElement);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showTypingIndicator() {
  typingIndicator.style.display = "flex";
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function hideTypingIndicator() {
  typingIndicator.style.display = "none";
}

// Fonction principale d’envoi
async function sendMessage() {
  const msg = messageInput.value.trim();
  if (msg === "") return;

  addMessage(msg, true); // message utilisateur
  messageInput.value = "";
  showTypingIndicator();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });

    const data = await res.json();
    hideTypingIndicator();
    addMessage(data.reply, false); // message bot
  } catch (error) {
    hideTypingIndicator();
    addMessage("Erreur de connexion au serveur.", false);
  }
}

// Envoyer via bouton ou touche Entrée
sendButton.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

// Message de bienvenue
setTimeout(() => {
  addMessage(
    "Salut ! Je suis Splashy, ton guide de la biodiversité marine 🐠. Pose-moi une question sur la vie sous-marine !"
  );
}, 500);
