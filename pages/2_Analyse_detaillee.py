
import streamlit as st
import plotly.express as px

from utils import (
    get_filtered_data,
    inject_style,
    style_chart,
    treemap_chart,
    polar_chart,
    hourly_combo_chart,
    average_price_chart,
    BLEU,
    ROUGE
)


# --------------------------------------------------
# CHARGEMENT DES DONNÉES
# --------------------------------------------------

inject_style()

df = get_filtered_data()


# --------------------------------------------------
# 1. HEATMAP : JOUR ET HEURE
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

heatmap_data = (
    df.pivot_table(
        index="jour",
        columns="heure",
        values="quantity",
        aggfunc="sum",
        fill_value=0
    )
    .reindex(list(jours.values()))
)

fig_heatmap = px.imshow(
    heatmap_data,
    labels={
        "x": "Heure",
        "y": "Jour",
        "color": "Quantités vendues"
    },
    color_continuous_scale=[
        "#F5E8E8",
        "#D98762",
        ROUGE,
        BLEU
    ],
    aspect="auto"
)

fig_heatmap.update_layout(
    title="Répartition des ventes par jour et par heure"
)

st.plotly_chart(
    style_chart(fig_heatmap, 420),
    use_container_width=True
)

st.divider()


# --------------------------------------------------
# 2. QUANTITÉS VENDUES + PRIX MOYEN
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    quantites_categories = (
        df.groupby("category")["quantity"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig_quantites = px.bar(
        quantites_categories,
        x="quantity",
        y="category",
        orientation="h",
        labels={
            "quantity": "Quantités vendues",
            "category": "Catégorie"
        }
    )

    fig_quantites.update_traces(
        marker_color=BLEU,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Quantités vendues : %{x:,.0f}"
            "<extra></extra>"
        )
    )

    fig_quantites.update_layout(
        title="Quantités vendues par catégorie"
    )

    st.plotly_chart(
        style_chart(fig_quantites, 360),
        use_container_width=True
    )


with col2:

    fig_prix = average_price_chart(df)

    st.plotly_chart(
        fig_prix,
        use_container_width=True
    )

st.divider()


# --------------------------------------------------
# 3. CA PAR TAILLE + COMMANDES PAR JOUR
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig_tailles = treemap_chart(
        df,
        "size",
        "chiffre_affaires",
        "Chiffre d'affaires par taille de pizza"
    )

    st.plotly_chart(
        fig_tailles,
        use_container_width=True
    )


with col2:

    commandes_jour = (
        df.groupby("jour_num")["order_id"]
        .nunique()
        .reset_index()
    )

    commandes_jour["jour"] = (
        commandes_jour["jour_num"].map(jours)
    )

    commandes_jour = commandes_jour.sort_values(
        "jour_num"
    )

    fig_jours = polar_chart(
        commandes_jour,
        "jour",
        "order_id",
        "Commandes par jour de la semaine"
    )

    # Couleurs personnalisées pour chaque jour
    couleurs_jours = {
        "Lundi": "#D52B35",
        "Mardi": "#173B70",
        "Mercredi": "#E9A64A",
        "Jeudi": "#83A85B",
        "Vendredi": "#8B78A8",
        "Samedi": "#D98762",
        "Dimanche": "#A6B4C8"
    }

    fig_jours.update_traces(
        marker=dict(
            color=[
                couleurs_jours[jour]
                for jour in commandes_jour["jour"]
            ]
        )
    )

    st.plotly_chart(
        fig_jours,
        use_container_width=True
    )

st.divider()


# --------------------------------------------------
# 4. ANALYSE HORAIRE
# --------------------------------------------------

fig_horaires = hourly_combo_chart(df)

st.plotly_chart(
    fig_horaires,
    use_container_width=True
)

st.divider()

st.caption(
    "Plato's Pizza | Analyse détaillée"
)
