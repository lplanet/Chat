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

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Posez votre question..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Obtenir la réponse de l'agent
    with st.chat_message("assistant"):
        with st.spinner("🔄 Réflexion en cours..."):
            try:
                result = Runner.run_sync(agent, prompt)
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

# Suggestions
if not st.session_state.messages:
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
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()
