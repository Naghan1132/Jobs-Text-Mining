import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
#import Scrapy

#GitHub Jobs API : GitHub propose une API d'emploi qui permet d'accéder aux offres d'emploi publiées sur GitHub. Vous pouvez trouver plus d'informations à l'adresse suivante : GitHub Jobs API.
#LinkedIn API : LinkedIn propose également une API qui peut être utilisée pour accéder à certaines informations sur les offres d'emploi. Cependant, l'accès à l'API LinkedIn est généralement soumis à des restrictions et nécessite une demande d'accès.
#Glassdoor API


# https://scrapeops.io/python-web-scraping-playbook/python-indeed-scraper/



# URL de la page à récupérer 
#url = 'https://www.glassdoor.fr/Emploi/index.htm'

url = "http://en.wikipedia.org/wiki/StackOverflow"
url = 'https://fr.indeed.com/jobs?q=Data&l=&vjk=f57d3991ea539587&advn=5159066406818317'
hdr = {'User-Agent': 'Mozilla/5.0'}

req = Request(url,headers=hdr)
web_page = urlopen(req).read()
soup = BeautifulSoup(web_page,'html.parser')
#print(soup)



# Option 2 :
# Envoyer une requête GET pour obtenir le contenu de la page
response = requests.get(url,headers=hdr)

# Vérifier si la requête a réussi (code 200)
if response.status_code == 200:
    # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupérer le HTML de la page
    html_content = soup.prettify()  # prettify() ajoute une indentation pour rendre le HTML plus lisible

    # Afficher le HTML ou effectuer d'autres opérations
    print(html_content)

else:
    print(f"La requête a échoué avec le code d'état {response.status_code}")