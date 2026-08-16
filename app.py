import streamlit as st
2
import pandas as pd
3
import plotly.graph_objects as go
4
import plotly.express as px
5
from io import BytesIO
6
from reportlab.pdfgen import canvas
7
 
8
# ==================================================
9
# CONFIGURATION
10
# ==================================================
11
 
12
st.set_page_config(
13
page_title="Reporting Comité RPC",
14
page_icon="📊",
15
layout="wide"
16
)
17
 
18
st.title("📊 Reporting Comité Actions RPC")
19
 
20
# ==================================================
21
# UPLOAD
22
# ==================================================
23
 
24
uploaded_file = st.file_uploader(
25
"Charger le fichier Excel",
26
type=["xlsx"]
27
)
28
 
29
if uploaded_file is not None:
30
 
31
try:
32
 
33
donnees = pd.read_excel(uploaded_file, sheet_name=0)
34
analyse = pd.read_excel(uploaded_file, sheet_name=1)
35
filtre = pd.read_excel(uploaded_file, sheet_name=2)
36
 
37
st.success("✅ Fichier chargé avec succès")
38
 
39
# ==================================================
40
# KPI
41
# ==================================================
42
 
43
analyse.columns = ["Indicateur", "Valeur"]
44
 
45
kpi = dict(
46
zip(
47
analyse["Indicateur"],
48
analyse["Valeur"]
49
)
50
)
51
 
52
perf_port = kpi.get(
53
"Performance absolue Portefeuille",
54
0
55
) * 100
56
 
57
perf_indice = kpi.get(
58
"Performance absolue Indice",
59
0
60
) * 100
61
 
62
alpha = kpi.get(
63
"Performance relative (Alpha brut)",
64
0
65
) * 100
66
 
67
beta = kpi.get("Beta", 0)
68
 
69
correlation = kpi.get("Correlation", 0)
70
 
71
tracking_error = (
72
kpi.get(
73
"Tracking Error annualisé",
74
kpi.get(
75
"Tracking Error annualise",
76
0
77
)
78
)
79
) * 100
80
 
81
information_ratio = kpi.get(
82
"Ratio Information corrigé",
83
kpi.get(
84
"Ratio Information",
85
0
86
)
87
)
88
 
89
hit_ratio = (
90
kpi.get(
91
"Hit Ratio",
92
0
93
)
94
) * 100
95
 
96
volatilite_port = (
97
kpi.get(
98
"Volatilité annualisée Portefeuille",
99
kpi.get(
100
"Volatilite annualisee Portefeuille",
101
0
102
)
103
)
104
) * 100
105
 
106
volatilite_indice = (
107
kpi.get(
108
"Volatilité annualisée Indice",
109
kpi.get(
110
"Volatilite annualisee Indice",
111
0
112
)
113
)
114
) * 100
115
 
116
# ==================================================
117
# SYNTHESE EXECUTIVE
118
# ==================================================
119
 
120
st.header("1. Synthèse Exécutive")
121
 
122
c1, c2, c3, c4 = st.columns(4)
123
 
124
c1.metric("Performance", f"{perf_port:.2f}%")
125
c2.metric("Benchmark", f"{perf_indice:.2f}%")
126
c3.metric("Alpha", f"{alpha:.2f}%")
127
c4.metric("Information Ratio", f"{information_ratio:.2f}")
128
 
129
