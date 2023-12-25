import requests

url = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search"
headers = {
    "Authorization": "Bearer VOTRE_CLE_API",
    # Ajoutez d'autres en-têtes requis selon la documentation
}

# Ajoutez les paramètres de requête nécessaires
params = {
    "parametre1": "valeur1",
    "parametre2": "valeur2",
    # Ajoutez d'autres paramètres selon la documentation
}

response = requests.get(url, headers=headers, params=params)

# Vérifiez la réponse
if response.status_code == 200:
    data = response.json()
    # Traitez les données
else:
    print(f"Erreur {response.status_code}: {response.text}")




# glassdoor : 
    
#http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=120&t.k=fz6JLNDfgVs&action=employers&q=pharmaceuticals&userip=192.168.43.42&useragent=Mozilla/%2F4.0
