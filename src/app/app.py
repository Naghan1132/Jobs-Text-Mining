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
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation



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

    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()


    req = """SELECT ville, longitude, latitude, titre, entreprise FROM D_location, D_titre, D_entreprise, F_description WHERE D_location.id_location = F_description.id_location AND D_titre.id_titre = F_description.id_titre AND D_entreprise.id_entreprise = F_description.id_entreprise;"""

    cursor.execute(req)
    rows = cursor.fetchall()

    conn.close()

    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])


    # Affichage de la carte
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(m)

    for index, row in df.iterrows():
        if pd.notnull(row['ville']) and pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            folium.Marker([row['latitude'], row['longitude']], popup=f"<b>{row['titre']}</b> <br> <i>{row['entreprise']}</i>",tooltip=row['titre']).add_to(marker_cluster)
    
    folium_static(m)

    # Utilisez une balise HTML pour séparer la carte des informations
    #st.markdown("---")
    
    # Affichage des informations
    #st.write("<h2>Informations du marqueur sélectionné</h2>", unsafe_allow_html=True)
    #marker_info = st.empty()  # Élément pour afficher les informations du marqueur

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
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

    req = """SELECT departement, salaire FROM H_departement, H_salaire, D_location, D_entreprise, F_description WHERE H_departement.id_departement = D_location.id_departement AND D_location.id_location = F_description.id_location AND H_salaire.id_salaire = D_entreprise.id_salaire AND D_entreprise.id_entreprise = F_description.id_entreprise;"""

    cursor.execute(req)
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    df['salaire'] = pd.to_numeric(df['salaire'], errors='coerce')
    
    # Calculez la moyenne des salaires par département
    moyennes_par_departement = df.groupby('departement')['salaire'].mean().reset_index()
    print(moyennes_par_departement)
    min_moyennes = moyennes_par_departement['salaire'].min(skipna=True)
    max_moyennes = moyennes_par_departement['salaire'].max(skipna=True)

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
            'fillColor': get_color(moyennes_par_departement[moyennes_par_departement['departement'] == feature['properties']['nom']]['salaire'].values),
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
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

    req = """SELECT region, salaire FROM H_departement, H_salaire, D_location, D_entreprise, F_description WHERE H_departement.id_departement = D_location.id_departement AND D_location.id_location = F_description.id_location AND H_salaire.id_salaire = D_entreprise.id_salaire AND D_entreprise.id_entreprise = F_description.id_entreprise;"""

    cursor.execute(req)
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    df['salaire'] = pd.to_numeric(df['salaire'], errors='coerce')
    
    # Calculez la moyenne des salaires par département
    moyennes_par_region = df.groupby('region')['salaire'].mean().reset_index()
    print(moyennes_par_region)
    min_moyennes = moyennes_par_region['salaire'].min(skipna=True)
    max_moyennes = moyennes_par_region['salaire'].max(skipna=True)


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
            'fillColor': get_color(moyennes_par_region[moyennes_par_region['region'] == feature['properties']['nom']]['salaire'].values),
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
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

    req = """SELECT titre,ville, source,experience, entreprise FROM D_location, D_titre,D_source, D_entreprise,H_experience, F_description WHERE D_location.id_location = F_description.id_location AND D_titre.id_titre = F_description.id_titre AND D_entreprise.id_entreprise = F_description.id_entreprise;"""
    cursor.execute(req)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    conn.close()

    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

    req_global = """SELECT * FROM F_description;"""
    cursor.execute(req_global)
    rows_g = cursor.fetchall()
    conn.close()
    

    st.write("Affichage des n premières lignes :")
    st.write("Taille du corpus : ",len(rows_g))
    st.write(df.head(15))

    
    

