from bs4 import BeautifulSoup

def preprocess_indeed_page(html_source):

     # Utiliser BeautifulSoup pour traiter les données
    soup = BeautifulSoup(html_source, 'html.parser')

    # Vous pouvez maintenant utiliser BeautifulSoup pour extraire et manipuler les données de la page
    # Exemple : récupérer tous les éléments <ul>
    ul_elements = soup.find_all('ul')

    # Afficher le contenu de chaque ul
    for ul in ul_elements:
        print("Contenu de l'élément <ul>:")
        print(ul.prettify())  # Utilisez prettify pour afficher le HTML de manière formatée
        print("\n" + "="*50 + "\n")  # Séparateur entre les éléments

    #print(source)


def preprocess_apec_page(html_source):

     # Utiliser BeautifulSoup pour traiter les données
    soup = BeautifulSoup(html_source, 'html.parser')

    # Vous pouvez maintenant utiliser BeautifulSoup pour extraire et manipuler les données de la page
    # Exemple : récupérer tous les éléments <ul>
    ul_elements = soup.find_all('ul')

    # Afficher le contenu de chaque ul
    for ul in ul_elements:
        print("Contenu de l'élément <ul>:")
        print(ul.prettify())  # Utilisez prettify pour afficher le HTML de manière formatée
        print("\n" + "="*50 + "\n")  # Séparateur entre les éléments

    #print(source)