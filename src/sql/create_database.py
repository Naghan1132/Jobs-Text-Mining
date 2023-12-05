import sqlite3

def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('job_database.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create the dimension tables
    create_title_table_sql = '''
    CREATE TABLE IF NOT EXISTS d_title (
        title_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
    );
    '''
    cursor.execute(create_title_table_sql)

    create_type_table_sql = '''
    CREATE TABLE IF NOT EXISTS d_type_job (
        type_job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_job TEXT
    );
    '''
    cursor.execute(create_type_table_sql)

    create_company_table_sql = '''
    CREATE TABLE IF NOT EXISTS d_company (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT
    );
    '''
    cursor.execute(create_company_table_sql)

    create_source_table_sql = '''
    CREATE TABLE IF NOT EXISTS d_source (
        source_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT
    );
    '''
    cursor.execute(create_source_table_sql)

    create_time_table_sql = '''
    CREATE TABLE IF NOT EXISTS d_time (
        time_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT
    );
    '''
    cursor.execute(create_time_table_sql)

    create_location_table_sql = '''
    CREATE TABLE IF NOT EXISTS d_location (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ville TEXT,
        departement_id INTEGER,
        FOREIGN KEY (departement_id) REFERENCES h_department(departement_id)
    );
    '''
    cursor.execute(create_location_table_sql)

    create_department_table_sql = '''
    CREATE TABLE IF NOT EXISTS h_department (
        departement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        departement TEXT,
        region TEXT
    );
    '''
    cursor.execute(create_department_table_sql)

    # Create the "Fact" table with foreign key references
    create_fact_table_sql = '''
    CREATE TABLE IF NOT EXISTS Fact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_id INTEGER,
        type_job_id INTEGER,
        source_id INTEGER,
        company_id INTEGER,
        time_id INTEGER,
        location_id INTEGER,
        description TEXT,
        FOREIGN KEY (title_id) REFERENCES d_title(title_id),
        FOREIGN KEY (type_job_id) REFERENCES d_type_job(type_job_id),
        FOREIGN KEY (source_id) REFERENCES d_source(source_id),
        FOREIGN KEY (company_id) REFERENCES d_company(company_id),
        FOREIGN KEY (time_id) REFERENCES d_time(time_id),
        FOREIGN KEY (location_id) REFERENCES d_location(location_id)
    );
    '''
    cursor.execute(create_fact_table_sql)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Run the function to create the database and dimension tables
create_database()

