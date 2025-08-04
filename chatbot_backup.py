import streamlit as st
import google.generativeai as genai

# Configurer l'API Gemini avec ta clé
API_KEY = "AIzaSyDYbbzEuu3i5gOalonwr2qZs_pwEgqJ0l8"
genai.configure(api_key=API_KEY)

# Initialiser le modèle Gemini Flash
model = genai.GenerativeModel("gemini-1.5-flash")

# Configuration de la page
st.set_page_config(
    page_title="VOO-Orange HR Assistant",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown(
    """
    <style>
    html, body, .main, .block-container {
        background: #f9f9f9;
        font-family: Arial, sans-serif;
        color: #333;
        margin: 0;
        padding: 0;
        height: auto;
        min-height: 100vh;
        overflow-x: hidden;
    }
    .block-container {
        display: flex;
        flex-direction: column;
        height: auto;
        min-height: 100vh;
        padding-bottom: 60px;
    }
    .content {
        flex: 1 0 auto;
        max-height: calc(100vh - 140px);
        overflow-y: hidden;
        overflow-x: hidden;
    }
    .sticky-footer {
        flex-shrink: 0;
        background: #fff;
        height: 40px;
        box-shadow: 0 -1px 8px rgba(0,0,0,0.03);
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        position: relative;
        bottom: 0;
    }
    header.stAppHeader {
        display: none !important;
    }
    [data-testid="stBottomBlockContainer"] {
        display: none !important;
    }
    .dialog-box {
        width: 70%;
        margin: 20px auto;
        padding: 15px;
        background: #fff;
        border: 1px solid #ff6200;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .dialog-box textarea {
        width: 100%;
        padding: 10px;
        background: #fff;
        color: #333;
        border: 1px solid #ff6200;
        border-radius: 5px;
        resize: none;
    }
    .dialog-box button {
        background: #f16e00;
        color: #fff;
        border-radius: 6px;
        font-weight: bold;
        border: none;
        padding: 8px 16px;
        margin-top: 10px;
        transition: background 0.2s;
    }
    .dialog-box button:hover {
        background: #ff6200;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background: #fff;
        border-bottom: 2px solid #ff6200;
        z-index: 10;
    }
    .header img {
        height: 40px;
    }
    .nav {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 15px;
        background: #fff;
        margin: 0 0 10px 0;
    }
    .nav a {
        color: #ff6200;
        text-decoration: none;
        font-weight: bold;
    }
    .nav a.active {
        color: #fff;
        background: #ff6200;
        padding: 4px 12px;
        border-radius: 6px;
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        margin: 20px 0;
        color: #ff6200;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 20px;
        color: #333;
    }
    .suggestions {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 20px 0;
    }
    .suggestions div {
        background: #fff;
        padding: 10px;
        border-radius: 5px;
        width: 200px;
        text-align: center;
        color: #333;
        border: 1px solid #ff6200;
    }
    .policies {
        text-align: center;
        font-size: 1.5em;
        margin: 20px 0;
        color: #ff6200;
    }
    .attestations {
        background: #fff;
        padding: 10px;
        border-radius: 5px;
        width: 200px;
        margin: 20px auto;
        text-align: center;
        color: #333;
        border: 1px solid #ff6200;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        background: #fff;
        color: #333;
        max-width: 70%;
        margin-left: auto;
        margin-right: auto;
    }
    .user-message {
        background-color: #f16e00;
        color: #fff;
    }
    .assistant-message {
        background-color: #fff;
        color: #ff6200;
        border: 1px solid #ffcc00;
    }
    .sidebar .sidebar-content .stExpander {
        background: #fff;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .sidebar .sidebar-content .stExpanderHeader {
        background: #fff;
        color: #ff6200;
        font-weight: bold;
    }
    .stButton>button {
        background: #f16e00;
        color: #fff;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        margin: 8px 0;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: #ff6200;
    }
    hr {
        border-color: #ff6200;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# En-tête avec logos Orange et Hey
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.image("https://www.orange.be/sites/b2c/files/2022-06/logo.svg", width=100)
with col2:
    st.empty()
with col3:
    st.image("https://www.heytelecom.be/themes/custom/hey/logo.svg", width=100)

# Navigation
st.markdown(
    """
    <div class="nav">
        <a href="#">Accueil</a>
        <a href="#">Actualités</a>
        <a href="#">Outils</a>
        <a href="#">Équipe</a>
        <a href="#">Documents</a>
        <a href="#" class="active">HR</a>
        <a href="#">Support</a>
    </div>
    """,
    unsafe_allow_html=True
)
# Entrée utilisateur
if prompt := st.chat_input("Tapez votre question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

    with st.spinner("Réponse en cours..."):
        try:
            response = model.generate_content(prompt)
            response_text = response.text
        except Exception as e:
            response_text = f"Désolé, une erreur est survenue : {str(e)}. Contactez HR Care si besoin."

    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(f"<div class='assistant-message'>{response_text}</div>", unsafe_allow_html=True)

# Titre et sous-titre

st.markdown("<div class='title'>PeeLo</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Chatbot IA pour vos questions RH</div>", unsafe_allow_html=True)

## Initialiser l'historique des messages AVANT le prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis votre assistant RH VOO-Orange. Comment puis-je vous aider aujourd’hui ?"}
    ]

# Prompt natif Streamlit pour le chat (doit être AVANT tout wrapper HTML personnalisé)

# Prompt natif Streamlit pour le chat (toujours visible en haut)
if prompt := st.chat_input("Tapez votre question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"<div class='user-message' style='padding:12px;text-align:center;font-size:1.1em;'>{prompt}</div>", unsafe_allow_html=True)

    with st.spinner("Réponse en cours..."):
        try:
            response = model.generate_content(prompt)
            response_text = response.text
        except Exception as e:
            response_text = f"Désolé, une erreur est survenue : {str(e)}. Contactez HR Care si besoin."

    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(f"<div class='assistant-message' style='padding:12px;text-align:center;font-size:1.1em;'>{response_text}</div>", unsafe_allow_html=True)

# Afficher l'historique APRÈS le prompt
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"<div class='user-message' style='padding:12px;text-align:center;font-size:1.1em;'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"<div class='assistant-message' style='padding:12px;text-align:center;font-size:1.1em;'>{message['content']}</div>", unsafe_allow_html=True)

# Suggestions
st.markdown(
    """
    <div class="suggestions">
        <div>Quand recevrai-je mon bonus ?</div>
        <div>Comment me former ?</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Politiques et Attestations
st.markdown("<div class='policies'>Politiques RH</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #333;'>Consultez vos droits et obligations RH.</p>", unsafe_allow_html=True)
st.markdown("<div class='attestations'>Attestations</div>", unsafe_allow_html=True)

# Sidebar avec FAQ RH
with st.sidebar:
    st.header("FAQ - Ressources Humaines")
    with st.expander("1. Congés et Absences", expanded=False):
        st.markdown("""
- **Jours de congé par an ?**  
  [X] jours, consultez votre solde sur [outil interne].  
- **Report de congés ?**  
  Possible, vérifiez avec le service RH.  
- **Demande de congé ?**  
  Via [plateforme RH], [X] jours à l’avance.  
- **Maladie pendant congé ?**  
  Certificat médical requis.
        """)
    with st.expander("2. Rémunération et Avantages", expanded=False):
        st.markdown("""
- **Fiche de paie ?**  
  Début de mois via [plateforme de paie].  
- **Erreur sur paie ?**  
  Contactez [email RH].  
- **Primes ou bonus ?**  
  Selon performance, voir [politique interne].  
- **Avantages ?**  
  [Tickets restaurant, assurance], détails sur [plateforme].
        """)
    with st.expander("3. Congé Maternité/Paternité", expanded=False):
        st.markdown("""
- **Droits ?**  
  Maternité: [X] semaines, Paternité: [X] jours.  
- **Payé ?**  
  Partiellement, selon contrat.  
- **Retour anticipé ?**  
  Informez [X] semaines avant.
        """)
    with st.expander("4. Mobilité et Télétravail", expanded=False):
        st.markdown("""
- **Télétravail ?**  
  [X] jours/semaine avec accord.  
- **Mobilité interne ?**  
  Offres sur [intranet].  
- **Frais de transport ?**  
  Remboursés via [procédure interne].
        """)
    st.markdown("**Contact HR Care** : hr@voo-orange.be")


## (Supprimé car déjà géré plus haut pour éviter le double prompt et double historique)


# Pied de page
st.markdown("""
<div class='sticky-footer'>
    © 2025 VOO-Orange - Tous droits réservés
</div>
""", unsafe_allow_html=True)