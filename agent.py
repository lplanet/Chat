"""
Agent IA conversationnel utilisant OpenAI Agents et Upstash Vector.
Cet agent peut répondre à des questions sur le portfolio de Leslie Planet
en utilisant la recherche sémantique dans les documents indexés.
"""

import os
from dotenv import load_dotenv
from upstash_vector import Index
from openai import OpenAI
from typing import List, Dict

# Charger les variables d'environnement
load_dotenv()

# Initialiser les clients
upstash_index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def search_documents(query: str, top_k: int = 3) -> List[Dict]:
    """
    Recherche les documents les plus pertinents dans Upstash Vector.
    
    Args:
        query: La question ou requête de l'utilisateur
        top_k: Nombre de documents à retourner
        
    Returns:
        Liste des documents pertinents avec leurs métadonnées
    """
    try:
        # Recherche sémantique dans Upstash
        results = upstash_index.query(
            data=query,
            top_k=top_k,
            include_metadata=True,
            include_data=True
        )
        
        return results
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        return []


def format_context(results: List) -> str:
    """
    Formate les résultats de recherche en contexte pour l'agent.
    
    Args:
        results: Résultats de la recherche Upstash
        
    Returns:
        Contexte formaté en texte
    """
    if not results:
        return "Aucun document pertinent trouvé."
    
    context_parts = []
    for i, result in enumerate(results, 1):
        metadata = result.metadata if hasattr(result, 'metadata') else {}
        data = result.data if hasattr(result, 'data') else ""
        source = metadata.get('source', 'Unknown')
        
        context_parts.append(f"--- Document {i} (Source: {source}) ---\n{data}\n")
    
    return "\n".join(context_parts)


def chat_with_agent(user_message: str, conversation_history: List[Dict] = None) -> str:
    """
    Envoie un message à l'agent et obtient une réponse.
    
    Args:
        user_message: Le message de l'utilisateur
        conversation_history: Historique de la conversation
        
    Returns:
        La réponse de l'agent
    """
    if conversation_history is None:
        conversation_history = []
    
    # Rechercher les documents pertinents
    print(f"🔍 Recherche de documents pertinents...")
    search_results = search_documents(user_message, top_k=3)
    
    # Formater le contexte
    context = format_context(search_results)
    
    # Construire le prompt système
    system_prompt = f"""Tu es un assistant IA spécialisé dans le portfolio de Leslie Planet, 
étudiante en BUT Sciences des Données à Niort. 

Tu as accès à des informations détaillées sur son profil, ses projets académiques, 
ses compétences techniques et son expérience professionnelle.

Utilise UNIQUEMENT les informations fournies dans le contexte ci-dessous pour répondre 
aux questions. Si l'information n'est pas dans le contexte, dis-le clairement.

Réponds de manière concise, précise et professionnelle en français.

CONTEXTE DISPONIBLE:
{context}
"""
    
    # Construire les messages
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Ajouter l'historique de conversation
    messages.extend(conversation_history)
    
    # Ajouter le message utilisateur
    messages.append({"role": "user", "content": user_message})
    
    # Appeler l'API OpenAI
    try:
        print(f"💬 Génération de la réponse...")
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Modèle compatible avec tous les comptes
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_message = response.choices[0].message.content
        return assistant_message
        
    except Exception as e:
        return f"❌ Erreur lors de la génération de la réponse: {e}"


def interactive_chat():
    """
    Lance une session de chat interactive avec l'agent.
    """
    print("=" * 70)
    print("🤖 Agent IA - Portfolio Leslie Planet")
    print("=" * 70)
    print("Posez vos questions sur le portfolio de Leslie.")
    print("Tapez 'exit' ou 'quit' pour quitter.\n")
    
    conversation_history = []
    
    while True:
        # Obtenir la question de l'utilisateur
        user_input = input("👤 Vous: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['exit', 'quit', 'quitter', 'q']:
            print("\n👋 Au revoir!")
            break
        
        # Obtenir la réponse de l'agent
        print()
        response = chat_with_agent(user_input, conversation_history)
        print(f"\n🤖 Agent: {response}\n")
        print("-" * 70)
        
        # Mettre à jour l'historique
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": response})
        
        # Limiter l'historique pour éviter les tokens excessifs
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]


def test_agent():
    """
    Teste l'agent avec quelques questions prédéfinies.
    """
    print("🧪 Test de l'agent avec des questions prédéfinies\n")
    
    test_questions = [
        "Qui est Leslie Planet ?",
        "Quels sont ses projets en Python ?",
        "Quelles compétences en bases de données possède-t-elle ?",
        "Parle-moi de son stage chez IMA"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*70}")
        print(f"Question {i}: {question}")
        print('='*70)
        
        response = chat_with_agent(question)
        print(f"\n🤖 Réponse: {response}\n")


if __name__ == "__main__":
    import sys
    
    # Si argument --test, lancer les tests
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_agent()
    else:
        # Sinon, lancer le mode interactif
        interactive_chat()
