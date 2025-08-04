import streamlit as st
import google.generativeai as genai
import base64

# Configurer l'API Gemini avec ta clé
API_KEY = "AIzaSyDYbbzEuu3i5gOalonwr2qZs_pwEgqJ0l8"  # Remplace par ta clé de Google AI Studio
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

# Style CSS personnalisé (Orange dominant)
st.markdown(
    """
    <style>
    .main {
        background-color: #ffffff; /* Fond blanc */
        font-family: Arial, sans-serif;
        color: #333333; /* Texte gris foncé */
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #ff6200; /* Orange VOO-Orange */
        color: #ffffff;
    }
    .assistant-message {
        background-color: #f5f5f5; /* Gris clair */
        color: #333333;
        border: 1px solid #ff6200;
    }
    .sidebar .sidebar-content {
        background-color: #ff6200; /* Sidebar orange */
        color: #ffffff;
    }
    h1 {
        color: #ff6200; /* Titre orange */
        text-align: center;
    }
    h2, h3 {
        color: #ff6200;
    }
    hr {
        border-color: #ff6200;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fonction pour charger une image en base64 (pour les logos locaux)
def load_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Charger les logos
orange_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Orange_logo.svg/1200px-Orange_logo.svg.png"

# Si tu as le logo Hey! en local, utilise cette option (décommente et ajuste le chemin)
# try:
#     hey_logo = load_image_base64("hey_logo.png")
#     st.sidebar.image(f"data:image/png;base64,{hey_logo}", width=100)
# except:
# Sinon, utilise une URL temporaire ou trouve le vrai logo
hey_logo_url = "https://www.heytelecom.be/themes/custom/hey/logo.svg"  # URL potentielle pour Hey! Telecom (à vérifier)


# En-tête avec logo Orange à gauche et logo Hey à droite
st.markdown(
    f"""
    <div style='width:100%;display:flex;justify-content:space-between;align-items:center;margin-top:18px;margin-bottom:8px;'>
        <img src='{orange_logo_url}' alt='Orange' style='height:70px;' />
        <h1 style='flex:1;text-align:center;margin:0;color:#ff6200;'>VOO-Orange HR Assistant</h1>
        <img src='{hey_logo_url}' alt='Hey' style='height:70px;' />
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("Bienvenue sur votre assistant RH post-fusion. Posez vos questions en toute simplicité !")

# Sidebar avec FAQ RH
with st.sidebar:
    st.header("FAQ - Ressources Humaines")
    with st.expander("1. Congés et Absences"):
        st.markdown("""
        - **Combien de jours de congé payé ai-je droit par an ?**  
          Vous avez droit à [X] jours de congés payés par an, soit [X] jours ouvrés. Consultez votre solde sur [outil interne].  
        - **Puis-je reporter mes congés non utilisés ?**  
          Oui, selon la politique, un report est possible. Vérifiez les règles avec le service RH.  
        - **Comment faire une demande de congé ?**  
          Via [plateforme RH], soumettez votre demande [X] jours à l’avance.  
        - **Que faire si je suis malade pendant mes congés ?**  
          Informez votre responsable avec un certificat médical pour convertir en congé maladie.
        """)
    with st.expander("2. Rémunération et Avantages"):
        st.markdown("""
        - **Quand vais-je recevoir ma fiche de paie ?**  
          Chaque [début de mois] via [plateforme de paie].  
        - **Que faire si je remarque une erreur ?**  
          Contactez [email RH] avec les détails.  
        - **Ai-je droit à des primes ou bonus ?**  
          Oui, selon performance. Voir [politique interne].  
        - **Quels avantages sont offerts ?**  
          [Tickets restaurant, assurance santé, etc.], détails sur [plateforme].
        """)
    with st.expander("3. Congé Maternité/Paternité"):
        st.markdown("""
        - **Quels sont mes droits ?**  
          Maternité : [X] semaines ; Paternité : [X] jours. Voir [guide RH].  
        - **Le congé maternité est-il payé ?**  
          Oui, partiellement, selon votre contrat.  
        - **Puis-je revenir avant la fin ?**  
          Oui, informez-nous [X] semaines avant.
        """)
    with st.expander("4. Mobilité et Télétravail"):
        st.markdown("""
        - **Puis-je travailler à distance ?**  
          Oui, [X] jours/semaine avec accord.  
        - **Soutien pour la mobilité interne ?**  
          Oui, voir offres sur [intranet].  
        - **Remboursement des frais de transport ?**  
          Oui, via [procédure interne].
        """)
    st.markdown("**Contact HR Care** : hr@voo-orange.be")

# Initialiser l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis votre assistant RH VOO-Orange. Comment puis-je vous aider aujourd’hui ?"}
    ]

# Afficher les messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)

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

# Pied de page
st.markdown("<hr><p style='text-align: center; color: #666666;'>© 2025 VOO-Orange - Tous droits réservés</p>", unsafe_allow_html=True)