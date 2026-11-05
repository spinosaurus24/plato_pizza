
from pathlib import Path
import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "pizza_sales.db"

TAILLES = ["Toutes", "S", "M", "L", "XL", "XXL"]

BLEU = "#173B70"
ROUGE = "#D52B35"
ORANGE = "#E9A64A"
VERT = "#83A85B"

FOND = "#F4F5F7"

POLICE_TITRES = "Montserrat"
POLICE_TEXTE = "Inter"

PALETTE = [
    BLEU,
    ROUGE,
    ORANGE,
    VERT,
    "#8B78A8",
    "#D98762"
]


# --------------------------------------------------
# CHARGEMENT DES DONNÉES
# --------------------------------------------------

@st.cache_data
def load_data():

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT * FROM vue_ventes",
            conn
        )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    ).fillna(0)

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    ).fillna(0)

    df["chiffre_affaires"] = pd.to_numeric(
        df["chiffre_affaires"],
        errors="coerce"
    ).fillna(0)

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["heure"] = pd.to_numeric(
        df["time"].astype(str).str.extract(
            r"(\d{1,2})",
            expand=False
        ),
        errors="coerce"
    )

    df["size"] = (
        df["size"]
        .astype(str)
        .str.upper()
    )

    return df.dropna(
        subset=["date", "heure"]
    )


# --------------------------------------------------
# STYLE GÉNÉRAL
# --------------------------------------------------

