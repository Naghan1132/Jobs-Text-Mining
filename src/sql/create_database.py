import sqlite3

def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('jobs.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS H_departement (
        departement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        departement TEXT,
        region TEXT
        )''')

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_location (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        departement_id INTEGER,
        FOREIGN KEY (departement_id) REFERENCES H_departement(departement_id)
        )''')
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_salary (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        salary TEXT
        )''')
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_type_job(
        type_job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_job TEXT
        )''')
        
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_company (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT
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
        '''CREATE TABLE IF NOT EXISTS D_skills (
        skills_id INTEGER PRIMARY KEY AUTOINCREMENT,
        skills TEXT
        )''')
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_title (
        title_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
        )''')
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_experience (
        experience_id INTEGER PRIMARY KEY AUTOINCREMENT,
        experience TEXT
        )''')
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS D_tokens (
        tokens_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tokens TEXT
        )''')
    

    # Create the "Fact" table with foreign key references
    create_fact_table_sql = '''
    CREATE TABLE IF NOT EXISTS F_description (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        company_id INTEGER,
        type_job_id INTEGER,
        date_id INTEGER,
        location_id INTEGER,
        salary_id INTEGER,
        skills_id INTEGER,
        title_id INTEGER,
        experience_id INTEGER,
        tokens_id INTEGER,
        description TEXT,
        FOREIGN KEY (source_id) REFERENCES D_source(source_id),
        FOREIGN KEY (company_id) REFERENCES D_company(company_id),
        FOREIGN KEY (type_job_id) REFERENCES D_type_job(type_job_id),
        FOREIGN KEY (salary_id) REFERENCES D_salary(salary_id),
        FOREIGN KEY (date_id) REFERENCES D_date(date_id),
        FOREIGN KEY (location_id) REFERENCES D_location(location_id),
        FOREIGN KEY (skills_id) REFERENCES D_skills(skills_id),
        FOREIGN KEY (title_id) REFERENCES D_title(title_id),
        FOREIGN KEY (experience_id) REFERENCES D_experience(experience_id),
        FOREIGN KEY (tokens_id) REFERENCES D_tokens(tokens_id)
    );
    '''
    cursor.execute(create_fact_table_sql)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    

create_database()