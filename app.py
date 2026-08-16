import streamlit as st
import pandas as pd
i*port plotly.graph_objects as go
im*ort plotly.express as px

# ======*==================================*========
# CONFIGURATION
# =======*==================================*=======

st.set_page_config(
    p*ge_title="Reporting Comité RPC",
 *  page_icon="📊",
    layout="wide*
)

st.title("📊 Reporting Comité *ctions RPC")

# ==================*===============================
# *PLOAD
# ==========================*=======================

uploaded_*ile = st.file_uploader(
    "Charg*r le fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    try:*
        donnees = pd.read_excel(
*           uploaded_file,
        *   sheet_name=0
        )

       *analyse = pd.read_excel(
         *  uploaded_file,
            sheet*name=1
        )

        filtre =*pd.read_excel(
            uploade*_file,
            sheet_name=2
  *     )

        st.success("✅ Fich*er chargé avec succès")

        #*==================================*===============
        # KPI
    *   # =============================*====================

        anal*se.columns = [
            "Indicateur",
            "Valeur"
        ]

        kpi = dict(
           *zip(
                analyse["Indicateur"],
                analyse["Valeur"]
            )
        )

 *      perf_port = (
            kp*.get(
                "Performance*absolue Portefeuille",
           *    0
            ) * 100
        *

        perf_indice = (
        *   kpi.get(
                "Perfo*mance absolue Indice",
           *    0
            ) * 100
        *

        alpha = (
            kp*.get(
                "Performance*relative (Alpha brut)",
          *     0
            ) * 100
       *)

        beta = kpi.get(
       *    "Beta",
            0
        *

        correlation = kpi.get(
 *          "Correlation",
         *  0
        )

        tracking_er*or = (
            kpi.get(
      *         "Tracking Error annualise*,
                0
            ) * 100
        )

        informatio*_ratio = kpi.get(
            "Rat*o Information",
            0
    *   )

        hit_ratio = (
      *     kpi.get(
                "Hit*Ratio",
                0
        *   ) * 100
        )

        vola*ilite_port = (
            kpi.get*
                "Volatilite annua*isee Portefeuille",
              * 0
            ) * 100
        )

*       volatilite_indice = (
     *      kpi.get(
                "Vo*atilite annualisee Indice",
      *         0
            ) * 100
   *    )

        # =================*================================
 *      # 1. SYNTHESE EXECUTIVE
    *   # =============================*====================

        st.h*ader("1. Synthèse Exécutive")

   *    c1, c2, c3, c4 = st.columns(4)*
        c1.metric(
            "P*rformance",
            f"{perf_po*t:.2f}%"
        )

        c2.met*ic(
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
                mode="lines",
                name="Portefeuille"
            )
        )

        fig_perf.add_trace(
            go.Scatter(
                x=donnees.iloc[:,0],
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

            "Indicateur":[
                "Volatilité Portefeuille",
                "Volatilité Indice",
                "Tracking Error"
            ],

            "Valeur":[
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
                    title={"text":"Beta"},
                    gauge={
                        "axis":{"range":[0,1.5]},
                        "steps":[
                            {"range":[0,1],"color":"lightgreen"},
                            {"range":[1,1.5],"color":"salmon"}
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
                    title={"text":"Hit Ratio"},
                    gauge={
                        "axis":{"range":[0,100]},
                        "steps":[
                            {"range":[0,50],"color":"red"},
                            {"range":[50,60],"color":"orange"},
                            {"range":[60,100],"color":"green"}
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

            "Indicateur":[
                "Alpha",
                "Information Ratio",
                "Beta",
                "Corrélation",
                "Hit Ratio"
            ],

            "Valeur":[
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
                "🔴 Revoir la sélection de titres afin d'améliorer l'alpha."
            )

        if information_ratio < 0:
            recommandations.append(
                "🔴 Les paris actifs ne créent pas de valeur. Réviser le processus d'investissement."
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

        st.info(f"""
Le portefeuille affiche une performance de {perf_port:.2f}% contre {perf_indice:.2f}% pour le benchmark.

L'alpha ressort à {alpha:.2f}% et l'Information Ratio à {information_ratio:.2f}, traduisant une sous-performance relative.

Le bêta ({beta:.2f}) et la corrélation ({correlation:.2f}) reflètent le niveau d'exposition au marché.

Le Tracking Error ressort à {tracking_error:.2f}% tandis que le Hit Ratio atteint {hit_ratio:.2f}%.

Une revue de la gestion active apparaît nécessaire afin de renforcer la création de valeur relative.
""")

    except Exception as e:

        st.error(
            f"Erreur lors du traitement : {e}"
        )
