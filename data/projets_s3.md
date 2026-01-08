# Projets du Semestre 3

## Projet Reporting d'une Analyse Multivariée

**Date :** Octobre 2024  
**Technologies :** R, données INSEE

### Contexte du projet

En 2021, 9,1 millions de personnes vivaient sous le seuil de pauvreté en France métropolitaine, soit environ 14 % de la population.

### Objectif du projet

Concevoir un outil visuel et automatisé pour le suivi et l'évaluation de la pauvreté en France. Cet outil devait faciliter la prise de décisions à l'échelle départementale et régionale.

### Données collectées

Pour contribuer à la réduction de ce taux, il est essentiel de fournir des données variées :
- Nombre de personnes concernées
- Tranches d'âge
- Niveau d'éducation
- Part des locataires en HLM
- Effectifs de police et de gendarmerie

### Technologies utilisées

Pour mener à bien cette étude, nous avons exploité les données de l'INSEE et développé une application à l'aide du langage R.

---

## Projet Besoin du Territoire

**Date :** Semestre 3 et 4 (projet au fil de l'eau)  
**Équipe :** Groupe de trois personnes  
**Public cible :** Deux classes de première du lycée Paul Guérin

### Mission du projet

Dispenser des cours de NSI (Numérique et Sciences Informatiques) à deux classes de première du lycée Paul Guérin.

### Contenu pédagogique

Les cours portaient sur la programmation web, avec l'apprentissage de :
- HTML
- Format CSV
- Notion de formulaire

### Organisation des cours

Nous avons animé :
- Deux séances de deux heures au lycée (une par classe)
- Une session supplémentaire à l'IUT avec les deux classes réunies

### Structure pédagogique

Chaque cours suivait le même déroulé :
- 15 à 20 minutes de théorie
- Exercices pratiques sur ordinateur (conçus par nous-mêmes)

---

## Projet Intégration de Données dans un Datawarehouse

**Date :** Décembre 2024  
**Contexte :** Entreprise fictive SportOne  
**Technologies :** Entrepôt de données, tableaux de bord

### Contexte de l'entreprise

SportOne est spécialisée dans la vente au détail d'articles de sport et de plein air, présente à l'international avec des magasins physiques et un site e-commerce.

### Objectif du projet

Concevoir un entrepôt de données pour centraliser et structurer les données issues de :
- Ventes (entre 2017 et 2022)
- Catalogue produit
- Clients
- Fournisseurs
- Informations géographiques

### Modélisation

L'entrepôt de données est modélisé selon plusieurs axes d'analyse :
- Géographie
- Temps
- Produit
- Client
- Employé

### Visualisation

À partir de cet entrepôt, nous avons conçu une dizaine de tableaux de bord interactifs permettant de visualiser l'évolution des ventes et les performances de l'entreprise.

### Indicateurs clés

Ces visualisations offrent des indicateurs clés pour le pilotage stratégique et opérationnel, en mettant en évidence les tendances par :
- Région
- Période
- Catégorie de produit
- Canal de vente (magasin vs e-commerce)

---

## Projet Collecte de Données Web

**Date :** Novembre 2024  
**Technologies :** Python, BeautifulSoup, Folium, API ADEME

### Objectif du projet

Développer une application Python combinant deux approches : le web scraping et l'exploitation d'une API publique, dans un contexte orienté données géographiques.

### Partie 1 : Web Scraping - Musées de France

#### Source de données
Liste des musées de France disponible sur Wikipedia.

#### Objectif
Récupérer des données géographiques et descriptives sur les musées :
- Nom
- Localisation
- Type
- Ville

#### Traitement des données
Une fois les données extraites avec BeautifulSoup, nous les avons nettoyées et organisées pour supprimer les doublons et filtrer les valeurs incomplètes.

#### Visualisation
Ces données ont ensuite été visualisées à l'aide de la bibliothèque Folium, via une carte interactive permettant de localiser les musées sur le territoire français. Un graphique complémentaire a été généré pour analyser la répartition des musées selon les régions ou les types d'établissement.

### Partie 2 : Exploitation de l'API ADEME

#### Source de données
API de l'ADEME fournissant des diagnostics de performance énergétique (DPE) pour les logements en France.

#### Fonctionnalités
Nous avons utilisé l'API pour interroger les données DPE d'une commune spécifique (ex. : Fors, code INSEE 79125) et les charger dans un DataFrame.

#### Interface utilisateur
L'application permet à l'utilisateur de saisir un nom de commune ou un code INSEE, ce qui déclenche l'affichage automatique d'une carte Folium où les logements sont représentés par des marqueurs colorés selon leur classe énergétique.

#### Analyse comparative
Un graphique de comparaison a été réalisé pour visualiser la répartition des logements par lettre de DPE dans les quatre principales villes de l'ancienne région Poitou-Charentes :
- La Rochelle
- Niort
- Poitiers
- Angoulême

#### Indicateurs
Un indicateur complémentaire a également été intégré afin de mettre en lumière la proportion de logements énergivores (classés F et G) par ville.

### Interface web
Le projet inclut enfin une interface web simple, permettant de naviguer entre les différentes fonctionnalités de manière intuitive.
