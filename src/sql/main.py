import streamlit as st
import pandas as pd
import sqlite3  # Vous pouvez utiliser également MySQLdb pour MySQL


# Connexion à la base de données
conn = sqlite3.connect('ma_base_de_donnees.db')  #  mysql -h votre_hote -u votre_utilisateur -p 

# Exemple de requête SQL
query = "SELECT * FROM ma_table;"

# Exécution de la requête et chargement des résultats dans un DataFrame
df = pd.read_sql(query, conn)

# Affichage des données dans Streamlit
st.dataframe(df)


