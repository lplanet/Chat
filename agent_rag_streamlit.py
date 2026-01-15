"""
Interface Streamlit pour l'agent RAG avec openai-agents.
Lance avec: streamlit run agent_rag_streamlit.py
"""

import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from upstash_vector import Index
from upstash_redis import Redis

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Agent RAG - Portfolio Leslie Planet",
    page_icon="🤖",
    layout="wide"
)

# Charger le style depuis le fichier CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialiser Upstash Vector
@st.cache_resource
def init_upstash():
    return Index(
        url=os.getenv("UPSTASH_VECTOR_REST_URL"),
        token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
    )

upstash_index = init_upstash()

# Initialiser Upstash Redis (optionnel pour l'historique)
@st.cache_resource
def init_redis():
    redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
    redis_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    
    if redis_url and redis_token:
        try:
            return Redis(url=redis_url, token=redis_token)
        except:
            return None
    return None

redis_client = init_redis()

# Fonctions pour gérer l'historique avec Redis
def save_conversation_to_redis(session_id: str, messages: list):
    """Sauvegarde une conversation dans Redis"""
    if redis_client:
        try:
            conversation_data = {
                "messages": messages,
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id
            }
            redis_client.set(f"conversation:{session_id}", json.dumps(conversation_data))
        except Exception as e:
            st.warning(f"Impossible de sauvegarder dans Redis: {e}")





