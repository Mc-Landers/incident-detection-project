import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT
import copy

def add_crisis(xx_final,crisis):
    #Compare the Time stamp of the Thematique DF and the Crisis DF and if it match add it to Gravité Columns
    new_rows = []
    xx_final["Gravité"]=0
    
    for i in range(len(xx_final)):
        i_row = xx_final.iloc[i]
        i_date = i_row["jour_hhmm"]

        if i_date in crisis["jour_hhmm"]:
            current_gravity = i_row['Gravité']
            i_row['Gravité'] = crisis.loc[i_date,'Gravité'] if crisis.loc[i_date,'Gravité'] > current_gravity else current_gravity
        new_rows.append(i_row)

    xx_final = pd.DataFrame(new_rows)
    
    return xx_final