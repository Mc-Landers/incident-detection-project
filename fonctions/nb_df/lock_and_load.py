import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT
import copy

def lock_and_load_df(xx):
    xx = xx.drop(columns=['jour','day','hh','categorie','description'])
    xx = xx.set_index(["jj_mm"])
    xx['nb'] = 1 #Ajout correspondat à un ticket par ligne. Utile à chaque encodage (fait maison) du Data set
    xx.index = pd.to_datetime(xx.index)
    xx[['sujet','info']] = xx['sujet'].apply(lambda x: pd.Series(str(x).split("-",1))) #An action quite long
    xx =  xx.rename(columns={"type": "types"})#Simplement pour éviter la confusion avec la fonction "Type" native
    
    variable_textuelle = [] #Création d'une variable contenant le nom de chaque colonne textuelle du DF.
    for i in xx:
        if i == 'nb':
            continue
        if i =='motif':
            continue
        variable_textuelle.append(i)
    variable_textuelle
    
    return xx,variable_textuelle