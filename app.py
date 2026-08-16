pip install streamlit pandas plotly openpyxl
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Reporting Comité RPC",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Reporting Comité RPC")

uploaded_file = st.file_uploader(
    "Choisir le fichier Excel",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:

    try:
        excel_file = pd.ExcelFile(uploaded_file)

        st.success("✅ Fichier chargé avec succès")

        # ------------------------------------------------------------------
        # VALEURS DE DEMONSTRATION
        # Remplacez-les ensuite par les valeurs lues depuis Excel
        # ------------------------------------------------------------------

        performance_portefeuille = -8.57
        performance_indice = -3.17
        alpha = -5.40
        beta = 0.84
        information_ratio = -1.46
        volatilite_portefeuille = 15.56
        volatilite_indice = 17.73

        # ------------------------------------------------------------------
        # KPI
        # ------------------------------------------------------------------

        st.header("Indicateurs Clés")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Performance Portefeuille",
            f"{performance_portefeuille:.2f}%"
        )

        col2.metric(
            "Performance Indice",
            f"{performance_indice:.2f}%"
        )

        col3.metric(
            "Alpha",
            f"{alpha:.2f}%"
        )

        col4.metric(
            "Bêta",
            f"{beta:.2f}"
        )

        col5.metric(
            "Information Ratio",
            f"{information_ratio:.2f}"
        )

        st.markdown("---")

        # ------------------------------------------------------------------
        # ANALYSE AUTOMATIQUE
        # ------------------------------------------------------------------

        st.header("Analyse automatique")

        if performance_portefeuille < performance_indice:
            st.warning(
                "⚠️ Le portefeuille sous-performe son benchmark."
            )
        else:
            st.success(
                "✅ Le portefeuille surperforme son benchmark."
            )

        if beta < 1:
            st.info(
                "ℹ️ Le portefeuille présente un profil de risque inférieur au marché."
            )

        if information_ratio < 0:
            st.error(
                "❌ La gestion active n'a pas créé de valeur sur la période."
            )

        st.markdown("---")

        # ------------------------------------------------------------------
        # GRAPHIQUE PERFORMANCE
        # ------------------------------------------------------------------

        st.header("Performance Portefeuille vs Benchmark")

        df_perf = pd.DataFrame({
            "Indicateur": [
                "Portefeuille RPC",
                "Benchmark"
            ],
            "Performance": [
                performance_portefeuille,
                performance_indice
            ]
        })

        fig_perf = px.bar(
            df_perf,
            x="Indicateur",
            y="Performance",
            color="Indicateur",
            text="Performance",
            title="Comparaison des performances"
        )

        fig_perf.update_traces(
            texttemplate='%{text:.2f}%',
            textposition='outside'
        )

        st.plotly_chart(
            fig_perf,
            use_container_width=True
        )

        # ------------------------------------------------------------------
        # GRAPHIQUE VOLATILITE
        # ------------------------------------------------------------------

        st.header("Analyse du Risque")

        df_risque = pd.DataFrame({
            "Indicateur": [
                "Portefeuille",
                "Benchmark"
            ],
            "Volatilité": [
                volatilite_portefeuille,
                volatilite_indice
            ]
        })

        fig_risque = px.bar(
            df_risque,
            x="Indicateur",
            y="Volatilité",
            color="Indicateur",
            text="Volatilité",
            title="Volatilité annualisée"
        )

        fig_risque.update_traces(
            texttemplate='%{text:.2f}%',
            textposition='outside'
        )

        st.plotly_chart(
            fig_risque,
            use_container_width=True
        )

        # ------------------------------------------------------------------
        # JAUGE BETA
        # ------------------------------------------------------------------

        st.header("Sensibilité au Marché")

        fig_beta = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=beta,
                title={"text": "Bêta"},
                gauge={
                    "axis": {"range": [0, 1.5]},
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {
                            "range": [0, 1],
                            "color": "lightgreen"
                        },
                        {
                            "range": [1, 1.5],
                            "color": "salmon"
                        }
                    ]
                }
            )
        )

        st.plotly_chart(
            fig_beta,
            use_container_width=True
        )

        # ------------------------------------------------------------------
        # CONCLUSION
        # ------------------------------------------------------------------

        st.markdown("---")

        st.header("Conclusion")

        commentaire = f"""
        Le portefeuille affiche une performance de
        {performance_portefeuille:.2f}% contre
        {performance_indice:.2f}% pour son benchmark.

        L'alpha ressort à {alpha:.2f}%,
        traduisant une sous-performance relative.

        Le bêta de {beta:.2f} indique un niveau
        de risque inférieur à celui du marché.

        L'Information Ratio de {information_ratio:.2f}
        confirme que la gestion active n'a pas
        créé de valeur sur la période observée.
        """

        st.write(commentaire)

    except Exception as e:
        st.error(f"Erreur : {str(e)}")
