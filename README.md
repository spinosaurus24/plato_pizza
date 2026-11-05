# Plato's Pizza — Dashboard d'analyse des ventes

## Présentation du projet

Ce projet consiste à concevoir un tableau de bord interactif avec **Python et Streamlit**, afin d'analyser les ventes de Plato's Pizza.

L'objectif est de transformer les données commerciales en indicateurs visuels pour mieux comprendre les performances de l'activité et identifier des pistes d'amélioration commerciales et opérationnelles.

## Fonctionnalités

Le dashboard est organisé en trois pages :

### Page 1 — Tableau de bord
- Présentation des principaux indicateurs de vente.
- Suivi du chiffre d'affaires.
- Nombre de commandes et quantités vendues.
- Panier moyen.
- Visualisation synthétique des performances.

### Page 2 — Analyse détaillée
- Analyse des ventes par catégorie de pizzas.
- Classement des pizzas selon leur chiffre d'affaires.
- Analyse des ventes par taille.
- Répartition des commandes selon les jours de la semaine.
- Analyse de l'activité selon les heures.

### Page 3 — Recommandations
- Identification des produits les plus vendus.
- Mise en évidence des catégories les plus performantes.
- Recommandations commerciales.
- Recommandations opérationnelles.
- Proposition d'un plan d'action fondé sur les ventes historiques.

## Technologies utilisées

- **Python** : traitement des données et logique de l'application.
- **Streamlit** : création du dashboard interactif.
- **Pandas** : manipulation et analyse des données.
- **Plotly** : création des visualisations interactives.
- **SQLite** : stockage et interrogation des données avec SQL.
- **CSS** : personnalisation de l'interface et de la typographie.

## Structure du projet

```text
plato_pizza/
│
├── app.py
├── utils.py
├── pizza_sales.db
├── requirements.txt
├── README.md
│
└── pages/
    ├── 2_Analyse_detaillee.py
    └── 3_Recommandations.py
```

## Installation et lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/spinosaurus24/plato_pizza.git
cd plato_pizza
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer l'application

```bash
streamlit run app.py
```

## Déploiement

L'application est destinée à être déployée sur **Streamlit Community Cloud**, directement depuis le dépôt GitHub.

## À propos des données

Les analyses et recommandations reposent sur les données historiques de ventes disponibles dans la base SQLite.

Les recommandations constituent des pistes d'action à tester. Les données ne contiennent pas d'informations détaillées sur les coûts des ingrédients ou les stocks réels.

---

Projet réalisé dans le cadre d'un travail d'analyse et de visualisation de données.