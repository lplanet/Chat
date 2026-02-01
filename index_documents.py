"""
Script d'indexation des documents Markdown dans Upstash Vector.
Ce script parcourt tous les fichiers .md dans le dossier data/ et les indexe
avec leurs métadonnées pour permettre une recherche sémantique.
Note: Upstash Vector génère automatiquement les embeddings à partir du texte.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from upstash_vector import Index, Vector

# Charger les variables d'environnement
load_dotenv()

# Initialiser le client Upstash
upstash_index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"),
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)

# Mapping des outils/logiciels par projet
PROJET_OUTILS = {
    "s1_reporting": ["VBA", "Excel"],
    "s1_gestion_fichier": ["Python"],
    "s1_martinique": ["Excel"],
    "s1_islande": ["PowerPoint"],
    "s2_bdr": ["Python", "Tkinter", "MySQL"],
    "s2_echantillonnage": ["R"],
    "s2_regression": ["R"],
    "s2_datavisualisation": ["PowerBI"],
    "s3_reporting_multivariee": ["R"],
    "s3_s4_besoin_territoire": ["HTML", "CSS", "PowerPoint"],
    "s4_solution_decisionnelle_ccam": ["Python", "MySQL"],
    "s3_datawarehouse": ["PowerBI"],
    "s3_collecte_web": ["Python"],
    "stage": ["Excel", "VBA", "Articque"]
}


def read_markdown_file(file_path: Path) -> tuple[str, dict]:
    """
    Lit un fichier Markdown et extrait son contenu et ses métadonnées.
    
    Args:
        file_path: Chemin vers le fichier Markdown
        
    Returns:
        Tuple (contenu, métadonnées)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire les métadonnées du chemin
    relative_path = file_path.relative_to(Path("data"))
    parts = relative_path.parts
    
    metadata = {
        "source": str(relative_path),
        "filename": file_path.name,
        "category": parts[0] if len(parts) > 1 else "general",
        "type": "markdown"
    }
    
    # Ajouter des métadonnées spécifiques selon la catégorie
    if "projets" in str(relative_path):
        # Extraire le semestre du nom de fichier (ex: s1_reporting.md -> S1)
        filename = file_path.stem
        if filename.startswith("s"):
            semestre = filename.split("_")[0].upper()
            metadata["semestre"] = semestre
        
        # Ajouter les outils/logiciels si disponibles
        if filename in PROJET_OUTILS:
            metadata["outils"] = ", ".join(PROJET_OUTILS[filename])
            metadata["outils_list"] = PROJET_OUTILS[filename]
    
    # Ajouter les outils pour le stage
    if "stage" in str(relative_path):
        if "stage" in PROJET_OUTILS:
            metadata["outils"] = ", ".join(PROJET_OUTILS["stage"])
            metadata["outils_list"] = PROJET_OUTILS["stage"]
    
    return content, metadata


def index_document(doc_id: str, content: str, metadata: dict):
    """
    Indexe un document dans Upstash Vector.
    Upstash génère automatiquement l'embedding à partir du texte.
    
    Args:
        doc_id: Identifiant unique du document
        content: Contenu textuel du document
        metadata: Métadonnées associées au document
    """
    # Indexer dans Upstash - l'embedding est généré automatiquement
    print(f"Indexation dans Upstash: {metadata['source']}")
    upstash_index.upsert(
        vectors=[
            Vector(
                id=doc_id,
                data=content,  # Upstash génère l'embedding automatiquement
                metadata=metadata
            )
        ]
    )


def index_all_documents():
    """
    Parcourt tous les fichiers Markdown dans le dossier data/ et les indexe.
    Exclut les fichiers projets_sX.md car ils sont des doublons des fichiers dans projets/
    """
    data_dir = Path("data")
    
    if not data_dir.exists():
        print(f"❌ Le dossier {data_dir} n'existe pas!")
        return
    
    # Trouver tous les fichiers .md
    all_md_files = list(data_dir.rglob("*.md"))
    

    
    print(f"📄 {len(all_md_files)} fichiers Markdown trouvés (exclusion des doublons projets_sX.md)")
    print("=" * 60)
    
    indexed_count = 0
    
    for md_file in all_md_files:
        try:
            # Lire le contenu et les métadonnées
            content, metadata = read_markdown_file(md_file)
            
            # Créer un ID unique basé sur le chemin relatif
            doc_id = str(md_file.relative_to(data_dir)).replace("\\", "/").replace(".md", "")
            
            # Indexer le document
            index_document(doc_id, content, metadata)
            
            indexed_count += 1
            print(f"✅ Indexé: {metadata['source']}")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Erreur lors de l'indexation de {md_file}: {e}")
            print("-" * 60)
    
    print("=" * 60)
    print(f"✨ Indexation terminée: {indexed_count}/{len(all_md_files)} documents indexés")
    
    # Afficher les statistiques de l'index
    try:
        info = upstash_index.info()
        print(f"📊 Statistiques de l'index Upstash:")
        print(f"   - Dimension: {info.dimension}")
        print(f"   - Total vectors: {info.vector_count}")
    except Exception as e:
        print(f"⚠️  Impossible de récupérer les stats: {e}")


if __name__ == "__main__":
    print("🚀 Démarrage de l'indexation des documents dans Upstash Vector")
    print("=" * 60)
    index_all_documents()
