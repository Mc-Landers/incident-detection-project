import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT
import copy

def save_crisis(crisis):
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    return crisis.to_csv(os.path.join(DATA_ROOT, 'Clean', 'crisis_messagerie_cleaned.csv'))

def get_crisis():
    return pd.read_csv(os.path.join(DATA_ROOT, 'Clean', 'crisis_messagerie_cleaned.csv'), index_col=0)
