import pandas as pd, os, datetime, sys
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT

def save_prediction_random(df_random,r,n,t,w,a, contact, info, sujet, solution, types):
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean','Rand')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean','Rand'))
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean','Rand',f'{n}_{t}')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean','Rand',f'{n}_{t}'))
    return df_random.to_csv(os.path.join(DATA_ROOT,'Clean','Rand', f'{n}_{t}', f'data_random_{r}_{n}_{t}_{w}_{a}_Co_{contact}_In_{info}_Su_{sujet}_So_{solution}_Ty_{types}.csv'))