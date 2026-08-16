import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

# ----------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------

st.set_page_config(
    page_title="Reporting Comité RPC",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Reporting Comité RPC")

# ----------------------------------------------------
# FONCTIONS EXPORT
# ----------------------------------------------------


def create_excel_report(kpi_df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        kpi_df.to_excel(
            writer,
            sheet_name="Reporting",
            index=False
        )

    return output.getvalue()


def create_pdf_report(commentaire):

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(pdf_buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Reporting Comité RPC",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            commentaire,
            styles["BodyText"]
        )
    )

    doc.build(content)

    pdf_buffer.seek(0)

    return pdf_buffer


# ----------------------------------------------------
# UPLOAD
# ----------------------------------------------------

uploaded_file = st.file_uploader(
    "Choisir le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    try:

        # ----------------------------------------------------
        # LECTURE EXCEL
        # ----------------------------------------------------

        indicateurs = pd.read_excel(
            uploaded_file,
            sheet_name=0
        )

        indicateurs.columns = [
            "Indicateur",
            "Valeur"
        ]

        indicateurs_dict = dict(
            zip(
                indicateurs["Indicateur"],
                indicateurs["Valeur"]
            )
        )

        # KPI

        performance_portefeuille = indicateurs_dict.get(
            "Performance Portefeuille",
            0
        ) * 100

        performance_indice = indicateurs_dict.get(
            "Performance Indice",
            0
        ) * 100

        alpha = indicateurs_dict.get(
            "Alpha",
            0
        ) * 100

        beta = indicateurs_dict.get(
            "Bêta",
            0
        )

        information_ratio = indicateurs_dict.get(
            "Information Ratio",
            0
        )

        volatilite_portefeuille = indicateurs_dict.get(
            "Volatilité Annualisée Portefeuille",
            0
        ) * 100

        volatilite_indice = indicateurs_dict.get(
            "Volatilité Annualisée Indice",
            0
        ) * 100

        tracking_error = indicateurs_dict.get(
            "Tracking Error Annualisé",
            0
        ) * 100

        hit_ratio = indicateurs_dict.get(
            "Hit Ratio",
            0
        ) * 100

        st.success(
            "✅ Fichier analysé avec succès"
        )

        # ----------------------------------------------------
        # KPI DASHBOARD
        # ----------------------------------------------------

        st.header("Indicateurs Clés")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Performance",
            f"{performance_portefeuille:.2f}%"
        )

        c2.metric(
            "Indice",
            f"{performance_indice:.2f}%"
        )

        c3.metric(
            "Alpha",
            f"{alpha:.2f}%"
        )

        c4.metric(
            "Bêta",
            f"{beta:.2f}"
        )

        c5.metric(
            "Info Ratio",
            f"{information_ratio:.2f}"
        )

        st.divider()

        # ----------------------------------------------------
        # ANALYSE
        # ----------------------------------------------------

        st.header("Analyse Automatique")

        commentaire = ""

        if alpha > 0:

            commentaire += (
                "Le portefeuille surperforme "
                "son benchmark. "
            )

        else:

            commentaire += (
                "Le portefeuille sous-performe "
                "son benchmark. "
            )

        if beta < 1:

            commentaire += (
                "Le profil de risque est "
                "plus défensif que le marché. "
            )

        else:

            commentaire += (
                "Le profil de risque est "
                "plus agressif que le marché. "
            )

        if information_ratio > 0:

            commentaire += (
                "La gestion active crée "
                "de la valeur."
            )

        else:

            commentaire += (
                "La gestion active ne crée "
                "pas de valeur."
            )

        st.info(commentaire)

        # ----------------------------------------------------
        # GRAPHIQUE PERFORMANCE
        # ----------------------------------------------------

        st.header("Performance Relative")

        df_perf = pd.DataFrame({

            "Indicateur": [
                "Portefeuille",
                "Indice"
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
            title="Performance Portefeuille vs Indice"
        )

        st.plotly_chart(
            fig_perf,
            use_container_width=True
        )

        # ----------------------------------------------------
        # RISQUE
        # ----------------------------------------------------

        st.header("Analyse du Risque")

        df_risk = pd.DataFrame({

            "Indicateur": [
                "Volatilité Portefeuille",
                "Volatilité Indice",
                "Tracking Error"
            ],

            "Valeur": [
                volatilite_portefeuille,
                volatilite_indice,
                tracking_error
            ]
        })

        fig_risk = px.bar(
            df_risk,
            x="Indicateur",
            y="Valeur",
            text="Valeur",
            color="Indicateur"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

        # ----------------------------------------------------
        # BETA
        # ----------------------------------------------------

        st.header("Sensibilité au Marché")

        fig_beta = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=beta,
                title={"text": "Bêta"},
                gauge={
                    "axis": {
                        "range": [0, 1.5]
                    },
                    "bar": {
                        "color": "darkblue"
                    },
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

        # ----------------------------------------------------
        # TABLEAU DE SYNTHESE
        # ----------------------------------------------------

        st.header("Tableau de Synthèse")

        kpi_df = pd.DataFrame({

            "Indicateur": [
                "Performance",
                "Alpha",
                "Bêta",
                "Information Ratio",
                "Volatilité",
                "Tracking Error",
                "Hit Ratio"
            ],

            "Valeur": [
                performance_portefeuille,
                alpha,
                beta,
                information_ratio,
                volatilite_portefeuille,
                tracking_error,
                hit_ratio
            ]
        })

        st.dataframe(
            kpi_df,
            use_container_width=True
        )

        # ----------------------------------------------------
        # EXPORTS
        # ----------------------------------------------------

        st.header("Téléchargements")

        excel_file = create_excel_report(
            kpi_df
        )

        st.download_button(
            label="📥 Télécharger Excel",
            data=excel_file,
            file_name="Reporting_Comite.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        pdf_file = create_pdf_report(
            commentaire
        )

        st.download_button(
            label="📄 Télécharger PDF",
            data=pdf_file,
            file_name="Reporting_Comite.pdf",
            mime="application/pdf"
        )

    except Exception as e:

        st.error(
            f"Erreur de traitement : {str(e)}"
        )