def analyse_texte():
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

    req = """SELECT titre, token FROM D_titre, D_token, F_description WHERE D_titre.id_titre = F_description.id_titre AND D_token.id_token = F_description.id_token;"""

    cursor.execute(req)
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

    # Titre de la section
    st.header("Analyse de Texte Word Cloud")

    # Concaténer tous les tokens en une seule chaîne
    all_tokens = ' '.join(df['token'].dropna())
    
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
    df_mots = pd.DataFrame(mots_communs, columns=['Mot', 'Occurence'])

    # Afficher le graphique à barres des 20 mots les plus courants
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Occurence', y='Mot', data=df_mots, palette='viridis')
    plt.title('20 mots les plus utilisés')
    plt.xlabel('Occurence')
    plt.ylabel('Mot')
    st.pyplot(plt)  # Afficher le plot dans Streamlit





def scrapping():
    # Chemin absolu actuel de main_streamlit.py
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_python = os.path.join(chemin_actuel, '..', 'python')
    # Ajouter le chemin au système PYTHONPATH
    sys.path.append(chemin_python)
    from web_scraping import main_web_scraping

    st.header("Scrapper les emplois de votre choix sur Pole Emploi / Apec / Welcome_to_the_jungle")
    st.markdown(''':rainbow[ATTENTION une offre scrappée = 2 secondes, prenez un café].''')

    liste_sites = ["Apec","Pole_Emploi", "Welcome_to_the_jungle"]
    
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
            main_web_scraping(job_name,n_jobs,sites_selectionnes)
            
            # Une fois le scraping terminé, mettre à jour le message
            st.success("Scrapping terminé avec succès!")

def recherche():

    st.header("retourne les emplois les plus pertinents en fonction de votre recherche")
    st.write("entrer peut-être le type emploi, le nom du job et compétences etc... via description")
    search_query_emploi = ''
    search_query_contrat = ''
    # Widget de barre de recherche
    search_query_emploi = st.text_input("Titre Emploi : ", "")
    search_query_contrat = st.text_input("Type contrat : ", "")
    # Bouton de recherche
    if st.button('Rechercher'):
        chaine_originale  = """SELECT titre, entreprise, type, salaire, experience, competence,date, ville, source, description FROM D_titre, H_experience, H_competence, D_entreprise, H_type_job, H_salaire, D_date, D_location, D_source, F_description WHERE H_type_job.id_type_job = D_entreprise.id_type_job AND H_salaire.id_salaire = D_entreprise.id_salaire AND D_entreprise.id_entreprise = F_description.id_entreprise AND H_experience.id_experience = D_titre.id_experience AND H_competence.id_competence = D_titre.id_competence AND D_titre.id_titre = F_description.id_titre AND D_source.id_source = F_description.id_source AND D_location.id_location = F_description.id_location AND D_date.id_date = F_description.id_date;"""
        if search_query_emploi == '' and search_query_contrat != '':
            st.write(f"Vous avez recherché: {search_query_contrat}")
            elements_a_inserer = f" AND H_type_job.type = '{search_query_contrat}'"
            index_insertion = len(chaine_originale) - 1
            req1 = chaine_originale[:index_insertion] + elements_a_inserer + chaine_originale[index_insertion:]

        elif search_query_emploi != '' and search_query_contrat == '':
            st.write(f"Vous avez recherché: {search_query_emploi}")
            elements_a_inserer = f" AND D_titre.titre = '{search_query_emploi}'"
            index_insertion = len(chaine_originale) - 1
            req1 = chaine_originale[:index_insertion] + elements_a_inserer + chaine_originale[index_insertion:]

        elif search_query_emploi != '' and search_query_contrat != '':
            st.write(f"Vous avez recherché: {search_query_emploi} et {search_query_contrat}")
            elements_a_inserer = f" AND D_titre.titre = '{search_query_emploi}' AND H_type_job.type = '{search_query_contrat}'"
            index_insertion = len(chaine_originale) - 1
            req1 = chaine_originale[:index_insertion] + elements_a_inserer + chaine_originale[index_insertion:]
        
        else :
            st.write("Vous n'avez rien recherché.")
            req1 = """SELECT titre, entreprise, type, salaire, experience, competence,date, ville, source, description FROM D_titre, H_experience, H_competence, D_entreprise, H_type_job, H_salaire, D_date, D_location, D_source, F_description WHERE H_type_job.id_type_job = D_entreprise.id_type_job AND H_salaire.id_salaire = D_entreprise.id_salaire AND D_entreprise.id_entreprise = F_description.id_entreprise AND H_experience.id_experience = D_titre.id_experience AND H_competence.id_competence = D_titre.id_competence AND D_titre.id_titre = F_description.id_titre AND D_source.id_source = F_description.id_source AND D_location.id_location = F_description.id_location AND D_date.id_date = F_description.id_date;"""
        
        chemin_actuel = os.path.dirname(os.path.abspath(__file__))
        chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

        conn = sqlite3.connect(chemin_sql+'/warehouse.db')
        cursor = conn.cursor()

        cursor.execute(req1)
        rows = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
        st.write(df)

