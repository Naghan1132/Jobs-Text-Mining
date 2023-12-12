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

    
def insert_observations(df, cursor):
    
    for index, row in df.iterrows():
    
        # Extract values from the DataFrame row
        title = row['title']
        type_job = row['type_job']
        salary = row['salary']
        company = row['compagny']
        location = row['location']
        language = row['language']
        skills = row['skills']
        date = row['date']
        description = row['description']
        # source = row['source']

        # Insert Observation
        type_job_id_1 = insert_dimension('H_type_job', 'type_job', type_job, cursor)
        language_id_1 = insert_dimension('H_language', 'language', language, cursor)
        competence_id_1 = insert_dimension('H_competences', 'competence', skills, cursor)
        print(type(type_job_id_1))

        #print(f"type_job_id_1: {type_job_id_1}")
        # source_id_1 = insert_dimension('D_source', 'source', source, cursor)
        company_id_1 = insert_dimension('D_company', 'company', company, cursor)
        salary_id_1 = insert_dimension('D_salary', 'salary', salary, cursor)
        date_id_1 = insert_dimension('D_date', 'date', date, cursor)
        location_id_1 = insert_dimension('D_location', 'location', location, cursor)
        description_id_1 = insert_dimension('D_description', 'description', description, cursor)
        
        # cursor.execute("INSERT INTO D_company (type_job_id)""VALUES (?)",(type_job_id_1))
        # cursor.execute("INSERT INTO D_description (language_id)""VALUES (?)",(language_id_1))
        # cursor.execute("INSERT INTO D_description (competence_id)""VALUES (?)",(competence_id_1))
        
        cursor.execute("INSERT INTO F_title (company_id, date_id, location_id, description_id, salary_id, title) "
                       "VALUES (?, ?, ?, ?, ?, ?)",
                       (company_id_1, date_id_1, location_id_1, description_id_1, salary_id_1, title))
    
    # conn.commit()
    # conn.close()

    
    
    
# old
def insert_observations1(values_list, cursor):

    # Extract values from the list
    title, type_job, salary, compagny, location, language, skills, date, description, source = values_list
    
    # Insert Observation
    type_job_id_1 = insert_dimension('D_type_job', 'type_job', type_job, cursor)
    source_id_1 = insert_dimension('D_source', 'source', source, cursor)
    company_id_1 = insert_dimension('D_company', 'company', compagny, cursor)
    time_id_1 = insert_dimension('D_date', 'date', date, cursor)
    location_id_1 = insert_dimension('D_location', 'ville', location, cursor)
    description_id_1 = insert_dimension('D_description', 'description', description, cursor)

    cursor.execute("INSERT INTO Fact (type_job_id, source_id, company_id, date_id, location_id, description_id, salary, title) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (type_job_id_1, source_id_1, company_id_1, time_id_1, location_id_1, description_id_1, salary, title))
    
    # conn.commit()
    # conn.close()
