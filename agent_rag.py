"""
Agent IA avec RAG utilisant openai-agents et Upstash Vector.
L'agent peut interroger la base de données vectorielle via une Tool.
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from upstash_vector import Index
from typing import List, Dict

# Charger les variables d'environnement
load_dotenv()

# Initialiser Upstash Vector
upstash_index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)


@function_tool
def search_portfolio(query: str, top_k: int = 3) -> str:
    """
    Recherche des informations dans le portfolio de Leslie Planet.
    
    Cette fonction effectue une recherche sémantique dans une base de données
    vectorielle contenant des informations sur le profil, les projets, les compétences
    et l'expérience professionnelle de Leslie.
    
    Args:
        query: La question ou le sujet à rechercher dans le portfolio
        top_k: Nombre de documents pertinents à retourner (par défaut 3)
        
    Returns:
        Les documents les plus pertinents trouvés, formatés en texte
    """
    try:
        # Recherche sémantique dans Upstash Vector
        results = upstash_index.query(
            data=query,
            top_k=top_k,
            include_metadata=True,
            include_data=True
        )
        
        if not results:
            return "Aucun document pertinent trouvé dans le portfolio."
        
        # Formater les résultats
        formatted_results = []
        for i, result in enumerate(results, 1):
            metadata = result.metadata if hasattr(result, 'metadata') else {}
            data = result.data if hasattr(result, 'data') else ""
            source = metadata.get('source', 'Unknown')
            category = metadata.get('category', '')
            
            formatted_results.append(
                f"Document {i} (Source: {source}, Catégorie: {category}):\n{data}\n"
            )
        
        return "\n---\n".join(formatted_results)
        
    except Exception as e:
        return f"Erreur lors de la recherche: {str(e)}"


def create_portfolio_agent():
    """
    Crée un agent IA avec accès au portfolio via RAG.
    """
    agent = Agent(
        name="portfolio-assistant",
        instructions="""Tu es un assistant IA spécialisé dans le portfolio de Leslie Planet, 
etudiante en BUT Sciences des Données à Niort.

Tu as accès à une fonction 'search_portfolio' qui te permet de rechercher des informations 
dans son portfolio (profil, projets, compétences, expérience).

IMPORTANT:
- Utilise TOUJOURS la fonction search_portfolio pour répondre aux questions sur Leslie
- Base tes réponses UNIQUEMENT sur les informations trouvées par la recherche
- Si l'information n'est pas dans les résultats de recherche, dis-le clairement
- Réponds de manière concise, précise et professionnelle en français
- Cite tes sources (documents) quand tu donnes des informations

Exemples de questions auxquelles tu peux répondre:
- Qui est Leslie Planet ?
- Quels sont ses projets ?
- Quelles sont ses compétences techniques ?
- Quelle est son expérience professionnelle ?
""",
        model="gpt-4.1-nano",
        tools=[search_portfolio],
    )
    
    return agent


def chat_interactive():
    """
    Lance une session de chat interactive avec l'agent.
    """
    print("=" * 70)
    print("🤖 Agent IA avec RAG - Portfolio Leslie Planet")
    print("=" * 70)
    print("Posez vos questions sur le portfolio de Leslie.")
    print("Tapez 'exit' ou 'quit' pour quitter.\n")
    
    agent = create_portfolio_agent()
    
    while True:
        user_input = input("👤 Vous: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['exit', 'quit', 'quitter', 'q']:
            print("\n👋 Au revoir!")
            break
        
        try:
            print("\n🔄 Réflexion en cours...\n")
            
            # Exécuter l'agent
            result = Runner.run_sync(agent, user_input)
            
            # Afficher la réponse
            print(f"🤖 Agent: {result.final_output}\n")
            print("-" * 70 + "\n")
            
        except Exception as e:
            print(f"❌ Erreur: {e}\n")


def test_agent_with_questions():
    """
    Teste l'agent avec plusieurs questions prédéfinies.
    """
    print("🧪 Test de l'agent avec des questions prédéfinies\n")
    
    agent = create_portfolio_agent()
    
    test_questions = [
        "Qui est Leslie Planet ?",
        "Quels sont ses projets en Python ?",
        "Quelles compétences possède-t-elle en bases de données ?",
        "Parle-moi de son stage chez IMA",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*70}")
        print(f"Question {i}: {question}")
        print('='*70)
        
        try:
            result = Runner.run_sync(agent, question)
            print(f"\n🤖 Réponse:\n{result.final_output}\n")
            
            # Afficher les étapes de raisonnement si disponibles
            if hasattr(result, 'events') and result.events:
                print(f"\n📋 Étapes:")
                for event in result.events:
                    if hasattr(event, 'type'):
                        print(f"  - {event.type}")
            
        except Exception as e:
            print(f"❌ Erreur: {e}\n")


def demo_search_tool():
    """
    Démo de la fonction search_portfolio utilisée par l'agent.
    """
    print("🔍 Démonstration de la fonction search_portfolio\n")
    
    queries = [
        "Leslie Planet",
        "projets Python",
        "stage IMA"
    ]
    
    for query in queries:
        print(f"\n{'='*70}")
        print(f"Recherche: {query}")
        print('='*70)
        
        result = search_portfolio(query, top_k=2)
        print(result)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_agent_with_questions()
        elif sys.argv[1] == "--demo":
            demo_search_tool()
    else:
        chat_interactive()
