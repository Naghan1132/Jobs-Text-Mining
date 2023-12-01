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
   
    soup = BeautifulSoup(html_source, 'html.parser')
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


# def get_hello_work_job_links(html_source):
#     soup = BeautifulSoup(html_source, 'html.parser')

#     li_result = soup.find_all('li', class_='!tw-mb-6 ')

#     jobs_id = []
#     list_link_modified = []

#     for li in li_result:
#         first_div = li.find('div', recursive=False)
#         if first_div:
#             id = first_div.get('id').text
#             jobs_id.append(id)

#     for id in jobs_id:
#         link = "https://www.hellowork.com/fr-fr/emplois/"+str(id)+".html"
#         list_link_modified.append(link)

#     return(list_link_modified)


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

    title = ""
    salary = ""
    expericence = ""
   
    outer_div = soup.find('div', class_='col-lg-4')
    if outer_div is not None:
        salary_div = outer_div.find_all('div')[0]
        experience_div = outer_div.find_all('div')[2]
        title_div = outer_div.find_all('div')[3]

        # Accéder au span avec la classe txt à l'intérieur de la quatrième div
        title = title_div.find('span').text
        salary = salary_div.find('span').text
        expericence = experience_div.find('span').text

        
        print(title)
        print(salary)
        print(expericence)

    body_div = soup.find('div',{'class':['col-lg-8 ', 'border-L']})
    description = ""
    if body_div is not None:    
        details = body_div.find_all('p')
        for d in details:
            print(d.text)
            description += d.text + " "

    print("=============")

    return [title, type_job, location,source,description]
    


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

    liste = [title, type_job, location, source,"description"]

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
        title = title.text.strip()
        print(f"title : {title}")
    else:
        title = ""
        print("Aucun emplacement trouvé.")

    if details:
        details = details.text.strip()
        print(f"details : {details}")
    else:
        details = ""
        print("Aucun emplacement trouvé.")
    if location:
        location = location.text.strip()
        print(f"location : {location}")
    else:
        location = ""
        print("Aucun emplacement trouvé.")
    

    print("\n ================== \n")

    liste = [title, "type_job", location, source,details]
    return liste