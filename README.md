# Reporting Comité Actions RPC

Application Streamlit permettant :

- Chargement d'un fichier Excel
- Analyse de performance
- Analyse du risque
- Analyse de la gestion active
- Calcul du Tracking Error
- Calcul du Ratio d'Information
- Export Excel
- Export PDF

## Installation

pip install streamlit pandas plotly openpyxl reportlab

## Lancement

streamlit run app.py

## Structure du fichier Excel

### Feuille 1 : Donnees

Historique des VL portefeuille et benchmark.

### Feuille 2 : Analyse

Indicateurs calculés :

- Performance absolue Portefeuille
- Performance absolue Indice
- Alpha
- Beta
- Correlation
- Tracking Error annualise
- Ratio Information
- Hit Ratio
- Volatilite annualisee Portefeuille
- Volatilite annualisee Indice

### Feuille 3 : Filtre

Série des Active Returns.

## Formule du Ratio d'Information

Information Ratio =
Alpha annualisé / Tracking Error annualisé

Exemple :

Alpha annualisé = -14,58 %

Tracking Error annualisé = 4,05 %

Information Ratio = -3,60
