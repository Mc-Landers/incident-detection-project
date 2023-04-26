import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT
import copy

def extract_data(file = "spas mail 2021 2022.csv"):
    xx = pd.read_csv(os.path.join(DATA_ROOT, file),sep = ';', header=None)
    xx =  xx.rename(columns={0:'jour', 1:'day',2:'hh',3:'jj_mm', 4:'categorie', 5:'motif', 6:'sous_motif', 7:'type', 8:'contact', 9:'sujet', 10:'solution', 11:'description'})
    return xx