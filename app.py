import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Reporting Comité RPC",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Reporting Comité Actions RPC")

uploaded_file = st.file_uploader(
    "Charger le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    try:

        # Lecture des feuilles
        donnees = pd.read_excel(
            uploaded_file,
            sheet_name=0
        )

        analyse = pd.read_excel(
            uploaded_file,
            sheet_name=1
        )

        st.success("✅ Fichier chargé")

        # Renommage des colonnes
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
            kpi.get(
                "Performance absolue Portefeuille",
                0
            ) * 100
        )

        perf_indice = (
            kpi.get(
                "Performance absolue Indice",
                0
            ) * 100
        )

        alpha = (
            kpi.get(
                "Performance relative (Alpha brut)",
                0
            ) * 100
        )

        beta = kpi.get(
            "Beta",
            0
        )

        ir = kpi.get(
            "Ratio Information",
            0
        )

        # KPI

        st.subheader("Synthèse Exécutive")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Performance",
            f"{perf_port:.2f}%"
        )

        c2.metric(
            "Indice",
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
            "Information Ratio",
            f"{ir:.2f}"
        )

        # Base 100

        portefeuille = donnees.iloc[:,1]

        benchmark = donnees.iloc[:,3]

        base100_port = (
            portefeuille /
            portefeuille.iloc[0]
        ) * 100

        base100_bench = (
            benchmark /
            benchmark.iloc[0]
        ) * 100

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=base100_port,
                name="Portefeuille"
            )
        )

        fig.add_trace(
            go.Scatter(
                y=base100_bench,
                name="Benchmark"
            )
        )

        fig.update_layout(
            title="Evolution Base 100"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Analyse

        st.subheader(
            "Commentaire Automatique"
        )

        commentaire = f"""
Performance du portefeuille :
{perf_port:.2f} %

Performance du benchmark :
{perf_indice:.2f} %

Alpha :
{alpha:.2f} %

Beta :
{beta:.2f}

Information Ratio :
{ir:.2f}
"""

        st.info(commentaire)

        st.subheader(
            "Données"
        )

        st.dataframe(
            donnees,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Erreur : {str(e)}"
        )
