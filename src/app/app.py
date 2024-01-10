import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
from collections import Counter
import streamlit.components.v1 as components
from streamlit_option_menu.streamlit_callback import register_callback


def load_data(file_path):
    data = pd.read_csv(file_path)
    return data





def afficher_accueil():
    job_name = "Data"
    st.write("Key Word : ",job_name)

    # Création d'une mise en page en utilisant des colonnes pour aligner les boutons côte à côte
    col1, col2,col3 = st.columns(3)

    # Dans la première colonne, ajoutez un bouton pour "Par défaut"
    if col1.button("Par défaut"):
        afficher_carte_par_defaut()

    # Dans la deuxième colonne, ajoutez un bouton pour "Département"
    if col2.button("Salaire Moyen Région"):
        afficher_carte_region()

    # Dans la deuxième colonne, ajoutez un bouton pour "Département"
    if col3.button("Salaire Moyen Département"):
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
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))

    # Calculez la moyenne des salaires par département
    moyennes_par_departement = df.groupby('departement')['salary'].mean().reset_index()
    min_moyennes = moyennes_par_departement['salary'].min(skipna=True)
    max_moyennes = moyennes_par_departement['salary'].max(skipna=True)

    #median_salary = moyennes_par_departement['salary'].median()
    #moyennes_par_departement['salary'].fillna(median_salary, inplace=True)
    print(moyennes_par_departement)

    # Créez une carte Folium centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Construire le chemin vers le fichier GeoJSON
    chemin_data = os.path.join(chemin_actuel, '..', 'data')
    chemin_geojson = os.path.join(chemin_data, 'departements.geojson')

    # Charger le fichier GeoJSON
    with open(chemin_geojson, 'r') as f:
        geojson_data = json.load(f)

    def get_color(moyenne_salary_array):

        if len(moyenne_salary_array) != 0:
            moyenne_salary = moyenne_salary_array[0]

            if np.isnan(moyenne_salary):
                return '#f8f7f5'

            # bug quand on a pas de données !!!

            # Normalisez la moyenne des salaires entre 0 et 1
            normalized_salary = (moyenne_salary - min_moyennes) / (max_moyennes - min_moyennes)

            r = 0
            g = max(30, int(255 * normalized_salary))
            b = 0

            color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

            return color_hex
        else:
            return '#f8f7f5'


    # Fonction pour formater le contenu de la popup
    def format_popup_content(departement, moyenne_salary):
        #print(f"Nom du département : {departement}<br>Moyenne Salaire : {moyenne_salary} €")
        return f"{departement}<br>Moyenne Salaire : {moyenne_salary} €"


    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': get_color(moyennes_par_departement[moyennes_par_departement['departement'] == feature['properties']['nom']]['salary'].values),
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 0.7,
            'popup': format_popup_content(feature['properties']['nom'], moyennes_par_departement.get(feature['properties']['nom'], 'Non disponible'))
        }
    ).add_to(m)

    folium_static(m)


