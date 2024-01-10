import sqlite3

class data_base:
    def __init__(self):
        self.con = sqlite3.connect('test2.db')
        self.cur = self.con.cursor()
        self.create_type_job()
        self.create_salaire()
        self.create_competence()
        self.create_experience()
        self.create_depatement()
        self.create_entreprise()
        self.create_date()
        self.create_titre()
        self.create_source()
        self.create_location()
        self.create_token()
        self.create_description()
    
    ### H_type_job
    # Create the table H_type_job
    def create_type_job(self):
        # self.cur.execute("""DROP TABLE H_type_job""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS H_type_job(
                         id_type_job INTEGER PRIMARY KEY AUTOINCREMENT,
                         type TEXT                                    
        )""")
    
    # Insert value into H_type_job
    def insert_type_job(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO H_type_job (type) VALUES(?)""", item)

    ### H_salaire
    #Create table H_salaire
    def create_salaire(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS H_salaire(
                         id_salaire INTEGER PRIMARY KEY AUTOINCREMENT,
                         salaire TEXT
        )""")

    # Insert value into H_salaire
    def insert_salaire(self,item):
        self.cur.execute("""INSERT OR IGNORE INTO H_salaire (salaire) VALUES(?)""", item)

    ### H_competanceCr eate table H_copetance
    #Create table H_copetence
    def create_competence(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS H_competence(
                         id_competence INTEGER PRIMARY KEY AUTOINCREMENT,
                         competence TEXT
        )""")

    # Insert velue into H_competance
    def insert_competence(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO H_competence (competence) VALUES(?)""", item)

    ### H_experience
    # Create table H_experience
    def create_experience(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS H_experience(
                         id_experience INTEGER PRIMARY KEY AUTOINCREMENT,
                         experience TEXT
        )""")

    # Insert value into H_langue
    def insert_experience(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO H_experience (experience) VALUES(?)""", item)

    ### H_departement
    #C reate table H_departement
    def create_depatement(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS H_departement(
                         id_departement INTEGER PRIMARY KEY AUTOINCREMENT,
                         departement TEXT
        )""")

    # Insert value into H_depatement
    def insert_departement(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO H_departement (departement) VALUES(?)""", item)


    ### D_entreprise
    # Create table D_entreprise
    def create_entreprise(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_entreprise(
                         id_entreprise INTEGER PRIMARY KEY AUTOINCREMENT,
                         id_type_job INTEGER ,
                         id_salaire INTEGER,
                         entreprise TEXT,
                         FOREIGN KEY(id_type_job) REFERENCES H_type_job(id_type_job),
                         FOREIGN KEY(id_salaire) REFERENCES H_salaire(id_salaire)
        )""")

    # Insert value into D_entreprise
    def insert_entreprise(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_entreprise (id_type_job, id_salaire, entreprise) VALUES(?,?,?)""", item)


    ### D_date 
    # Create table D_date
    def create_date(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_date(
                         id_date INTEGER PRIMARY KEY AUTOINCREMENT,
                         date TEXT
        )""")

    # Insert value sinto D_date
    def insert_date(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_date (date) VALUES(?)""", item)

    ### D_titre
    def create_titre(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_titre(
                         id_titre INTEGER PRIMARY KEY AUTOINCREMENT,
                         id_competence INTEGER,
                         id_experience INTEGER,
                         titre TEXT,
                         FOREIGN KEY(id_competence) REFERENCES H_competence(id_competence),
                         FOREIGN KEY(id_experience) REFERENCES H_experience(id_experience)
        )""")

    def insert_titre(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_titre (id_competence, id_experience, titre) VALUES(?,?,?)""", item)

    ### D_source
    def create_source(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_source(
                         id_source INTEGER PRIMARY KEY AUTOINCREMENT,
                         source TEXT
        )""")

    def insert_source(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_source (source) VALUES(?)""", item)

    ### D_location
    def create_location(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_location(
                         id_location INTEGER PRIMARY KEY AUTOINCREMENT,
                         id_departement INTEGER,
                         ville TEXT,
                         longitude,
                         latitude,
                         FOREIGN KEY(id_departement) REFERENCES H_depatement(id_departement)
        )""")

    def insert_location(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_location (id_departement, ville, longitude, latitude) VALUES(?,?,?,?)""", item)

    ### D_token
    
    def create_token(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS D_token(
                         id_token INTEGER PRIMARY KEY AUTOINCREMENT,
                         token TEXT
        )""")

    def insert_token(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO D_token (token) VALUES(?)""", item)


    # F_description
    def create_description(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS F_description(
                         id_description INTEGER PRIMARY KEY AUTOINCREMENT,
                         id_entreprise INTEGER,
                         id_date INTEGER,
                         id_titre INTEGER,
                         id_source INTEGER,
                         id_location INTEGER,
                         id_token INTEGER,
                         description TEXT,
                         FOREIGN KEY(id_entreprise) REFERENCES D_entreprise(id_entreprise),
                         FOREIGN KEY(id_date) REFERENCES D_date(id_date),
                         FOREIGN KEY(id_titre) REFERENCES D_titre(id_titre),
                         FOREIGN KEY(id_source) REFERENCES D_source(id_source),
                         FOREIGN KEY(id_location) REFERENCES D_location(id_location),
                         FOREIGN KEY(id_token) REFERENCES D_token(id_token)
        )""")

    def insert_description(self,item):
        self.cur.execute("""INSERT OR IGNORE INTO F_description (id_entreprise, id_date, id_titre, id_source, id_location, id_token, description) VALUES(?,?,?,?,?,?,?)""", item)

    def commit_change(self):
        self.con.commit()

    def close_connection(self):
        self.con.close()

    def req(self, requete):
        self.cur.execute(requete)
        rows = self.cur.fetchall()
        return rows
