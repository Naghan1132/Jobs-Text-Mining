import sys
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
sys.path.append(chemin_actuel)

# Importer un autre fichier depuis le dossier sql
from SQLite_v2 import *
from insert import *
import pandas as pd



def exec():
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    df, df2 = load_data(path=chemin_actuel+'/base_brute.db')
    create_dw(df, df2,chemin_actuel)