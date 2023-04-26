import pandas as pd, os, datetime, sys
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT, name_algorithm
from fonctions.metrics.save_metrics import *

def compute_tableau_metrics(name_algorithm,n,t,w,a,contact, info, sujet, solution, types):
    list_tableaux = {}
    for j in name_algorithm:
        list_tableaux[f'{j}'] = get_metrics(f'{j}',30,"T",1,1,500,5000,1000,750,750)

    df_metrics_final = pd.concat(list_tableaux, sort=False)
    
    return df_metrics_final
    