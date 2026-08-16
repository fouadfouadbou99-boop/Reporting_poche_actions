import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

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
# FONCTION UTILITAIRE
# ==================================================

def safe_get(kpi, *keys, default=0):
    for key in keys:
        if key in kpi:
            value = kpi[key]
            if pd.notna(value):
                return value
    return default

# ==================================================
# UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Charger le fichier Excel",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:

        donnees = pd.read_excel(uploaded_file, sheet_name=0)
        analyse = pd.read_excel(uploaded_file, sheet_name=1)
        filtre = pd.read_excel(uploaded_file, sheet_name=2)

        st.success("✅ Fichier chargé avec succès")

        # ==================================================
        # KPI
        # ==================================================

        analyse.columns = ["Indicateur", "Valeur"]

        kpi = dict(
            zip(
                analyse["Indicateur"],
                analyse["Valeur"]
            )
        )

        perf_port = float(
            safe_get(
                kpi,
                "Performance absolue Portefeuille"
            )
        ) * 100

        perf_indice = float(
            safe_get(
                kpi,
                "Performance absolue Indice"
            )
        ) * 100

        alpha = float(
            safe_get(
                kpi,
                "Performance relative (Alpha brut)"
            )
        ) * 100

        beta = float(
            safe_get(
                kpi,
                "Beta"
            )
        )

        correlation = float(
            safe_get(
                kpi,
                "Correlation"
            )
        )

        tracking_error = float(
            safe_get(
                kpi,
                "Tracking Error annualisé",
                "Tracking Error annualise"
            )
        ) * 100

        information_ratio = float(
            safe_get(
                kpi,
                "Ratio Information corrigé",
                "Ratio Information"
            )
        )

        hit_ratio = float(
            safe_get(
                kpi,
                "Hit Ratio"
            )
        ) * 100

        volatilite_port = float(
            safe_get(
                kpi,
                "Volatilité annualisée Portefeuille",
                "Volatilite annualisee Portefeuille"
            )
        ) * 100

        volatilite_indice = float(
            safe_get(
                kpi,
                "Volatilité annualisée Indice",
                "Volatilite annualisee Indice"
            )
        ) * 100

        # ==================================================
        # SYNTHESE
        # ==================================================

        st.header("1. Synthèse Exécutive")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Performance", f"{perf_port:.2f}%")
        c2.metric("Benchmark", f"{perf_indice:.2f}%")
        c3.metric("Alpha", f"{alpha:.2f}%")
        c4.metric("Information Ratio", f"{information_ratio:.2f}")

        c5, c6, c7 = st.columns(3)

        c5.metric("Beta", f"{beta:.2f}")
        c6.metric("Tracking Error", f"{tracking_error:.2f}%")
        c7.metric("Hit Ratio", f"{hit_ratio:.2f}%")

        # ==================================================
        # PERFORMANCE
        # ==================================================

        st.header("2. Analyse Performance")

        portefeuille = donnees.iloc[:, 1]
        benchmark = donnees.iloc[:, 3]

        base100_port = portefeuille / portefeuille.iloc[0] * 100
        base100_bench = benchmark / benchmark.iloc[0] * 100

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
        # RISQUE
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
            color="Indicateur"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

        # ==================================================
        # GESTION ACTIVE
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
        # RECOMMANDATIONS
        # ==================================================

        st.header("5. Recommandations")

        if alpha < 0:
            st.warning("Alpha négatif.")

        if information_ratio < 0:
            st.warning("Les positions actives détruisent de la valeur.")

        if tracking_error > 5:
            st.info("Surveiller le Tracking Error.")

        if beta < 1:
            st.success("Profil plutôt défensif.")

        if hit_ratio < 50:
            st.warning("Hit Ratio inférieur à 50 %.")

        # ==================================================
        # EXPORT EXCEL
        # ==================================================

        st.header("📥 Téléchargements")

        export_df = pd.DataFrame({
            "Indicateur": [
                "Performance Portefeuille",
                "Performance Benchmark",
                "Alpha",
                "Information Ratio",
                "Beta",
                "Tracking Error",
                "Hit Ratio",
                "Corrélation"
            ],
            "Valeur": [
                perf_port,
                perf_indice,
                alpha,
                information_ratio,
                beta,
                tracking_error,
                hit_ratio,
                correlation
            ]
        })

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            export_df.to_excel(
                writer,
                index=False,
                sheet_name="Reporting"
            )

        st.download_button(
            "📊 Télécharger Excel",
            excel_buffer.getvalue(),
            "Reporting_Comite_RPC.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error(
            f"Erreur lors du traitement : {str(e)}"
        )
