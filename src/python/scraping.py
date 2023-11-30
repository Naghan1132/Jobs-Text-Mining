from bs4 import BeautifulSoup
import time

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



def scrap_apec_job(html_source):
   
    soup = BeautifulSoup(html_source, 'html.parser')

    source = "apec"
    compagny = ""
    type_job = ""
    location = ""

    head_div = soup.find('div', {'class':['card-offer__text']}) 
    if head_div is not None:
        liste = head_div.find('ul')
        li_elements = liste.find_all('li') 
  
        if len(li_elements) >= 1:
            compagny = li_elements[0].text
        if len(li_elements) >= 2:
            type_job = li_elements[1].text
        if len(li_elements) >= 3:
            location = li_elements[2].text

        print(compagny)
        print(location)
        print(type_job)

        print("=============")

    # Récupérer toutes les divs avec la classe "card-body"
    #job_detail = soup.find('div', class_='card-body')
    #print(job_detail)
    #detail = job_detail.find('div', class_='details-post')
    #print(detail)

    return [compagny, location, type_job, source]
    


def scrap_indeed_job(html_source):

    soup = BeautifulSoup(html_source, 'html.parser')

    source = "indeed"

    div_title = soup.find('h1', class_='jobsearch-JobInfoHeader-title')
    
    if  div_title is None:
        print("NULL")
        print("\n ================== \n")
        return 
    
    title = div_title.find('span')
    location = soup.find('div', class_='css-6z8o9s eu4oa1w0')
    type_job = soup.find('div', {'class':['css-tvvxwd', 'ecydgvn1']})


    if title:
        title = title.text.strip()
        print(f"title : {title}")
    else:
        title = ""
        print("Aucun emplacement trouvé.")

    if location:
        location = location.text.strip()
        print(f"location : {location}")
    else:
        location = ""
        print("Aucun emplacement trouvé.")
    
    if type_job:
        type_job = type_job.text.strip()
        print(f"type_job : {type_job}")
    else:
        type_job = ""
        print("Aucun emplacement trouvé.")



    print("\n ================== \n")

    liste = [title, type_job, location, source]

    return liste

    
def scrap_glassdoor_job(html_source):
    
    soup = BeautifulSoup(html_source, 'html.parser')

    source = "glassdoor"
    compagny = soup.find('div', {'class': 'EmployerProfile_employerInfo__GaPbq'})
    title = soup.find('div', {'class': 'JobDetails_jobTitle__Rw_gn'})
    details = soup.find('div', {'class':['JobDetails_jobDescription__6VeBn', 'JobDetails_blurDescription__fRQYh']})
    location = soup.find('div', {'class': 'JobDetails_location__MbnUM'})

    #JobDetails_jobDescription__6VeBn JobDetails_blurDescription__fRQYh
    if compagny:
        compagny_text = compagny.text.strip()
        print(f"compagny : {compagny_text}")
    else:
        print("Aucun emplacement trouvé.")

    if title:
        title_text = title.text.strip()
        print(f"title : {title_text}")
    else:
        print("Aucun emplacement trouvé.")

    if details:
        details_text = details.text.strip()
        print(f"details : {details_text}")
    else:
        print("Aucun emplacement trouvé.")

    if location:
        location_text = location.text.strip()
        print(f"location : {location_text}")
    else:
        print("Aucun emplacement trouvé.")
    
    

    print("\n ================== \n")