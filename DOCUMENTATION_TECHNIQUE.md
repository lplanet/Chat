# Documentation Technique - Portfolio Chatbot RAG

## Vue d'ensemble du projet


Ce projet a pour objectif de crée un chatbot basé sur son propre porfolio afin de permettre aux vistiteur et au recruteur de poser des question et de rendre le portfolio plus interactif. Pour ce faire je me suis aidée d'un modele d'inteligence artificielle déja existante que j'ai entrainer a reponde sur mon porfolio a l'aide de l'architecture RAG.


## Étapes de développement

### 1. Hiérarchisation et organisation des données

La première étape a consisté à structurer l'ensemble des informations de mon portfolio dans des fichiers Markdown organisés de manière hiérarchique. J'ai créé un dossier `data` contenant plusieurs sous-dossiers thématiques pour organiser les informations de manière logique. Le dossier `profil` regroupe mes informations générales, ma passion pour l'informatique et mes centres d'intérêt. Le dossier `competences` détaille mes compétences techniques en les catégorisant par domaine : langages de programmation, outils de visualisation, bases de données, APIs, analyses statistiques, domaines d'application et compétences transversales. Enfin, le dossier `projets` contient l'ensemble de mes projets académiques organisés par semestre, du S1 au S4, ainsi que mon expérience de stage.

Cette organisation hiérarchique permet une navigation claire et une récupération efficace des informations. Chaque fichier Markdown est rédigé avec des titres et sous-titres structurés qui facilitent le découpage et l'indexation ultérieure des contenus. Pour chaque projet, j'ai documenté les objectifs, les technologies utilisées, les résultats obtenus et les compétences développées. -

### 2. Indexation des documents

La deuxième étape, implémentée dans le fichier `index_documents.py`, consiste à transformer ces documents Markdown en vecteurs numériques stockés dans une base de données vectorielle Upstash. Le processus commence par la lecture récursive de tous les fichiers Markdown présents dans le dossier `data`. Pour chaque fichier, le système extrait automatiquement des métadonnées enrichies à partir du chemin du fichier et de son contenu. Ces métadonnées incluent la source du document, son nom, sa catégorie (profil, compétences, projets) et son type.

Pour les projets, j'ai mis en place un système d'enrichissement supplémentaire des métadonnées. Chaque projet est associé manuellement à un dictionnaire qui liste les technologies et outils utilisés (Python, R, Excel, MySQL, PowerBI, etc.). Le système extrait également automatiquement le semestre correspondant à partir du nom du fichier. Cette association manuelle des technologies garantit une précision maximale lors des recherches par outil spécifique, car elle ne dépend pas de la présence explicite de ces termes dans le texte.

Une fois les métadonnées extraites et enrichies, chaque document est envoyé à Upstash Vector qui génère automatiquement des embeddings (représentations vectorielles) à partir du texte en utilisant le modèle BAAI/bge-m3. Ces embeddings permettent ensuite de réaliser des recherches sémantiques, c'est-à-dire de trouver les documents pertinents même si les mots exacts de la question ne figurent pas dans le texte. 

### 3. Création de l'agent conversationnel

La troisième étape, consiste à créer un agent intelligent capable d'interagir avec les utilisateurs (gent_rag_streamlit.py). Cet agent est construit avec la bibliothèque `openai-agents` et utilise le modèle GPT-4.1-nano d'OpenAI. L'agent dispose de trois outils spécialisés appelés "function tools" qui lui permettent de rechercher les informations nécessaires pour répondre aux questions.

Le premier outil, `search_portfolio`, effectue une recherche sémantique générale dans l'ensemble des documents indexés. Il est utilisé pour les questions larges concernant mes compétences, mon parcours ou mes expériences. Le deuxième outil, `search_projects_with_person`, est spécialisé dans la recherche de projets réalisés avec des personnes spécifiques. Il effectue plusieurs recherches avec différentes formulations puis filtre les résultats pour ne garder que les projets où la personne est effectivement mentionnée dans l'équipe. Le troisième outil, `search_projects_by_tool`, permet de rechercher tous les projets utilisant une technologie particulière en consultant directement les métadonnées enrichies lors de l'indexation.

L'agent est configuré avec des instructions système détaillées qui définissent son comportement. Il est programmé pour répondre à la première personne en tant que Leslie Planet, pour toujours chercher les informations dans les documents avant de répondre, pour ne jamais inventer d'informations et pour utiliser le bon outil selon le type de question posée. Cette configuration garantit que les réponses sont toujours basées sur des informations authentiques et pertinentes extraites du portfolio.

### 4. Intégration dans une interface web

La dernière étape consiste à intégrer l'agent dans une interface utilisateur accessible via le web grâce à Sreamlit. 

L'application propose quatre questions suggérées au démarrage pour guider les visiteurs : "Qui est Leslie Planet ?", "Quelles sont ses compétences en Python ?", "Parle-moi de ses projets" et "Quelle est son expérience chez IMA ?". Lorsqu'un utilisateur pose une question, l'agent la traite en appelant les outils appropriés, récupère les documents pertinents, génère une réponse contextualisée et l'affiche instantanément à l'utilisateur.

Le fichier `assets/style.css` permet de personnaliser l'apparence visuelle de l'interface pour qu'elle corresponde à l'identité graphique du portfolio. 

## Système d'historisation des conversations

Un aspect important du projet est l'historisation automatique des conversations dans Upstash Redis. Chaque échange entre un visiteur et l'agent est sauvegardé avec un horodatage et un identifiant de session unique. Cette fonctionnalité a été développée avec un objectif précis : me permettre d'analyser les questions posées par les recruteurs et visiteurs pour améliorer continuellement mon portfolio et me préparer aux entretiens.

J'ai fait le choix délibéré de ne pas afficher cet historique aux utilisateurs pour plusieurs raisons. Premièrement, l'historique des conversations d'autres personnes n'apporte aucune valeur ajoutée aux recruteurs qui découvrent le portfolio. Chaque visiteur doit pouvoir démarrer une conversation propre et personnalisée sans être distrait par les questions posées par d'autres utilisateurs. Deuxièmement, si l'historique était accessible publiquement, il faudrait impérativement implémenter un système d'authentification complet avec login et mot de passe pour protéger la confidentialité des conversations. Cette complexité technique ne serait pas justifiée pour une fonctionnalité qui n'est pas essentielle à l'expérience utilisateur.

L'objectif stratégique de cette historisation est purement analytique. En tant que propriétaire du portfolio, je peux consulter ces conversations via la console Upstash Redis ou via un script Python personnalisé. Cette analyse me permet de comprendre quels types de questions les recruteurs posent le plus souvent, d'identifier les informations manquantes ou peu claires dans mon portfolio, d'anticiper les questions qui pourraient être posées lors d'entretiens d'embauche et d'ajuster continuellement le contenu et les instructions de l'agent en fonction des tendances observées. C'est donc un outil d'amélioration continue plutôt qu'une fonctionnalité destinée aux visiteurs.

## Technologies utilisées

Le projet repose sur plusieurs technologies clés. Python 3.12 constitue le langage principal du projet. La bibliothèque `openai-agents` permet de créer l'agent intelligent avec le modèle GPT-4.1-nano. Streamlit fournit le framework pour l'interface web interactive. Upstash Vector sert de base de données vectorielle pour la recherche sémantique avec le modèle d'embedding BAAI/bge-m3, tandis qu'Upstash Redis stocke l'historique des conversations. La bibliothèque `python-dotenv` gère de manière sécurisée les variables d'environnement et les clés API, et `pytest` permet d'exécuter les tests unitaires pour vérifier le bon fonctionnement du système.

