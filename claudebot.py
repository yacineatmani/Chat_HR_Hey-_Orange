import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(
    page_title="Peelo - Assistant IA",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Styles CSS pour reproduire exactement l'interface Peelo
st.markdown("""
<style>
    /* Reset et base */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #f5f5f5;
    }
    
    /* Cacher les éléments Streamlit par défaut */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stAppHeader {display: none;}
    
    /* Header Orange */
    .orange-header {
        background-color: #ff6600;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 20px;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .orange-logo {
        background-color: #ff6600;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 14px;
    }
    
    .search-container {
        flex: 1;
        max-width: 600px;
        margin: 0 40px;
        position: relative;
    }
    
    .search-input {
        width: 100%;
        padding: 10px 20px;
        border: none;
        border-radius: 25px;
        font-size: 14px;
        outline: none;
        background-color: white;
    }
    
    .search-btn {
        position: absolute;
        right: 5px;
        top: 50%;
        transform: translateY(-50%);
        background-color: #ff6600;
        border: none;
        border-radius: 20px;
        width: 35px;
        height: 35px;
        color: white;
        cursor: pointer;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        color: white;
        font-size: 14px;
    }
    
    .user-avatar {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        background-color: #4a5568;
        margin-right: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    /* Navigation */
    .nav-bar {
        background-color: #4a5568;
        height: 50px;
        display: flex;
        align-items: center;
        padding: 0 20px;
        position: fixed;
        top: 60px;
        left: 0;
        right: 0;
        z-index: 999;
    }
    
    .nav-item {
        color: #a0aec0;
        padding: 10px 20px;
        text-decoration: none;
        font-size: 14px;
        display: flex;
        align-items: center;
        transition: color 0.2s;
    }
    
    .nav-item:hover {
        color: white;
    }
    
    .nav-item.active {
        background-color: #ff6600;
        color: white;
        border-radius: 4px;
    }
    
    .nav-icon {
        margin-right: 8px;
        font-size: 16px;
    }
    
    /* Contenu principal */
    .main-content {
        margin-top: 120px;
        padding: 40px 20px;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Titre Peelo */
    .peelo-title {
        text-align: center;
        margin-bottom: 60px;
    }
    
    .peelo-title h1 {
        font-size: 4rem;
        font-weight: 300;
        color: #ff6600;
        margin-bottom: 10px;
        letter-spacing: -2px;
    }
    
    .peelo-subtitle {
        color: #718096;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Zone de chat */
    .chat-section {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 40px;
        min-height: 400px;
    }
    
    .chat-input-container {
        padding: 30px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .chat-input-wrapper {
        position: relative;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .peelo-chat-input {
        width: 100%;
        padding: 15px 60px 15px 20px;
        border: 2px solid #e2e8f0;
        border-radius: 25px;
        font-size: 16px;
        outline: none;
        transition: border-color 0.2s;
        background-color: #f8f9fa;
    }
    
    .peelo-chat-input:focus {
        border-color: #ff6600;
        background-color: white;
    }
    
    .chat-send-btn {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        background-color: #ff6600;
        border: none;
        border-radius: 20px;
        width: 40px;
        height: 40px;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .chat-send-btn:hover {
        background-color: #e55a00;
    }
    
    /* Messages */
    .chat-messages {
        padding: 20px 30px;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .message {
        margin-bottom: 20px;
        display: flex;
        align-items: flex-start;
    }
    
    .message.user {
        justify-content: flex-end;
    }
    
    .message-content {
        max-width: 70%;
        padding: 12px 18px;
        border-radius: 20px;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .message.user .message-content {
        background-color: #ff6600;
        color: white;
        border-bottom-right-radius: 6px;
    }
    
    .message.assistant .message-content {
        background-color: #f1f3f4;
        color: #2d3748;
        border-bottom-left-radius: 6px;
    }
    
    /* Questions suggérées */
    .suggested-questions {
        padding: 20px 30px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 15px;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .suggestion-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 14px;
        color: #4a5568;
        line-height: 1.4;
    }
    
    .suggestion-card:hover {
        border-color: #ff6600;
        box-shadow: 0 2px 8px rgba(255, 102, 0, 0.1);
        transform: translateY(-1px);
    }
    
    /* Section politiques */
    .policies-section {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        padding: 30px;
        margin-bottom: 40px;
    }
    
    .policies-title {
        font-size: 1.8rem;
        color: #2d3748;
        margin-bottom: 10px;
        font-weight: 500;
    }
    
    .policies-subtitle {
        color: #718096;
        margin-bottom: 30px;
        line-height: 1.5;
    }
    
    .policies-content {
        color: #4a5568;
        font-size: 2rem;
        font-weight: 300;
    }
    
    .attestations-section {
        text-align: center;
        padding: 20px;
        color: #718096;
        font-size: 1.1rem;
    }
    
    /* Loading spinner */
    .loading-spinner {
        border: 2px solid #f3f3f3;
        border-top: 2px solid #ff6600;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .peelo-title h1 {
            font-size: 2.5rem;
        }
        
        .suggested-questions {
            grid-template-columns: 1fr;
        }
        
        .main-content {
            padding: 20px 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Configurer l'API Gemini
API_KEY = "AIzaSyDYbbzEuu3i5gOalonwr2qZs_pwEgqJ0l8"  # Remplace par ta clé API
genai.configure(api_key=API_KEY)

# Initialiser le modèle Gemini Flash
model = genai.GenerativeModel("gemini-1.5-flash")

# Header Orange
st.markdown("""
<div class="orange-header">
    <div class="orange-logo">orange</div>
    <div class="search-container">
        <input type="text" class="search-input" placeholder="Rechercher...">
        <button class="search-btn">🔍</button>
    </div>
    <div class="user-info">
        <div class="user-avatar">👤</div>
        <span>Bonjour, Utilisateur</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("""
<div class="nav-bar">
    <a href="#" class="nav-item">
        <span class="nav-icon">🏠</span> Accueil
    </a>
    <a href="#" class="nav-item">
        <span class="nav-icon">📰</span> Actualités
    </a>
    <a href="#" class="nav-item">
        <span class="nav-icon">🔧</span> Outils
    </a>
    <a href="#" class="nav-item">
        <span class="nav-icon">👥</span> Équipe
    </a>
    <a href="#" class="nav-item">
        <span class="nav-icon">📄</span> Documents
    </a>
    <a href="#" class="nav-item active">
        <span class="nav-icon">👤</span> HR
    </a>
    <a href="#" class="nav-item">
        <span class="nav-icon">🎧</span> Support
    </a>
</div>
""", unsafe_allow_html=True)

# Contenu principal
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Titre Peelo
st.markdown("""
<div class="peelo-title">
    <h1>Peelo</h1>
    <p class="peelo-subtitle">chatbot IA pour vos questions sur les ressources humaines</p>
</div>
""", unsafe_allow_html=True)

# Initialiser l'historique de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Section de chat
st.markdown('<div class="chat-section">', unsafe_allow_html=True)

# Zone de saisie (placée en haut comme dans l'image)
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)

# Formulaire pour l'input personnalisé
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([10, 1])
    with col1:
        user_input = st.text_input(
            "",
            placeholder="Posez votre question",
            key="user_question",
            label_visibility="collapsed"
        )
    with col2:
        submit_button = st.form_submit_button("➤")

st.markdown('</div>', unsafe_allow_html=True)

# Affichage des messages
if st.session_state.messages:
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        role_class = "user" if message["role"] == "user" else "assistant"
        st.markdown(f"""
        <div class="message {role_class}">
            <div class="message-content">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Traitement de la soumission
if submit_button and user_input:
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Générer la réponse avec Gemini
    try:
        # Configuration pour des réponses adaptées aux RH
        prompt_contexte = f"""Tu es Peelo, un assistant IA spécialisé dans les ressources humaines. 
        Réponds de manière professionnelle et utile aux questions RH.
        
        Question: {user_input}"""
        
        response = model.generate_content(prompt_contexte)
        response_text = response.text
        
    except Exception as e:
        response_text = f"Désolé, une erreur s'est produite. Veuillez réessayer."
    
    # Ajouter la réponse à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # Rafraîchir la page pour afficher les nouveaux messages
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Questions suggérées (si pas de conversation en cours)
if not st.session_state.messages:
    st.markdown("""
    <div class="suggested-questions">
        <div class="suggestion-card" onclick="document.querySelector('[data-testid=\\"textInput\\"]').value='Quand est-ce que j\\'aurais mon bonus ?'">
            Quand est-ce que j'aurais mon bonus ?
        </div>
        <div class="suggestion-card" onclick="document.querySelector('[data-testid=\\"textInput\\"]').value='Quand est-ce que les salaires sont versés ?'">
            Quand est-ce que les salaires sont versés ?
        </div>
        <div class="suggestion-card" onclick="document.querySelector('[data-testid=\\"textInput\\"]').value='Puis-je bénéficier du télétravail, et comment en faire la demande ?'">
            Puis-je bénéficier du télétravail, et comment en faire la demande ?
        </div>
        <div class="suggestion-card" onclick="document.querySelector('[data-testid=\\"textInput\\"]').value='Comment me développer ?'">
            Comment me développer ?
        </div>
        <div class="suggestion-card" onclick="document.querySelector('[data-testid=\\"textInput\\"]').value='Comment déclarer un arrêt maladie ?'">
            Comment déclarer un arrêt maladie ?
        </div>
        <div class="suggestion-card" onclick="document.querySelector('[data-testid=\\"textInput\\"]').value='Quels sont les avantages sociaux auxquels j\\'ai droit ?'">
            Quels sont les avantages sociaux auxquels j'ai droit ?
        </div>
    </div>
    """, unsafe_allow_html=True)

# Section Politiques de ressources humaines
st.markdown("""
<div class="policies-section">
    <h2 class="policies-title">Politiques de ressources humaines</h2>
    <p class="policies-subtitle">Lorem ipsum dolor sit amet consectetur. Enim justo diam malesuada scelerisque ac.</p>
    <div class="policies-content">A</div>
</div>
""", unsafe_allow_html=True)

# Section Attestations
st.markdown("""
<div class="attestations-section">
    <h3>Attestations</h3>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# JavaScript pour les suggestions cliquables
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const suggestions = document.querySelectorAll('.suggestion-card');
    suggestions.forEach(card => {
        card.addEventListener('click', function() {
            const question = this.textContent.trim();
            const input = document.querySelector('input[aria-label=""]');
            if (input) {
                input.value = question;
                input.focus();
            }
        });
    });
});
</script>
""", unsafe_allow_html=True)