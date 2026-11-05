
import streamlit as st
import plotly.express as px

from utils import (
    get_filtered_data,
    inject_style,
    style_chart,
    pizza_pie,
    lollipop_chart,
    BLEU,
    ROUGE,
    ORANGE
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Plato's Pizza",
    layout="wide"
)


# --------------------------------------------------
# PAGE 1 : VUE D'ENSEMBLE
# --------------------------------------------------

def page1():

    inject_style()

    df = get_filtered_data()

    # Titre principal
    st.markdown(
        """
        <h1 style="
            font-size: 56px;
            color: #173B70;
            font-weight: 800;
            margin-bottom: 0;
        ">
            Plato's Pizza
        </h1>
        <p style="
            font-size: 18px;
            color: #6B7280;
            margin-top: 0;
        ">
            Vue d'ensemble des ventes
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------
    # INDICATEURS CLÉS
    # --------------------------------------------------

    chiffre_affaires = df["chiffre_affaires"].sum()

    nombre_commandes = df["order_id"].nunique()

    quantite_totale = df["quantity"].sum()

    panier_moyen = (
        chiffre_affaires / nombre_commandes
        if nombre_commandes > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Chiffre d'affaires",
        f"${chiffre_affaires:,.2f}"
    )

    col2.metric(
        "Nombre de commandes",
        f"{nombre_commandes:,.0f}"
    )

    col3.metric(
        "Quantités vendues",
        f"{quantite_totale:,.0f}"
    )

    col4.metric(
        "Panier moyen",
        f"${panier_moyen:,.2f}"
    )

    st.divider()

    # --------------------------------------------------
    # CHIFFRE D'AFFAIRES MENSUEL
    # --------------------------------------------------

    df_mensuel = df.copy()

    df_mensuel["mois"] = (
        df_mensuel["date"]
        .dt.to_period("M")
        .astype(str)
    )

    ca_mensuel = (
        df_mensuel.groupby("mois")["chiffre_affaires"]
        .sum()
        .reset_index()
    )

    fig_mensuel = px.line(
        ca_mensuel,
        x="mois",
        y="chiffre_affaires",
        markers=True,
        labels={
            "mois": "Mois",
            "chiffre_affaires": "Chiffre d'affaires ($)"
        },
        title="Évolution mensuelle du chiffre d'affaires"
    )

    fig_mensuel.update_traces(
        line=dict(
            color=BLEU,
            width=3
        ),
        marker=dict(
            color=ROUGE,
            size=8
        )
    )

    st.plotly_chart(
        style_chart(fig_mensuel, 380),
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------
    # CA PAR CATÉGORIE + TOP 10 QUANTITÉS
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig_categories = pizza_pie(
            df,
            "category",
            "chiffre_affaires",
            "Chiffre d'affaires par catégorie"
        )

        st.plotly_chart(
            fig_categories,
            use_container_width=True
        )

    with col2:

        top_quantites = (
            df.groupby("pizza_name")["quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values(ascending=True)
            .reset_index()
        )

        fig_quantites = px.bar(
            top_quantites,
            x="quantity",
            y="pizza_name",
            orientation="h",
            labels={
                "quantity": "Quantités vendues",
                "pizza_name": "Pizza"
            },
            title="Top 10 des pizzas par quantité"
        )

        fig_quantites.update_traces(
            marker_color=ROUGE
        )

        st.plotly_chart(
            style_chart(fig_quantites, 400),
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------
    # TOP 10 CHIFFRE D'AFFAIRES
    # --------------------------------------------------

    fig_top_ca = lollipop_chart(
        df,
        "pizza_name",
        "chiffre_affaires",
        "Top 10 des pizzas par chiffre d'affaires"
    )

    st.plotly_chart(
        fig_top_ca,
        use_container_width=True
    )

    st.divider()

    st.caption(
        "Plato's Pizza | Vue d'ensemble"
    )


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

pages = [
    st.Page(
        page1,
        title="Page 1",
        default=True
    ),

    st.Page(
        "pages/2_Analyse_detaillee.py",
        title="Page 2"
    ),

    st.Page(
        "pages/3_Recommandations.py",
        title="Page 3"
    )
]

navigation = st.navigation(pages)

navigation.run()