@function_tool
def search_portfolio(query: str, top_k: int = 5) -> str:
    """
    Recherche des informations dans le portfolio de Leslie Planet.
    
    Args:
        query: La question ou le sujet à rechercher
        top_k: Nombre de documents à retourner (par défaut 5)
        
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
        
        # Utiliser un dict pour éviter les doublons basés sur la source
        unique_docs = {}
        for result in results:
            metadata = result.metadata if hasattr(result, 'metadata') else {}
            data = result.data if hasattr(result, 'data') else ""
            source = metadata.get('source', 'Unknown')
            
            # Éviter les doublons
            if source not in unique_docs:
                unique_docs[source] = {
                    'data': data,
                    'metadata': metadata
                }
        
        formatted_results = []
        for i, (source, doc) in enumerate(unique_docs.items(), 1):
            result_text = f"Document {i} (Source: {source})"
            
            # Ajouter les outils si disponibles
            if 'outils' in doc['metadata'] and doc['metadata']['outils']:
                result_text += f"\nOutils/Technologies: {doc['metadata']['outils']}"
            
            result_text += f":\n{doc['data']}\n"
            formatted_results.append(result_text)
        
        return "\n---\n".join(formatted_results)
        
    except Exception as e:
        return f"Erreur: {str(e)}"


@function_tool
def search_projects_with_person(person_name: str) -> str:
    """
    Recherche spécifiquement tous les projets/SAE réalisés avec une personne donnée.
    Fait plusieurs recherches pour être exhaustif et filtre pour ne garder que 
    les projets où la personne est vraiment dans l'équipe.
    
    Args:
        person_name: Le nom de la personne (ex: "Hélène", "Hélène VIZOSO")
        
    Returns:
        Liste complète des projets trouvés avec cette personne
    """
    try:
        # Faire plusieurs recherches avec différents termes
        queries = [
            f"projets avec {person_name}",
            f"équipe {person_name}",
            f"binôme {person_name}",
            f"groupe {person_name}",
            f"SAE {person_name}"
        ]
        
        all_docs = {}
        for query in queries:
            results = upstash_index.query(
                data=query,
                top_k=10,  # Rechercher plus de documents
                include_metadata=True,
                include_data=True
            )
            
            for result in results:
                metadata = result.metadata if hasattr(result, 'metadata') else {}
                data = result.data if hasattr(result, 'data') else ""
                source = metadata.get('source', 'Unknown')
                
                # Filtrage strict : vérifier que la personne est mentionnée dans une ligne d'équipe
                lines = data.split('\n')
                person_in_team = False
                
                # Extraire le prénom et le nom de famille si possible
                person_parts = person_name.split()
                first_name = person_parts[0].lower()
                last_name = person_parts[-1].lower() if len(person_parts) > 1 else ""
                
                for line in lines:
                    line_lower = line.lower()
                    # Vérifier si c'est une ligne d'équipe/binôme/groupe
                    if any(keyword in line_lower for keyword in ['équipe :', 'équipe:', 'binôme', 'groupe']):
                        # Vérifier si la personne est mentionnée dans cette ligne
                        if first_name in line_lower:
                            # Si on a un nom de famille, vérifier qu'il est aussi présent
                            if last_name and last_name in line_lower:
                                person_in_team = True
                                break
                            # Si on n'a que le prénom, accepter
                            elif not last_name:
                                person_in_team = True
                                break
                            # Si on a un nom de famille dans la recherche mais pas dans la ligne, vérifier quand même
                            elif last_name:
                                person_in_team = True
                                break
                
                # Ajouter seulement si la personne est dans l'équipe
                if person_in_team and source not in all_docs:
                    all_docs[source] = {
                        'data': data,
                        'metadata': metadata
                    }
        
        if not all_docs:
            return f"Aucun projet trouvé avec {person_name}."
        
        formatted_results = []
        for i, (source, doc) in enumerate(all_docs.items(), 1):
            result_text = f"Document {i} (Source: {source})"
            
            # Ajouter les outils si disponibles
            if 'outils' in doc['metadata'] and doc['metadata']['outils']:
                result_text += f"\nOutils/Technologies: {doc['metadata']['outils']}"
            
            result_text += f":\n{doc['data']}\n"
            formatted_results.append(result_text)
        
        return f"Trouvé {len(all_docs)} document(s) mentionnant {person_name} dans l'équipe:\n\n" + "\n---\n".join(formatted_results)
        
    except Exception as e:
        return f"Erreur: {str(e)}"


@function_tool
def search_projects_by_tool(tool_name: str) -> str:
    """
    Recherche tous les projets/SAE qui utilisent un outil ou technologie spécifique.
    Recherche dans les métadonnées des outils, pas dans le contenu textuel.
    
    Args:
        tool_name: Le nom de l'outil/technologie (ex: "Python", "R", "Excel", "PowerBI")
        
    Returns:
        Liste des projets utilisant cet outil
    """
    try:
        # Récupérer tous les documents de type projet
        results = upstash_index.query(
            data="projets SAE",
            top_k=50,  # Récupérer beaucoup de documents
            include_metadata=True,
            include_data=True
        )
        
        if not results:
            return f"Aucun projet trouvé."
        
        projects_with_tool = {}
        tool_lower = tool_name.lower().strip()
        
        for result in results:
            metadata = result.metadata if hasattr(result, 'metadata') else {}
            data = result.data if hasattr(result, 'data') else ""
            source = metadata.get('source', 'Unknown')
            
            # Vérifier si le document a des métadonnées d'outils
            if 'outils_list' in metadata and metadata['outils_list']:
                outils_list = metadata['outils_list']
                # Convertir en liste si c'est une chaîne
                if isinstance(outils_list, str):
                    outils_list = [o.strip() for o in outils_list.split(',')]
                
                # Vérifier si l'outil recherché est dans la liste
                for outil in outils_list:
                    if tool_lower == outil.lower().strip():
                        if source not in projects_with_tool:
                            # Extraire le nom du projet du contenu
                            lines = data.split('\n')
                            project_name = source
                            for line in lines:
                                if line.startswith('#') and not line.startswith('##'):
                                    project_name = line.replace('#', '').strip()
                                    break
                            
                            projects_with_tool[source] = {
                                'name': project_name,
                                'tools': ', '.join(outils_list),
                                'data': data,
                                'metadata': metadata
                            }
                        break
        
        if not projects_with_tool:
            return f"Aucun projet trouvé utilisant {tool_name}."
        
        # Formater les résultats
        formatted_results = []
        for i, (source, proj) in enumerate(projects_with_tool.items(), 1):
            result_text = f"{i}. {proj['name']}\n   - Source: {source}\n   - Outils: {proj['tools']}"
            formatted_results.append(result_text)
        
        return f"Trouvé {len(projects_with_tool)} projet(s) utilisant {tool_name}:\n\n" + "\n\n".join(formatted_results)
        
    except Exception as e:
        return f"Erreur: {str(e)}"


@st.cache_resource
def create_agent():
    """Crée l'agent RAG."""
    return Agent(
        name="portfolio-assistant",
        instructions="""Tu es un assistant IA spécialisé dans le portfolio de Leslie Planet.

Tu as accès à trois fonctions:
1. search_portfolio: pour les recherches générales
2. search_projects_with_person: pour trouver TOUS les projets avec une personne spécifique
3. search_projects_by_tool: pour trouver TOUS les projets utilisant un outil/technologie spécifique

IMPORTANT pour les questions sur les projets/SAE avec une personne:
- Utilise TOUJOURS search_projects_with_person(nom_personne) pour ces questions
- Cette fonction fait plusieurs recherches automatiquement pour être exhaustive
- Elle retourne TOUS les documents où la personne est mentionnée dans l'équipe

IMPORTANT pour les questions sur les outils/technologies:
- Utilise TOUJOURS search_projects_by_tool(nom_outil) pour les questions comme "combien de projets avec Python/R/Excel"
- Cette fonction recherche dans les métadonnées des outils, pas dans le texte
- Elle donne le nombre EXACT de projets utilisant cet outil
- Exemples: "Combien de projets avec Python?", "Quels projets utilisent R?", "Liste des SAE avec PowerBI"

IMPORTANT pour les questions sur les études/matières:
- Quand on demande "Qu'est-ce que Leslie étudie?", "Quelles matières?", "Quels domaines?"
- Réponds avec les MATIÈRES et DOMAINES d'études (mathématiques, statistiques, informatique, etc.)
- Ne réponds pas juste avec le nom du diplôme
- Cherche dans les documents sur le profil et les domaines d'études

Pour les autres questions, utilise search_portfolio normalement.

Réponds de manière concise et professionnelle en français, en te basant UNIQUEMENT sur les résultats trouvés.""",
        model="gpt-4.1-nano",
        tools=[search_portfolio, search_projects_with_person, search_projects_by_tool],
    )

agent = create_agent()

# Initialiser les variables de session AVANT tout le reste
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None

if "hide_suggestions" not in st.session_state:
    st.session_state.hide_suggestions = False

if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# Interface Streamlit
st.title("🤖 Agent RAG - Portfolio Leslie Planet")
st.markdown("---")

# Sidebar - Historique des conversations
with st.sidebar:
       
        # Bouton nouvelle conversation
    if st.button("➕ Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.hide_suggestions = False
        st.rerun()


    
    st.markdown("---")
    
    # Stats
    try:
        info = upstash_index.info()
        st.metric("📊 Documents indexés", info.vector_count)
    except:
        pass

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
    
    # Sauvegarder automatiquement dans Redis si disponible
    if redis_client:
        save_conversation_to_redis(st.session_state.session_id, st.session_state.messages)
    
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
