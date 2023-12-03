import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import spacy

from langdetect import detect


# Téléchargez les ressources nécessaires
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')


def scrap_description_apec(texte,fields_to_find):
    # déterminer la langue du post !!!      
    print(f"description : {texte}")
    language = detect_language(texte)
    print(extract_salary_re(texte,language))
    print(get_tokens(texte,language))

def scrap_description_indeed(texte,fields_to_find):
    print(f"description : {texte}")
    language = detect_language(texte)
    print(extract_salary_re(texte,language))
    print(get_tokens(texte,language))

def scrap_description_glassdoor(texte,fields_to_find):
    print(f"description : {texte}")
    language = detect_language(texte)
    print(extract_salary_re(texte,language))
    print(get_tokens(texte,language))


def extract_salary_re(text,language):
    # Utilisez une expression régulière pour extraire le salaire
    match = re.search(r'\$\s?\d+(?:,\d{3})*(?:\.\d{2})?', text)
    if match:
        return match.group(0)
    else:
        return None
    


def extract_keywords_spacy(text, keywords=["salaire", "salary", "rémunération"], num_words_after=15):

    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(text.lower())  # Assurez-vous que le texte est en minuscules

    for token in doc:
        if token.text in keywords:
            # Recherchez le mot-clé et récupérez les n mots qui suivent
            start_index = token.i + 1
            end_index = start_index + num_words_after
            salary_words = [t.text for t in doc[start_index:end_index]]
            return " ".join(salary_words)

    return None


def get_tokens(text,language):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum()]  # Supprimez la ponctuation
    tokens = [word for word in tokens if word.isalpha()]  # Supprimez les chiffres
    tokens = [word.lower() for word in tokens]  # Convertissez en minuscules

    # détecter automatiquement la langue du post 
    if language == "fr":
        language = "french"
    elif language == "en":
        language = "english"
    else:
        language = "english"

    tokens = [word for word in tokens if word not in stopwords.words(language)]  # Supprimez les mots vides
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatization
    word_counts = Counter(tokens)
    return word_counts


def detect_language(text):
    try:
        language = detect(text)
        return language
    except Exception as e:
        # En cas d'erreur, renvoyer None ou gérer l'erreur selon vos besoins
        print(f"Langue non dététée : {e}")
        return None

