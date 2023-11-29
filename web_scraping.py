from preprocess import preprocess_indeed_page

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # N'oubliez pas cette ligne
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains



urls = ["https://fr.indeed.com/jobs?q=data&l=&from=searchOnHP&vjk=a6feb24775e416a2",
        "https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=Data&typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687",
        "https://www.emploipublic.fr/offre-emploi/resultats-offre",
        "https://www.glassdoor.fr/Emploi/france-data-emplois-SRCH_IL.0,6_IN86_KO7,11.htm"]

# Indeed OK
# APEC OK
# LinkedIn KO
# Emploi Public OK
# Glassdoor OK

def create_driver():
    # Configurer les options du navigateur en mode headless
    chrome_options = Options()
    chrome_options.add_argument('--headless') # pas d'utilisation de l'interface graphique
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')  # Taille de la fenêtre pour éviter la détection de tête sans fenêtre (parfait)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Instancier le navigateur avec les options configurées
    driver = webdriver.Chrome(options=chrome_options)
    return(driver)

def web_scrap(driver,url,n_pages=1,n_current_page=0):
    if(n_current_page==n_pages):
        return
    
    driver.get(url)
    if "indeed" in url:
        source = "indeed"
    elif "apec" in url:
        source = "apec" 
    elif "emploi-public" in url:
        source = "emploi-public"
    elif "glassdoor" in url:
        source = "glassdoor"
    else:
        source = "unknown"


    # Attendre que la page soit complètement chargée
    driver.implicitly_wait(5)

    # Récupérer la page source (HTML) actuelle
    html_source = driver.page_source

    #### ####

    # page suivante
    if source == "apec":

        preprocess_indeed_page(html_source)

        suivant_button = driver.find_element(By.CSS_SELECTOR, 'a.page-link')
        driver.execute_script("arguments[0].click();", suivant_button)
        url = driver.current_url
        print("URL actuelle:", url)
        web_scrap(driver,url,n_pages,n_current_page+1)

        web_scrap(driver,url,n_pages,n_current_page+1)

    elif source == "indeed":

        preprocess_indeed_page(html_source)

        suivant_button = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"].css-akkh0a')
        driver.execute_script("arguments[0].click();", suivant_button)
        url = driver.current_url
        print("URL actuelle:", url)
        web_scrap(driver,url,n_pages,n_current_page+1)


    # Fermer le navigateur (peut etre pas, pour changer de page etc....)
    driver.quit()

driver = create_driver()
web_scrap(driver,urls[1],n_pages=2)