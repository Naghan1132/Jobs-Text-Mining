import requests

api_key = 'VOTRE_CLE_API'
base_url = 'http://api.glassdoor.com/api/api.htm'

# Exemple de recherche d'emploi
params = {
    't.p': api_key,
    't.k': 'keyword',
    'userip': '0.0.0.0',  # Votre adresse IP
    'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}

response = requests.get(base_url, params=params)
data = response.json()

# Traiter les données retournées
print(data)
