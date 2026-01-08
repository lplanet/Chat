# Projet Collecte de Données Web

**Semestre :** 3  
**Date :** Novembre 2024  
**Technologies :** Python, BeautifulSoup, Folium, API ADEME

## Objectif du projet

Développer une application Python combinant deux approches : le web scraping et l'exploitation d'une API publique, dans un contexte orienté données géographiques.

## Partie 1 : Web Scraping - Musées de France

### Source de données
Liste des musées de France disponible sur Wikipedia.

### Objectif
Récupérer des données géographiques et descriptives sur les musées :
- Nom
- Localisation
- Type
- Ville

### Traitement des données
Une fois les données extraites avec BeautifulSoup, nous les avons nettoyées et organisées pour supprimer les doublons et filtrer les valeurs incomplètes.

### Visualisation
Ces données ont ensuite été visualisées à l'aide de la bibliothèque Folium, via une carte interactive permettant de localiser les musées sur le territoire français. Un graphique complémentaire a été généré pour analyser la répartition des musées selon les régions ou les types d'établissement.

## Partie 2 : Exploitation de l'API ADEME

### Source de données
API de l'ADEME fournissant des diagnostics de performance énergétique (DPE) pour les logements en France.

### Fonctionnalités
Nous avons utilisé l'API pour interroger les données DPE d'une commune spécifique (ex. : Fors, code INSEE 79125) et les charger dans un DataFrame.

### Interface utilisateur
L'application permet à l'utilisateur de saisir un nom de commune ou un code INSEE, ce qui déclenche l'affichage automatique d'une carte Folium où les logements sont représentés par des marqueurs colorés selon leur classe énergétique.

### Analyse comparative
Un graphique de comparaison a été réalisé pour visualiser la répartition des logements par lettre de DPE dans les quatre principales villes de l'ancienne région Poitou-Charentes :
- La Rochelle
- Niort
- Poitiers
- Angoulême

### Indicateurs
Un indicateur complémentaire a également été intégré afin de mettre en lumière la proportion de logements énergivores (classés F et G) par ville.

## Interface web
Le projet inclut enfin une interface web simple, permettant de naviguer entre les différentes fonctionnalités de manière intuitive.