#####Analyse

def analyse_distribution_salaires():

    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

    req = """SELECT salaire FROM H_salaire, D_entreprise, F_description 
             WHERE H_salaire.id_salaire = D_entreprise.id_salaire 
             AND D_entreprise.id_entreprise = F_description.id_entreprise;"""

    cursor.execute(req)
    rows = cursor.fetchall()

    conn.close()

    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    
    df['salaire'] = pd.to_numeric(df['salaire'], errors='coerce')

    df = df.sort_values(by='salaire')

    st.header("Analyse de la Distribution des Salaires")

    # Affichez un histogramme ou un boxplot pour la distribution des salaires
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['salaire'].dropna(), bins=30, kde=True, ax=ax)

    # Personnalisez le graphique
    ax.set_title('Distribution des Salaires')
    ax.set_xlabel('Salaire')
    ax.set_ylabel('Nombre d\'Offres d\'Emploi')

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)




def barplot_types_job():
    
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

     # Requête SQL pour récupérer les types de job
    req = """
    SELECT H_type_job.type
    FROM D_entreprise
    INNER JOIN H_type_job ON D_entreprise.id_type_job = H_type_job.id_type_job
    """

    cursor.execute(req)
    rows = cursor.fetchall()
    conn.close()

    # Création du DataFrame
    df = pd.DataFrame(rows, columns=['type_job'])

    # Interface Streamlit
    st.header("Barplot des Types de Job")

    # Créer un graphique à barres pour les types de job
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='type_job', data=df, ax=ax, order=df['type_job'].value_counts().index, palette="Reds")

    # Personnaliser le graphique
    ax.set_title('Répartition des Types de Job')
    ax.set_xlabel('Type de Job')
    ax.set_ylabel('Nombre d\'Occurrences')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')  # Rotation des étiquettes pour une meilleure lisibilité

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)


def wordcloud_competences_demandees():
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()
    
    query = "SELECT titre, competence FROM D_titre INNER JOIN H_competence ON D_titre.id_competence = H_competence.id_competence"
    result = cursor.execute(query).fetchall()

    conn.close()

    columns = ['title', 'skills']
    df = pd.DataFrame(result, columns=columns).dropna()

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

    # Clustering 
    st.subheader("Clustering de documents par compétence")

    num_clusters = st.slider("Sélectionner le nombre de clusters", min_value=2, max_value=10, value=3)

    tokens = df['skills'].dropna()

    # Vectorizer le data avec TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    X_tfidf = tfidf_vectorizer.fit_transform(tokens)

    # Latent Dirichlet Allocation (LDA)
    lda = LatentDirichletAllocation(n_components=num_clusters, random_state=42)
    document_topics = lda.fit_transform(X_tfidf)

    # nouvelle colonne avec les clusters 
    df['Cluster'] = document_topics.argmax(axis=1)

    # Montrer les mots particuliers à chaque cluster et le titre le plus populaire
    for cluster_id in range(lda.n_components):
        cluster_words_indices = lda.components_[cluster_id].argsort()[:-6:-1]  # Indices of the top 5 words
        cluster_words = [word for word in tfidf_vectorizer.get_feature_names_out() if
                        tfidf_vectorizer.vocabulary_[word] in cluster_words_indices]

        st.markdown(f"**Mots-clés du Cluster {cluster_id + 1}:** {' | '.join(cluster_words)}")

        # Trouver le titre le plus populaire pour chaque cluster
        most_popular_title = df[df['Cluster'] == cluster_id]['title'].mode().values[0]
        st.markdown(f"**Titre d'emploi le plus populaire:** {most_popular_title}")
    
        # Add a separator between clusters for better readability
        st.markdown("---")




