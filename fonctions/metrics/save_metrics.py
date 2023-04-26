import pandas as pd, os, datetime, sys
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT

def save_metrics(tableau_metrics,name_algorithm,n,t,w,a,contact, info, sujet, solution, types):
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean','Metrics')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean','Metrics'))
    return tableau_metrics.to_csv(os.path.join(DATA_ROOT,'Clean','Metrics', f'metrics_{name_algorithm}_{n}_{t}_{w}_{a}_Co_{contact}_In_{info}_Su_{sujet}_So_{solution}_Ty_{types}.csv'))

def save_metrics_final(df_metrics_final,n,t,w,a,contact, info, sujet, solution, types):
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean','Metrics')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean','Metrics'))
    return df_metrics_final.to_csv(os.path.join(DATA_ROOT,'Clean','Metrics', f'METRICS_FINAL_{n}_{t}_{w}_{a}_Co_{contact}_In_{info}_Su_{sujet}_So_{solution}_Ty_{types}.csv'))
    

def get_metrics(name_algorithm,n,t,w,a,contact, info, sujet, solution, types):
    return pd.read_csv(os.path.join(DATA_ROOT,'Clean','Metrics', f'metrics_{name_algorithm}_{n}_{t}_{w}_{a}_Co_{contact}_In_{info}_Su_{sujet}_So_{solution}_Ty_{types}.csv'), index_col=0)

def get_metrics_final():
    return pd.read_csv(os.path.join(DATA_ROOT,'Clean','Metrics',f'METRICS_FINAL_{n}_{t}_{w}_{a}_Co_{contact}_In_{info}_Su_{sujet}_So_{solution}_Ty_{types}.csv'), index_col=0)