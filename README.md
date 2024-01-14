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
![Scraping](https://private-user-images.githubusercontent.com/66120091/296605997-bbdbd7a7-7cc7-4fb8-adca-08ce0ab6786f.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUyNTMyMTQsIm5iZiI6MTcwNTI1MjkxNCwicGF0aCI6Ii82NjEyMDA5MS8yOTY2MDU5OTctYmJkYmQ3YTctN2NjNy00ZmI4LWFkY2EtMDhjZTBhYjY3ODZmLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAxMTQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMTE0VDE3MjE1NFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWQ0Mzc2ZjIwYmU0MmRkYTBhMmQwZmQ1ZDEyZTJlNzk2NzA4Y2E5MGI3Mjc4MDYzYjljZDJlZGIyNWU1MDM4OTcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.YKYZkMRmWsSXYDMbenzRUTG5FubsPzOi02jh7-kbc1A)
2. Recherche
![Recherche](https://github.com/Naghan1132/Jobs-Text-Mining/assets/66120091/c0faa0fb-2e0b-40d1-8d32-279076f43d03)

3. Visualisation
![Map](https://private-user-images.githubusercontent.com/66120091/296606326-9961ce46-639e-4608-869c-89b49c78aba2.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUyNTQ4OTYsIm5iZiI6MTcwNTI1NDU5NiwicGF0aCI6Ii82NjEyMDA5MS8yOTY2MDYzMjYtOTk2MWNlNDYtNjM5ZS00NjA4LTg2OWMtODliNDljNzhhYmEyLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAxMTQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMTE0VDE3NDk1NlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTczNTk2Yzk4NjNmMGVmZDI1MDE3YTI2NGE0Njk5OTk5N2FiOWRjNWY1MDAzOGM0Y2U0ZTYyZmVmOTRjOWFkZmMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.qPNj-wsHeKM4kBfPrq68PMXzKqJJEh-w5jx-dvF9c80)

4. Analyse
![Screenshot from 2024-01-14 18-30-10](https://github.com/Naghan1132/Jobs-Text-Mining/assets/66120091/fba22c91-1b82-4929-a919-df30743799b1)

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
