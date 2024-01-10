import pandas as pd
import sqlite3
from SQLite_v2 import data_base
import sys

def load_data(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM 'data';""")
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

    df = df.dropna()
    df = df.reset_index()

    # A FAIRE DANS LE PREPROCESSING
    accent_dict = {"'": ' '}
    def remove_accents(input_str):
        return ''.join(accent_dict.get(char, char) for char in input_str)
    df = df.applymap(lambda x: remove_accents(str(x)) if pd.notnull(x) else x)

    df2 = df[['title','type_job','salary','compagny','location','region','departement','latitude','longitude','experience','skills','date','description','tokens','source']].drop_duplicates()
    df2 = df2.reset_index()

    return df, df2

def create_dw(df, df2,chemin_actuel):

    bd = data_base(chemin_actuel)

    ### insert into H_salaire
    for i in list(df['salary'].unique()):
        item = (i,)
        bd.insert_salaire(item)

    ### insert into H_type_job
    for i in list(df['type_job'].unique()):
        item = (i,)
        bd.insert_type_job(item)

    ### insert into D_entreprise
    for i in range(len(df2)):
        val_type = df2['type_job'][i]
        requete_type = f"""SELECT id_type_job FROM H_type_job WHERE type = '{val_type}'"""
        res_type = bd.req(requete= requete_type)[0][0]
            

        val_salary = df2['salary'][i]
        requete_salary = f"""SELECT id_salaire FROM H_salaire WHERE salaire = '{val_salary}'"""
        res_salary = bd.req(requete=requete_salary)[0][0]
            
        res_compagny = df2['compagny'][i]

        item = (res_type, res_salary,res_compagny)
        bd.insert_entreprise(item)

    ###########

    ### insert into H_departement   
    for row in df[['departement', 'region']].drop_duplicates().itertuples(index=False):
        item = row[:2]
        bd.insert_departement(item)

    ### insert into D_location 

    for i in range(len(df2)):
        val_dep = df2['departement'][i]

        requete_dep = f"""SELECT id_departement FROM H_departement WHERE departement = '{val_dep}'"""
        res_dep = bd.req(requete= requete_dep)[0][0]

        res_long = df2['longitude'][i]
        res_lat = df2['latitude'][i]
        res_location = df2['location'][i]

        item = (res_dep, res_location, res_long, res_lat)
        bd.insert_location(item)

    ###########

    ### insert into D_source
            
    for i in list(df['source'].unique()):
        item = (i,)
        bd.insert_source(item)

    ###########
            
    ### insert into H_experience
    for i in list(df['experience'].unique()):
        item = (i,)
        bd.insert_experience(item) 

    ### insert into H_competence
    for i in list(df['skills'].unique()):
        item = (i,)
        bd.insert_competence(item)   

    ### insert into D_titre
    for i in range(len(df2)):
        val_experience = df2['experience'][i]
        requete_experience = f"""SELECT id_experience FROM H_experience WHERE experience = '{val_experience}'"""
        res_experience = bd.req(requete= requete_experience)[0][0]
            

        val_comp = df2['skills'][i]
        requete_comp = f"""SELECT id_competence FROM H_competence WHERE competence = '{val_comp}'"""
        res_comp = bd.req(requete=requete_comp)[0][0]
            
        res_titre = df2['title'][i]

        item = (res_comp, res_experience,res_titre)
        bd.insert_titre(item) 

    ###########
            
    ### insert into D_date
    for i in list(df['date'].unique()):
        item = (i,)
        bd.insert_date(item) 

    ###########
            
    ### insert into D_token
    for i in list(df['tokens'].unique()):
        item = (i,)
        bd.insert_token(item) 

    ###########
        
    ### insert into F_description

    for i in range(len(df2)):
        val_entreprise = df2['compagny'][i]
        requete_entreprise = f"""SELECT id_entreprise FROM D_entreprise WHERE entreprise = '{val_entreprise}'"""
        res_entreprise = bd.req(requete= requete_entreprise)[0][0]
            
        val_date = df2['date'][i]
        requete_date = f"""SELECT id_date FROM D_date WHERE date = '{val_date}'"""
        res_date = bd.req(requete=requete_date)[0][0]
            
        val_titre = df2['title'][i]
        requete_titre = f"""SELECT id_titre FROM D_titre WHERE titre = '{val_titre}'"""
        res_titre = bd.req(requete=requete_titre)[0][0]
        
        val_source = df2['source'][i]
        requete_source = f"""SELECT id_source FROM D_source WHERE source = '{val_source}'"""
        res_source = bd.req(requete=requete_source)[0][0]

        val_location = df2['location'][i]
        requete_location = f"""SELECT id_location FROM D_location WHERE ville = '{val_location}'"""
        res_location = bd.req(requete=requete_location)[0][0]

        val_token = df2['tokens'][i]
        requete_token = f"""SELECT id_token FROM D_token WHERE token = '{val_token}'"""
        res_token = bd.req(requete=requete_token)[0][0]

        res_description = df2['description'][i]

        item = (res_entreprise, res_date, res_titre, res_source, res_location, res_token, res_description)
        bd.insert_description(item) 

    bd.commit_change()
    bd.close_connection()


