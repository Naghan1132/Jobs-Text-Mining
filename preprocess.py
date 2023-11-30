from bs4 import BeautifulSoup


def get_linkedin_job_links(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    
    # Trouver toutes les balises <h2> avec les classes spécifiées
    h2_tags = soup.find_all('h2', class_=['jobTitle', 'jobTitle-newJob', 'css-mr1oe7', 'eu4oa1w0'])

    # Extraire les liens des balises <a> à partir des balises <h2>
    list_links = [h.find('a')['href'] if h.find('a') else None for h in h2_tags]

    return list_links



def get_apec_job_links(html_source):
    # Utiliser BeautifulSoup pour traiter les données
    soup = BeautifulSoup(html_source, 'html.parser')

    # Vous pouvez maintenant utiliser BeautifulSoup pour extraire et manipuler les données de la page
    # Récupérer toutes les divs avec la classe "container-result"
    container_result = soup.find_all('div', class_='container-result')

    divs_emplois = []

    for div_container in container_result:
        divs = div_container.find_all('div', recursive=False)[:-1] # sauf le dernier toujours un None
        divs_emplois.extend(divs)

    list_link = []
    for emploi in divs_emplois:
         lien = emploi.find('a')['href'] if emploi.find('a') else None
         list_link.append(lien)
    return(list_link)



def preprocess_apec_job(html_source):
   
     # Utiliser BeautifulSoup pour traiter les données
    soup = BeautifulSoup(html_source, 'html.parser')

    # Récupérer toutes les divs avec la classe "card-body"
    job_detail = soup.find('div', class_='card-body')
    print(job_detail)
    detail = job_detail.find('div', class_='details-post')
    print(detail)


def preprocess_indeed_page(html_source):

     # Utiliser BeautifulSoup pour traiter les données
    soup = BeautifulSoup(html_source, 'html.parser')

    div_title = soup.find('h1', class_='jobsearch-JobInfoHeader-title')
    title = div_title.find('span').text
    print(title)
    location = soup.find('div', class_='css-6z8o9s eu4oa1w0').text
    print(location)
 
    type_job = soup.find('div', {'class':['css-tvvxwd', 'ecydgvn1']})
    print(type_job)

    print("\n ================== \n")

    
def get_glassdoor_job_links(html_source):
     # Utiliser BeautifulSoup pour traiter les données
    soup = BeautifulSoup(html_source, 'html.parser')

    container_result = soup.find_all('button', class_='JobCard_trackingLink__zUSOo')

    list_link = []
    for c in container_result:
        list_link.append(c['href'])

    return(list_link)

def preprocess_glassdoor_page(html_source):

     # Utiliser BeautifulSoup pour traiter les données
    soup = BeautifulSoup(html_source, 'html.parser')
    #print(soup)
    
    title = soup.find('div', {'class': 'JobDetails_jobTitle__Rw_gn'}).text
    print(title)
    #div = soup.find_all('div', class_='JobDetails_jobDetailsHeader__qKuvs')
    #print(div)
    #location = div.find('div', class_='JobDetails_location__MbnUM').text
    #print(location)
  
 
    #type_job = soup.find('div', {'class':['css-tvvxwd', 'ecydgvn1']})
    

    print("\n ================== \n")