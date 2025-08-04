import streamlit as st
import google.generativeai as genai

# Configurer l'API Gemini avec ta clé (remplace par ta clé API)
API_KEY = "AIzaSyCorPicjHK5MdwqiK0NQ8n8meRZj5ifxYc"  # Nouvelle clé API fournie
genai.configure(api_key=API_KEY)

# Initialiser le modèle Gemini Flash
model = genai.GenerativeModel("gemini-1.5-flash")  # Version légère et rapide

# Titre de l'application Streamlit
st.title("Chatbot avec Gemini Flash")

# Initialiser l'historique de la conversation dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Pose-moi une question !"):
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer une réponse avec Gemini Flash
    try:
        response = model.generate_content(prompt)
        response_text = response.text
    except Exception as e:
        response_text = f"Erreur : {str(e)}"

    # Ajouter la réponse du chatbot à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)
