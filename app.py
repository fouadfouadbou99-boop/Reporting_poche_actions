import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ==================================================
# CONFIGURATION
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
    "Charger le fichier Excel",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:

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

        st.success("✅ Fichier chargé avec succès")

        # ==================================================
        # KPI
        # ==================================================

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

        perf_port = kpi.get(
            "Performance absolue Portefeuille",
            0
        ) * 100

        perf_indice = kpi.get(
            "Performance absolue Indice",
            0
        ) * 100

        alpha = kpi.get(
            "Performance relative (Alpha brut)",
            0
        ) * 100

        beta = kpi.get(
            "Beta",
            0
        )

        correlation = kpi.get(
            "Correlation",
            0
        )

        tracking_error = kpi.get(
            "Tracking Error annualise",
            0
        ) * 100

        information_ratio = kpi.get(
            "Ratio Information",
            0
        )

        hit_ratio = kpi.get(
            "Hit Ratio",
            0
        ) * 100

        volatilite_port = kpi.get(
            "Volatilite annualisee Portefeuille",
            0
        ) * 100

        volatilite_indice = kpi.get(
            "Volatilite annualisee Indice",
            0
        ) * 100

        # ==================================================
        # 1. SYNTHESE EXECUTIVE
        # ==================================================

        st.header("1. Synthèse Exécutive")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Performance",
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
            "Information Ratio",
            f"{information_ratio:.2f}"
        )

        c5, c6, c7 = st.columns(3)

        c5.metric(
            "Beta",
            f"{beta:.2f}"
        )

        c6.metric(
            "Tracking Error",
            f"{tracking_error:.2f}%"
        )

        c7.metric(
            "Hit Ratio",
            f"{hit_ratio:.2f}%"
        )

        # ==================================================
        # 2. ANALYSE PERFORMANCE
        # ==================================================

        st.header("2. Analyse Performance")

        portefeuille = donnees.iloc[:, 1]
        benchmark = donnees.iloc[:, 3]

        base100_port = (
            portefeuille / portefeuille.iloc[0]
        ) * 100

        base100_bench = (
            benchmark / benchmark.iloc[0]
        ) * 100

        fig_perf = go.Figure()

        fig_perf.add_trace(
            go.Scatter(
                x=donnees.iloc[:, 0],
                y=base100_port,
                mode="lines",
                name="Portefeuille"
            )
        )

        fig_perf.add_trace(
            go.Scatter(
                x=donnees.iloc[:, 0],
                y=base100_bench,
                mode="lines",
                name="Benchmark"
            )
        )

        fig_perf.update_layout(
            title="Evolution Base 100",
            height=500
        )

        st.plotly_chart(
            fig_perf,
            use_container_width=True
        )

        # ==================================================
        # 3. ANALYSE RISQUE
        # ==================================================

        st.header("3. Analyse Risque")

        risque_df = pd.DataFrame({
            "Indicateur": [
                "Volatilité Portefeuille",
                "Volatilité Indice",
                "Tracking Error"
            ],
            "Valeur": [
                volatilite_port,
                volatilite_indice,
                tracking_error
            ]
        })

        fig_risk = px.bar(
            risque_df,
            x="Indicateur",
            y="Valeur",
            color="Indicateur",
            text="Valeur"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

        col_beta, col_hit = st.columns(2)

        with col_beta:

            fig_beta = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=beta,
                    title={"text": "Beta"},
                    gauge={
                        "axis": {"range": [0, 1.5]},
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

        with col_hit:

            fig_hit = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=hit_ratio,
                    title={"text": "Hit Ratio"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "steps": [
                            {
                                "range": [0, 50],
                                "color": "red"
                            },
                            {
                                "range": [50, 60],
                                "color": "orange"
                            },
                            {
                                "range": [60, 100],
                                "color": "green"
                            }
                        ]
                    }
                )
            )

            st.plotly_chart(
                fig_hit,
                use_container_width=True
            )

        # ==================================================
        # 4. GESTION ACTIVE
        # ==================================================

        st.header("4. Gestion Active")

        active_df = pd.DataFrame({
            "Indicateur": [
                "Alpha",
                "Information Ratio",
                "Beta",
                "Corrélation",
                "Hit Ratio"
            ],
            "Valeur": [
                alpha,
                information_ratio,
                beta,
                correlation,
                hit_ratio
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
                nbins=15,
                title="Distribution des Active Returns"
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
                "🔴 Revoir la sélection des titres afin d'améliorer l'Alpha."
            )

        if information_ratio < 0:
            recommandations.append(
                "🔴 Les positions actives détruisent de la valeur."
            )

        if tracking_error > 5:
            recommandations.append(
                "🟠 Surveiller le niveau de risque actif."
            )

        if beta < 1:
            recommandations.append(
                "🟢 Le portefeuille conserve un profil défensif."
            )

        if hit_ratio < 50:
            recommandations.append(
                "🔴 Le Hit Ratio est insuffisant."
            )

        for ligne in recommandations:
            st.write(ligne)

        # ==================================================
        # NOTE COMITE
        # ==================================================

        st.header("Note au Comité")

        st.info(
            f"""
Performance du portefeuille : {perf_port:.2f} %

Performance benchmark : {perf_indice:.2f} %

Alpha : {alpha:.2f} %

Information Ratio : {information_ratio:.2f}

Tracking Error : {tracking_error:.2f} %

Beta : {beta:.2f}

Hit Ratio : {hit_ratio:.2f} %
"""
        )

    except Exception as e:

        st.error(
            f"Erreur lors du traitement : {e}"
        )
