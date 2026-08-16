import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from io import BytesIO

# ------------------------------------------------
# CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Reporting Comité RPC",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Reporting Comité Actions RPC")

# ------------------------------------------------
# UPLOAD
# ------------------------------------------------

uploaded_file = st.file_uploader(
    "Charger le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    try:

        # ----------------------------------------
        # LECTURE DONNEES
        # ----------------------------------------

        data = pd.read_excel(
            uploaded_file,
            sheet_name="Donnees"
        )

        analyse = pd.read_excel(
            uploaded_file,
            sheet_name="Analyse"
        )

        # ----------------------------------------
        # CONVERSION KPI
        # ----------------------------------------

        analyse.columns = [
            "Indicateur",
            "Valeur"
        ]

        kpi = dict(
            zip(
                analyse["Indicateur"],
                analyse["Valeur"]
            )
        )

        perf_port = (
            kpi["Performance absolue Portefeuille"]
            * 100
        )

        perf_indice = (
            kpi["Performance absolue Indice"]
            * 100
        )

        alpha = (
            kpi["Performance relative (Alpha brut)"]
            * 100
        )

        beta = kpi["Beta"]

        correlation = kpi["Correlation"]

        vol_port = (
            kpi["Volatilite annualisee Portefeuille"]
            * 100
        )

        vol_indice = (
            kpi["Volatilite annualisee Indice"]
            * 100
        )

        te = (
            kpi["Tracking Error annualise"]
            * 100
        )

        ir = kpi["Ratio Information"]

        # ----------------------------------------
        # KPI
        # ----------------------------------------

        st.subheader(
            "Synthèse Exécutive"
        )

        c1,c2,c3,c4,c5 = st.columns(5)

        c1.metric(
            "Perf Portefeuille",
            f"{perf_port:.2f}%"
        )

        c2.metric(
            "Perf Indice",
            f"{perf_indice:.2f}%"
        )

        c3.metric(
            "Alpha",
            f"{alpha:.2f}%"
        )

        c4.metric(
            "Beta",
            f"{beta:.2f}"
        )

        c5.metric(
            "Info Ratio",
            f"{ir:.2f}"
        )

        # ----------------------------------------
        # BASE 100
        # ----------------------------------------

        portefeuille = data[
            "VL_ portefeuille_actions"
        ]

        benchmark = data[
            "MAISI_RB"
        ]

        base100_portefeuille = (
            portefeuille /
            portefeuille.iloc[0]
        ) * 100

        base100_benchmark = (
            benchmark /
            benchmark.iloc[0]
        ) * 100

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=base100_portefeuille,
                name="Portefeuille"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=base100_benchmark,
                name="Indice"
            )
        )

        fig.update_layout(
            title="Evolution Base 100",
            height=600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------
        # RISQUE
        # ----------------------------------------

        st.subheader(
            "Analyse du Risque"
        )

        risk_df = pd.DataFrame({

            "Indicateur":[
                "Volatilité Portefeuille",
                "Volatilité Indice",
                "Tracking Error"
            ],

            "Valeur":[
                vol_port,
                vol_indice,
                te
            ]
        })

        fig_risk = px.bar(
            risk_df,
            x="Indicateur",
            y="Valeur",
            text="Valeur",
            color="Indicateur"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

        # ----------------------------------------
        # GESTION ACTIVE
        # ----------------------------------------

        st.subheader(
            "Gestion Active"
        )

        active_df = pd.DataFrame({

            "Indicateur":[
                "Alpha",
                "Information Ratio",
                "Correlation",
                "Beta"
            ],

            "Valeur":[
                alpha,
                ir,
                correlation,
                beta
            ]
        })

        st.dataframe(
            active_df,
            use_container_width=True
        )

        # ----------------------------------------
        # COMMENTAIRE
        # ----------------------------------------

        commentaire = f"""
Le portefeuille affiche une performance
de {perf_port:.2f} % contre
{perf_indice:.2f} % pour l'indice.

L'alpha ressort à {alpha:.2f} %,
ce qui traduit une sous-performance
relative importante.

Le bêta de {beta:.2f}
et la corrélation de
{correlation:.2f}
indiquent un profil peu sensible
aux mouvements du marché.

La volatilité du portefeuille
({vol_port:.2f} %)
est très inférieure à celle
du benchmark
({vol_indice:.2f} %).

Le Tracking Error atteint
{te:.2f} %.

L'Information Ratio ressort à
{ir:.2f},
indiquant une destruction
de valeur par la gestion active.
"""

        st.subheader(
            "Note pour le Comité"
        )

        st.info(commentaire)

        # ----------------------------------------
        # TABLEAU KPI
        # ----------------------------------------

        st.subheader("Tableau KPI")

        table = pd.DataFrame({

            "Indicateur":[
                "Performance Portefeuille",
                "Performance Indice",
                "Alpha",
                "Beta",
                "Corrélation",
                "Volatilité Portefeuille",
                "Volatilité Indice",
                "Tracking Error",
                "Information Ratio"
            ],

            "Valeur":[
                perf_port,
                perf_indice,
                alpha,
                beta,
                correlation,
                vol_port,
                vol_indice,
                te,
                ir
            ]
        })

        st.dataframe(
            table,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Erreur : {str(e)}"
        )
