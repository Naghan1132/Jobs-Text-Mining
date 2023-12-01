import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

# Fonction pour afficher l'accueil
def afficher_accueil():
    st.write("Jobs Text Minning")

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
        # Analyse de la fréquence des mots
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


# Options de navigation dans la barre latérale
options_navigation = ["Accueil", "Afficher les données", "Analyse de Texte","Scrapper des données"]
selected_option = st.sidebar.selectbox("Navigation", options_navigation)

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