def afficher_carte_region():
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))

    # Calculez la moyenne des salaires par département
    moyennes_par_region = df.groupby('region')['salary'].mean().reset_index()
    min_moyennes = moyennes_par_region['salary'].min(skipna=True)
    max_moyennes = moyennes_par_region['salary'].max(skipna=True)

    #median_salary = moyennes_par_region['salary'].median()
    #moyennes_par_region['salary'].fillna(median_salary, inplace=True)
    print(moyennes_par_region)

    # Créez une carte Folium centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Construire le chemin vers le fichier GeoJSON
    chemin_data = os.path.join(chemin_actuel, '..', 'data')
    chemin_geojson = os.path.join(chemin_data, 'regions.geojson')

    # Charger le fichier GeoJSON
    with open(chemin_geojson, 'r') as f:
        geojson_data = json.load(f)

    def get_color(moyenne_salary_array):

        if len(moyenne_salary_array) != 0:
            moyenne_salary = moyenne_salary_array[0]

            #print("moyenne_salary : ")
            #print(moyenne_salary)

            if np.isnan(moyenne_salary):
                return '#f8f7f5'

            # bug quand on a pas de données !!!

            # Normalisez la moyenne des salaires entre 0 et 1
            normalized_salary = (moyenne_salary - min_moyennes) / (max_moyennes - min_moyennes)
            #print(normalized_salary)

            r = 0
            g = max(30, int(255 * normalized_salary))
            b = 0

            color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

            return color_hex
        else:
            return '#f8f7f5'


    # Fonction pour formater le contenu de la popup
    def format_popup_content(departement, moyenne_salary):
        #print(f"Nom du département : {departement}<br>Moyenne Salaire : {moyenne_salary} €")
        return f"{departement}<br>Moyenne Salaire : {moyenne_salary} €"


    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': get_color(moyennes_par_region[moyennes_par_region['region'] == feature['properties']['nom']]['salary'].values),
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 0.7,
            'popup': format_popup_content(feature['properties']['nom'], moyennes_par_region.get(feature['properties']['nom'], 'Non disponible'))
        }
    ).add_to(m)

    legend_html = '''
    <div style="position: fixed;
                bottom: 50px; left: 50px; width: 150px; height: 120px;
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color: white;
                ">&nbsp; Légende <br>
                  &nbsp; Min - Max <br>
                  &nbsp; <i style="background:#f8f7f5"></i> Non disponible <br>
                  &nbsp; <i style="background:#001E00"></i> Salaires moyens <br>
    </div>
    '''

    # Ajouter la légende à la carte
    m.get_root().html.add_child(folium.Element(legend_html))

    folium_static(m)


def afficher_donnees():
    st.write("Affichage des 5 premières lignes du fichier CSV :")
    st.write("Taille du corpus : ",len(df))
    st.write(df.head())


def analyse_texte():
    # Titre de la section
    st.header("Analyse de Texte Word Cloud")

    # description
    st.markdown("""
    ## Description
    Cette analyse de texte inclut un Word Cloud pour visualiser les mots les plus fréquemment utilisés dans le corpus de données, ainsi qu'un graphique à barres montrant les 20 mots les plus utilisés avec leur pourcentage d'occurrence.
    """)

    # Concaténer tous les tokens en une seule chaîne
    all_tokens = ' '.join(df['tokens'].dropna())

    # Générer le wordcloud
    wordcloud = WordCloud(width=800, height=400, background_color='white',colormap='Reds').generate(all_tokens)

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
    df_mots = pd.DataFrame(mots_communs, columns=['Mot', 'Occurence'])

    # Afficher le graphique à barres des 20 mots les plus courants
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Occurence', y='Mot', data=df_mots, palette='Reds')
    plt.title('20 mots les plus utilisés')
    plt.xlabel('Occurence')
    plt.ylabel('Mot')
    st.pyplot(plt)  # Afficher le plot dans Streamlit


#####Analyse

def analyse_distribution_salaires():
    st.header("Analyse de la Distribution des Salaires")

    # Affichez un histogramme ou un boxplot pour la distribution des salaires
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['salary'].dropna(), bins=30, kde=True, ax=ax)

    # Personnalisez le graphique
    ax.set_title('Distribution des Salaires')
    ax.set_xlabel('Salaire')
    ax.set_ylabel('Nombre d\'Offres d\'Emploi')

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

