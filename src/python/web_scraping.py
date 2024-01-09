import time
from scraping import *
from build_data import *
import os

import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
        "https://fr.indeed.com/jobs?q=JobToInput&l=France&from=searchOnHP",
        "https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=JobToInput",
        "https://www.glassdoor.fr/Emploi/france-JobToInput-emplois-SRCH_IL.0,6_IN86_KO7,11.htm",
        "https://candidat.pole-emploi.fr/offres/recherche?motsCles=JobToInput&offresPartenaires=true&rayon=10&tri=0",
        "https://www.welcometothejungle.com/fr/jobs?refinementList%5Boffices.country_code%5D%5B%5D=FR&query=JobToInput&page=1"]
    
    urls = []
    for s in sites:
        if s == "Indeed":
            urls.append(base_urls[0])
        elif s == "Apec":
            urls.append(base_urls[1])
        elif s == "Glassdoor":
            urls.append(base_urls[2])
        elif s == "Pole_Emploi":
            urls.append(base_urls[3])
        elif s == "Welcome_to_the_jungle":
            urls.append(base_urls[4])
        

    modified_urls = []
    for url in urls:
        if "indeed" in url:
            job_name_modified = job_name.replace(" ", "+")
            modified_url = url.replace("JobToInput",job_name_modified)

        elif "apec" in url:
            job_name_modified = job_name.replace(" ", " ") # do nothing
            modified_url = url.replace("JobToInput",job_name_modified)

        elif "glassdoor" in url:
            job_name = job_name.lower()
            job_name_modified = job_name.replace(" ", "-")
            modified_url = url.replace("JobToInput",job_name_modified)

            # Le nombre de caractere dans le job et dans la ville change un parametre dans la requete donc ajouter le parametre
            debut_sous_chaine = "https://www.glassdoor.fr/Emploi/"
            fin_sous_chaine = "-emplois"

            index_debut = modified_url.find(debut_sous_chaine) + len(debut_sous_chaine)
            index_fin = modified_url.find(fin_sous_chaine)
        
            # Extraire la sous-chaîne entre les indices
            sous_chaine_interieure = modified_url[index_debut:index_fin]
            nombre_caracteres = len(sous_chaine_interieure)

            
            match = re.search(r',(\d+)\.htm', modified_url)
            if match:
                # Remplacer la valeur par la nouvelle valeur
                modified_url = re.sub(r',\d+\.htm', f',{nombre_caracteres}.htm', modified_url)
                
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
    #chrome_options.add_argument('--headless') # pas d'utilisation de l'interface graphique
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')  # Taille de la fenêtre pour éviter la détection de tête sans fenêtre (parfait)
    #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0")
    driver = webdriver.Chrome(options=chrome_options)
    return(driver)



def web_scrap(df,url,n_posts_max):    
    
    if "indeed" in url:
        source = "indeed"
    elif "apec" in url:
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

    if source == "indeed":                
        while True:
            base_url = driver.current_url
            html_source = driver.page_source

            links,dates = get_indeed_job_links(html_source)
            if links is None:
                driver.quit()
                return df

            for link in links:    
                if link is not None:    
                    driver.get("https://fr.indeed.com/viewjob?jk="+str(link))
                    # checkbox anti - bot OK
                    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Widget containing a Cloudflare security challenge']")))
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ctp-checkbox-label"))).click()
                    print("CAPTCHA vérifié")
                    time.sleep(8)
                    # attendre que la page job se charge
                    # try:
                    #     WebDriverWait(driver, 20).until(
                    #         EC.presence_of_element_located((By.CSS_SELECTOR, "h1.jobsearch-JobInfoHeader-title.css-1hwk56k.e1tiznh50"))
                    #     )
                    # except TimeoutException:
                    #     print("err")
                    
                 
                    html_source = driver.page_source
                    df = add_row(df,scrap_indeed_job(html_source,dates[links.index(link)]))
                    n_current_posts += 1
                    if n_current_posts >= n_posts_max:
                        driver.quit()
                        return df
                time.sleep(3) # ajouter du temps sinon l'anti-bot detecte
            
            driver.get(base_url)
            # clicker sur la page d'après
            suivant_button = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"].css-akkh0a') 
            # appyuer sur le bouton suivant "Plus d'offres d'emploi"
            driver.execute_script("arguments[0].click();", suivant_button)
            time.sleep(3) # attendre que les offres chargent

    elif source == "apec":
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



def concat_data(sites,folder_path='src/data/'):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Le dossier {folder_path} n'existe pas.")
    dfs = []
    list_csv = [site + ".csv" for site in sites]  # Add ".csv" to each element in the list
    for filename in list_csv:
        file_path = os.path.join(folder_path, filename)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            dfs.append(df)   
    concatenated_df = pd.concat(dfs, ignore_index=True)
    output_file_path = os.path.join(folder_path, 'all_data.csv')
    concatenated_df.to_csv(output_file_path, index=False)


def main_web_scraping(job_name,n_posts_max,sites):
    urls = build_url_job_research(job_name,sites)
    for url in urls:
        df = create_df()
        df = web_scrap(df,url,n_posts_max=n_posts_max)
        save_df(df,df['source'][0])
    concat_data(sites)


#liste_sites = ["Apec","Indeed","Pole_Emploi", "Welcome_to_the_jungle"]
liste_sites = ["Welcome_to_the_jungle","Apec","Pole_Emploi"]
job_name = "Data"
main_web_scraping(job_name,100,liste_sites)


# Indeed à rajouter une sécurité pour le scrapping.... plus possible maintenant

# TODO =>
# re-scrapper Indeed pour les compétences
# mettre en dataframe plutot qu'en csv (faire les 2 en réalité, c'est pas dur)

# Homogénisation format de type_job (CDI, CDD etc...), expérience, date (jour/mois/annee), etc... !!!
# réduire au MAXIMUM les time.sleep() => pour diminuer le temps de scrapping


# Axes d'analyse :
# - barplot des type de contrats ?
# - filtres carte ou autres (date, type de contrat, salaire, etc...)
# - moteur de recherche sur les comptétences ou tokens sinon : et ressortir les offres qui correspondent le mieux
# - améliorer le wordcloud
