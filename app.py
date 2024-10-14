# Fichier: app.py

import streamlit as st
import pandas as pd
from streamlit_apex_charts import st_apex_charts
import base64
from io import BytesIO
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Outil de Visualisation et de Génération de Graphiques")

# Sélection du type de graphique
st.subheader("Sélectionnez le type de graphique")
chart_type = st.selectbox(
    "Type de graphique",
    options=["line", "bar", "area"],
    index=0
)

# Section pour la saisie de données
st.subheader("Entrez vos données")

# Noms des colonnes
columns = st.text_input("Entrez les noms des colonnes (séparés par des virgules)", "X,Y")

# Séparer les colonnes
column_list = [col.strip() for col in columns.split(",")]

# Table input (les données peuvent être saisies par l'utilisateur)
data_input = st.text_area("Entrez les données (séparées par des virgules et des retours à la ligne)", "1,2\n3,4")

# Conversion des données saisies en DataFrame
data_lines = data_input.split("\n")
data_list = [line.split(",") for line in data_lines]
df = pd.DataFrame(data_list, columns=column_list)

# Affichage des données sous forme de tableau
st.subheader("Vos données")
st.dataframe(df)

# Visualisation avec ApexCharts
st.subheader("Visualisation des données avec ApexCharts")

# Préparer les données pour le graphique
if len(column_list) >= 2 and not df.empty:
    x_values = df[column_list[0]].astype(str).tolist()  # Axe X
    y_values = df[column_list[1]].astype(float).tolist()  # Axe Y

    # Options pour le graphique ApexCharts
    options = {
        "chart": {"type": chart_type},
        "series": [{
            "name": "Series 1",
            "data": y_values  # Données de l'axe Y
        }],
        "xaxis": {
            "categories": x_values  # Données de l'axe X
        }
    }

    # Afficher le graphique
    st_apex_charts(options)

    # Télécharger le graphique au format PNG
    st.subheader("Télécharger le graphique")
    
    def download_image():
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, marker='o')
        ax.set_xlabel(column_list[0])
        ax.set_ylabel(column_list[1])
        ax.set_title(f"Graphique {chart_type.capitalize()}")

        # Sauvegarder l'image en mémoire sous forme PNG
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        return buf

    image_buf = download_image()

    # Convertir l'image en base64 pour permettre le téléchargement
    b64 = base64.b64encode(image_buf.read()).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="chart.png">Télécharger le graphique en PNG</a>'
    st.markdown(href, unsafe_allow_html=True)
