import streamlit as st
import pandas as pd
import numpy as np
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
# OUTILS
# ==================================================

def annualized_vol(returns):
    return returns.std() * np.sqrt(52)

def tracking_error(port_ret, bench_ret):
    return (port_ret - bench_ret).std() * np.sqrt(52)

def beta(port_ret, bench_ret):
    cov = np.cov(port_ret, bench_ret)[0, 1]
    var = np.var(bench_ret)
    if var == 0:
        return 0
    return cov / var

def information_ratio(port_ret, bench_ret):
    active = port_ret - bench_ret

    te = active.std() * np.sqrt(52)

    if te == 0:
        return 0

    alpha_annual = active.mean() * 52

    return alpha_annual / te

def max_drawdown(base100):
    running_max = base100.cummax()
    drawdown = base100 / running_max - 1
    return drawdown.min()

def hit_ratio(port_ret, bench_ret):
    return ((port_ret - bench_ret) > 0).mean()

# ==================================================
# UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Charger le fichier Excel",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:

        df = pd.read_excel(uploaded_file, sheet_name=0)

        st.success("✅ Fichier chargé avec succès")

        # ------------------------------------------------
        # Normalisation colonnes
        # ------------------------------------------------

        df.columns = [str(c).strip() for c in df.columns]

        date_col = df.columns[0]

        port_col = "VL_portefeuille_actions"
        bench_col = "MASI_RB"

        df[date_col] = pd.to_datetime(df[date_col])

        df = df.sort_values(date_col)

        # ------------------------------------------------
        # HORIZON
        # ------------------------------------------------

        st.sidebar.header("⚙️ Paramètres")

        horizon = st.sidebar.selectbox(
            "Horizon d'analyse",
            [
                "Depuis l'origine",
                "YTD",
                "1 mois",
                "3 mois",
                "6 mois",
                "12 mois",
                "Personnalisé"
            ]
        )

        end_date = df[date_col].max()

        if horizon == "Depuis l'origine":

            start_date = df[date_col].min()

        elif horizon == "YTD":

            start_date = pd.Timestamp(year=end_date.year,
                                      month=1,
                                      day=1)

        elif horizon == "1 mois":

            start_date = end_date - pd.DateOffset(months=1)

        elif horizon == "3 mois":

            start_date = end_date - pd.DateOffset(months=3)

        elif horizon == "6 mois":

            start_date = end_date - pd.DateOffset(months=6)

        elif horizon == "12 mois":

            start_date = end_date - pd.DateOffset(months=12)

        else:

            start_date, end_date = st.sidebar.date_input(
                "Période",
                value=(
                    df[date_col].min(),
                    df[date_col].max()
                )
            )

        df_period = df[
            (df[date_col] >= pd.to_datetime(start_date))
            &
            (df[date_col] <= pd.to_datetime(end_date))
        ].copy()

        # ------------------------------------------------
        # CALCULS
        # ------------------------------------------------

        port_base100 = (
            df_period[port_col]
            / df_period[port_col].iloc[0]
        ) * 100

        bench_base100 = (
            df_period[bench_col]
            / df_period[bench_col].iloc[0]
        ) * 100

        perf_port = (
            df_period[port_col].iloc[-1]
            /
            df_period[port_col].iloc[0]
            -
            1
        )

        perf_bench = (
            df_period[bench_col].iloc[-1]
            /
            df_period[bench_col].iloc[0]
            -
            1
        )

        alpha = perf_port - perf_bench

        port_returns = df_period[port_col].pct_change().dropna()
        bench_returns = df_period[bench_col].pct_change().dropna()

        vol_port = annualized_vol(port_returns)
        vol_bench = annualized_vol(bench_returns)

        beta_value = beta(
            port_returns,
            bench_returns
        )

        corr = port_returns.corr(
            bench_returns
        )

        te = tracking_error(
            port_returns,
            bench_returns
        )

        ir = information_ratio(
            port_returns,
            bench_returns
        )

        hit = hit_ratio(
            port_returns,
            bench_returns
        )

        mdd = max_drawdown(
            port_base100
        )

        # ==================================================
        # KPI
        # ==================================================

        st.header("1. Synthèse Exécutive")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Performance",
            f"{perf_port*100:.2f}%"
        )

        c2.metric(
            "Benchmark",
            f"{perf_bench*100:.2f}%"
        )

        c3.metric(
            "Alpha",
            f"{alpha*100:.2f}%"
        )

        c4.metric(
            "Information Ratio",
            f"{ir:.2f}"
        )

        c5, c6, c7, c8 = st.columns(4)

        c5.metric(
            "Bêta",
            f"{beta_value:.2f}"
        )

        c6.metric(
            "Tracking Error",
            f"{te*100:.2f}%"
        )

        c7.metric(
            "Hit Ratio",
            f"{hit*100:.2f}%"
        )

        c8.metric(
            "Max Drawdown",
            f"{mdd*100:.2f}%"
        )

        # ==================================================
        # PERFORMANCE
        # ==================================================

        st.header("2. Analyse Performance")

        fig_perf = go.Figure()

        fig_perf.add_trace(
            go.Scatter(
                x=df_period[date_col],
                y=port_base100,
                name="Portefeuille",
                line=dict(width=3)
            )
        )

        fig_perf.add_trace(
            go.Scatter(
                x=df_period[date_col],
                y=bench_base100,
                name="MASI RB",
                line=dict(width=3)
            )
        )

        fig_perf.update_layout(
            title=f"Evolution Base 100 - {horizon}",
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

        risk_df = pd.DataFrame({
            "Indicateur": [
                "Volatilité Portefeuille",
                "Volatilité Benchmark",
                "Tracking Error"
            ],
            "Valeur": [
                vol_port * 100,
                vol_bench * 100,
                te * 100
            ]
        })

        fig_risk = px.bar(
            risk_df,
            x="Indicateur",
            y="Valeur",
            text="Valeur"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

        # ==================================================
        # RECOMMANDATIONS
        # ==================================================

        st.header("4. Recommandations")

        if alpha < 0:
            st.warning(
                "🔴 Sous-performance par rapport au benchmark."
            )

        if ir < 0:
            st.warning(
                "🔴 Le risque actif pris n'est pas rémunéré."
            )

        if te > 0.05:
            st.info(
                "🟠 Niveau de Tracking Error à surveiller."
            )

        if beta_value < 1:
            st.success(
                "🟢 Profil défensif par rapport au marché."
            )

        if hit < 0.50:
            st.warning(
                "🔴 Faible taux de succès de gestion."
            )

        # ==================================================
        # NOTE COMITE
        # ==================================================

        st.header("5. Note au Comité")

        note = f"""
**Horizon analysé :** {horizon}

**Performance portefeuille :** {perf_port*100:.2f}%  
**Performance benchmark :** {perf_bench*100:.2f}%  
**Alpha :** {alpha*100:.2f}%  
**Information Ratio :** {ir:.2f}  
**Tracking Error :** {te*100:.2f}%  
**Bêta :** {beta_value:.2f}  
**Corrélation :** {corr:.2f}  
**Hit Ratio :** {hit*100:.2f}%  
**Maximum Drawdown :** {mdd*100:.2f}%  
"""

        st.markdown(note)

        # ==================================================
        # EXPORT
        # ==================================================

        export_df = pd.DataFrame({
            "Indicateur": [
                "Performance Portefeuille",
                "Performance Benchmark",
                "Alpha",
                "Information Ratio",
                "Bêta",
                "Tracking Error",
                "Hit Ratio",
                "Corrélation",
                "Max Drawdown"
            ],
            "Valeur": [
                perf_port,
                perf_bench,
                alpha,
                ir,
                beta_value,
                te,
                hit,
                corr,
                mdd
            ]
        })

        buffer = BytesIO()

        with pd.ExcelWriter(
            buffer,
            engine="openpyxl"
        ) as writer:

            export_df.to_excel(
                writer,
                sheet_name="Reporting",
                index=False
            )

        st.download_button(
            "📥 Télécharger les KPI",
            buffer.getvalue(),
            file_name="Reporting_RPC.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error(
            f"Erreur : {str(e)}"
        )
