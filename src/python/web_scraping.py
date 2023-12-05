import time
from scraping import *
from build_data import *

import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # N'oubliez pas cette ligne
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException



# Indeed OK (pagination + scrapping OK)
# APEC OK (pagination + scrapping OK)
# Glassdoor OK (pagination + scrapping OK)
# hello work en test
# Pole Emploi OK (pagination + scrapping OK)

# LinkedIn KO (compliqué à revoir, faut se connecter etc...)
# Emploi Public KO (pas de mots clé dans l'url)
# Emploi Territorial (moteur de recherche très mauvais => à abandonner)

def build_url_job_research(job_name):
    urls = ["https://fr.indeed.com/jobs?q=JobToInput&l=France",
        "https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=JobToInput",
        "https://www.glassdoor.fr/Emploi/france-JobToInput-emplois-SRCH_IL.0,6_IN86_KO7,11.htm",
        "https://candidat.pole-emploi.fr/offres/recherche?motsCles=JobToInput&offresPartenaires=true&rayon=10&tri=0"]

    cpt = 0
    modified_urls = []
    for url in urls:
        if cpt == 0:
            job_name_modified = job_name.replace(" ", "+")
            modified_url = url.replace("JobToInput",job_name_modified)

        elif cpt == 1:
            job_name_modified = job_name.replace(" ", " ") # do nothing
            modified_url = url.replace("JobToInput",job_name_modified)

        elif cpt == 2:
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
                
        if cpt == 3:
            job_name_modified = job_name.replace(" ", "-")
            modified_url = url.replace("JobToInput",job_name_modified)
        
        modified_urls.append(modified_url)
        cpt = cpt + 1

    return modified_urls


def create_driver():
    # Configurer les options du navigateur en mode headless
    chrome_options = Options()
    #chrome_options.add_argument('--headless') # pas d'utilisation de l'interface graphique
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')  # Taille de la fenêtre pour éviter la détection de tête sans fenêtre (parfait)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Instancier le navigateur avec les options configurées
    driver = webdriver.Chrome(options=chrome_options)
    return(driver)



