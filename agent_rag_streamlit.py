"""
Interface Streamlit pour l'agent RAG avec openai-agents.
Lance avec: streamlit run agent_rag_streamlit.py
"""

import streamlit as st
import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from upstash_vector import Index

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Agent RAG - Portfolio Leslie Planet",
    page_icon="🤖",
    layout="wide"
)

# Appliquer le style du portfolio
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Style global */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Arrière-plan et couleurs principales */
    .stApp {
        background: #F8F5CD;
    }
    
    /* Titres */
    h1, h2, h3 {
        color: #ce52a9 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Messages de chat */
    .stChatMessage {
        background-color: #ffe6f8 !important;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Zone de saisie */
    .stChatInputContainer {
        background-color: #ffe6f8;
        border-radius: 8px;
    }
    
    /* Boutons */
    .stButton > button {
        background: #00abf0;
        color: #F8F5CD;
        border: 2px solid #00abf0;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .stButton > button:hover {
        background: #F8F5CD;
        color: #00abf0;
        border: 2px solid #00abf0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffe6f8;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #ce52a9 !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #0B1b29;
    }
    
    /* Métriques */
    [data-testid="stMetricValue"] {
        color: #ce52a9;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #ffe6f8;
        color: #ce52a9;
        border-radius: 8px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #00abf0 !important;
    }
    
    /* Input text */
    .stTextInput > div > div > input {
        background-color: white;
        color: #0B1b29;
        border: 2px solid #00abf0;
        border-radius: 8px;
    }
    
    /* Messages texte */
    p, li {
        color: #0B1b29;
    }
    
    /* Liens */
    a {
        color: #00abf0;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #ce52a9;
    }
    
    /* Markdown en général */
    .stMarkdown {
        color: #0B1b29;
    }
    
    /* Colonnes */
    [data-testid="column"] {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Initialiser Upstash Vector
@st.cache_resource
def init_upstash():
    return Index(
        url=os.getenv("UPSTASH_VECTOR_REST_URL"),
        token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
    )

upstash_index = init_upstash()


@function_tool
def search_portfolio(query: str, top_k: int = 3) -> str:
    """
    Recherche des informations dans le portfolio de Leslie Planet.
    
    Args:
        query: La question ou le sujet à rechercher
        top_k: Nombre de documents à retourner
        
    Returns:
        Documents pertinents formatés
    """
    try:
        results = upstash_index.query(
            data=query,
            top_k=top_k,
            include_metadata=True,
            include_data=True
        )
        
        if not results:
            return "Aucun document pertinent trouvé."
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            metadata = result.metadata if hasattr(result, 'metadata') else {}
            data = result.data if hasattr(result, 'data') else ""
            source = metadata.get('source', 'Unknown')
            
            formatted_results.append(
                f"Document {i} (Source: {source}):\n{data}\n"
            )
        
        return "\n---\n".join(formatted_results)
        
    except Exception as e:
        return f"Erreur: {str(e)}"


@st.cache_resource
def create_agent():
    """Crée l'agent RAG."""
    return Agent(
        name="portfolio-assistant",
        instructions="""Tu es un assistant IA spécialisé dans le portfolio de Leslie Planet.

Utilise la fonction search_portfolio pour rechercher des informations et base tes réponses 
UNIQUEMENT sur les résultats trouvés. Réponds de manière concise et professionnelle en français.""",
        model="gpt-4.1-nano",
        tools=[search_portfolio],
    )

agent = create_agent()

# Interface Streamlit
st.title("🤖 Agent RAG - Portfolio Leslie Planet")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("ℹ️ À propos")
    st.markdown("""
    Cet agent utilise **RAG (Retrieval Augmented Generation)** :
    
    1. 🔍 **Recherche** dans Upstash Vector
    2. 📄 **Récupère** les documents pertinents
    3. 🤖 **Génère** une réponse avec GPT
    
    **Technologies :**
    - openai-agents
    - Upstash Vector
    - GPT-4o-mini
    - Streamlit
    """)
    
    st.markdown("---")
    
    # Stats
    try:
        info = upstash_index.info()
        st.metric("📊 Documents indexés", info.vector_count)
    except:
        pass
    
    st.markdown("---")
    
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.messages = []
        st.rerun()

# Initialiser l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialiser la question sélectionnée
if "selected_question" not in st.session_state:
    st.session_state.selected_question = None

# Initialiser le flag pour cacher les suggestions
if "hide_suggestions" not in st.session_state:
    st.session_state.hide_suggestions = False

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Fonction pour traiter une question
def process_question(question: str):
    """Traite une question et génère la réponse."""
    # Cacher les suggestions après avoir cliqué
    st.session_state.hide_suggestions = True
    
    # Ajouter le message utilisateur s'il n'est pas déjà dans l'historique
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != question:
        st.session_state.messages.append({"role": "user", "content": question})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(question)
    
    # Obtenir la réponse de l'agent
    with st.chat_message("assistant"):
        with st.spinner("🔄 Réflexion en cours..."):
            try:
                result = Runner.run_sync(agent, question)
                response = result.final_output
                st.markdown(response)
                
                # Afficher les étapes (optionnel)
                if hasattr(result, 'events') and result.events:
                    with st.expander("📋 Voir les étapes de raisonnement"):
                        for event in result.events:
                            if hasattr(event, 'type'):
                                st.text(f"- {event.type}")
                
            except Exception as e:
                response = f"❌ Erreur: {e}"
                st.error(response)
    
    # Ajouter la réponse à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Réinitialiser la question sélectionnée
    st.session_state.selected_question = None

# Input utilisateur avec gestion de la question sélectionnée
if st.session_state.selected_question:
    # Traiter la question sélectionnée
    process_question(st.session_state.selected_question)
    st.rerun()

# Afficher les suggestions UNIQUEMENT si l'historique est vide et qu'elles ne sont pas cachées
# Utiliser un container pour les positionner juste avant le chat_input
if not st.session_state.messages and not st.session_state.hide_suggestions:
    suggestions_container = st.container()
    with suggestions_container:
        st.markdown("### 💡 Questions suggérées")
        col1, col2 = st.columns(2)
        
        suggestions = [
            ("👤 Qui est Leslie ?", "Qui est Leslie Planet ?"),
            ("🛠️ Compétences Python", "Quelles sont ses compétences en Python ?"),
            ("💼 Projets", "Parle-moi de ses projets"),
            ("🏢 Stage IMA", "Quelle est son expérience chez IMA ?")
        ]
        
        for i, (label, question) in enumerate(suggestions):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(label, key=f"btn_{i}"):
                    st.session_state.selected_question = question
                    st.rerun()

# Le chat_input doit être appelé en dernier pour apparaître en bas
prompt = st.chat_input("Posez votre question...")
if prompt:
    process_question(prompt)
    st.rerun()
