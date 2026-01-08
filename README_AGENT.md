# 🤖 Agent IA - Portfolio Leslie Planet

Agent conversationnel intelligent utilisant RAG (Retrieval Augmented Generation) pour répondre aux questions sur le portfolio de Leslie Planet.

## 🎯 Fonctionnalités

- **Recherche sémantique** dans les documents indexés via Upstash Vector
- **Réponses contextuelles** basées sur les informations réelles du portfolio
- **Conversation naturelle** en français
- **Interface en ligne de commande** ou **interface web avec Streamlit**

## 🚀 Utilisation

### Mode Ligne de Commande

Pour lancer l'agent en mode interactif :

```bash
python agent.py
```

Pour tester l'agent avec des questions prédéfinies :

```bash
python agent.py --test
```

### Mode Interface Web (Streamlit)

Pour lancer l'interface web :

```bash
streamlit run agent_streamlit.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 📋 Prérequis

1. **Documents indexés** dans Upstash Vector (exécuter `python index_documents.py` avant)
2. **Variables d'environnement** configurées dans `.env` :
   ```env
   OPENAI_API_KEY=votre_cle_openai
   UPSTASH_VECTOR_REST_URL=votre_url_upstash
   UPSTASH_VECTOR_REST_TOKEN=votre_token_upstash
   ```

## 💡 Exemples de questions

- "Qui est Leslie Planet ?"
- "Quels sont ses projets en Python ?"
- "Quelles compétences en bases de données possède-t-elle ?"
- "Parle-moi de son stage chez IMA"
- "Quels projets a-t-elle réalisés au semestre 3 ?"
- "Quelles sont ses compétences en analyse de données ?"

## 🏗️ Architecture

```
┌─────────────┐
│  Utilisateur │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Agent IA       │
│  (OpenAI GPT)   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Upstash│ │ Documents MD │
│ Vector │ │  (contexte)  │
└────────┘ └──────────────┘
```

## 🔧 Fonctionnement

1. **L'utilisateur** pose une question
2. **Recherche sémantique** dans Upstash Vector pour trouver les documents pertinents
3. **Formatage du contexte** avec les documents trouvés
4. **Génération de la réponse** par GPT en utilisant uniquement le contexte fourni
5. **Affichage de la réponse** à l'utilisateur

## 📊 Modèle utilisé

- **Modèle principal** : `gpt-4o-mini` (OpenAI)
- **Embeddings** : Générés automatiquement par Upstash Vector
- **Top-K** : 3 documents les plus pertinents pour chaque question

## 🛠️ Personnalisation

### Modifier le nombre de documents récupérés

Dans `agent.py` ou `agent_streamlit.py`, changez le paramètre `top_k` :

```python
search_results = search_documents(user_message, top_k=5)  # Récupère 5 documents au lieu de 3
```

### Changer le modèle OpenAI

Modifiez le paramètre `model` dans la fonction `chat_with_agent()` :

```python
response = openai_client.chat.completions.create(
    model="gpt-4o",  # Ou "gpt-4", "gpt-3.5-turbo", etc.
    messages=messages,
    temperature=0.7,
    max_tokens=500
)
```

### Ajuster la température

Pour des réponses plus créatives ou plus factuelles :

```python
temperature=0.7  # Valeur entre 0 (très factuel) et 1 (plus créatif)
```

## 📝 Notes

- L'agent utilise **uniquement** les informations présentes dans les documents indexés
- Si une information n'est pas disponible, l'agent l'indique clairement
- L'historique de conversation est conservé pendant la session pour un contexte cohérent
- Les réponses sont limitées à 500 tokens pour éviter les coûts excessifs

## 🐛 Dépannage

### L'agent ne trouve pas de documents

Vérifiez que les documents sont bien indexés :
```bash
python index_documents.py
```

### Erreur d'authentification OpenAI

Vérifiez votre clé API dans le fichier `.env` et assurez-vous qu'elle est valide.

### Erreur Upstash Vector

Vérifiez vos credentials Upstash dans le fichier `.env`.

## 🚀 Prochaines améliorations possibles

- [ ] Ajout de la mémorisation longue durée avec Redis
- [ ] Support multi-langues (anglais/français)
- [ ] Export des conversations
- [ ] Analytics des questions posées
- [ ] Mode vocal avec speech-to-text
