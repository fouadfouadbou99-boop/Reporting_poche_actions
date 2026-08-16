import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from io import BytesIO

from pptx import Presentation

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


# ------------------------------------------------
# PAGE
# ------------------------------------------------

st.set_page_config(
    page_title="Reporting Comité RPC",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Reporting Comité RPC")


# ------------------------------------------------
# EXPORT EXCEL
# ------------------------------------------------

def create_excel_report(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="KPI",
            index=False
        )

    output.seek(0)

    return output


# ------------------------------------------------
# EXPORT PDF
# ------------------------------------------------

def create_pdf_report(commentaire, kpi_df):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Reporting Comité RPC",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<b>Indicateurs clés</b>",
            styles["Heading2"]
        )
    )

    for _, row in kpi_df.iterrows():

        content.append(
            Paragraph(
                f"{row['Indicateur']} : {row['Valeur']}",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<b>Analyse</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            commentaire,
            styles["BodyText"]
        )
    )

    doc.build(content)

    buffer.seek(0)

    return buffer


# ------------------------------------------------
# EXPORT POWERPOINT
# ------------------------------------------------

def create_ppt(
    perf_portefeuille,
    perf_indice,
    alpha,
    beta,
    information_ratio,
):

    prs = Presentation()

    slide = prs.slides.add_slide(
        prs.slide_layouts[0]
    )

    slide.shapes.title.text = (
        "Reporting Comité RPC"
    )

    slide.placeholders[1].text = (
        f"""
Performance Portefeuille : {perf_portefeuille:.2f} %

Performance Indice : {perf_indice:.2f} %

Alpha : {alpha:.2f} %
"""
    )

    slide2 = prs.slides.add_slide(
        prs.slide_layouts[1]
    )

    slide2.shapes.title.text = (
        "Analyse du Risque"
    )

    slide2.placeholders[1].text = (
        f"""
Bêta : {beta:.2f}

Information Ratio : {information_ratio:.2f}
"""
    )

    buffer = BytesIO()

    prs.save(buffer)

    buffer.seek(0)

    return buffer


# ------------------------------------------------
# UPLOAD EXCEL
# ------------------------------------------------

uploaded_file = st.file_uploader(
    "Choisir le fichier Excel",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:

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

        performance_portefeuille = (
            indicateurs_dict.get(
                "Performance Portefeuille",
                0
            ) * 100
        )

        performance_indice = (
            indicateurs_dict.get(
                "Performance Indice",
                0
            ) * 100
        )

        alpha = (
            indicateurs_dict.get(
                "Alpha",
                0
            ) * 100
        )

        beta = indicateurs_dict.get(
            "Bêta",
            0
        )

        information_ratio = indicateurs_dict.get(
            "Information Ratio",
            0
        )

        volatilite = (
            indicateurs_dict.get(
                "Volatilité Annualisée Portefeuille",
                0
            ) * 100
        )

        tracking_error = (
            indicateurs_dict.get(
                "Tracking Error Annualisé",
                0
            ) * 100
        )

        hit_ratio = (
            indicateurs_dict.get(
                "Hit Ratio",
                0
            ) * 100
        )

        # -----------------------------------------
        # KPI
        # -----------------------------------------

        st.header("Tableau de Bord")

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

        # -----------------------------------------
        # PERFORMANCE
        # -----------------------------------------

        df_perf = pd.DataFrame({

            "Indicateur": [
                "Portefeuille",
                "Indice"
            ],

            "Valeur": [
                performance_portefeuille,
                performance_indice
            ]
        })

        fig = px.bar(
            df_perf,
            x="Indicateur",
            y="Valeur",
            color="Indicateur",
            text="Valeur",
            title="Performance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # -----------------------------------------
        # RISQUE
        # -----------------------------------------

        fig_beta = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=beta,
                title={"text": "Bêta"},
                gauge={
                    "axis": {
                        "range": [0, 1.5]
                    }
                }
            )
        )

        st.plotly_chart(
            fig_beta,
            use_container_width=True
        )

        # -----------------------------------------
        # COMMENTAIRE
        # -----------------------------------------

        commentaire = f"""
Le portefeuille affiche une performance de
{performance_portefeuille:.2f}% contre
{performance_indice:.2f}% pour le benchmark.

L'alpha ressort à {alpha:.2f}%.

Le bêta s'établit à {beta:.2f}.

L'Information Ratio est de
{information_ratio:.2f}.

Le Tracking Error ressort à
{tracking_error:.2f}%.

Le Hit Ratio est de
{hit_ratio:.2f}%.
"""

        st.subheader(
            "Commentaire automatique"
        )

        st.info(commentaire)

        # -----------------------------------------
        # TABLEAU KPI
        # -----------------------------------------

        kpi_df = pd.DataFrame({

            "Indicateur": [
                "Performance",
                "Benchmark",
                "Alpha",
                "Bêta",
                "Information Ratio",
                "Volatilité",
                "Tracking Error",
                "Hit Ratio"
            ],

            "Valeur": [
                performance_portefeuille,
                performance_indice,
                alpha,
                beta,
                information_ratio,
                volatilite,
                tracking_error,
                hit_ratio
            ]
        })

        st.dataframe(
            kpi_df,
            use_container_width=True
        )

        # -----------------------------------------
        # TELECHARGEMENTS
        # -----------------------------------------

        st.header(
            "Exports"
        )

        excel_file = create_excel_report(
            kpi_df
        )

        st.download_button(
            "📥 Télécharger Excel",
            excel_file,
            file_name="Reporting_Comite.xlsx"
        )

        pdf_file = create_pdf_report(
            commentaire,
            kpi_df
        )

        st.download_button(
            "📄 Télécharger PDF",
            pdf_file,
            file_name="Reporting_Comite.pdf"
        )

        ppt_file = create_ppt(
            performance_portefeuille,
            performance_indice,
            alpha,
            beta,
            information_ratio
        )

        st.download_button(
            "📽 Télécharger PowerPoint",
            ppt_file,
            file_name="Reporting_Comite.pptx"
        )

    except Exception as e:

        st.error(
            f"Erreur : {str(e)}"
        )
