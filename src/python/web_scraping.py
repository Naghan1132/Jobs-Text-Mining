import time
from scraping import *
from build_data import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # N'oubliez pas cette ligne
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException



urls = ["https://fr.indeed.com/jobs?q=data&l=&from=searchOnHP&vjk=a6feb24775e416a2",
        "https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=Data&typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687",
        "https://www.emploipublic.fr/offre-emploi/resultats-offre",
        "https://www.emploi-territorial.fr/emploi-mobilite/?adv-search=Data",
        "https://www.glassdoor.fr/Emploi/france-data-emplois-SRCH_IL.0,6_IN86_KO7,11.htm"]


# Indeed OK (pagination OK)
# APEC OK (pagination OK)
# Glassdoor OK (pagination OK)


# LinkedIn KO (compliqué à revoir)
# Emploi Public KO (pas de mots clé dans l'url)
# Emploi Territorial (moteur de recherche très mauvais => à abandonner surement)


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
    elif "emploi-public" in url:
        source = "emploi-public"
    elif "emploi-territorial" in url:
        source = "emploi-territorial"
    elif "glassdoor" in url:
        source = "glassdoor"
    else:
        source = "unknown"

    print("URL actuelle:", url)

    driver.get(url)
    # Attendre que la page soit complètement chargée
    driver.implicitly_wait(5)
    # Récupérer la page source (HTML) actuelle
    html_source = driver.page_source


    if source == "apec":
        # APEC scrap + pagination OK 
        cpt = 1
        while True:
            base_url = driver.current_url
            html_source = driver.page_source
            links = get_apec_job_links(html_source)        

            n_current_posts = n_current_posts + len(links) 
            print("nombre jobs : ",n_current_posts)
            
            for link in links:    
                if link is not None:
                    driver.get("https://www.apec.fr"+link)
                    html_source = driver.page_source
                    df = add_row(df,scrap_apec_job(html_source))
                time.sleep(1) # ajouter du temps sinon l'anti-bot détecte
            
            if n_current_posts >= n_posts_max:
                return df
            else:
                url = "https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=Data&typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687&page="+str(cpt)
                driver.get(url)
                cpt += 1
                time.sleep(2) # attendre que les offres chargent

        
    elif source == "indeed":
        
        while True:
            base_url = driver.current_url
            html_source = driver.page_source
            

            links = get_linkedin_job_links(html_source)
            n_current_posts = n_current_posts + len(links) 
            print("nombre jobs : ",n_current_posts)
        
            
            for link in links:    
                if link is not None:
                    driver.get("https://www.indeed.com"+link)
                    html_source = driver.page_source
                    df = add_row(df,scrap_indeed_job(html_source))
                time.sleep(3) # ajouter du temps sinon l'anti-bot detecte
            
            if n_current_posts >= n_posts_max:
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

        jobs = []
        
        while(True):

            jobs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class="JobsList_jobListItem__JBBUV"]'))
            )

            time.sleep(10)

            print(len(jobs))

            if len(jobs) >= n_posts_max:
                jobs = jobs[:n_posts_max] # prends les n posts demandés
                break  # Sortir de la boucle si le nombre d'offres souhaité est atteint


            # appyuer sur le bouton suivant "Plus d'offres d'emploi"
            suivant_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="load-more"]'))
            )
            #suivant_button.click()
            print("Suivant button clicked")
            driver.execute_script("arguments[0].click();", suivant_button)
            
            # attendre que les nouvelles offres soient chargées
            time.sleep(10)

           
            closeButton = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="CloseButton"]'))
                )
            try:
                # Trouver le bouton de la popup 
                closeButton = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="CloseButton"]'))
                )

                # Cliquer sur le bouton de la popup
                driver.execute_script("arguments[0].click();", closeButton)
                print("Close button clicked")
                time.sleep(10)
              

            except NoSuchElementException:
                print("Pas de popup")
    

        for job in jobs:
            driver.execute_script("arguments[0].click();", job) # works
            html_source = driver.page_source
            df = add_row(df,scrap_glassdoor_job(html_source))
            #scrap_glassdoor_job(html_source)

    else:
        print("Source inconnue")
        driver.quit()
        exit()


    driver.quit()
    return df




#driver = create_driver()
#df = create_df()
#df = web_scrap(driver,df,urls[1],n_posts_max=45)
#save_df(df,df['source'][0])


urls_OK = ["https://fr.indeed.com/jobs?q=data&l=&from=searchOnHP&vjk=a6feb24775e416a2",
        "https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=Data&typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687",
       ]


def main_web_scraping(urls,n_posts_max = 50):
    for url in urls:
        df = create_df()
        driver = create_driver()
        df = web_scrap(driver,df,url,n_posts_max=n_posts_max)
        save_df(df,df['source'][0])

main_web_scraping(urls_OK,45)

