"""
Script pour nettoyer l'index Upstash Vector.
Utile pour supprimer tous les documents indexés et repartir de zéro.
"""

import os
from dotenv import load_dotenv
from upstash_vector import Index

# Charger les variables d'environnement
load_dotenv()

# Initialiser le client Upstash
upstash_index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)


def reset_index():
    """
    Supprime tous les vecteurs de l'index Upstash.
    """
    try:
        print("🗑️  Nettoyage de l'index Upstash Vector...")
        
        # Obtenir les informations de l'index
        info = upstash_index.info()
        print(f"📊 Nombre de vecteurs avant nettoyage: {info.vector_count}")
        
        # Upstash Vector ne permet pas de tout supprimer d'un coup facilement
        # On doit utiliser reset() si disponible, sinon on devra recréer l'index
        upstash_index.reset()
        
        print("✅ Index nettoyé avec succès!")
        
        # Vérifier
        info_after = upstash_index.info()
        print(f"📊 Nombre de vecteurs après nettoyage: {info_after.vector_count}")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
        print("💡 Si la méthode reset() n'existe pas, vous devrez recréer l'index manuellement sur le dashboard Upstash.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        reset_index()
    else:
        confirmation = input("⚠️  Êtes-vous sûr de vouloir supprimer tous les documents indexés? (oui/non): ")
        if confirmation.lower() in ["oui", "yes", "o", "y"]:
            reset_index()
        else:
            print("❌ Opération annulée")
