"""
Script pour lister les modèles OpenAI disponibles sur votre compte.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("🔍 Récupération des modèles disponibles...\n")

try:
    models = client.models.list()
    
    print(f"📊 Total de modèles disponibles: {len(models.data)}\n")
    
    # Filtrer les modèles de chat
    chat_models = [m for m in models.data if 'gpt' in m.id.lower()]
    
    if chat_models:
        print("💬 Modèles de chat disponibles:")
        for model in sorted(chat_models, key=lambda x: x.id):
            print(f"  - {model.id}")
    else:
        print("❌ Aucun modèle GPT disponible sur votre compte")
        print("\n⚠️  Votre compte OpenAI nécessite:")
        print("   1. D'ajouter un moyen de paiement")
        print("   2. D'ajouter des crédits")
        print("   3. D'attendre l'activation des modèles\n")
        print("   Visitez: https://platform.openai.com/account/billing")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
