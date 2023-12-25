import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

st.set_option('deprecation.showPyplotGlobalUse', False)

# Fonction pour afficher l'accueil
def afficher_accueil():
    st.write("Key Word : Data")
    df = load_data("src/data/concatenated_data_with_coordinates.csv")

    # Affichage de la carte
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(m)

    for index, row in df.iterrows():
        if pd.notnull(row['location']):
            folium.Marker([row['latitude'], row['longitude']], popup=f"<b>{row['title']}</b>",tooltip=row['title']).add_to(marker_cluster)
    
    folium_static(m)

    # Utilisez une balise HTML pour séparer la carte des informations
    st.markdown("---")
    
    # Affichage des informations
    st.write("<h2>Informations du marqueur sélectionné</h2>", unsafe_allow_html=True)
    marker_info = st.empty()  # Élément pour afficher les informations du marqueur

    # Code JavaScript pour mettre à jour les informations lorsque vous cliquez sur un marqueur
    js_code = """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const markers = document.querySelectorAll('.leaflet-marker-icon');
            markers.forEach(marker => {
                marker.addEventListener('click', function() {
                    const title = marker.alt;
                    const infoDiv = document.querySelector('#marker_info');
                    infoDiv.innerHTML = "<h2>Informations du marqueur sélectionné</h2><p>" + title + "</p>";
                });
            });
        });
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# Fonction pour afficher les données
def afficher_donnees():
    # Read the CSV file
    df = pd.read_csv("../data/apec.csv")

    # Afficher les 5 premières lignes du CSV
    st.write("Affichage des 5 premières lignes du fichier CSV :")
    st.write(df.head())

# Fonction pour l'analyse de texte
def analyse_texte():
    # Titre de la section
    st.header("Analyse de Texte Word Cloud")

    # Zone de texte pour saisir le texte
    texte_utilisateur = st.text_area("Collez votre texte ici :", "Votre texte ici...")

    # Bouton pour lancer l'analyse
    if st.button("Analyser le texte"):
        mots = texte_utilisateur.split()
        df_mots = pd.Series(mots).value_counts().reset_index()
        df_mots.columns = ['Mot', 'Fréquence']

        # Affichage de la table avec la fréquence des mots
        st.write("### Fréquence des Mots")
        st.table(df_mots)

        # Word cloud
        st.write("### Nuage de Mots")
        nuage_mots = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(df_mots.set_index('Mot').to_dict()['Fréquence'])
        plt.figure(figsize=(10, 5))
        plt.imshow(nuage_mots, interpolation='bilinear')
        plt.axis('off')
        st.pyplot()

def scrapping():
    st.header("Scrapper les emplois de votre choix sur Indeed, Glassdoor et Apec")
    
    texte_utilisateur = st.text_area("Entrer un métier:", "exemple : data scientist")

    # Bouton pour lancer l'analyse
    if st.button("Analyser le texte"):
        pass



# Titre de l'application
st.title("JOBS TEXT MINNING")

# Appliquer le style CSS pour les onglets et supprimer les puces
st.markdown("""
<style>
div.stRadio > div > label {
    list-style-type: none;
}
div.stRadio > div > label > div {
    display: inline-block;
    border: 2px solid #ccc;
    padding: 8px 16px;
    margin-right: 5px;
}
</style>
""", unsafe_allow_html=True)

# Options de navigation pour les onglets
options_navigation = ["Accueil", "Afficher les données", "Analyse de Texte", "Scrapper des données"]
selected_option = st.sidebar.radio("Navigation", options_navigation)

# Contenu de l'application en fonction de l'option sélectionnée
if selected_option == "Accueil":
    afficher_accueil()
elif selected_option == "Afficher les données":
    afficher_donnees()
elif selected_option == "Analyse de Texte":
    analyse_texte()
elif selected_option == "Scrapper des données":
    scrapping()
else:
    st.write("Sélectionnez une option de navigation dans la barre latérale.")
