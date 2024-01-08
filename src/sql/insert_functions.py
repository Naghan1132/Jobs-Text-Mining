import sqlite3

# Function to insert data into a dimension table with value check
def insert_dimension(table_name, column_name, value, cursor):
    cursor.execute(f"SELECT {column_name}_id FROM {table_name} WHERE {column_name} = ?", (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (?)", (value,))
        cursor.execute(f"SELECT last_insert_rowid() AS {column_name}_id")
        return cursor.fetchone()[0]
    
# Function to insert data into a dimension table with value check
def insert_location(latitude, longitude, location, departement, region, cursor):
    cursor.execute(f"SELECT latitude FROM D_location WHERE latitude = ?", (latitude,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(f"INSERT INTO D_location (latitude, longitude, location, departement, region) VALUES (?,?,?,?,?)", 
                       (latitude, longitude, location, departement, region))
        cursor.execute(f"SELECT last_insert_rowid() AS location_id")
        return cursor.fetchone()[0]

    
def insert_observations(df, cursor):
    
    for index, row in df.iterrows():
    
        # Extract values from the DataFrame row
        title = row['title']
        type_job = row['type_job']
        salary = row['salary']
        company = row['compagny']
        location = row['location']
        region = row['region']
        departement = row['departement']
        latitude = row['latitude']
        longitude = row['longitude']
        experience = row['experience']
        skills = row['skills']
        date = row['date']
        description = row['description']
        tokens = row['tokens']
        source = row['source']

        # Insert Observation
        #departement_id_1 = insert_departement(departement, region, cursor)
        skills_id_1 = insert_dimension('D_skills', 'skills', skills, cursor)
        experience_id_1 = insert_dimension('D_experience', 'experience', experience, cursor)
        tokens_id_1 = insert_dimension('D_tokens', 'tokens', tokens, cursor)
        source_id_1 = insert_dimension('D_source', 'source', source, cursor)
        company_id_1 = insert_dimension('D_company', 'company', company, cursor)
        type_job_id_1 = insert_dimension('D_type_job', 'type_job', type_job, cursor)
        salary_id_1 = insert_dimension('D_salary', 'salary', salary, cursor)
        date_id_1 = insert_dimension('D_date', 'date', date, cursor)
        #location_id_1 = insert_dimension('D_location', 'location', location, cursor)
        title_id_1 = insert_dimension('D_title', 'title', title, cursor)
        location_id_1 = insert_location(latitude, longitude, location, departement, region, cursor)
        
        # cursor.execute(f"INSERT INTO D_location (departement_id) VALUES (?)", (departement_id_1))
        
        cursor.execute("INSERT INTO F_description (company_id, type_job_id, date_id, location_id, title_id, salary_id, skills_id, experience_id, tokens_id, description) "
                       "VALUES (?, ?, ?, ?, ?, ?,?,?,?,?)",
                       (company_id_1, type_job_id_1 ,date_id_1, location_id_1, title_id_1, salary_id_1,skills_id_1, experience_id_1, tokens_id_1, description))
        
    
    # conn.commit()
    # conn.close()
    



    
    
