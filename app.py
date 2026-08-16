import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Configuration de la page
# -----------------------------
st.set_page_config(
    page_title="Reporting Comité RPC",
    layout="wide"
)

st.title("📊 Reporting Comité RPC")

# -----------------------------
# Upload fichier Excel
# -----------------------------
uploaded_file = st.file_uploader(
    "Choisir le fichier Excel",
    type=["xlsx"]
)

# -----------------------------
# Traitement
# -----------------------------
if uploaded_file is not None:

    try:

        # Lecture des feuilles
        indicateurs = pd.read_excel(
            uploaded_file,
            sheet_name=0
        )

        data = pd.read_excel(
            uploaded_file,
            sheet_name=2
        )

        st.success("✅ Fichier chargé avec succès")

        # Renommer les colonnes
        indicateurs.columns = ["Indicateur", "Valeur"]

        # Création dictionnaire indicateurs
        indicateurs_dict = dict(
            zip(
                indicateurs["Indicateur"],
                indicateurs["Valeur"]
            )
        )

        # Extraction des KPI
        perf_portefeuille = indicateurs_dict.get(
            "Performance Portefeuille", 0
        )

        perf_indice = indicateurs_dict.get(
            "Performance Indice", 0
        )

        alpha = indicateurs_dict.get(
            "Alpha", 0
        )

        beta = indicateurs_dict.get(
            "Bêta", 0
        )

        info_ratio = indicateurs_dict.get(
            "Information Ratio", 0
        )

        # -----------------------------
        # KPI
        # -----------------------------
        st.subheader("Indicateurs Clés")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Performance Portefeuille",
            f"{perf_portefeuille:.2%}"
        )

        col2.metric(
            "Performance Indice",
            f"{perf_indice:.2%}"
        )

        col3.metric(
            "Alpha",
            f"{alpha:.2%}"
        )

        col4.metric(
            "Bêta",
            f"{beta:.2f}"
        )

        col5.metric(
            "Information Ratio",
            f"{info_ratio:.2f}"
        )

        # -----------------------------
        # Analyse automatique
        # -----------------------------
        st.subheader("Analyse automatique")

        commentaire = ""

        if alpha > 0:
            commentaire += (
                "✅ Le portefeuille surperforme "
                "son benchmark.\n\n"
            )
        else:
            commentaire += (
                "⚠️ Le portefeuille sous-performe "
                "son benchmark.\n\n"
            )

        if beta < 1:
            commentaire += (
                "✅ Le portefeuille présente "
                "un profil défensif.\n\n"
            )
        else:
            commentaire += (
                "⚠️ Le portefeuille est plus "
                "risqué que le marché.\n\n"
            )

        if info_ratio > 0:
            commentaire += (
                "✅ La gestion active crée "
                "de la valeur.\n\n"
            )
        else:
            commentaire += (
                "⚠️ La gestion active ne crée "
                "pas de valeur.\n\n"
            )

        st.write(commentaire)

        # -----------------------------
        # Vérification données
        # -----------------------------
        st.subheader("Graphique de performance")

        cols = list(data.columns)

        st.write("Colonnes détectées :")
        st.write(cols)

        portefeuille_col = None
        benchmark_col = None

        for col in cols:

            if "VL" in str(col):
                portefeuille_col = col

            if "MAISI" in str(col):
                benchmark_col = col

        if portefeuille_col and benchmark_col:

            portefeuille = data[portefeuille_col]

            benchmark = data[benchmark_col]

            portefeuille_base100 = (
                portefeuille
                / portefeuille.iloc[0]
            ) * 100

            benchmark_base100 = (
                benchmark
                / benchmark.iloc[0]
            ) * 100

            fig, ax = plt.subplots(
                figsize=(10, 5)
            )

            ax.plot(
                portefeuille_base100,
                label="Portefeuille",
                linewidth=2
            )

            ax.plot(
                benchmark_base100,
                label="Benchmark",
                linewidth=2
            )

            ax.set_title(
                "Evolution Base 100"
            )

            ax.legend()

            st.pyplot(fig)

        else:

            st.warning(
                "Impossible de détecter "
                "les colonnes Portefeuille "
                "et Benchmark."
            )

        # -----------------------------
        # Tableau des données
        # -----------------------------
        st.subheader("Aperçu des données")

        st.dataframe(data)

    except Exception as e:

        st.error(
            f"Erreur lors de la lecture du fichier : {e}"
        )
