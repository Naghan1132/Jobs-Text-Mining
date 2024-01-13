import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
import string
from langdetect import detect
import numpy as np


def get_tokens_and_find_language(texte):
    language = detect_language(texte)
    return get_tokens(texte,language)

def get_text_tokenize_and_find_language(texte):
    language = detect_language(texte)
    return get_text_tokenize(texte,language)


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
    return tokens


def get_text_tokenize(text,language):
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
    #word_counts = Counter(tokens)
    #print(word_counts)
    text = " ".join(tokens)
    return text


def detect_language(text):
    try:
        language = detect(text)
        return language
    except Exception as e:
        # En cas d'erreur, renvoyer None ou gérer l'erreur selon vos besoins
        print(f"Langue non dététée : {e}")
        return None


def clean_description(description):
    cleaned_description = description.replace('\n', ' ').replace('\r', ' ')
    # Supprimer les emojis en utilisant une expression régulière
    emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F700-\U0001F77F"  # alchemical symbols
                            u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                            u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                            u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                            u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                            u"\U00002500-\U00002BEF"  # Chinese char
                            u"\U00002702-\U000027B0"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            u"\U0001f926-\U0001f937"
                            u"\U00010000-\U0010ffff"
                            u"\u2640-\u2642"
                            u"\u2600-\u2B55"
                            u"\u200d"
                            u"\u23cf"
                            u"\u23e9"
                            u"\u231a"
                            u"\ufe0f"  # dingbats
                            u"\u3030"
                            "]+", re.UNICODE)
    
    cleaned_description = re.sub(emoji_pattern, '', cleaned_description)
    return cleaned_description

    


def clean_column(column):
    if isinstance(column, str):
        cleaned_column = column.replace("(", "").replace(")", "")
        return cleaned_column
    elif isinstance(column, list):
        cleaned_column = ','.join(map(str, column))
        return cleaned_column
    else:
        return column
    
def imputing_missing_values(df):
    # Identifiez les colonnes numériques pour imputer la médiane
    colonnes_numeriques = df.select_dtypes(include=[np.number]).columns.tolist()

    # Imputez la médiane pour les valeurs manquantes dans les colonnes numériques
    for col in colonnes_numeriques:
        df[col].fillna(df[col].median(), inplace=True)

    return df
    