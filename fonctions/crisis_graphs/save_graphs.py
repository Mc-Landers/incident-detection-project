import sys
import pandas as pd, os, datetime
import altair as alt
from altair_saver import save as altair_saver

from fonctions.param import DATA_ROOT

def save_graphs_total(schema_totaux,n,t,w,a,contact,info,sujet,solution,types):
    for i in schema_totaux:
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation'))
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}'))
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}', 'Période')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Période'))
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Période',f'{i}')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Période',f'{i}'))
                     
        graph = (schema_totaux[f'{i}']).save(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Période',f'{i}',f'Période_de_crise_{i}_{n}_{t}_{w}_{a}_{contact}_{info}_{sujet}_{solution}_{types}.html'))
    return graph

def save_graphs_variable(schema,n,t,w,a,contact,info,sujet,solution,types):
    for i in schema:
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation'))
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}'))
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}', 'Période')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Période'))
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Période',f'{i}')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Période',f'{i}'))
                     
        graph = (schema[f'{i}']).save(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Période',f'{i}',f'Période_de_crise_{i}_Variables_{n}_{t}_{w}_{a}_{contact}_{info}_{sujet}_{solution}_{types}.html'))
    
    return graph

def save_graphs_variable_par_variable(schema_variables,n,t,w,a,contact,info,sujet,solution,types):
    for i in schema_variables:
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation'))
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}'))
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}', 'Variable')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Variable'))
        if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Variable',f'{i}_variable')):
            os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Variable',f'{i}_variable'))
                     
        graph = (schema_variables[f'{i}']).save(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Variable',f'{i}_variable',f'Variables_{i}_{n}_{t}_{w}_{a}_{contact}_{info}_{sujet}_{solution}_{types}.html'))
    
    return graph

def save_histogrammes_totaux(hist_totaux,n,t,w,a,contact,info,sujet,solution,types):
    if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation')):
        os.mkdir(os.path.join(DATA_ROOT,'Visualisation'))
    if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}')):
        os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}'))
    if not os.path.exists(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}', 'Overall')):
        os.mkdir(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Overall'))
                     
        graph = hist_totaux.save(os.path.join(DATA_ROOT,'Visualisation',f'{n}_{t}','Overall',f'Histogrammes_totaux_{n}_{t}_{w}_{a}_{contact}_{info}_{sujet}_{solution}_{types}.html'))
    
    return graph