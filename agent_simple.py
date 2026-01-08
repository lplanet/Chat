"""
Agent IA simple utilisant uniquement Upstash Vector (sans OpenAI Chat).
Cette version retourne directement les documents pertinents trouvés.
"""

import os
from dotenv import load_dotenv
from upstash_vector import Index
from typing import List, Dict

# Charger les variables d'environnement
load_dotenv()

# Initialiser le client Upstash
upstash_index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)


def search_and_format(query: str, top_k: int = 3) -> str:
    """
    Recherche et formate les documents pertinents.
    
    Args:
        query: La question de l'utilisateur
        top_k: Nombre de documents à retourner
        
    Returns:
        Réponse formatée avec les documents trouvés
    """
    try:
        print(f"🔍 Recherche de documents pertinents pour: '{query}'")
        
        # Recherche sémantique dans Upstash
        results = upstash_index.query(
            data=query,
            top_k=top_k,
            include_metadata=True,
            include_data=True
        )
        
        if not results:
            return "❌ Aucun document pertinent trouvé pour cette question."
        
        # Formater la réponse
        response_parts = [f"\n📚 J'ai trouvé {len(results)} document(s) pertinent(s):\n"]
        
        for i, result in enumerate(results, 1):
            metadata = result.metadata if hasattr(result, 'metadata') else {}
            data = result.data if hasattr(result, 'data') else ""
            source = metadata.get('source', 'Unknown')
            score = result.score if hasattr(result, 'score') else 0
            
            response_parts.append(f"\n{'='*70}")
            response_parts.append(f"📄 Document {i} - {source} (Score: {score:.3f})")
            response_parts.append('='*70)
            response_parts.append(data)
            response_parts.append("")
        
        return "\n".join(response_parts)
        
    except Exception as e:
        return f"❌ Erreur lors de la recherche: {e}"


def interactive_search():
    """
    Lance une session de recherche interactive.
    """
    print("=" * 70)
    print("🔍 Recherche Sémantique - Portfolio Leslie Planet")
    print("=" * 70)
    print("Posez vos questions. Tapez 'exit' ou 'quit' pour quitter.\n")
    
    while True:
        user_input = input("👤 Question: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['exit', 'quit', 'quitter', 'q']:
            print("\n👋 Au revoir!")
            break
        
        # Rechercher et afficher les résultats
        response = search_and_format(user_input, top_k=3)
        print(response)
        print("\n" + "-"*70 + "\n")


def test_search():
    """
    Teste la recherche avec des questions prédéfinies.
    """
    print("🧪 Test de la recherche sémantique\n")
    
    test_questions = [
        "Qui est Leslie Planet ?",
        "Quels sont ses projets en Python ?",
        "Quelles compétences en bases de données possède-t-elle ?",
        "Parle-moi de son stage chez IMA",
        "Quels sont ses centres d'intérêt ?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*70}")
        print(f"Question {i}: {question}")
        response = search_and_format(question, top_k=2)
        print(response)


def stats():
    """
    Affiche les statistiques de l'index Upstash.
    """
    try:
        info = upstash_index.info()
        print("\n📊 Statistiques de l'index Upstash Vector:")
        print(f"   - Dimension: {info.dimension}")
        print(f"   - Total de vecteurs: {info.vector_count}")
        print(f"   - Similarité: {info.similarity_function}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des stats: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_search()
        elif sys.argv[1] == "--stats":
            stats()
    else:
        interactive_search()
