from bs4 import BeautifulSoup
from scrap_description import *
import time
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from geopy.geocoders import Photon


geolocator = Nominatim(user_agent="my_geocoder")
geolocator_region = Nominatim(user_agent="my_geocoder")

def get_region_department(lat, lon, only_dep = False):
    location = geolocator_region.reverse((lat, lon), exactly_one=True) 
    if location:
        address = location.raw['address']
        #print("raw : ")
        #   print(address)
        if address.get('city') == 'Paris':
            return address.get('state', ''), address.get('city_district', '')
        elif address:
            if only_dep == False:
                return address.get('state', ''), address.get('county', '')
            else:
                return address.get('county', '')

    return None,None

def get_coordinates(city):
    location = geolocator.geocode(f"{city}, France")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None
    

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

def get_jungle_job_link(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    a_tags = soup.find_all('a', {'class': ['sc-6i2fyx-0', 'gIvJqh']})
    href_list = [a.get('href') for a in a_tags]
    return href_list


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
        if type_job:
            pattern_1 = r"indéterminée"
            pattern_2 = r"déterminée"
            pattern_3 = r"intérimaire"

            if re.search(pattern_1, type_job):
                type_job = "CDI"
            elif re.search(pattern_2, type_job):
                # prendre nombre mois ?? "intérimaire - 3 Mois"
                type_job = "CDD"
            elif re.search(pattern_3, type_job):
                type_job = "Intérim"

    else:
        type_job = ""

    salary_container = soup.find('ul', {'style': 'list-style-type: none; margin:0; padding: 0'})

    # Vérifie si la balise <ul> a été trouvée
    if salary_container:
        # Récupère toutes les valeurs des éléments <li> sous la balise <ul>
        salary = [li.text.strip() for li in salary_container.find_all('li')]
        salary = ', '.join(salary)
        salary = salary.strip()
        salary = salary.lower()

        # Expression régulière pour rechercher "Selon profils", "Selon profil" ou "négociable"
        pattern = r"selon profils?|\bselon profil\b|négociable"
        pattern_chiffres = r"\D+"

        if not re.search(pattern_chiffres, salary) or re.search(pattern, salary, re.IGNORECASE):
            # pas de chiffre ou à négocier => pas de salaire
            salary = ""
        else:
            monthly_pattern = r"mensuel de (\d+,\d{2}) euros"
            annual_borne_pattern = r"annuel de (\d+,\d{2}) euros à (\d+,\d{2}) euros"
            annual_pattern = r"annuel de (\d+,\d{2}) euros"
            horaire_borne_pattern = r"horaire de (\d+,\d{2}) euros à (\d+,\d{2}) euros"

            monthly_match = re.search(monthly_pattern, salary)
            annual_borne_match = re.search(annual_borne_pattern, salary)
            annual_match = re.search(annual_pattern, salary)
            horaire_borne_match = re.search(horaire_borne_pattern, salary)

            if monthly_match:
                print("salaire mois")
                print(salary)
                print(monthly_match)
                monthly_salary = float(monthly_match.group(1).replace(',', '.'))
                annual_salary = monthly_salary * 12
                salary = annual_salary
                print("res : ")
                print(salary)
            
            elif annual_borne_match:
                print("salaire année")
                print(salary)
                lower_salary = float(annual_borne_match.group(1).replace(',', '.'))
                upper_salary = float(annual_borne_match.group(2).replace(',', '.'))
                print("upper")
                print(upper_salary)
                print("lower")
                print(lower_salary)
                annual_salary = (lower_salary + upper_salary) / 2
                salary = annual_salary
                print("res : ")
                print(salary)
            elif annual_match:
                salary = float(annual_match.group(1).replace(',', '.'))
                
            elif horaire_borne_match:
                salary = "" # galère 
            else:
                salary = ""

    else:
        salary = ""
    
    global_location = locality + " " + postal_code + " " + region

    date_spans = soup.find_all('span', {'itemprop': 'datePosted'})
    date_span = date_spans[0]
    date = date_span.get('content', '')


    print(title) # OK
    print(type_job) # OK
    print(global_location) # OK
    print(date) # OK

    latitude, longitude = get_coordinates(locality + " - " + postal_code) # OK
    departement = get_region_department(latitude, longitude,only_dep=True) # OK
    print(region)
    tokens = scrap_description(description)

    print("======")

    return [title,type_job,salary,compagny,global_location,region,departement,latitude,longitude,"language",skills,date,description,tokens,"Pole_Emploi"]


def scrap_apec_job(html_source):
   
    soup = BeautifulSoup(html_source, 'html.parser')

    source = "Apec"
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

    if type_job[1].isdigit():
        # Supprimer le premier caractère (le chiffre) et les espaces
        type_job = type_job[4:]
    print(type_job)

    title = ""
    salary = ""
    description = ""
    experience = ""
    date = ""
    
    date = soup.find('div',{'class':['date-offre']})
    if date is not None:
        date = date.text
        match = re.search(r'\d{2}/\d{2}/\d{4}', date)
        if match:
            date = match.group()
            date = re.sub(r'\s+', '', date)
            print(date)

    outer_div = soup.find('div', class_='col-lg-4')
    if outer_div is not None:
        salary_div = outer_div.find_all('div')[0]
        experience_div = outer_div.find_all('div')[2]
        title_div = outer_div.find_all('div')[3]

        title = title_div.find('span').text # OK
        salary = salary_div.find('span').text # OK

        if "A négocier" in salary:
            salary = ""
        elif "A partir" in salary:
            match = re.search(r'(A partir de )?(\d+) k€ brut annuel', salary)
            if match:
                salary = int(match.group(2)) * 1000 # Convertir k€ en €
            else:
                salary = ""

        elif "brut annuel" in salary:
            match = re.search(r'(\d+) - (\d+) k€ brut annuel', salary)
            if match:
                min_value = int(match.group(1)) * 1000
                max_value = int(match.group(2)) * 1000
                # Prendre la moitié
                salary = (min_value + max_value) / 2 
            else:
                salary = ""
    
        experience = experience_div.find('span').text

    
    body_div = soup.find('div',{'class':['col-lg-8 ', 'border-L']})
    if body_div is not None:
        details = body_div.select('p:not(.mb-20)') # pas  la dernière => useless
        for d in details:
            description += d.text + " "

    latitude, longitude = get_coordinates(location)
    region, departement = get_region_department(latitude, longitude)

    tokens = scrap_description(description)

    print("=============")

    liste = [title,type_job,salary,compagny,location,region,departement,latitude,longitude,experience,"skills",date,description,tokens,source]
    
    return liste

    


def scrap_indeed_job(html_source,date):

    soup = BeautifulSoup(html_source, 'html.parser')

    source = "Indeed"

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

    latitude, longitude = get_coordinates(location)
    region, departement = get_region_department(latitude, longitude)

    tokens = scrap_description(description)

    print("\n ================== \n")

    liste = [title,type_job,salary,compagny,location,region, departement,latitude,longitude,"language",skills,date,description,tokens,source]

    return liste

    
def scrap_glassdoor_job(html_source):
    
    soup = BeautifulSoup(html_source, 'html.parser')
    job_header = soup.find('header', {'class':['JobDetails_jobDetailsHeaderWrapper__iHvDC JobDetails_sticky__fQ4Aq']})
     
    source = "Glassdoor"

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
        print(description)

    
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

    latitude, longitude = get_coordinates(location)
    region, departement = get_region_department(latitude, longitude)

    tokens = scrap_description(description)

    print("\n ================== \n")


    liste = [title,type_job,salaire,compagny,location,region, departement,latitude,longitude,"language","skills",date,description,tokens,source]
    return liste


def scrap_jungle_job(html_source):
   
    soup = BeautifulSoup(html_source, 'html.parser')

    source = "Welcome_to_the_jungle"
    compagny = ""
    type_job = ""
    location = ""
    title = ""
    salary = ""
  
    compagny = soup.find('span',{'class':['sc-ERObt', 'kkLHbJ', 'wui-text']})
    compagny = compagny.text
    title = soup.find('h2',{'class':['sc-ERObt','fMYXdq','wui-text']})
    title = title.text
   
    infos_div = soup.find('div',{'class':['sc-bXCLTC ','hdepoj']})
    location = infos_div.find('span',{'class':['sc-1eoldvz-0' ,'bZJPQK']})
    location = location.text

    
    i_tag = soup.find('i', {'name': 'salary'})
    if i_tag:
        div_with_salary = i_tag.find_parent('div')
        if div_with_salary:
            salary = div_with_salary.text.strip()
            if "Non spécifié" in salary:
                salary = ""
            elif "par mois" in salary:
                match = re.search(r"Salaire : ([\d,\.]+)(K?)\s*€ par mois", salary)
                if match:
                    salaire = match.group(1).replace(',', '')  # Supprimez les virgules pour la conversion
                    is_k = match.group(2)
                    salaire_annuel = float(salaire)
                    if is_k:
                        salaire_annuel *= 1000
                    salaire_annuel *= 12
                    salary = salaire_annuel
                else:
                    salary = ""
            else:
                match = re.search(r"Salaire : (\d+)K à (\d+)K\s*€", salary)
                if match:
                    salaire_min = int(match.group(1)) * 1000  # Convertir en euros
                    salaire_max = int(match.group(2)) * 1000  # Convertir en euros
                    
                    # Calculer la moyenne des salaires
                    salaire_moyen = (salaire_min + salaire_max) / 2
                    
                    salary = salaire_moyen
                else:
                    salary = ""
            print(salary)

    i_tag = soup.find('i', {'name': 'suitcase'})
    if i_tag:
        div_with_experience = i_tag.find_parent('div')
        if div_with_experience:
            experience = div_with_experience.text.strip()
            print(experience)

    i_tag = soup.find('i', {'name': 'contract'})
    if i_tag:
        div_with_contract = i_tag.find_parent('div')
        if div_with_contract:
            type_job = div_with_contract.text.strip()
            print(type_job)

    i_tag = soup.find('i', {'name': 'education_level'})
    if i_tag:
        div_with_education = i_tag.find_parent('div')
        if div_with_education:
            education = div_with_education.text.strip()
            print(education)

    competence_div = soup.find('div',class_=['sc-18ygef-1','ezamTS'])
    #print(competence_div.text)

    date = soup.find('time')['datetime']
    print(date)

    print(location)
    print(title)
    print(compagny)    
    latitude, longitude = get_coordinates(location)
    region, departement = get_region_department(latitude, longitude)

    tokens = scrap_description(competence_div.text)
    print(tokens)


    print("=============")

    liste = [title,type_job,salary,compagny,location,region, departement,latitude,longitude,"language","skills",date,competence_div.text,tokens,source]
    return liste


