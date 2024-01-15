# Jobs Text Mining

## Description
Ce projet vise à analyser des données textuelles pour extraire des informations utiles et des insights à partir de diverses sources de données.

## Fonctionnalités

- **Scraping des données**: Collecte d'informations à partir de sites Web (Pole Emploi, Apec, Welcome To The jungle) pour enrichir la base de données. 
- **Analyse de texte**: Extraction de mots-clés, fréquences des mots, et autres statistiques textuelles.
- **Visualisation régionale / départementale**: L'application permets de visualiser les emplois disponibles et France par régions et départements, ainsi que les informations de celles-ci.
- **Visualisation**: Utilisation de graphiques et de nuages de mots pour représenter les données textuelles.

## Installation

1. Clonez le dépôt GitHub :
   ```bash
   git clone https://github.com/Naghan1132/Jobs-Text-Mining.git
2. Aller dans le dossier source :
   ```bash
   cd src/ 
2. Construire l'image du docker :
   ```bash
   docker build -t jobsminingdocker . 
2. Lancer le docker :
   ```bash
   docker run -p 8501:8501 jobsminingdocker 
   
## Utilisation
1. Scraping de données
![Scraping](https://private-user-images.githubusercontent.com/66120091/296605997-bbdbd7a7-7cc7-4fb8-adca-08ce0ab6786f.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUzMDk2NjksIm5iZiI6MTcwNTMwOTM2OSwicGF0aCI6Ii82NjEyMDA5MS8yOTY2MDU5OTctYmJkYmQ3YTctN2NjNy00ZmI4LWFkY2EtMDhjZTBhYjY3ODZmLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAxMTUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMTE1VDA5MDI0OVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTI3NTVmMDI0Y2FhNzkyOWVlNmEwNzMzNmE5M2M2YjBiMDMyMzMyZGU1YzhmYWNjMGEwMTNmZjRmMDc0MjlhNDMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.Di5deqHfOLdQzSOvMwKRnUQnM-RAuZRaVVKAknMug4U)
2. Recherche
![Recherche](https://github.com/Naghan1132/Jobs-Text-Mining/assets/66120091/c0faa0fb-2e0b-40d1-8d32-279076f43d03)

3. Visualisation
![Map](https://private-user-images.githubusercontent.com/66120091/296606422-fba22c91-1b82-4929-a919-df30743799b1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUzMDk4MTMsIm5iZiI6MTcwNTMwOTUxMywicGF0aCI6Ii82NjEyMDA5MS8yOTY2MDY0MjItZmJhMjJjOTEtMWI4Mi00OTI5LWE5MTktZGYzMDc0Mzc5OWIxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAxMTUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMTE1VDA5MDUxM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPThhMmQxMmQ4YTdhOTY1ZGNkNGE2YmUzMTQ3ZDIzNmE4YmRlNjE3MDY0MGFlYzM2ZWMyZWY5Mzg2YjFjZGY2NWQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.Pot91TZFevTjsQuT2yZielqQbx1ViE3ckMISmyIqdrY)

4. Analyse
![analyse](https://private-user-images.githubusercontent.com/66120091/296606326-9961ce46-639e-4608-869c-89b49c78aba2.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUzMDk2NDAsIm5iZiI6MTcwNTMwOTM0MCwicGF0aCI6Ii82NjEyMDA5MS8yOTY2MDYzMjYtOTk2MWNlNDYtNjM5ZS00NjA4LTg2OWMtODliNDljNzhhYmEyLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAxMTUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMTE1VDA5MDIyMFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWJiZTk5NzU0OTQyYTBhMTExNWNmMjVhMjdlZjM1YjdhZTliNDBjNGUxMTNkODU1OWY5MDNkNzcyMTg3OWU0NDQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.78wdXQBkc9wxqbO_I_phhup0Vn1sW1VVgOYSvG43Iv4)

## Structure du projet
- **`src/`:**
 - **`python/`:**
   - **`web_scraping.py` :** Contient les scripts
   - **`build_data.py` :** Contient les scripts
   - **`scraping.py` :** Contient les scripts
   - **`preprocess_text.py` :** Contient les scripts
 - **`sql/`:**
   - **`execute.py` :** Créer un nouveau warehouse 
   - **`insert.py` :** Insérer des données
   - **`SQLite_v2.py` :** Classe de la base SQL
   - **`warehouse.db` :** Base SQL
 - **`app/`:**
   - **`app.py` :** Main streamlit
 - **`data/`:**
   - **`regions.geojson` :** Coordonnées de toutes les régions françaises
   - **`departements.geojson` :** Coordonnées de tous les départements français
 - **`requirements.txt` :** Ce fichier contient la liste des dépendances requises pour le projet.
 - **`Dockerfile` :** Fichier docker
 
## Auteurs

- Nathan GRIMAULT   
- Hugo ANDRE--ANTICHAN
- Joseph PELHAM
- Ndeye-Fatou DIENG