def inject_style():

    st.markdown(
        """
        <style>

        /* IMPORTATION DES POLICES */

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@400;500;600;700;800&display=swap');


        /* POLICE GÉNÉRALE */

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: #F4F5F7;
            font-family: 'Inter', sans-serif;
        }


        /* TITRES */

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif !important;
            color: #173B70;
            font-weight: 600;
        }

        h1 {
            font-weight: 800;
            letter-spacing: -1px;
        }

        h2 {
            font-weight: 700;
        }

        h3 {
            font-weight: 600;
        }


        /* TEXTES ET PARAGRAPHES */

        p, li, label, span {
            font-family: 'Inter', sans-serif;
        }


        /* INDICATEURS */

        [data-testid="stMetric"] {
            background-color: white;
            border: 1px solid #E7EAF0;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }

        [data-testid="stMetricLabel"] {
            color: #65738A;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
        }

        [data-testid="stMetricValue"] {
            color: #173B70;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
        }


        /* MENU LATÉRAL */

        [data-testid="stSidebar"] {
            background-color: white;
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            font-family: 'Montserrat', sans-serif !important;
        }


        /* FILTRES */

        [data-testid="stSelectSlider"],
        [data-testid="stSelectbox"] {
            font-family: 'Inter', sans-serif;
        }


        /* GRAPHIQUES */

        div[data-testid="stPlotlyChart"] {
            background-color: white;
            border-radius: 12px;
            padding: 8px;
        }


        /* BOUTONS */

        button, [data-testid="stBaseButton"] {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600;
        }


        /* CAPTIONS */

        [data-testid="stCaptionContainer"] {
            font-family: 'Inter', sans-serif;
            color: #65738A;
        }


        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# FILTRE COMMUN AUX DEUX PAGES
# --------------------------------------------------

def get_filtered_data():

    df = load_data()

    st.sidebar.markdown("## Filtres")
    st.sidebar.markdown("**Taille des pizzas**")

    taille = st.sidebar.select_slider(
        "Sélectionner une taille",
        options=TAILLES,
        value="Toutes",
        key="pizza_size_filter"
    )

    if taille != "Toutes":
        df = df[df["size"] == taille]

    st.sidebar.caption(
        f"{len(df):,} lignes de vente".replace(",", " ")
    )

    return df


# --------------------------------------------------
# STYLE DES GRAPHIQUES
# --------------------------------------------------

def style_chart(fig, height=340):

    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Montserrat, Inter, sans-serif",
            color=BLEU
        ),
        margin=dict(
            t=65,
            b=45,
            l=35,
            r=35
        ),
        title_font=dict(
            family="Montserrat, sans-serif",
            size=17,
            color=BLEU
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_color=BLEU,
            font_family="Inter, sans-serif"
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E9EDF2",
        zeroline=False,
        tickfont=dict(
            family="Inter, sans-serif"
        )
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        tickfont=dict(
            family="Inter, sans-serif"
        )
    )

    return fig


# --------------------------------------------------
# CAMEMBERT : CA PAR CATÉGORIE
# --------------------------------------------------

def pizza_pie(df, labels_col, values_col, title):

    donnees = (
        df.groupby(labels_col)[values_col]
        .sum()
        .reset_index()
        .sort_values(
            values_col,
            ascending=False
        )
    )

    fig = go.Figure(
        go.Pie(
            labels=donnees[labels_col],
            values=donnees[values_col],
            hole=0,
            marker=dict(
                colors=PALETTE,
                line=dict(
                    color="white",
                    width=4
                )
            ),
            textinfo="label+percent",
            textposition="inside",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Chiffre d'affaires : $%{value:,.2f}<br>"
                "Part : %{percent}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=title,
        showlegend=False
    )

    return style_chart(fig, 360)


# --------------------------------------------------
# LOLLIPOP : TOP 10 PAR CHIFFRE D'AFFAIRES
# --------------------------------------------------

def lollipop_chart(
    df,
    category_col,
    value_col,
    title,
    color=ROUGE,
    height=400
):

    donnees = (
        df.groupby(category_col)[value_col]
        .sum()
        .nlargest(10)
        .sort_values(ascending=True)
        .reset_index()
    )

    # Création de segments horizontaux indépendants

    x_lignes = []
    y_lignes = []

    for _, ligne in donnees.iterrows():

        x_lignes.extend([
            0,
            ligne[value_col],
            None
        ])

        y_lignes.extend([
            ligne[category_col],
            ligne[category_col],
            None
        ])

    fig = go.Figure()

    # Tiges horizontales

    fig.add_trace(
        go.Scatter(
            x=x_lignes,
            y=y_lignes,
            mode="lines",
            line=dict(
                color="#D9E0EA",
                width=3
            ),
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Points rouges

    fig.add_trace(
        go.Scatter(
            x=donnees[value_col],
            y=donnees[category_col],
            mode="markers",
            marker=dict(
                color=color,
                size=13
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Chiffre d'affaires : $%{x:,.2f}"
                "<extra></extra>"
            ),
            showlegend=False
        )
    )

    fig.update_layout(
        title=title,
        showlegend=False,
        xaxis_title="Chiffre d'affaires ($)",
        yaxis_title="",
        yaxis=dict(
            categoryorder="array",
            categoryarray=donnees[category_col].tolist()
        )
    )

    return style_chart(fig, height)


# --------------------------------------------------
# TREEMAP : CA PAR TAILLE
# --------------------------------------------------

def treemap_chart(df, labels_col, values_col, title):

    donnees = (
        df.groupby(labels_col)[values_col]
        .sum()
        .reset_index()
        .sort_values(
            values_col,
            ascending=False
        )
    )

    fig = go.Figure(
        go.Treemap(
            labels=donnees[labels_col],
            parents=[""] * len(donnees),
            values=donnees[values_col],
            marker=dict(
                colors=PALETTE,
                line=dict(
                    color="white",
                    width=3
                )
            ),
            textinfo="label+percent root",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Chiffre d'affaires : $%{value:,.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(title=title)

    return style_chart(fig, 360)


# --------------------------------------------------
# POLAIRE : COMMANDES PAR JOUR
# --------------------------------------------------

def polar_chart(
    donnees,
    category_col,
    value_col,
    title
):

    fig = go.Figure(
        go.Barpolar(
            r=donnees[value_col],
            theta=donnees[category_col],
            marker=dict(
                color=PALETTE,
                line=dict(
                    color="white",
                    width=2
                )
            ),
            hovertemplate=(
                "<b>%{theta}</b><br>"
                "Commandes : %{r:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=title,
        polar=dict(
            bgcolor="white",
            radialaxis=dict(
                showgrid=True,
                gridcolor="#E9EDF2"
            )
        )
    )

    return style_chart(fig, 360)


# --------------------------------------------------
# CA ET COMMANDES PAR HEURE
# --------------------------------------------------

def hourly_combo_chart(df):

    donnees = (
        df.groupby("heure")
        .agg(
            chiffre_affaires=(
                "chiffre_affaires",
                "sum"
            ),
            commandes=(
                "order_id",
                "nunique"
            )
        )
        .reset_index()
        .sort_values("heure")
    )

    fig = go.Figure()

    # Barres : chiffre d'affaires

    fig.add_trace(
        go.Bar(
            x=donnees["heure"],
            y=donnees["chiffre_affaires"],
            name="Chiffre d'affaires",
            marker_color=BLEU,
            hovertemplate=(
                "Heure : %{x}h<br>"
                "CA : $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )

    # Courbe : nombre de commandes

    fig.add_trace(
        go.Scatter(
            x=donnees["heure"],
            y=donnees["commandes"],
            name="Nombre de commandes",
            mode="lines+markers",
            line=dict(
                color=ROUGE,
                width=3
            ),
            marker=dict(size=8),
            yaxis="y2",
            hovertemplate=(
                "Heure : %{x}h<br>"
                "Commandes : %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Chiffre d'affaires et commandes par heure",
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Montserrat, Inter, sans-serif",
            color=BLEU
        ),
        margin=dict(
            t=75,
            b=50,
            l=65,
            r=75
        ),
        xaxis=dict(
            title="Heure",
            tickmode="linear",
            dtick=1,
            tickfont=dict(family="Inter, sans-serif")
        ),
        yaxis=dict(
            title="Chiffre d'affaires ($)",
            rangemode="tozero",
            tickfont=dict(family="Inter, sans-serif")
        ),
        yaxis2=dict(
            title="Nombre de commandes",
            overlaying="y",
            side="right",
            rangemode="tozero",
            tickfont=dict(family="Inter, sans-serif")
        ),
        legend=dict(
            orientation="h",
            y=1.15,
            x=0,
            font=dict(family="Inter, sans-serif")
        ),
        title_font=dict(
            family="Montserrat, sans-serif",
            size=17,
            color=BLEU
        )
    )

    return fig


# --------------------------------------------------
# PRIX MOYEN PAR CATÉGORIE
# --------------------------------------------------

def average_price_chart(df):

    pizzas_uniques = df[
        [
            "pizza_name",
            "category",
            "size",
            "price"
        ]
    ].drop_duplicates()

    donnees = (
        pizzas_uniques.groupby("category")["price"]
        .mean()
        .sort_values()
        .reset_index()
    )

    fig = go.Figure(
        go.Bar(
            x=donnees["price"],
            y=donnees["category"],
            orientation="h",
            marker_color=ORANGE,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Prix moyen : $%{x:.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Prix moyen par catégorie",
        xaxis_title="Prix moyen ($)",
        yaxis_title=""
    )

    return style_chart(fig, 360)