def web_scrap(driver,df,url,n_posts_max = 5,n_current_posts = 0):

    if(n_current_posts == n_posts_max):
        return
    
    if "indeed" in url:
        source = "indeed"
    elif "apec" in url:
        source = "apec" 
    elif "glassdoor" in url:
        source = "glassdoor"
    elif "pole-emploi" in url:
        source = "pole_emploi"
    else:
        source = "unknown"

    print("URL actuelle:", url)

    driver.get(url)

    # Attendre que la page soit complètement chargée
    driver.implicitly_wait(5)
    time.sleep(3)
    # Récupérer la page source (HTML) actuelle
    html_source = driver.page_source


    if source == "apec":
        cpt = 1
        while True:
            base_url = driver.current_url
            html_source = driver.page_source
            links = get_apec_job_links(html_source)     

            if links is None:
                driver.quit()
                return df
            print(links)
            
            n_current_posts = n_current_posts + len(links) 
            print("nombre jobs : ",n_current_posts)
            
            for link in links:    
                if link is not None:
                    driver.get("https://www.apec.fr"+link)
                    print(link)
                    time.sleep(2)
                    html_source = driver.page_source
                    df = add_row(df,scrap_apec_job(html_source))
                time.sleep(1) # ajouter du temps sinon l'anti-bot détecte
            
            if n_current_posts >= n_posts_max:
                driver.quit()
                return df
            else:
                #url = base_url+"&page="+str(cpt)
                #test
                #typesConvention=143687&typesConvention=143706&selectedIndex=13&page=0
                # pb de ça !! c'est le numéro des emplois, alors il faut ajouter 19 à chaue fois surement

                # OU ALORS JSUTE CLIUER SUR 'OFFRE SUIVANTE' VIA LE POST CA MARCHE

                # ou alors juste appuyer sur page-link  
                #suivant_button = driver.find_element(By.CSS_SELECTOR, "a.page-link")
                driver.get(base_url)
                suivant_button = driver.find_element(By.CSS_SELECTOR, 'a[class="page-   link"]') 
                driver.execute_script("arguments[0].click();", suivant_button)
                time.sleep(3) # attendre que les offres chargent
                #print(url)
                #driver.get(url)
                #cpt += 1
                #time.sleep(2) # attendre que les offres chargent

            # régler le scrapping de type_job et location,ça s'inverse 
            # et aussi régler probleme pagination, enfin page suivante quoi

    elif source == "pole_emploi":
        cookies = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="footer_tc_privacy_button_2"]'))
            )

        if cookies is not None:
            driver.execute_script("arguments[0].click();", cookies)
            time.sleep(2)

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
                        time.sleep(1)
                        html_source = driver.page_source
                        df = add_row(df,scrap_pole_job(html_source))
                      
            n_current_posts = n_current_posts + len(links) 
            print("nombre jobs : ",n_current_posts)

            if n_current_posts >= n_posts_max:
                driver.quit()
                return df
            else:
                #bouton page suivante
                suivant_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
                driver.execute_script("arguments[0].click();", suivant_button)
                time.sleep(3) # attendre que les offres chargent



    elif source == "indeed":
        
        while True:
            base_url = driver.current_url
            html_source = driver.page_source
            

            links = get_linkedin_job_links(html_source)
            if links is None:
                driver.quit()
                return df
            
            n_current_posts = n_current_posts + len(links) 
            print("nombre jobs : ",n_current_posts)
    
            for link in links:    
                if link is not None:    
                    driver.get("https://fr.indeed.com/viewjob?jk="+str(link))
                    time.sleep(5)
                    html_source = driver.page_source
                    df = add_row(df,scrap_indeed_job(html_source))
                time.sleep(3) # ajouter du temps sinon l'anti-bot detecte
            
            if n_current_posts >= n_posts_max:
                driver.quit()
                return df
            else:
                driver.get(base_url)
                # clicker sur la page d'après
                suivant_button = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"].css-akkh0a') 
                # appyuer sur le bouton suivant "Plus d'offres d'emploi"
                driver.execute_script("arguments[0].click();", suivant_button)
                time.sleep(3) # attendre que les offres chargent


    elif source == "glassdoor":

        # cliquez sur une offre => cliquez sur "Voir plus" => scrapping => cliquez sur l'offre suivante etc....
        
        while(True):

            jobs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class="JobsList_jobListItem__JBBUV"]'))
            )

            time.sleep(2)

            if jobs is None:
                driver.quit()
                return df

            print(len(jobs))

            if len(jobs) >= n_posts_max:
                #jobs = jobs[:n_posts_max] # prends les n posts demandés
                break  # Sortir de la boucle si le nombre d'offres souhaité est atteint


            # appyuer sur le bouton suivant "Plus d'offres d'emploi"
            suivant_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="load-more"]'))
            )
    
            driver.execute_script("arguments[0].click();", suivant_button)
            
            # attendre que les nouvelles offres soient chargées
            time.sleep(2)

            # Trouver le bouton de la popup 
            closeButton = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="CloseButton"]'))
            )
            if closeButton is not None:
                # Cliquer sur le bouton de la popup si elle existe
                driver.execute_script("arguments[0].click();", closeButton)
                time.sleep(2)

        # scrapper toutes les offres récupérées
        for job in jobs:
            driver.execute_script("arguments[0].click();", job) # works
            time.sleep(10)
            html_source = driver.page_source
            df = add_row(df,scrap_glassdoor_job(html_source))
          

        driver.quit()
        return df

    else:
        print("Source inconnue")
        driver.quit()
        return df



def main_web_scraping(job_name,n_posts_max = 50):
    urls = build_url_job_research(job_name)
    for url in urls:
        df = create_df()
        driver = create_driver()
        df = web_scrap(driver,df,url,n_posts_max=n_posts_max)
        save_df(df,df['source'][0])

#main_web_scraping(job_name,45)

job_name = "Data Scientist"
urls = build_url_job_research(job_name)

driver = create_driver()
df = create_df()
df = web_scrap(driver,df,urls[1],n_posts_max=45)
save_df(df,df['source'][0])




# to do -> rajouter la date de publication de l'offre ??? ou date de l'alimentaion dans la base de données
# tester si il n'y a pas ou plus de jobs à scrapper !!

# réger type_job et salaire Glassdoor !!!
# ajouter type_job et salaire pour Indeed !!!
# extraire les compétences avec une recherche dans la description comme pour le salaire indeed etc...
# probleme de concatenation de texte dans glassdoor (quelques fois) => Type post : CadreSalaire : 30k    




# web scrap pole emploi
# https://candidat.pole-emploi.fr/offres/recherche?motsCles=Data&offresPartenaires=true&rayon=10&tri=0