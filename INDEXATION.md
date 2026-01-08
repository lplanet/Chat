# Indexation des Documents dans Upstash Vector

Ce projet permet d'indexer automatiquement vos documents Markdown dans Upstash Vector pour créer un système de recherche sémantique.

## 📋 Prérequis

1. **Compte Upstash Vector**
   - Créez un compte sur [Upstash](https://upstash.com/)
   - Créez un index Vector
   - Récupérez votre `UPSTASH_VECTOR_REST_URL` et `UPSTASH_VECTOR_REST_TOKEN`

2. **Clé API OpenAI**
   - Créez un compte sur [OpenAI](https://platform.openai.com/)
   - Générez une clé API
   - Récupérez votre `OPENAI_API_KEY`

## 🔧 Configuration

1. **Copier le fichier d'exemple**
   ```bash
   cp .env.example .env
   ```

2. **Remplir vos clés API dans `.env`**
   ```env
   OPENAI_API_KEY=sk-...
   UPSTASH_VECTOR_REST_URL=https://...
   UPSTASH_VECTOR_REST_TOKEN=...
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Utilisation

### Indexer tous les documents

Pour indexer tous les fichiers Markdown du dossier `data/` :

```bash
python index_documents.py
```

Ce script va :
- Parcourir tous les fichiers `.md` dans `data/`
- Générer des embeddings avec OpenAI (text-embedding-3-small)
- Indexer chaque document dans Upstash Vector avec ses métadonnées

### Nettoyer l'index

Pour supprimer tous les documents indexés :

```bash
python reset_index.py
```

## 📁 Structure des documents

Les documents sont organisés de la manière suivante :

```
data/
├── profil/
│   ├── informations_generales.md
│   ├── passion_informatique.md
│   └── centres_interet.md
├── projets/
│   ├── s1_reporting.md
│   ├── s2_bdr.md
│   └── ...
├── competences/
│   ├── langages_programmation.md
│   ├── analyse_statistiques.md
│   └── ...
├── stage.md
└── bilan.md
```

## 🏷️ Métadonnées

Chaque document indexé contient les métadonnées suivantes :
- `source` : Chemin relatif du fichier
- `filename` : Nom du fichier
- `category` : Catégorie (profil, projets, competences, etc.)
- `type` : Type de document (markdown)
- `semestre` : Semestre (pour les projets uniquement)

## 🧪 Tests

Pour tester la connexion à Upstash :

```bash
pytest tests/test_upstash_vector.py
```

## 📊 Vérification

Après l'indexation, vous pouvez vérifier :
- Le nombre de vecteurs indexés dans le terminal
- Les statistiques directement sur le dashboard Upstash

## 🔍 Prochaines étapes

Une fois les documents indexés, vous pourrez :
1. Créer un chatbot qui utilise ces documents comme source de connaissance
2. Implémenter une recherche sémantique sur votre portfolio
3. Construire un agent conversationnel avec RAG (Retrieval Augmented Generation)
