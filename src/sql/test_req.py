import sqlite3
import pandas as pd
import os

os.chdir('C:/Documents/COURS/M2/NLP/sql')


# afficher_carte_par_defaut
conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()

req = """SELECT ville, longitude, latitude, titre, entreprise FROM D_location, D_titre, D_entreprise, F_description WHERE D_location.id_location = F_description.id_location AND D_titre.id_titre = F_description.id_titre AND D_entreprise.id_entreprise = F_description.id_entreprise;"""

cursor.execute(req)
rows = cursor.fetchall()

conn.close()

df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])


# afficher_carte_departement
conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()

req = """SELECT departement, salaire FROM H_departement, H_salaire, D_location, D_entreprise, F_description WHERE H_departement.id_departement = D_location.id_departement AND D_location.id_location = F_description.id_location AND H_salaire.id_salaire = D_entreprise.id_salaire AND D_entreprise.id_entreprise = F_description.id_entreprise;"""

cursor.execute(req)
rows = cursor.fetchall()

conn.close()

df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

# afficher_carte_region
conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()

req = """SELECT region, salaire FROM H_departement, H_salaire, D_location, D_entreprise, F_description WHERE H_departement.id_departement = D_location.id_departement AND D_location.id_location = F_description.id_location AND H_salaire.id_salaire = D_entreprise.id_salaire AND D_entreprise.id_entreprise = F_description.id_entreprise;"""

cursor.execute(req)
rows = cursor.fetchall()

conn.close()

df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
print(df)

# afficher_donnees
conn = sqlite3.connect('base_brute.db')
cursor = conn.cursor()

req = """SELECT * FROM data;"""

cursor.execute(req)
rows = cursor.fetchall()

conn.close()

df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

# analyse_texte
conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()

req = """SELECT token FROM D_token, F_description WHERE D_token.id_token = F_description.id_token;"""

cursor.execute(req)
rows = cursor.fetchall()

conn.close()

df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])


