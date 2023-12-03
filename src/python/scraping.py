from bs4 import BeautifulSoup
from scrap_description import *
import time

def get_linkedin_job_links(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    h2_tags = soup.find_all('h2', class_=['jobTitle', 'css-mr1oe7', 'eu4oa1w0'])
    list_id = [h.find('a')['data-jk'] if h.find('a') else None for h in h2_tags]
    return list_id



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
    description = ""
   
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
    
    if body_div is not None:    
        details = body_div.find_all('p')
        for d in details:
            #print(d.text)
            description += d.text + " "

    if description != "":
        scrap_description_apec(description,["salary","type_job"])

    print("=============")

    liste = [title, type_job,salary,compagny, location,description,source]
    
    return liste

    


def scrap_indeed_job(html_source):

    soup = BeautifulSoup(html_source, 'html.parser')

    source = "indeed"

    div_title = soup.find('h1', class_='jobsearch-JobInfoHeader-title')
    
    if  div_title is None:
        print("NULL")
        print("\n ================== \n")
        return 
    
    title = div_title.find('span')
    location = soup.find('div', {'data-testid':['inlineHeader-companyLocation']})

    infos_widget = soup.find_all('div', {'class':['css-tvvxwd', 'ecydgvn1']})
    print(infos_widget)
    description = soup.find('div', {'id':['jobDescriptionText']})
    details_post = soup.find('div',{'id': ['jobDetailsSection']})
    compagny_div = soup.find('div', {'data-testid':['inlineHeader-companyName']})
    compagny = compagny_div.find('a', {'class':['css-1f8zkg3','e19afand0']})
    salary_div = soup.find('div', {'id':['salaryInfoAndJobType']})
    salary = ""
    type_job = ""
    skills = ""
    skills_ul = soup.find('ul',{'class':['js-match-insights-provider-bcv69m','eu4oa1w0']})
    print(skills_ul)
    if skills_ul is not None:
        skills = skills_ul.find('li')
        print(skills)
    
    #print(skills_ul.find_all('li'))
    print(salary)
    print(type_job)
    print(skills)
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

    if compagny:
        compagny = compagny.text.strip()
        print(f"compagny : {compagny}")
    else:
        compagny = ""
        print("Aucun emplacement trouvé.")

    if description:
        description = description.text.strip()
        fields_to_find = []
        if not salary:
            fields_to_find.append("salary")
        if not type_job:
            fields_to_find.append("type_job")
        if not skills_ul:
            fields_to_find.append("skills")
            
        scrap_description_indeed(description,["salary","type_job"])
    else:
        description = ""
        print("Aucun emplacement trouvé.")



    print("\n ================== \n")

    liste = [title, type_job,salary,compagny, location,description,source]

    return liste

    
def scrap_glassdoor_job(html_source):
    
    soup = BeautifulSoup(html_source, 'html.parser')
    job_header = soup.find('header', {'class':['JobDetails_jobDetailsHeaderWrapper__iHvDC JobDetails_sticky__fQ4Aq']})
     
    source = "glassdoor"

    compagny = job_header.find('span', {'class': ['EmployerProfile_employerName__Xemli']})
    title = soup.find('div', {'class': ['JobDetails_jobTitle__Rw_gn']})
    description = soup.find('div', {'class':['JobDetails_jobDescription__6VeBn','JobDetails_blurDescription__fRQYh']})
    location = job_header.find('div', {'class': ['JobDetails_location__MbnUM']})
    # Recherchez le paragraphe contenant "Type d'emploi"
    type_job = soup.find('p', text=lambda t: t and "Type d'emploi" in t)
    salaire = soup.find('p', text=lambda t: t and "Salaire" in t)
    skills = soup.find('p', text=lambda t: t and "Compétences" in t)


    if type_job:
        type_job = type_job.text.strip()
        print(f"type_job : {type_job}")
    else:
        type_job = ""
        print("Aucun emplacement trouvé.")
    if salaire:
        salaire = salaire.text.strip()
        print(f"salaire : {salaire}")
    else:
        salaire = ""
        print("Aucun emplacement trouvé.")
    if title:
        title = title.text.strip()
        print(f"title : {title}")
    else:
        title = ""
        print("Aucun emplacement trouvé.")

    if compagny:    
        compagny = compagny.text.strip()
        print(f"compagny : {compagny}")
    else:
        print("Aucun emplacement trouvé.")
    if skills:    
        skills = skills.text.strip()
        print(f"skills : {skills}")
    else:
        print("Aucun emplacement trouvé.")

    if description:
        description = description.text.strip()
        fields_to_find = []
        if not salaire:
            fields_to_find.append("salary")
        if not type_job:
            fields_to_find.append("type_job")
        if not skills:
            fields_to_find.append("type_job")
            
        scrap = scrap_description_glassdoor(description,fields_to_find)
    else:
        description = ""
        print("Aucun emplacement trouvé.")
    if location:
        location = location.text.strip()
        print(f"location : {location}")
    else:
        location = ""
        print("Aucun emplacement trouvé.")
    

    print("\n ================== \n")

    liste = [title,type_job,salaire,compagny,location,description,source]
    return liste