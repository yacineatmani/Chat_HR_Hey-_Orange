import streamlit as st
import google.generativeai as genai
import re

# Configurer l'API Gemini avec ta clé
API_KEY = "AIzaSyCorPicjHK5MdwqiK0NQ8n8meRZj5ifxYc"  # Nouvelle clé API fonctionnelle
genai.configure(api_key=API_KEY)

# Initialiser le modèle Gemini Flash
model = genai.GenerativeModel("gemini-1.5-flash")

# Configuration de la page
st.set_page_config(
    page_title="Hey!_Orange HR Assistant",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé - CORRIGÉ pour voir les messages
st.markdown(
    """
    <style>
    html, body, .main, .block-container {
        background: #f9f9f9;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Styles de base seulement */
    html, body, .main, .block-container {
        background: #f9f9f9;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Zone de chat avec fond blanc propre */
    .chat-section {
        background: #ffffff !important;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(255, 98, 0, 0.1);
        border: 1px solid #e0e0e0;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .chat-section::-webkit-scrollbar {
        width: 6px;
    }
    .chat-section::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    .chat-section::-webkit-scrollbar-thumb {
        background: #ff6200;
        border-radius: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Logos Orange à gauche et Hey à droite au-dessus de la navbar
st.markdown(
    """
    <div style='width:100%;display:flex;justify-content:space-between;align-items:center;margin-top:18px;margin-bottom:8px;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Orange_logo.svg/1200px-Orange_logo.svg.png' alt='Orange' style='height:100px;' />
        <img src='https://www.heytelecom.be/themes/custom/hey/logo.svg' alt='Hey' style='height:100px;' />
    </div>
    """,
    unsafe_allow_html=True
)

# Navbar custom Orange/Hey en haut
st.markdown(
    """
    <style>
    .navbar {
        display: flex;
        align-items: center;
        background: #222;
        padding: 0 32px;
        height: 60px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        position: relative;
        z-index: 100;
    }
    .navbar-logo {
        height: 40px;
        margin-right: 24px;
    }
    .navbar-search {
        flex: 1;
        display: flex;
        align-items: center;
        margin-right: 32px;
    }
    .navbar-search input {
        width: 320px;
        padding: 8px 16px;
        border-radius: 24px 0 0 24px;
        border: none;
        font-size: 1em;
        background: #f6f6f6;
        outline: none;
    }
    .navbar-search button {
        background: #ff6200;
        border: none;
        border-radius: 0 24px 24px 0;
        padding: 8px 16px;
        color: #fff;
        font-size: 1em;
        cursor: pointer;
    }
    .navbar-links {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .navbar-link {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #fff;
        background: none;
        border: none;
        padding: 8px 18px;
        border-radius: 6px;
        font-size: 1em;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.2s;
        text-decoration: none;
    }
    .navbar-link.active {
        background: #ff6200;
        color: #fff;
        font-weight: 600;
    }
    .navbar-link svg {
        vertical-align: middle;
    }
    .navbar-user {
        display: flex;
        align-items: center;
        margin-left: 32px;
        gap: 8px;
    }
    .navbar-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #eee;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2em;
        color: #888;
    }
    </style>
    <div class="navbar">
        <form class="navbar-search" onsubmit="return false;">
            <input type="text" placeholder="Rechercher..." />
            <button type="submit">🔍</button>
        </form>
        <div class="navbar-links">
            <a class="navbar-link" href="https://www.heytelecom.be/fr" target="_blank">🏠 Accueil</a>
            <a class="navbar-link" href="https://actu.orange.fr/" target="_blank">📰 Actualités</a>
            <a class="navbar-link" href="https://business.orange.be/fr/services-exclusifs-pour-les-clients-business/outils-en-ligne" target="_blank">🧰 Outils</a>
            <a class="navbar-link" href="https://corporate.orange.be/fr/propos-dorange/comit%C3%A9-ex%C3%A9cutif" target="_blank">👥 Équipe</a>
            <a class="navbar-link" href="https://www.orange.be/fr/formulaire" target="_blank">📄 Documents</a>
            <a class="navbar-link active" href="https://corporate.orange.be/fr/contact" target="_blank">🧑‍💼 HR</a>
            <a class="navbar-link" href="https://www.orange.be/fr/support" target="_blank">🎧 Support</a>
        </div>
        <div class="navbar-user">
            <div class="navbar-avatar">👤</div>
            <span style="color:#fff;font-size:1em;">Bonjour, Utilisateur</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Titre et sous-titre
st.markdown("<div class='title'>PeeLo</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Chatbot IA pour vos questions RH</div>", unsafe_allow_html=True)

# Initialiser l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis votre assistant RH Hey!_Orange. Comment puis-je vous aider aujourd'hui ?"}
    ]

# Fonction pour nettoyer les balises </div> et <div ...> indésirables
def clean_html_tags(text):
    # Supprime toutes les balises HTML
    cleaned = re.sub(r'<[^>]+>', '', text)
    # Supprime les espaces/retours à la ligne en début/fin
    cleaned = cleaned.strip()
    # Remplace les multiples retours à la ligne par un seul
    cleaned = re.sub(r'\n{2,}', '\n', cleaned)
    return cleaned

# Section de chat SANS styling personnalisé - laissons Streamlit faire
with st.container():
    # Afficher les messages avec un contraste visible
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            # Message utilisateur avec fond contrasté
            st.markdown(f"""
            <div style="background-color: #e0e0e0; padding: 15px; border-radius: 10px; margin: 10px 0; margin-left: 20%; color: black;">
                <strong>👤 Vous :</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Message assistant avec fond orange, sans balises </div> indésirables
            cleaned_content = clean_html_tags(message["content"])
            st.markdown(f"""
            <div style="background-color: #ff6200; padding: 15px; border-radius: 10px; margin: 10px 0; margin-right: 20%; color: white;">
                <strong>🤖 PeeLo :</strong><br>
                {cleaned_content}
            </div>
            """, unsafe_allow_html=True)

# Suggestions rapides
st.markdown("### 💡 Questions fréquentes")
col1, col2 = st.columns(2)

with col1:
    if st.button("💰 Quand recevrai-je mon bonus ?", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Quand recevrai-je mon bonus ?"})
        try:
            response = model.generate_content("Tu es PeeLo, assistant RH Hey!_Orange. Réponds à: Quand recevrai-je mon bonus ?")
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.session_state.messages.append({"role": "assistant", "content": "Pour les informations sur les bonus, veuillez contacter HR Care."})
        st.rerun()

with col2:
    if st.button("📚 Comment me former ?", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Comment me former ?"})
        try:
            response = model.generate_content("Tu es PeeLo, assistant RH Hey!_Orange. Réponds à: Comment me former ?")
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.session_state.messages.append({"role": "assistant", "content": "Pour les formations disponibles, consultez votre manager ou contactez HR Care."})
        st.rerun()

# Traitement des questions via le formulaire sticky
if "pending_question" in st.session_state and st.session_state.pending_question:
    user_question = st.session_state.pending_question
    st.session_state.pending_question = ""
    
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Générer la réponse avec Gemini
    try:
        contexte_rh = f"Tu es PeeLo, assistant RH Hey!_Orange. Réponds à: {user_question}"
        with st.spinner("🤔 PeeLo réfléchit..."):
            response = model.generate_content(contexte_rh)
            response_text = response.text
    except Exception as e:
        response_text = "😔 Désolé, une erreur est survenue. Veuillez réessayer ou contacter HR Care si le problème persiste."
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.rerun()

# Politiques et Attestations
st.markdown("<div class='policies'>📋 Politiques RH</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #333;'>Consultez vos droits et obligations RH.</p>", unsafe_allow_html=True)
st.markdown("<div class='attestations'>📄 Attestations<br><small>Téléchargez vos documents officiels</small></div>", unsafe_allow_html=True)

# Interface de chat en bas (prompt natif, sans wrapper HTML)
user_input = st.chat_input("💬 Tapez votre question RH ici...")

if user_input:
    st.session_state.pending_question = user_input
    st.rerun()

# Sidebar avec FAQ RH
with st.sidebar:
    st.markdown("""
    <div style='width:100%;text-align:center;margin-bottom:8px;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Orange_logo.svg/1200px-Orange_logo.svg.png' alt='Orange' style='height:60px;' />
    </div>
    <div style='width:100%;text-align:center;margin-bottom:16px;'>
        <img src='https://www.heytelecom.be/themes/custom/hey/logo.svg' alt='Hey' style='height:48px;' />
    </div>
    """, unsafe_allow_html=True)
    st.header("❓ FAQ - Ressources Humaines")
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Bonjour ! Je suis votre assistant RH Hey!_Orange. Comment puis-je vous aider aujourd'hui ?"}
        ]
        st.rerun()
    
    st.markdown("---")
    
    with st.expander("🏖️ Congés et Absences", expanded=False):
        st.markdown("""
- **Jours de congé par an ?**  
  [X] jours, consultez votre solde sur [outil interne].  
- **Report de congés ?**  
  Possible, vérifiez avec le service RH.  
- **Demande de congé ?**  
  Via [plateforme RH], [X] jours à l'avance.  
- **Maladie pendant congé ?**  
  Certificat médical requis.
        """)
    with st.expander("💰 Rémunération et Avantages", expanded=False):
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
    with st.expander("👶 Congé Maternité/Paternité", expanded=False):
        st.markdown("""
- **Droits ?**  
  Maternité: [X] semaines, Paternité: [X] jours.  
- **Payé ?**  
  Partiellement, selon contrat.  
- **Retour anticipé ?**  
  Informez [X] semaines avant.
        """)
    with st.expander("🏠 Mobilité et Télétravail", expanded=False):
        st.markdown("""
- **Télétravail ?**  
  [X] jours/semaine avec accord.  
- **Mobilité interne ?**  
  Offres sur [intranet].  
- **Frais de transport ?**  
  Remboursés via [procédure interne].
        """)
    st.markdown("📧 **Contact HR Care** : hr@voo-orange.be")

# JavaScript simple pour scroll
st.markdown("""
<script>
function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
}
setTimeout(scrollToBottom, 500);
</script>
""", unsafe_allow_html=True)