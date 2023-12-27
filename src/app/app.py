import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import numpy as np
import json
from collections import Counter
import seaborn as sns
import os
import sys
import time

# Chemin absolu actuel de main_streamlit.py
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
# Construire le chemin vers le dossier 'python' en utilisant le chemin relatif
chemin_python = os.path.join(chemin_actuel, '..', 'python')
# Ajouter le chemin au système PYTHONPATH
sys.path.append(chemin_python)

# Vous pouvez maintenant importer des modules de 'python'
from web_scraping import main_web_scraping



def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def afficher_accueil():
    job_name = "Data"
    st.write("Key Word : ",job_name)

    # Création d'une mise en page en utilisant des colonnes pour aligner les boutons côte à côte
    col1, col2 = st.columns(2)


    # Dans la première colonne, ajoutez un bouton pour "Par défaut"
    if col1.button("Par défaut"):
        afficher_carte_par_defaut()

    # Dans la deuxième colonne, ajoutez un bouton pour "Département"
    if col2.button("Département"):
        afficher_carte_departement()



def afficher_carte_par_defaut():

    # Affichage de la carte
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(m)

    for index, row in df.iterrows():
        if pd.notnull(row['location']) and pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            folium.Marker([row['latitude'], row['longitude']], popup=f"<b>{row['title']}</b> <br> <i>{row['compagny']}</i>",tooltip=row['title']).add_to(marker_cluster)
    
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


def afficher_carte_departement():

    # Calculez la moyenne des salaires par région
    moyenne_par_departement = df.groupby('departement')['latitude'].mean().reset_index()
    print(moyenne_par_departement)

    # Créez une carte Folium centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Définir des intervalles de couleurs basés sur les quantiles
    quantiles = np.quantile(moyenne_par_departement['latitude'], [0, 0.25, 0.5, 0.75, 1])
    colors = ['blue', 'green', 'yellow', 'orange', 'red']
    

    # Ajoutez des marqueurs pour chaque région avec la moyenne des salaires comme popup
    for index, row in moyenne_par_departement.iterrows():
        departement = row['departement']
        moyenne_salary = row['latitude']

        # Trouver la couleur correspondante basée sur le quantile
        color_idx = np.sum(moyenne_salary > quantiles)
        color = colors[color_idx]

        # Ajouter le marqueur avec la couleur appropriée
        folium.Marker(
            location=[0, 0],  # Remplacez ceci par les coordonnées GPS de chaque département si nécessaire
            popup=f"Département: {departement}<br>Moyenne Salaire: {moyenne_salary:.2f} €",
            icon=folium.Icon(color=color)
        ).add_to(m)


    # Charger le fichier GeoJSON des départements français
    with open('./departements.geojson', 'r') as f:
        geojson_data = json.load(f)

    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': 'green' if feature['properties']['NOM_DEPT'] in df['departement'].values else 'red',
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 0.5,
        }
    ).add_to(m)

    folium_static(m)



def afficher_donnees():
    st.write("Affichage des 5 premières lignes du fichier CSV :")
    st.write(df.head())


def analyse_texte():
    # Titre de la section
    st.header("Analyse de Texte Word Cloud")

    # Concaténer tous les tokens en une seule chaîne
    all_tokens = ' '.join(df['tokens'].dropna())
    
    # Générer le wordcloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_tokens)
    
    # Afficher le wordcloud à l'aide de matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Masquer les axes
    st.pyplot(plt)  # Afficher le plot dans Streamlit

    # Créer un graphique des 20 mots les plus utilisés
    from collections import Counter
    import seaborn as sns

    # Divisez les tokens pour compter leur fréquence
    mots = all_tokens.split()
    compteur = Counter(mots)

    # Sélectionnez les 20 mots les plus courants
    mots_communs = compteur.most_common(20)

    # Créer un DataFrame pour les 20 mots les plus courants
    df_mots = pd.DataFrame(mots_communs, columns=['Mot', 'Fréquence'])

    # Afficher le graphique à barres des 20 mots les plus courants
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Fréquence', y='Mot', data=df_mots, palette='viridis')
    plt.title('20 mots les plus utilisés')
    plt.xlabel('Fréquence')
    plt.ylabel('Mot')
    st.pyplot(plt)  # Afficher le plot dans Streamlit



def scrapping():
    st.header("Scrapper les emplois de votre choix sur Indeed, Glassdoor et Apec etc...")
    st.markdown(''':rainbow[ATTENTION une offre scrappée = 2 secondes, prenez un café].''')

    liste_sites = ["Apec","Indeed", "Glassdoor","Pole_Emploi", "Welcome_to_the_jungle"]
    
    sites_selectionnes = st.multiselect("Sélectionnez les sites à scrapper :", liste_sites, default=["Apec"])
    
    # Zone de texte avec une taille réduite pour entrer le métier
    job_name = st.text_area("Entrer un métier :", "exemple : data scientist", height=10)
    
    # Sélecteur numérique pour entrer le nombre d'emplois à scrapper par site
    n_jobs = st.number_input("Nombre d'emplois à scrapper par sites :", min_value=1, max_value=1000, value=30)
    
    # Bouton pour lancer le scraping
    if st.button("Scrapper les emplois"):
        st.write(f"Vous avez sélectionné les sites suivants pour le scraping : {sites_selectionnes}")
        st.write(f"Métier sélectionné : {job_name}")
        st.write(f"Nombre d'emplois à scrapper par sites : {n_jobs}")
       
        with st.spinner("Scrapping en cours..."):
            
            # Appeler votre fonction de scraping
            result = main_web_scraping(job_name,n_jobs,sites_selectionnes)
            
            # Une fois le scraping terminé, mettre à jour le message
            st.success("Scrapping terminé avec succès!")

        


def main():

    job_name = ""
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Titre de l'application
    st.title("JOBS TEXT MINNING")

    # Appliquer le style CSS pour les onglets et supprimer les puces
    st.markdown("""
    <style>
    div.stRadio > div > label {
        list-style-type: none;
    }
    div.stRadio > div > label > div {
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


df = load_data("src/data/apec.csv")

if __name__ == "__main__":
    main()