def carte_interactive(df):
    st.header("Carte Interactive avec Filtrage par Région/Département")

    # Ajouter des widgets interactifs pour le filtrage par région/département
    utiliser_filtres = st.checkbox("Utiliser des filtres")

    if utiliser_filtres:
        selected_region = st.selectbox("Sélectionner une Région :", df['region'].unique())
        selected_departement = st.selectbox("Sélectionner un Département :", df['departement'].unique())

        # Filtrer le DataFrame en fonction des sélections
        filtered_data = df[(df['region'] == selected_region) & (df['departement'] == selected_departement)]
    else:
        filtered_data = df  # Utiliser l'ensemble des données non filtrées

    # Créer une carte centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Ajouter un cluster de marqueurs à la carte
    marker_cluster = MarkerCluster().add_to(m)

    # Ajouter les marqueurs pour les offres d'emploi filtrées
    for index, row in filtered_data.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            folium.Marker([row['latitude'], row['longitude']], popup=f"<b>{row['title']}</b> <br> <i>{row['compagny']}</i>", tooltip=row['title']).add_to(marker_cluster)

    # Afficher la carte dans Streamlit
    folium_static(m)


def barplot_types_job(df):
    st.header("Barplot des Types de Contrats")

    # Créer un graphique à barres pour les types de contrats
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='type_job', data=df, ax=ax, order=df['type_job'].value_counts().index)

    # Personnaliser le graphique
    ax.set_title('Répartition des Types de Contrats')
    ax.set_xlabel('Type de Contrat')
    ax.set_ylabel('Nombre d\'Offres d\'Emploi')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')  # Rotation des étiquettes pour une meilleure lisibilité

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)



def wordcloud_competences_demandees():

    # Sélection du titre d'emploi
    selected_job_title = st.selectbox("Sélectionner le Titre d'Emploi :", df['title'].unique())

    st.header(f"Analyse des Compétences pour le Titre d'Emploi : {selected_job_title}")

    # Filtrer les données en fonction du titre d'emploi sélectionné
    filtered_data = df[df['title'] == selected_job_title]

    # Concaténer toutes les compétences en une seule chaîne
    all_skills = ' '.join(df['skills'].dropna())

    # Générer le nuage de mots
    wordcloud = WordCloud(width=800, height=400, background_color='white',colormap='Reds').generate(all_skills)

    # Afficher le wordcloud à l'aide de matplotlib
    st.image(wordcloud.to_image(), use_column_width=True)

    # Créer un graphique des 10 compétences les plus demandées
    skills = all_skills.split(',')
    compteur = Counter(skills)
    competences_communes = compteur.most_common(10)
    df_competences = pd.DataFrame(competences_communes, columns=['Compétence', 'Occurrence'])

    # Afficher le graphique à barres des compétences les plus demandées avec une palette de couleurs rouge
    plt.figure(figsize=(10, 8))
    custom_palette = sns.color_palette("Reds", n_colors=10)
    sns.barplot(x='Occurrence', y='Compétence', data=df_competences, palette=custom_palette)
    plt.title('Top 10 des Compétences les plus demandées')
    plt.xlabel('Occurrence')
    plt.ylabel('Compétence')
    st.pyplot(plt)






def experience_salaire():
    st.header("Nuage de Points pour la Relation Expérience/Salaire")

    # Supprimer les lignes avec des valeurs manquantes pour 'experience' et 'salary'
    df_filtered = df.dropna(subset=['experience', 'salary'])

    # Créer un nuage de points avec seaborn
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='experience', y='salary', data=df_filtered, alpha=0.5)

    # Ajouter des étiquettes et un titre
    plt.title('Relation Expérience/Salaire')
    plt.xlabel('Expérience (années)')
    plt.ylabel('Salaire (€)')

    # Afficher le nuage de points dans Streamlit
    st.pyplot(plt)



