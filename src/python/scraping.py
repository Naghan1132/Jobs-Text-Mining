from bs4 import BeautifulSoup
from scrap_description import *
import time
from datetime import datetime, timedelta


def get_indeed_job_links(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    h2_tags = soup.find_all('h2', class_=['jobTitle', 'css-mr1oe7', 'eu4oa1w0'])
    list_id = [h.find('a')['data-jk'] if h.find('a') else None for h in h2_tags]
    date = soup.find_all('span', {'class': ['date']})
    return list_id,date


def get_first_apec_job_link(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    container_result = soup.find('div', class_='container-result')
    div = container_result.find('div') # sauf le dernier toujours un None
    lien = div.find('a')['href'] if div.find('a') else None
    return(lien)

def get_pole_job_links(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    li = soup.find_all('li', {'data-id-offre': True})
    data_id_offre_list = [item['data-id-offre'] for item in li]
    return data_id_offre_list



def scrap_pole_job(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')

    title = soup.find('span', {'itemprop':['title']}) 
    title = title.text if title else ""

    compagny = soup.find('h3',{'class':['t4','title']})
    compagny = compagny.text.strip() if compagny else ""

    postal_code = soup.find('span',{'itemprop':['postalCode']})
    postal_code = postal_code.get('content', '')
    locality = soup.find('span',{'itemprop':['addressLocality']})
    locality = locality.get('content', '')
    region = soup.find('span',{'itemprop':['addressRegion']})
    region = region.get('content', '')
    country = soup.find('span',{'itemprop':['addressCountry']})
    country = country.get('content', '')

    location = soup.find('span',{'itemprop':['name']})
    
    
    postal_code = postal_code if postal_code else ""
    locality = locality if locality else ""
    region = region if region else ""
    country = country if country else ""

    description_div = soup.find('div',{'itemprop':['description']})
    description = description_div.find('p').text if description_div else ""

    skills = get_skills(description)

    dd_element = soup.select_one('dl.icon-group dd') 
        # Vérifie si la balise <dd> a été trouvée
    if dd_element:
        # Récupère le texte de la balise <dd> jusqu'à la balise <br/>
        type_job = dd_element.get_text(separator='\n', strip=True).split('\n', 1)[0]
        type_job = type_job.strip()
    else:
        type_job = ""

    salary_container = soup.find('ul', {'style': 'list-style-type: none; margin:0; padding: 0'})

    # Vérifie si la balise <ul> a été trouvée
    if salary_container:
        # Récupère toutes les valeurs des éléments <li> sous la balise <ul>
        salary = [li.text.strip() for li in salary_container.find_all('li')]
        salary = ', '.join(salary)
        salary = salary.strip()
    else:
        salary = ""


    skills_elements = soup.find_all('span', {'itemprop': 'skills'})
    skills2 = [skills.text.strip() for skills in skills_elements]

    
    global_location = postal_code + " " + locality + " " + region + " " + country

    date_spans = soup.find_all('span', {'itemprop': 'datePosted'})
    date_span = date_spans[0]
    date = date_span.get('content', '')


    print(title)
    print(type_job)
    print(skills)
    print(global_location)
    print("date : ",date)
    print("======")

    return [title,type_job,salary,compagny,global_location,"language",skills,date,description,"pole_emploi"]


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
    
        if len(li_elements) == 2:
            type_job = li_elements[0].text
            location = li_elements[1].text
        if len(li_elements) == 3:
            compagny = li_elements[0].text
            type_job = li_elements[1].text
            location = li_elements[2].text

        print("compagny : ",compagny) # OK
        print("location : ",location) # OK
        print("type job : ",type_job) # OK

    title = ""
    salary = ""
    description = ""
    skills = ""
    experience = ""
    date = "" # OK
    
    date = soup.find('div',{'class':['date-offre']}).text
    print("date : ",date)

    outer_div = soup.find('div', class_='col-lg-4')
    if outer_div is not None:
        salary_div = outer_div.find_all('div')[0]
        experience_div = outer_div.find_all('div')[2]
        title_div = outer_div.find_all('div')[3]

        title = title_div.find('span').text # OK
        salary = salary_div.find('span').text # OK
        experience = experience_div.find('span').text

    
    body_div = soup.find('div',{'class':['col-lg-8 ', 'border-L']})
    if body_div is not None:
        skills = soup.find_all('div', {'class':['added-skills-manager__knowledge','mb-0']}) 
        #print(skills)

        details = body_div.select('p:not(.mb-20)') # pas  la dernière => useless

        for d in details:
            description += d.text + " "
        #print(description) 

    if description != "":
        skills = get_skills(description)

    print("=============")

    liste = [title,type_job,salary,compagny,location,"language",skills,date,description,source]
    
    return liste

    


def scrap_indeed_job(html_source,date):

    soup = BeautifulSoup(html_source, 'html.parser')

    source = "indeed"

    div_title = soup.find('h1', class_='jobsearch-JobInfoHeader-title')   
    title = div_title.find('span')

    location = soup.find('div', {'data-testid':['inlineHeader-companyLocation']}) 
    description = soup.find('div', {'id':['jobDescriptionText']})

    compagny_div = soup.find('div', {'data-testid':['inlineHeader-companyName']})
    compagny = compagny_div.find('a', {'class':['css-1f8zkg3','e19afand0']})
    salary = ""
    type_job = ""

    # OK
    salary_and_jobtype_header = soup.find('div', {'id':['salaryInfoAndJobType']}) 
    if salary_and_jobtype_header is not None:
        salary = salary_and_jobtype_header.find('span',{'class':['css-2iqe2o']})
        type_job = salary_and_jobtype_header.find('span',{'class':['css-k5flys']})

    if salary != "" and salary is not None:
        salary = salary.text
    if type_job != "" and type_job is not None:
        type_job = type_job.text

    type_job = type_job.replace("-", "")


    date = date.text
    new_string = date.replace("Posted", "")

    if "Aujourd'hui" in new_string:
        date = datetime.now()
    elif "plus de 30" in new_string:
        days = re.findall(r'\d+', new_string)
        date = datetime.now() - timedelta(days=30)
    else:
        days = re.findall(r'\d+', new_string)
        date = datetime.now() - timedelta(days=int(days[0]))

    date = date.strftime("%Y-%m-%d")
    print("date : ",date)


    # régler les skills !
    #skills_div = soup.find('div', {'class': ['js-match-insights-provider-e6s05i', 'eu4oa1w0']})

    print("salaire : ",salary)
    print("type job : ",type_job)
    

    if title:
        title = title.text.strip()
        print(f"title : {title}")
    else:
        title = ""

    if location:
        location = location.text.strip()
        print(f"location : {location}")
    else:
        location = ""
    if compagny:
        compagny = compagny.text.strip()
        print(f"compagny : {compagny}")
    else:
        compagny = ""

    if description:
        skills = get_skills(description.text)
        description = description.text.strip()
        # fields_to_find = []
        # if not salary:
        #     fields_to_find.append("salary")
        # if not type_job:
        #     fields_to_find.append("type_job")
        # if not skills_ul:
        #     fields_to_find.append("skills")
            
        # scrap_description_indeed(description,["salary","type_job"])
    else:
        description = ""

    print("\n ================== \n")

    liste = [title,type_job,salary,compagny,location,"language",skills,date,description,source]

    return liste

    
def scrap_glassdoor_job(html_source):
    
    soup = BeautifulSoup(html_source, 'html.parser')
    job_header = soup.find('header', {'class':['JobDetails_jobDetailsHeaderWrapper__iHvDC JobDetails_sticky__fQ4Aq']})
     
    source = "glassdoor"

    type_job = ""
    salaire = ""
    title = ""
    compagny = ""
    skills = ""
    location = ""
    description = ""
    date = ""
    compagny = job_header.find('span', {'class': ['EmployerProfile_employerName__Xemli']})
    compagny = compagny.text if compagny else ""
    title = soup.find('div', {'class': ['JobDetails_jobTitle__Rw_gn']})
    title = title.text if title else ""
    description = soup.find('div', {'class':['JobDetails_jobDescription__6VeBn','JobDetails_blurDescription__fRQYh']})
    location = job_header.find('div', {'class': ['JobDetails_location__MbnUM']})
    location = location.text if location else ""

    # Recherchez le paragraphe contenant "Type d'emploi"
    type_job = soup.find('p', text=lambda t: t and "Type d'emploi" in t)
    type_job = type_job.text if type_job else ""
    salaire = soup.find('p', text=lambda t: t and "Salaire" in t)
    salaire = salaire.text if salaire else ""
    skills = soup.find('p', text=lambda t: t and "Compétences" in t)

    
    print(f"type_job : {type_job}")
    print(f"salaire : {salaire}")
    print(f"title : {title}")
    print(f"skills : {skills}")
    print(f"location : {location}")

    if description:
        description = description.text.strip()
        #skills = get_skills(description)

        fields_to_find = []
        if not salaire:
            fields_to_find.append("salary")
        if not type_job:
            fields_to_find.append("type_job")
        if not skills:
            fields_to_find.append("type_job")
            
        #scrap = scrap_description_glassdoor(description,fields_to_find)

    
    date_posted = soup.find('div', {'data-test': ['job-age']})
    date_posted = date_posted.text if date_posted else ""
    date_du_jour = datetime.now()
    if "h" in date_posted:
        # Soustrayez les heures à la date du jour
        hours = re.findall(r'\d+', date_posted)
        date = date_du_jour - timedelta(hours=int(hours[0]))
    elif "j" in date_posted:
        if "+" in date_posted:
            # + de 30 jours (peut-être faire un autre truc)
            days = re.findall(r'\d+', date_posted)
            date = date_du_jour - timedelta(days=int(days[0]))
        else:
            days = re.findall(r'\d+', date_posted)
            date = date_du_jour - timedelta(days=int(days[0]))


    date = date.strftime("%Y-%m-%d")
    print("date : ",date)

    print("\n ================== \n")


    liste = [title,type_job,salaire,compagny,location,"language","skills",date,description,source]
    return liste