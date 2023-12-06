# from build_data import *
# from web_scraping import *
# from scrap_description import *

# #main_web_scraping(job_name,45)

# job_name = "Data Scientist"
# urls = build_url_job_research(job_name)

# driver = create_driver()
# df = create_df()
# df = web_scrap(driver,df,urls[1],n_posts_max=45)
# save_df(df,df['source'][0])

# df.head()

# import sqlite3
# import pandas as pd

# # Import data
# df = pd.read_csv('apec.csv')

# # Clean data
# df.columns = df.columns.str.strip()

# # Create/connect to a sqlite data
# connection = sqlite3.connect('demo.db')

import sqlite3

class data_base:
    def __init__(self):
        self.con = sqlite3.connect('test.db')
        self.cur = self.con.cursor()
        self.create_type_job()
        self.create_salaire()
        self.create_competence()
        self.create_langue()
        self.create_depatement()
        self.create_entreprise()
        self.create_date()
        self.create_description()
        self.create_source()
        self.create_location()
        self.create_titre()
    
    ### H_type_job
    # Create the table H_type_job
    def create_type_job(self):
        # self.cur.execute("""DROP TABLE H_type_job""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS H_type_job(
                         id_type_job INTEGER PRIMARY KEY,
                         type TEXT                                    
        )""")
    
    # Insert value into H_type_job
    def insert_type_job(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO H_type_job VALUES(?,?)""", item)

    ### H_salaire
    #Create table H_salaire
    def create_salaire(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS H_salaire(
                         id_salaire INTEGER PRIMARY KEY AUTOINCREMENT,
                         salaire TEXT
        )""")

    # Insert value into H_salaire
    def insert_salaire(self,item):
        self.cur.execute("""INSERT OR IGNORE INTO H_salaire VALUES(?,?)""", item)

    ### H_competanceCr eate table H_copetance
    #Create table H_copetence
    def create_competence(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS H_competence(
                         id_competence INTEGER PRIMARY KEY,
                         competance TEXT
        )""")

    # Insert velue into H_competance
    def insert_competance(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO H_competence VALUES(?,?)""", item)

    ### H_langue
    # Create table H_langue
    def create_langue(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS H_langue(
                         id_langue INTEGER PRIMARY KEY,
                         langue TEXT
        )""")

    # Insert value into H_langue
    def insert_langue(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO H_langue VALUES(?,?)""", item)

    ### H_departement
    #C reate table H_departement
    def create_depatement(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS H_departement(
                         id_departement INTEGER PRIMARY KEY,
                         departement TEXT
        )""")

    # Insert value into H_depatement
    def insert_departement(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO H_departement VALUES(?,?)""", item)


    ### D_entreprise
    # Create table D_entreprise
    def create_entreprise(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_entreprise(
                         id_entreprise INTEGER PRIMARY KEY,
                         id_type_job INTEGER ,
                         id_salaire INTEGER,
                         entreprise TEXT,
                         FOREIGN KEY(id_type_job) REFERENCES H_type_job(id_type_job),
                         FOREIGN KEY(id_salaire) REFERENCES H_salaire(id_salaire)
        )""")

    # Insert value into D_entreprise
    def insert_entreprise(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_entreprise VALUES(?,?,?,?)""", item)


    ### D_date 
    # Create table D_date
    def create_date(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_date(
                         id_date INTEGER PRIMARY KEY,
                         date TEXT
        )""")

    # Insert value sinto D_date
    def insert_date(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_date VALUES(?,?)""", item)

    ### D_description
    def create_description(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_description(
                         id_description INTEGER PRIMARY KEY,
                         id_competence INTEGER,
                         id_langue INTEGER,
                         description TEXT,
                         FOREIGN KEY(id_competence) REFERENCES H_competence(id_competence),
                         FOREIGN KEY(id_langue) REFERENCES H_langue(id_langue)
        )""")

    def instert_description(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_description VALUES(?,?,?,?)""", item)

    ### D_source
    def create_source(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_source(
                         id_source INTEGER PRMIMARY KEY,
                         source TEXT
        )""")

        def insert_source(self, item):
            self.cur.execute("""INSERT OR IGNORE INTO D_source VALUES(?,?)""", item)

    ### D_location
    def create_location(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_location(
                         id_location INTEGER PRIMARY KEY,
                         id_departement INTEGER,
                         ville TEXT,
                         FOREIGN KEY(id_departement) REFERENCES H_depatement(id_departement)
        )""")

    def insert_location(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_location VALUES(?,?,?)""", item)

    # F_titre
    def create_titre(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS F_titre(
                         id_titre INTEGER PRIMARY KEY,
                         id_entreprise INTEGER,
                         id_date INTEGER,
                         id_description INTEGER,
                         id_source INTEGER,
                         id_location INTEGER,
                         titre TEXT,
                         FOREIGN KEY(id_entreprise) REFERENCES D_entreprise(id_entreprise),
                         FOREIGN KEY(id_date) REFERENCES D_date(id_date),
                         FOREIGN KEY(id_description) REFERENCES D_description(id_description),
                         FOREIGN KEY(id_source) REFERENCES D_source(id_source),
                         FOREIGN KEY(id_location) REFERENCES D_location(id_location)
        )""")

    def insert_titre(self,item):
        self.cur.execute("""INSERT OR IGNORE INTO F_titre(?,?,?,?,?,?,?)""", item)

    def commit_change(self):
        self.con.commit()

    def close_connection(self):
        self.con.close()
