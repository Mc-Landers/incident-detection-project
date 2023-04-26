import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT

#Load the Crisis DataFrame
def load_crisis_dataset():
    
    df = pd.read_excel(os.path.join(DATA_ROOT, 'V360_incident_mail_label_2021_2022S1_20221221.xlsx'))
    df = df.rename(columns={"Date/Heure\nDébut" :'Début', "Date/Heure\nFin" : 'Fin'})
    df = df.drop(42, axis=0)
    
    #Pass the selected times in date format
    df["Début"] = df["Début"].apply( lambda x : pd.to_datetime(x, format = "%d/%m/%Y %H:%M"))
    df["Fin"] = df["Fin"].apply( lambda x : pd.to_datetime(x, format = "%d/%m/%Y %H:%M"))
    
    return df