def entreprise_salaire():
 
    # Connexion à la base de données
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()
      
    # Requête SQL pour obtenir la liste des types de contrat
    query_contrats = "SELECT DISTINCT type FROM H_type_job;"

    # Exécution de la requête
    result_contrats = conn.execute(query_contrats).fetchall()

    # Fermeture de la connexion
    conn.close()

    # Interface utilisateur avec Streamlit
    st.title("Analyse des Entreprises Payant le Mieux")

    # Sélection du type de contrat avec une liste déroulante
    type_contrat_filtre = st.selectbox("Sélectionnez le Type de Contrat :", [row[0] for row in result_contrats])

    # Connexion à la base de données
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

    # Requête SQL pour calculer la moyenne des salaires par entreprise, en filtrant par type de contrat
    query = f"""
        SELECT D_entreprise.entreprise, AVG(H_salaire.salaire) as moyenne_salaire
        FROM D_entreprise
        JOIN H_salaire ON D_entreprise.id_salaire = H_salaire.id_salaire
        JOIN H_type_job ON D_entreprise.id_type_job = H_type_job.id_type_job
        WHERE H_type_job.type = '{type_contrat_filtre}'
        GROUP BY D_entreprise.entreprise
        ORDER BY moyenne_salaire DESC;
    """

    # Exécution de la requête
    result = conn.execute(query).fetchall()

    # Fermeture de la connexion
    conn.close()

    # Création d'un DataFrame avec les résultats
    columns = ['entreprise', 'moyenne_salaire']
    df = pd.DataFrame(result, columns=columns)

    # Affichage du top des entreprises payant le mieux pour un type de contrat spécifique
    top_entreprises = df.head(10)  # Vous pouvez ajuster le nombre d'entreprises à afficher
    st.table(top_entreprises)

    # Création d'un graphique barplot
    plt.figure(figsize=(10, 6))
    plt.bar(top_entreprises['entreprise'], top_entreprises['moyenne_salaire'],  color='red')
    plt.xlabel('Entreprise')
    plt.ylabel('Moyenne des Salaires')
    plt.title(f'Top des Entreprises Payant le Mieux pour le Type de Contrat "{type_contrat_filtre}"')
    plt.xticks(rotation=45, ha='right')  # Rotation des étiquettes pour une meilleure lisibilité


    # Affichage du graphique dans Streamlit
    st.pyplot(plt)