def top_skills_par_job():

    st.header("Top 10 des Compétences les Plus Demandées")
    # Liste des jobs uniques dans le DataFrame
    liste_jobs = df['type_job'].unique()

    # Widget de sélection pour le job
    job_interesse = st.selectbox("Sélectionner le Job d'Intérêt :", liste_jobs)

    st.header(f"Top 10 des Compétences les Plus Demandées pour le Contrat '{job_interesse}'")

    # Filtrer le DataFrame pour le job spécifié
    df_filtered = df[df['type_job'] == job_interesse]

    # Concaténer toutes les compétences en une seule chaîne
    all_skills = ' '.join(df_filtered['skills'].dropna())

    # Diviser les compétences en mots
    skills_list = all_skills.split()

    # Compter la fréquence des compétences
    skills_counts = Counter(skills_list)

    # Sélectionner les 10 compétences les plus fréquentes
    top_skills = skills_counts.most_common(10)

    # Créer un DataFrame pour les 10 compétences les plus fréquentes
    df_top_skills = pd.DataFrame(top_skills, columns=['Compétence', 'Nombre'])

    # Afficher un barplot pour les 10 compétences les plus fréquentes
    plt.figure(figsize=(10, 6))
    plt.barh(df_top_skills['Compétence'], df_top_skills['Nombre'], color='red')
    plt.xlabel('Nombre d\'Occurrences')
    plt.title(f'Top 10 des Compétences pour le Job "{job_interesse}"')
    plt.gca().invert_yaxis()  # Inverser l'axe y pour avoir la compétence la plus demandée en haut

    # Afficher le barplot dans Streamlit
    st.pyplot(plt)

def scrapping():
    # Chemin absolu actuel de main_streamlit.py
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_python = os.path.join(chemin_actuel, '..', 'python')
    # Ajouter le chemin au système PYTHONPATH
    sys.path.append(chemin_python)
    from web_scraping import main_web_scraping

    st.header("Scrapper les emplois de votre choix sur Indeed, Pole Emploi et Apec etc...")
    st.markdown(''':rainbow[ATTENTION une offre scrappée = 2 secondes, prenez un café].''')

    liste_sites = ["Apec","Indeed","Pole_Emploi", "Welcome_to_the_jungle"]

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


def recherche():

    st.header("Recherche d'emplois")

    #Zone de texte pour entrer le titre de l'emploi
    search_query_emploi = st.text_input("Titre de l'Emploi :", "")

    # Zone de texte pour entrer le type de contrat
    search_query_contrat = st.text_input("Type de Contrat :", "")

    st.header("Résultats de la Recherche")

    # Filtrer les données en fonction des critères de recherche
    filtered_data = df[
        (df['title'].str.contains(search_query_emploi, case=False)) &
        (df['type_job'].str.contains(search_query_contrat, case=False))
    ]

    # Afficher les résultats de la recherche
    if not filtered_data.empty:
        st.table(filtered_data[['title', 'type_job', 'compagny', 'location', 'salary']])
    else:
        st.warning("Aucun résultat correspondant trouvé.")



def main():

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
    options_navigation = ["Accueil","Recherche","Afficher les données", "Analyse de Texte","Compétences","Carte","Type de contrat","Top 10 job","Distribution salaires","Experience/Salaire","Scrapper des données"]
    selected_option = st.sidebar.radio("Navigation", options_navigation)

    # Contenu de l'application en fonction de l'option sélectionnée

    if selected_option == "Accueil":
        afficher_accueil()
    elif selected_option == "Recherche":
        recherche()
    elif selected_option == "Afficher les données":
        afficher_donnees()
    elif selected_option == "Analyse de Texte":
        analyse_texte()
    elif selected_option == "Compétences":
        wordcloud_competences_demandees()
    elif selected_option == "Carte":
        carte_interactive(df)
    elif selected_option == "Type de contrat":
        barplot_types_job(df)
    elif selected_option == "Top 10 job":
        top_skills_par_job()
    elif selected_option == "Distribution salaires":
        analyse_distribution_salaires()
    elif selected_option == "Experience/Salaire":
        experience_salaire()
    elif selected_option == "Scrapper des données":
        scrapping()
    else:
        st.write("Sélectionnez une option de navigation dans la barre latérale.")


df = load_data("src/data/all_data.csv")



if __name__ == "__main__":
    main()

