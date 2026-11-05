
import streamlit as st

from utils import (
    get_filtered_data,
    inject_style,
    BLEU,
    ROUGE,
    ORANGE,
    VERT
)


# --------------------------------------------------
# CHARGEMENT DES DONNÉES
# --------------------------------------------------

inject_style()

df = get_filtered_data()

st.title("Recommandations")

st.markdown(
    "Des pistes d'action commerciales et opérationnelles "
    "à partir des ventes de Plato's Pizza."
)

st.divider()


# --------------------------------------------------
# PRÉPARATION DES DONNÉES
# --------------------------------------------------

jours = {
    0: "Lundi",
    1: "Mardi",
    2: "Mercredi",
    3: "Jeudi",
    4: "Vendredi",
    5: "Samedi",
    6: "Dimanche"
}

df["jour_num"] = df["date"].dt.dayofweek
df["jour"] = df["jour_num"].map(jours)


# Agrégations principales

ca_pizza = (
    df.groupby("pizza_name")["chiffre_affaires"]
    .sum()
    .sort_values(ascending=False)
)

quantite_pizza = (
    df.groupby("pizza_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

ca_categorie = (
    df.groupby("category")["chiffre_affaires"]
    .sum()
    .sort_values(ascending=False)
)

commandes_jour = (
    df.groupby("jour")["order_id"]
    .nunique()
    .reindex(list(jours.values()))
)

commandes_heure = (
    df.groupby("heure")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

ca_taille = (
    df.groupby("size")["chiffre_affaires"]
    .sum()
    .sort_values(ascending=False)
)


# Données principales

meilleure_pizza = ca_pizza.index[0]
ca_meilleure_pizza = ca_pizza.iloc[0]

pizza_plus_vendue = quantite_pizza.index[0]
quantite_plus_vendue = quantite_pizza.iloc[0]

meilleure_categorie = ca_categorie.index[0]

jour_fort = commandes_jour.idxmax()
jour_faible = commandes_jour.idxmin()

heure_forte = commandes_heure.index[0]
heure_faible = commandes_heure.index[-1]

taille_forte = ca_taille.index[0]


# --------------------------------------------------
# 1. POINTS CLÉS
# --------------------------------------------------

st.subheader("Les points clés")

col1, col2 = st.columns(2)

col1.metric(
    "Pizza la plus vendue",
    pizza_plus_vendue
)

col2.metric(
    "Jour le plus actif",
    jour_fort
)

st.divider()


# --------------------------------------------------
# 2. RECOMMANDATIONS COMMERCIALES
# --------------------------------------------------

st.subheader("Recommandations commerciales")


# --------------------------------------------------
# RECOMMANDATION 1 : PIZZA PHARE
# --------------------------------------------------

st.markdown(
    f"""
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {BLEU};
        margin-bottom: 15px;
    ">
        <h4 style="color: {BLEU};">
            1. Mettre en avant la pizza phare
        </h4>
        <p>
            <b>Constat :</b> {pizza_plus_vendue} est la pizza
            qui enregistre le plus grand volume de ventes,
            avec {quantite_plus_vendue:,.0f} unités vendues.
        </p>
        <p>
            <b>Action :</b> la mettre en avant sur la carte,
            dans les supports de communication ou dans une
            formule déjeuner.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# RECOMMANDATION 2 : CATÉGORIE PRINCIPALE
# --------------------------------------------------

st.markdown(
    f"""
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {ROUGE};
        margin-bottom: 15px;
    ">
        <h4 style="color: {ROUGE};">
            2. Valoriser la catégorie qui génère le plus de CA
        </h4>
        <p>
            <b>Constat :</b> la catégorie {meilleure_categorie}
            génère le chiffre d'affaires le plus élevé.
        </p>
        <p>
            <b>Action :</b> créer une offre ou une communication
            autour de cette catégorie, tout en surveillant
            l'évolution des ventes des autres catégories.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# RECOMMANDATION 3 : JOUR LE PLUS CALME
# --------------------------------------------------

st.markdown(
    f"""
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {ORANGE};
        margin-bottom: 15px;
    ">
        <h4 style="color: #B7791F;">
            3. Stimuler les ventes le jour le plus calme
        </h4>
        <p>
            <b>Constat :</b> {jour_faible} est le jour qui
            enregistre le moins de commandes.
        </p>
        <p>
            <b>Action :</b> tester une offre limitée ce jour-là,
            par exemple une formule ou une promotion ciblée,
            puis comparer les résultats avec la période précédente.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 3. RECOMMANDATIONS OPÉRATIONNELLES
# --------------------------------------------------

st.subheader("Recommandations opérationnelles")


# --------------------------------------------------
# RECOMMANDATION 4 : HEURES DE POINTE
# --------------------------------------------------

st.markdown(
    f"""
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {VERT};
        margin-bottom: 15px;
    ">
        <h4 style="color: #547A32;">
            4. Adapter l'organisation aux heures de pointe
        </h4>
        <p>
            <b>Constat :</b> l'heure du midi est celle
            qui enregistre le plus de commandes.
        </p>
        <p>
            <b>Action :</b> anticiper la préparation des
            ingrédients et adapter la répartition des équipes
            autour de cette période.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# RECOMMANDATION 5 : PRÉPARATION DES PRODUITS
# --------------------------------------------------

st.markdown(
    f"""
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {BLEU};
        margin-bottom: 15px;
    ">
        <h4 style="color: {BLEU};">
            5. Ajuster la préparation des produits
        </h4>
        <p>
            <b>Constat :</b> {pizza_plus_vendue} est le produit
            le plus vendu. La taille {taille_forte} représente
            la plus grande part du chiffre d'affaires par taille.
        </p>
        <p>
            <b>Action :</b> utiliser ces tendances pour mieux
            planifier les préparations et suivre les besoins
            en ingrédients. Les données de stock réelles
            restent nécessaires pour prévoir les ruptures.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 4. PLAN D'ACTION
# --------------------------------------------------

st.divider()

st.subheader("Plan d'action")

st.markdown(
    f"""
    - Mettre en avant **{pizza_plus_vendue}**, la pizza la plus vendue.
    - Valoriser la catégorie **{meilleure_categorie}**.
    - Tester une action commerciale le **{jour_faible}**.
    - Adapter l'organisation à midi.
    - Anticiper les préparations en fonction des ventes observées.
    """
)

st.caption(
    "Les recommandations sont calculées à partir des ventes "
    "historiques. Elles constituent des pistes d'action à tester, "
    "et non des prévisions garanties."
)

st.divider()

st.caption(
    "Plato's Pizza | Recommandations"
)
