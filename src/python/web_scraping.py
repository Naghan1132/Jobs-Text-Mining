import time
from scraping import *
from preprocess_text import *
from build_data import *
import os

import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import sqlite3
import sys


#### RÉSUMÉ ####

# APEC PARFAIT
# Pole Emploi PARFAIT 
# Welcome to the jungle PARFAIT

# Indeed (réessayer quand meme car compétences à scrapper !!!)

# Glassdoor (bco d'infos manquantes/dures à scrapper) => à abandonner
# LinkedIn KO (compliqué à revoir, faut se connecter etc...)
# Emploi Public KO (pas de mots clé dans l'url)
# Emploi Territorial (moteur de recherche très mauvais => à abandonner)
# Hello work KO anti-bot trop fort

def build_url_job_research(job_name,sites):
    base_urls = [
        "https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=JobToInput",
        "https://candidat.pole-emploi.fr/offres/recherche?motsCles=JobToInput&offresPartenaires=true&rayon=10&tri=0",
        "https://www.welcometothejungle.com/fr/jobs?refinementList%5Boffices.country_code%5D%5B%5D=FR&query=JobToInput&page=1"]
    
    urls = []
    for s in sites:
        if s == "Apec":
            urls.append(base_urls[0])
        elif s == "Pole_Emploi":
            urls.append(base_urls[1])
        elif s == "Welcome_to_the_jungle":
            urls.append(base_urls[2])

    modified_urls = []
    for url in urls:
        if "apec" in url:
            job_name_modified = job_name.replace(" ", " ") # do nothing
            modified_url = url.replace("JobToInput",job_name_modified)
                
        elif "candidat.pole-emploi" in url:
            job_name_modified = job_name.replace(" ", "-")
            modified_url = url.replace("JobToInput",job_name_modified)

        elif "welcometothejungle" in url:
            job_name_modified = job_name.replace(" ", " ") # do nothing
            modified_url = url.replace("JobToInput",job_name_modified)
        
        modified_urls.append(modified_url)

    return modified_urls


def create_driver():
    # Configurer les options du navigateur en mode headless
    chrome_options = Options()
    chrome_options.add_argument('--headless') # pas d'utilisation de l'interface graphique
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')      
    chrome_options.add_argument('--window-size=1920x1080')  # Taille de la fenêtre pour éviter la détection de tête sans fenêtre (parfait)
    #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0")
    driver = webdriver.Chrome(options=chrome_options)
    return(driver)



def web_scrap(df,url,n_posts_max):    
    
    if "apec" in url:
        source = "apec" 
    elif "glassdoor" in url:
        source = "glassdoor"
    elif "pole-emploi" in url:
        source = "pole_emploi"
    elif "welcometothejungle" in url:
        source = "welcome_to_the_jungle"
    else:
        source = "unknown"

    print("URL actuelle:", url)

    driver = create_driver()
    driver.get(url)

    # Attendre que la page soit complètement chargée
    driver.implicitly_wait(5)
    time.sleep(3)
    # Récupérer la page source (HTML) actuelle
    html_source = driver.page_source

    n_current_posts = 0


    if source == "apec":
        base_url = driver.current_url
        html_source = driver.page_source
        link = get_first_apec_job_link(html_source)     

        if link is None:
            driver.quit()
            return df
        
        driver.get("https://www.apec.fr"+link)
        html_source = driver.page_source

        while n_current_posts < n_posts_max:
            suivant_button = driver.find_element(By.CSS_SELECTOR, 'a[class="nextpage"]') 
            driver.execute_script("arguments[0].click();", suivant_button)
            #time.sleep(2) # attendre que les offres chargent
            html_source = driver.page_source
            df = add_row(df,scrap_apec_job(html_source))
            n_current_posts += 1
       
        driver.quit()
        return df

    elif source == "pole_emploi":
        try:
            cookies = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "cookie-id"))
            )
            driver.execute_script("arguments[0].click();", cookies)
            
        except TimeoutException:
            while True:
                base_url = driver.current_url
                html_source = driver.page_source
                
                links = get_pole_job_links(html_source)
            
                if links is None:
                    driver.quit()
                    return df
            
                for link in links:    
                        if link is not None:
                            u = "https://candidat.pole-emploi.fr/offres/recherche/detail/"+link
                            driver.get(u)
                            #time.sleep(1)
                            html_source = driver.page_source
                            df = add_row(df,scrap_pole_job(html_source))
                            n_current_posts += 1
                            if n_current_posts >= n_posts_max:
                                driver.quit()
                                return df
                        
                
                # bouton page suivante
                suivant_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
                driver.execute_script("arguments[0].click();", suivant_button)
                #time.sleep(3) # attendre que les offres chargent

    elif source == "welcome_to_the_jungle":
        cpt = 0
        while True:
            base_url = driver.current_url
            html_source = driver.page_source
            links = get_jungle_job_link(html_source)  
            time.sleep(5)   
        
            if links is None:
                driver.quit()
                return df
        
            for link in links:      
                if link is not None:    
                    driver.get("https://www.welcometothejungle.com"+str(link))
                    time.sleep(2)
                    html_source = driver.page_source
                    df = add_row(df,scrap_jungle_job(html_source))
                    n_current_posts += 1
                    if n_current_posts >= n_posts_max:
                        driver.quit()
                        return df
            
            cpt = cpt + 1
            page_modified = "page="+str(cpt)
            base_url = re.sub(r'page=\d+', page_modified, base_url)
            driver.get(base_url)
            time.sleep(3) # attendre que les offres chargent
        
    else:
        print("Source inconnue")
        driver.quit()
        return df




def update_db(concatenated_df):
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_sql = os.path.abspath(os.path.join(chemin_actuel, '..', 'sql'))

    print(concatenated_df.columns)
    print(concatenated_df['departement'])

    # Appliquer la transformation à la colonne 'skills'
    concatenated_df['skills'] = concatenated_df['skills'].apply(clean_column)
    concatenated_df['tokens'] = concatenated_df['tokens'].apply(clean_column)
    concatenated_df['location'] = concatenated_df['location'].apply(clean_column)
    concatenated_df['departement'] = concatenated_df['departement'].apply(clean_column)
    concatenated_df['region'] = concatenated_df['region'].apply(clean_column)
    concatenated_df['title'] = concatenated_df['title'].apply(clean_column)


    print(concatenated_df.head())

    # Connexion à la base de données SQLite
    conn = sqlite3.connect(chemin_sql+'/base_brute.db')
    concatenated_df.to_sql('data', conn, if_exists='replace', index=False)

    conn.close()
    # Importer et exécuter la fonction exec() du fichier execute.py
    chemin_execute_py = os.path.join(chemin_sql, 'execute.py')

    import importlib.util
    # Charger le module execute.py
    spec = importlib.util.spec_from_file_location("execute", chemin_execute_py)
    execute_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(execute_module)

    # Appeler la fonction 'exec' de execute.py
    execute_module.exec() 

def main_web_scraping(job_name,n_posts_max,sites):
    dfs = []
    urls = build_url_job_research(job_name,sites)
    for url in urls:
        df = create_df()
        df = web_scrap(df,url,n_posts_max=n_posts_max)
        dfs.append(df)
        if len(dfs) > 1:
            concatenated_df = pd.concat(dfs, ignore_index=True)
            concatenated_df = imputing_missing_values(concatenated_df)
        else :
            concatenated_df = df
            concatenated_df = imputing_missing_values(concatenated_df)
    update_db(concatenated_df)


