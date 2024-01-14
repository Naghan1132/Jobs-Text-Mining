from bs4 import BeautifulSoup
from preprocess_text import *
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from geopy.geocoders import Photon


geolocator = Nominatim(user_agent="my_geocoder")
geolocator_region = Nominatim(user_agent="my_geocoder")

def get_region_department(lat, lon, only_dep = False):
    location = geolocator_region.reverse((lat, lon), exactly_one=True) 
    if location:
        address = location.raw['address']
        if address.get('city') == 'Paris':
            return address.get('state', ''), address.get('city_district', '')
        elif address:
            if only_dep == False:
                return address.get('state', ''),address.get('county', '')
            else:
                return address.get('county', '')

    return None,None

def get_coordinates(city):
    location = geolocator.geocode(f"{city}, France")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None



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
    if title != "":
        # Expression régulière pour trouver "H/F" ou "(H/F)"
        pattern = r'\bH/F\b|\(H/F\)'  # Utilisation de \b pour s'assurer que nous avons des limites de mots
        # Remplacer "H/F" et "(H/F)" par une chaîne vide
        title = re.sub(pattern, "", title)

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
    description = clean_description(description)
    

    dd_element = soup.select_one('dl.icon-group dd') 
    if dd_element:
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
            # pas de chiffre ou presence de "à négocier" etc... => pas de salaire
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
                monthly_salary = float(monthly_match.group(1).replace(',', '.'))
                salary = monthly_salary * 12
            elif annual_borne_match:
                lower_salary = float(annual_borne_match.group(1).replace(',', '.'))
                upper_salary = float(annual_borne_match.group(2).replace(',', '.'))
                salary = (lower_salary + upper_salary) / 2
            elif annual_match:
                salary = float(annual_match.group(1).replace(',', '.'))
            elif horaire_borne_match:
                salary = "" # galère 
            else:
                salary = ""

    else:
        salary = ""

    experience = ""
    span_with_experience = soup.find('span', itemprop="experienceRequirements")
    if span_with_experience:
        experience = span_with_experience.text
        if "Débutant accepté" in experience:
            experience = "Pas d'importance"
        print(experience)

    skills = []
    skills_elements = soup.find_all(attrs={"itemprop": "skills"})
    for skills_element in skills_elements:
        if skills_element:
            skills.append(skills_element.text)

    skills = clean_skills(skills)
    #skills = get_tokens_and_find_language(skills)
    
    
    global_location = locality + " " + postal_code + " " + region

    date_spans = soup.find_all('span', {'itemprop': 'datePosted'})
    date_span = date_spans[0]
    date = date_span.get('content', '')
    date = datetime.strptime(date, '%Y-%m-%d')
    date = date.strftime('%d/%m/%Y')

    print(type_job) # OK
    print(date) # OK

    latitude, longitude = get_coordinates(locality + " - " + postal_code) # OK
    departement = get_region_department(latitude, longitude,only_dep=True) # OK
    departement = str(departement)
    departement = departement.replace("(", "").replace(")", "")

    tokens = get_text_tokenize_and_find_language(description)

    print("======")

    return [title,type_job,salary,compagny,global_location,region,departement,latitude,longitude,experience,skills,date,description,tokens,"Pole_Emploi"]


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
        if "CDD" or "cdd" in type_job:
            type_job = "CDD"
        elif "CDI" or "cdi"  in type_job:
            type_job = "CDI"
        elif "Stage" or "stage" in type_job:
            type_job = "Stage"
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
        if title != "":
            pattern = r'\bH/F\b|\(H/F\)'
            title = re.sub(pattern, "", title)

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
        pattern = r'Minimum\s+(.+)'  
        match = re.search(pattern, experience)
        if match:
            experience = match.group(1)
        else:
            if "Tous niveaux" in experience:
                experience = "Pas d'importance"
        print(experience)

    
    body_div = soup.find('div',{'class':['col-lg-8 ', 'border-L']})
    if body_div is not None:
        details = body_div.select('p:not(.mb-20)') # pas  la dernière => useless
        for d in details:
            description += d.text + " "

    description = clean_description(description)

    skills = []
    divs = soup.find_all('div', class_='infos_skills')

    for div in divs:
        first_p = div.find('p')
        if first_p:
            skills.append(first_p.text) 
    
    apec_details = soup.find_all('apec-competence-detail')
    for detail in apec_details:
        p_elements = detail.find('p')
        if p_elements:
            skills.append(p_elements.text) 
            

    if skills == []:
        # alors prendre les mannuelement le texte
        h4_element = soup.find('h4', string='Profil recherché')
        if h4_element:
            next_p_element = h4_element.find_next_sibling('p')
            if next_p_element:
                skills = get_tokens_and_find_language(next_p_element.text)
    else:
        # tokenizer les skills aussi ??
        skills = [skill.lower() for skill in skills]

    skills = clean_skills(skills)
    #skills = get_tokens_and_find_language(skills)

    latitude, longitude = get_coordinates(location)
    region, departement = get_region_department(latitude, longitude)
    departement = str(departement)
    departement = departement.replace("(", "").replace(")", "")

    tokens = get_tokens_and_find_language(description)

    print("=============")

    liste = [title,type_job,salary,compagny,location,region,departement,latitude,longitude,experience,skills,date,description,tokens,source]
    
    return liste

    

def scrap_jungle_job(html_source):
   
    soup = BeautifulSoup(html_source, 'html.parser')

    source = "Welcome_to_the_jungle"
    compagny = ""
    type_job = ""
    location = ""
    title = ""
    salary = ""
    experience = ""
  
    compagny = soup.find('span',{'class':['sc-ERObt', 'kkLHbJ', 'wui-text']})
    compagny = compagny.text
    title = soup.find('h2',{'class':['sc-ERObt','fMYXdq','wui-text']})
    title = title.text
    if title != "":
        pattern = r'\bH/F\b|\(H/F\)'
        title = re.sub(pattern, "", title)
   
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
            #Expérience : < 6 mois

    i_tag = soup.find('i', {'name': 'contract'})
    if i_tag:
        div_with_contract = i_tag.find_parent('div')
        if div_with_contract:
            type_job = div_with_contract.text.strip()
            if "CDD" or "cdd" in type_job:
                type_job = "CDD"
            elif "CDI" or "cdi"  in type_job:
                type_job = "CDI"
            elif "Stage" or "stage" in type_job:
                type_job = "Stage"
            print(type_job)

    skills = []
    competence_div = soup.find('div',class_=['sc-18ygef-1','ezamTS'])
    
    if competence_div:
        competence_text = competence_div.text
        clean_competence = clean_description(competence_text)
        skills = clean_skills(clean_competence)
        #skills = get_tokens_and_find_language(clean_competence)
        #skills = [skill.lower() for skill in skills]

        

    date = soup.find('time')['datetime']
    date = date.split('T')[0]
    date = datetime.strptime(date, '%Y-%m-%d')
    date = date.strftime('%d/%m/%Y')

    latitude, longitude = get_coordinates(location)
    region, departement = get_region_department(latitude, longitude)
    departement = str(departement)
    departement = departement.replace("(", "").replace(")", "")


    description = clean_description(competence_div.text)
    tokens = get_text_tokenize_and_find_language(description)

    print("=============")

    liste = [title,type_job,salary,compagny,location,region, departement,latitude,longitude,experience,skills,date,description,tokens,source]
    return liste


