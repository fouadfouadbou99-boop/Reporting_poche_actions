import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Reporting Comité RPC",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Reporting Comité Actions RPC")

# ==================================================
# UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Choisir le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    try:

        # ------------------------------------------
        # LECTURE DES FEUILLES
        # ------------------------------------------

        donnees = pd.read_excel(
            uploaded_file,
            sheet_name=0
        )

        analyse = pd.read_excel(
            uploaded_file,
            sheet_name=1
        )

        filtre = pd.read_excel(
            uploaded_file,
            sheet_name=2
        )

        st.success("✅ Fichier chargé")

        # ------------------------------------------
        # KPI
        # ------------------------------------------

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

        beta = kpi.get("Beta",0)

        correlation = kpi.get(
            "Correlation",
            0
        )

        tracking_error = (
            kpi.get(
                "Tracking Error annualise",
                0
            ) * 100
        )

        information_ratio = kpi.get(
            "Ratio Information",
            0
        )

        hit_ratio = (
            kpi.get(
                "Hit Ratio",
                0
            ) * 100
        )

        volatilite_port = (
            kpi.get(
                "Volatilite annualisee Portefeuille",
                0
            ) * 100
        )

        volatilite_indice = (
            kpi.get(
                "Volatilite annualisee Indice",
                0
            ) * 100
        )

        # ==================================================
        # 1. SYNTHESE EXECUTIVE
        # ==================================================

        st.header("1. Synthèse Exécutive")

        c1,c2,c3,c4,c5,c6 = st.columns(6)

        c1.metric(
            "Perf Portefeuille",
            f"{perf_port:.2f}%"
        )

        c2.metric(
            "Benchmark",
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
            "Tracking Error",
            f"{tracking_error:.2f}%"
        )

        c6.metric(
            "Info Ratio",
            f"{information_ratio:.2f}"
        )

        # ==================================================
        # 2. ANALYSE PERFORMANCE
        # ==================================================

        st.header("2. Analyse Performance")

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

        fig_perf = go.Figure()

        fig_perf.add_trace(
            go.Scatter(
                x=donnees.iloc[:,0],
                y=base100_port,
                name="Portefeuille"
            )
        )

        fig_perf.add_trace(
            go.Scatter(
                x=donnees.iloc[:,0],
                y=base100_bench,
                name="Benchmark"
            )
        )

        fig_perf.update_layout(
            title="Evolution Base 100"
        )

        st.plotly_chart(
            fig_perf,
            use_container_width=True
        )

        # ==================================================
        # 3. ANALYSE RISQUE
        # ==================================================

        st.header("3. Analyse Risque")

        df_risque = pd.DataFrame({

            "Indicateur":[
                "Volatilité Portefeuille",
                "Volatilité Benchmark",
                "Tracking Error"
            ],

            "Valeur":[
                volatilite_port,
                volatilite_indice,
                tracking_error
            ]
        })

        fig_risk = px.bar(
            df_risque,
            x="Indicateur",
            y="Valeur",
            text="Valeur"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

        # ==================================================
        # 4. GESTION ACTIVE
        # ==================================================

        st.header("4. Gestion Active")

        active_df = pd.DataFrame({

            "Indicateur":[
                "Alpha",
                "Information Ratio",
                "Beta",
                "Corrélation"
            ],

            "Valeur":[
                alpha,
                information_ratio,
                beta,
                correlation
            ]
        })

        st.dataframe(
            active_df,
            use_container_width=True
        )

        if len(filtre.columns) > 0:

            fig_active = px.histogram(
                filtre,
                x=filtre.columns[0],
                title="Distribution Active Return"
            )

            st.plotly_chart(
                fig_active,
                use_container_width=True
            )

        # ==================================================
        # 5. RECOMMANDATIONS
        # ==================================================

        st.header("5. Recommandations")

        recommandations = []

        if alpha < 0:
            recommandations.append(
                "🔴 Revoir la sélection de titres afin d'améliorer l'alpha."
            )

        if information_ratio < 0:
            recommandations.append(
                "🔴 Réévaluer les choix de gestion active."
            )

        if tracking_error > 5:
            recommandations.append(
                "🟠 Surveiller le niveau de risque actif."
            )

        if beta < 1:
            recommandations.append(
                "🟢 Le portefeuille conserve un profil défensif."
            )

        for r in recommandations:
            st.write(r)

        # ==================================================
        # NOTE COMITE
        # ==================================================

        st.header("Note au Comité")

        st.info(
            f"""
Le portefeuille affiche une performance de {perf_port:.2f}% contre {perf_indice:.2f}% pour le benchmark.

L'alpha ressort à {alpha:.2f}% et l'Information Ratio à {information_ratio:.2f}, indiquant une sous-performance relative.

Le bêta ({beta:.2f}) et la corrélation ({correlation:.2f}) traduisent le degré de sensibilité du portefeuille au marché.

Le Tracking Error s'établit à {tracking_error:.2f}% tandis que la volatilité annualisée ressort à {volatilite_port:.2f}%.
"""
        )

    except Exception as e:

        st.error(
            f"Erreur : {e}"
        )
