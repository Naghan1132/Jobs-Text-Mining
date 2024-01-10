import os
from SQLite_v2 import *
from insert import *
import pandas as pd


def exec():
    print(os.getcwd())
    df, df2 = load_data(path=f'{os.getcwd()}/base_brute.db')
    create_dw(df, df2)