def experience_salaire():

    # Connexion à la base de données
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

    # Case à cocher pour tout visualiser sans filtre
    tout_visualiser = st.checkbox("Tout visualiser sans filtre")

    if tout_visualiser:
        selected_contrat = "Tous"
    else:
        # Requête SQL pour obtenir la liste des types de contrats
        types_contrats_query = "SELECT DISTINCT type FROM H_type_job;"
        types_contrats = [row[0] for row in conn.execute(types_contrats_query).fetchall()]

        # Ajouter une option "Tous" pour le type de contrat
        selected_contrat = st.selectbox("Sélectionner le type de contrat :", types_contrats + ["Tous"])

    # Requête SQL pour obtenir le salaire moyen par expérience avec filtre sur le type de contrat
    if selected_contrat != "Tous":
        query = f"""
            SELECT
                H_experience.experience,
                AVG(H_salaire.salaire) as moyenne_salaire
            FROM
                H_experience
            JOIN
                D_titre ON H_experience.id_experience = D_titre.id_experience
            JOIN
                F_description ON D_titre.id_titre = F_description.id_titre
            JOIN
                D_entreprise ON F_description.id_entreprise = D_entreprise.id_entreprise
            JOIN
                H_salaire ON D_entreprise.id_salaire = H_salaire.id_salaire
            JOIN
                H_type_job ON D_entreprise.id_type_job = H_type_job.id_type_job
            WHERE
                H_type_job.type = '{selected_contrat}'
            GROUP BY
                H_experience.experience
            ORDER BY
                H_experience.experience;
        """
    else:
        # Aucun filtre sur le type de contrat
        query = """
            SELECT
                H_experience.experience,
                AVG(H_salaire.salaire) as moyenne_salaire
            FROM
                H_experience
            JOIN
                D_titre ON H_experience.id_experience = D_titre.id_experience
            JOIN
                F_description ON D_titre.id_titre = F_description.id_titre
            JOIN
                D_entreprise ON F_description.id_entreprise = D_entreprise.id_entreprise
            JOIN
                H_salaire ON D_entreprise.id_salaire = H_salaire.id_salaire
            GROUP BY
                H_experience.experience
            ORDER BY
                H_experience.experience;
        """

    # Exécution de la requête
    result = conn.execute(query).fetchall()

    # Fermeture de la connexion
    conn.close()

    # Création d'un DataFrame avec les résultats
    columns = ['experience', 'moyenne_salaire']
    df = pd.DataFrame(result, columns=columns)

    # Visualisation avec Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(df['experience'], df['moyenne_salaire'], marker='o', color='red')
    plt.xlabel('Expérience')
    plt.ylabel('Salaire moyen')
    plt.title('Salaire moyen en fonction de l\'expérience')
    plt.grid(True)
    plt.show()

    # Afficher le barplot dans Streamlit
    st.pyplot(plt)


def top_skills_par_job():
    
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    conn = sqlite3.connect(chemin_sql+'/warehouse.db')
    cursor = conn.cursor()

    query = "SELECT D_titre.titre, H_competence.competence FROM D_titre INNER JOIN H_competence ON D_titre.id_competence = H_competence.id_competence"

    result = cursor.execute(query).fetchall()

    conn.close()

    # Création du DataFrame
    columns = ['titre_job', 'competence']
    df = pd.DataFrame(result, columns=columns).dropna()



    # Liste des titres de job uniques dans le DataFrame
    liste_titres = df['titre_job'].unique()

    # Widget de sélection pour le titre de job
    titre_interesse = st.selectbox("Sélectionner le Titre de Job d'Intérêt :", liste_titres)

    st.header(f"Top 10 des Compétences pour le Titre de Job '{titre_interesse}'")

    # Filtrer le DataFrame pour le titre de job spécifié
    df_filtered = df[df['titre_job'] == titre_interesse]

    # Concaténer toutes les compétences en une seule chaîne
    all_skills = ' '.join(df_filtered['competence'].dropna())

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
    plt.title(f'Top 10 des Compétences pour le Titre de Job "{titre_interesse}"')
    plt.gca().invert_yaxis()  # Inverser l'axe y pour avoir la compétence la plus demandée en haut

    # Afficher le barplot dans Streamlit
    st.pyplot(plt)

  


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
    options_navigation = ["Accueil","Recherche","Afficher les données", "Analyse de Texte","Compétences","Type de contrat","Top 10 job","Distribution salaires","Entreprise/Salaire","Expérience/Salaire","Scrapper des données"]
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
    elif selected_option == "Type de contrat":
        barplot_types_job()
    elif selected_option == "Top 10 job":
        top_skills_par_job()
    elif selected_option == "Distribution salaires":
        analyse_distribution_salaires()
    elif selected_option == "Entreprise/Salaire":
        entreprise_salaire()
    elif selected_option == "Expérience/Salaire":
         experience_salaire()
    elif selected_option == "Scrapper des données":
        scrapping()
    else:
        st.write("Sélectionnez une option de navigation dans la barre latérale.")

# df = load_data("src/data/all_data.csv")

if __name__ == "__main__":
    main()
