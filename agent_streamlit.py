"""
Interface Streamlit pour l'agent IA du portfolio de Leslie Planet.
Lance avec: streamlit run agent_streamlit.py
"""

import streamlit as st
import os
from dotenv import load_dotenv
from upstash_vector import Index
from openai import OpenAI

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Portfolio IA - Leslie Planet",
    page_icon="🤖",
    layout="wide"
)

# Initialiser les clients
@st.cache_resource
def init_clients():
    upstash = Index(
        url=os.getenv("UPSTASH_VECTOR_REST_URL"),
        token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
    )
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return upstash, openai_client

upstash_index, openai_client = init_clients()


def search_documents(query: str, top_k: int = 3):
    """Recherche les documents pertinents."""
    try:
        results = upstash_index.query(
            data=query,
            top_k=top_k,
            include_metadata=True,
            include_data=True
        )
        return results
    except Exception as e:
        st.error(f"Erreur lors de la recherche: {e}")
        return []


def format_context(results):
    """Formate les résultats en contexte."""
    if not results:
        return "Aucun document pertinent trouvé."
    
    context_parts = []
    for i, result in enumerate(results, 1):
        metadata = result.metadata if hasattr(result, 'metadata') else {}
        data = result.data if hasattr(result, 'data') else ""
        source = metadata.get('source', 'Unknown')
        context_parts.append(f"--- Document {i} (Source: {source}) ---\n{data}\n")
    
    return "\n".join(context_parts)


def chat_with_agent(user_message: str, conversation_history: list) -> str:
    """Génère une réponse de l'agent."""
    # Rechercher les documents
    with st.spinner("🔍 Recherche de documents pertinents..."):
        search_results = search_documents(user_message, top_k=3)
    
    context = format_context(search_results)
    
    # Construire le prompt
    system_prompt = f"""Tu es un assistant IA spécialisé dans le portfolio de Leslie Planet, 
étudiante en BUT Sciences des Données à Niort.

Utilise UNIQUEMENT les informations fournies dans le contexte ci-dessous pour répondre 
aux questions. Si l'information n'est pas dans le contexte, dis-le clairement.

Réponds de manière concise, précise et professionnelle en français.

CONTEXTE DISPONIBLE:
{context}
"""
    
    # Messages
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})
    
    # Appeler OpenAI
    try:
        with st.spinner("💬 Génération de la réponse..."):
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur: {e}"


# Interface Streamlit
st.title("🤖 Agent IA - Portfolio Leslie Planet")
st.markdown("---")

# Initialiser l'historique de conversation dans la session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Barre latérale avec informations
with st.sidebar:
    st.header("ℹ️ À propos")
    st.markdown("""
    Cet agent IA peut répondre à vos questions sur :
    - 👤 Le profil de Leslie
    - 💼 Ses projets académiques
    - 🛠️ Ses compétences techniques
    - 🏢 Son expérience professionnelle
    
    **Technologies utilisées :**
    - OpenAI GPT-4o-mini
    - Upstash Vector (RAG)
    - Streamlit
    """)
    
    st.markdown("---")
    
    # Statistiques de l'index
    try:
        info = upstash_index.info()
        st.metric("📊 Documents indexés", info.vector_count)
        st.metric("📏 Dimension", info.dimension)
    except:
        pass
    
    st.markdown("---")
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.messages = []
        st.rerun()

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Posez votre question sur le portfolio de Leslie..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Obtenir la réponse de l'agent
    with st.chat_message("assistant"):
        response = chat_with_agent(prompt, st.session_state.messages[:-1])
        st.markdown(response)
    
    # Ajouter la réponse à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})

# Suggestions de questions
if not st.session_state.messages:
    st.markdown("### 💡 Questions suggérées")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤 Qui est Leslie Planet ?"):
            st.session_state.messages.append({"role": "user", "content": "Qui est Leslie Planet ?"})
            st.rerun()
        
        if st.button("🛠️ Quelles sont ses compétences en Python ?"):
            st.session_state.messages.append({"role": "user", "content": "Quelles sont ses compétences en Python ?"})
            st.rerun()
    
    with col2:
        if st.button("💼 Parle-moi de ses projets"):
            st.session_state.messages.append({"role": "user", "content": "Parle-moi de ses projets"})
            st.rerun()
        
        if st.button("🏢 Quelle est son expérience professionnelle ?"):
            st.session_state.messages.append({"role": "user", "content": "Quelle est son expérience professionnelle ?"})
            st.rerun()
