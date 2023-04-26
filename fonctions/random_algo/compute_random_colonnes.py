import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import copy

from fonctions.random_algo.bernoulli import *

def compute_random_colonnes(df_total):
    for r in range(10,100,10):
        #Implantation de période de crise random
        df_total[f'rand_{r}'] = 0

        for i in range(len(df_total)):#Filling the columns.
            i_row = copy.deepcopy(df_total.iloc[i])
            i_row[f'rand_{r}'] = tirage_de_bernoulli((r*0.01))
            df_total.loc[df_total.index[i],f'rand_{r}'] = i_row[f'rand_{r}']
            
        #All algorithm crisis need to be over 1 to make the graphs usable on every algorithm spikes -> therefor Ints and then 0 or 2
        df_total.loc[df_total[f'rand_{r}'] == False, f'rand_{r}'] = 0
        df_total.loc[df_total[f'rand_{r}'] == True, f'rand_{r}'] = 2
    
    return df_total