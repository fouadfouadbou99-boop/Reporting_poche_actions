import streamlit as st
import pandas as pd
import ma*plotlib.pyplot as plt

st.set_page*config(
    page_title="Reporting *omité RPC",
    layout="wide"
)

s*.title("📊 Reporting Comité RPC")
*uploaded_file = st.file_uploader(
*   "Choisir le fichier Excel",
   *type=["xlsx"]
)

if uploaded_file:*
    xls = pd.ExcelFile(uploaded_f*le)

    indicateurs = pd.read_exc*l(
        uploaded_file,
        *heet_name=0
    )

    data = pd.r*ad_excel(
        uploaded_file,
 *      sheet_name=2
    )

    st.s*ccess("Fichier chargé avec succès"*

    # -------------------------
*   # KPI
    # -------------------*-----

    indicateurs.columns = ["Indicateur", "Valeur"]

    perf_p*rtefeuille = float(
        indica*eurs.loc[
            indicateurs["Indicateur"] ==
            "Performance Portefeuille",
            "Valeur"
        ].iloc[0]
    )

    perf_indice = float(
        indicateurs.loc[
            indicateurs["Indicateur"] ==
            "Performance Indice",
            "Valeur"
        ].iloc[0]
    )

    alpha = float(
        indicateurs.loc[
            indicateurs["Indicateur"] ==
            "Alpha",
            "Valeur"
        ].iloc[0]
    )

    beta = float(
        indicateurs.loc[
            indicateurs["Indicateur"] ==
            "Bêta",
            "Valeur"
        ].iloc[0]
    )

    info_ratio = float(
        indicateurs.loc[
            indicateurs["Indicateur"] ==
            "Information Ratio",
            "Valeur"
        ].iloc[0]
    )

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

    st.divider()

    # -------------------------
    # Commentaire automatique
    # -------------------------

    st.subheader("Analyse automatique")

    commentaire = []

    if alpha > 0:
        commentaire.append(
            "✅ Le portefeuille surperforme son benchmark."
        )
    else:
        commentaire.append(
            "⚠️ Le portefeuille sous-performe son benchmark."
        )

    if beta < 1:
        commentaire.append(
            "✅ Le portefeuille présente un profil défensif."
        )
    else:
        commentaire.append(
            "⚠️ Le portefeuille est plus risqué que le marché."
        )

    if info_ratio > 0:
        commentaire.append(
            "✅ Les décisions actives créent de la valeur."
        )
    else:
        commentaire.append(
            "⚠️ La gestion active ne crée pas de valeur."
        )

    for ligne in commentaire:
        st.write(ligne)

    st.divider()

    # -------------------------
    # Graphique
    # -------------------------

    st.subheader("Evolution Portefeuille vs Marché")

    portefeuille = data["VL_ portefeuille_actions"]

    benchmark = data["MAISI_RB"]

    portefeuille_base100 = (
        portefeuille /
        portefeuille.iloc[0]
    ) * 100

    benchmark_base100 = (
        benchmark /
        benchmark.iloc[0]
    ) * 100

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        portefeuille_base100,
        label="Portefeuille"
    )

    ax.plot(
        benchmark_base100,
        label="Benchmark"
    )

    ax.set_title(
        "Evolution base 100"
    )

    ax.legend()

    st.pyplot(fig)

    st.divider()

    st.subheader("Données utilisées")

    st.dataframe(data)
