import pandas as pd, os, datetime, sys
import copy
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT
from fonctions.get_holidays import get_holidays
from fonctions.compute_rolling_mean import compute_rolling_mean
from jours_feries_france import JoursFeries

def build_dataset(xx_final,periode_start,periode_end,w,a,unique_values,variable_textuelle):
    #Création du DataFrame
    xx_final = xx_final.fillna(0) #Replace NaN value by 0
    
    if w==1 and a==1:
        #Adding a column to make some groupby by timestamp
        xx_final["jour_hhmm"] = xx_final.index 
        xx_final['jour_semaine'] = xx_final["jour_hhmm"].apply(lambda x: x.weekday())
        xx_final['time'] = xx_final["jour_hhmm"].apply(lambda x: x.time())
        xx_final['jour'] = xx_final["jour_hhmm"].apply(lambda x: x.date())
        xx_final['jour'] = pd.to_datetime(xx_final["jour"], format='%Y-%m-%d')
        xx_final['jour_semaine'] = get_holidays(xx_final,periode_start,periode_end)
        xx_final['jour_hhmm'] = (xx_final['jour_hhmm']).astype(str)#Needed to compare it with the imported crisis.csv
        
        #Dataframe Values by values inplace
        for j in variable_textuelle: 
            unique_values[f"{j}_mean"] = []
            for i in unique_values[f'{j}']:
                xx_final[f"{i}_mean"] = xx_final[[f"{i}","time","jour_semaine"]].groupby(['jour_semaine','time']).transform('mean')
                unique_values[f"{j}_mean"].append(f"{i}_mean")
                
    else:
        #Adding a column to make some groupby by timestamp
        xx_final["jour_hhmm"] = xx_final.index 
        xx_final['jour_semaine'] = xx_final["jour_hhmm"].apply(lambda x: x.weekday())
        xx_final['time'] = xx_final["jour_hhmm"].apply(lambda x: x.time())
        xx_final['jour'] = xx_final["jour_hhmm"].apply(lambda x: x.date())
        xx_final['jour'] = pd.to_datetime(xx_final["jour"], format='%Y-%m-%d')
        xx_final['jour_semaine'] = get_holidays(xx_final,periode_start,periode_end)
        xx_final['jour_hhmm'] = (xx_final['jour_hhmm']).astype(str)#Needed to compare it with the imported crisis.csv
        xx_final[f'nb'] = compute_rolling_mean(xx_final[f'nb'],w,a)
        
        #Dataframe Values by values inplace
        for j in variable_textuelle:
            unique_values[f"{j}_mean"] = []
            for i in unique_values[f'{j}']:
                xx_final[f'{i}'] = compute_rolling_mean(xx_final[f'{i}'],w,a)
                xx_final[f"{i}_mean"] = xx_final[[f"{i}","time","jour_semaine"]].groupby(['jour_semaine','time']).transform('mean')
                unique_values[f"{j}_mean"].append(f"{i}_mean")
        
    return xx_final, unique_values