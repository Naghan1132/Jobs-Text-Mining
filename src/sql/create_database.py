import sqlite3

def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('jobs.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS H_department (
        departement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        departement TEXT,
        region TEXT
        )''')

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_location (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        departement_id INTEGER,
        FOREIGN KEY (departement_id) REFERENCES H_department(departement_id)
        )''')
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_salary (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        salary TEXT
        )''')
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS H_type_job(
        type_job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_job TEXT
        )''')
        
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_company (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        type_job_id INTEGER, 
        FOREIGN KEY (type_job_id) REFERENCES H_type_job(type_job_id)
        )''')

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_source (
        source_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT
        )''')


    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_date (
        date_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT
        )''')
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS H_competences (
        competence_id INTEGER PRIMARY KEY AUTOINCREMENT,
        competence TEXT
        )''')
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS H_language (
        language_id INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT
        )''')


    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_description (
        description_id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        language_id INTEGER,
        competence_id INTEGER,
        FOREIGN KEY (language_id) REFERENCES H_language(language_id),
        FOREIGN KEY (competence_id) REFERENCES H_competences(competence_id)
        )''')
    
    

    # Create the "Fact" table with foreign key references
    create_fact_table_sql = '''
    CREATE TABLE IF NOT EXISTS F_title (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        company_id INTEGER,
        date_id INTEGER,
        location_id INTEGER,
        salary_id INTEGER,
        competence_id INTEGER,
        description_id INTEGER,
        title TEXT,
        FOREIGN KEY (source_id) REFERENCES D_source(source_id),
        FOREIGN KEY (company_id) REFERENCES D_company(company_id),
        FOREIGN KEY (salary_id) REFERENCES D_salary(salary_id),
        FOREIGN KEY (date_id) REFERENCES D_date(date_id),
        FOREIGN KEY (location_id) REFERENCES D_location(location_id),
        FOREIGN KEY (competence_id) REFERENCES D_competences(competence_id),
        FOREIGN KEY (description_id) REFERENCES D_description(description_id)
    );
    '''
    cursor.execute(create_fact_table_sql)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    

create_database()