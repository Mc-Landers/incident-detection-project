import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT
import copy

def data_cleaning_strings(xx,variable_textuelle):
    
    for i in variable_textuelle:
        xx.drop(xx[xx[f'{i}']=='\\N'].index, inplace = True)
        xx[f'{i}'] = xx[f'{i}'].str.strip()
        xx[f'{i}'] = xx[f'{i}'].str.lower()
        xx[f'{i}'] = xx[f'{i}'].apply(lambda x: pd.Series(str(x).replace('/','_')))

    return xx