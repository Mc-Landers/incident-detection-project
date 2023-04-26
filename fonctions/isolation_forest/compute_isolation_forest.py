import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

from fonctions.param import DATA_ROOT
from fonctions.metrics.fonctions_metrics import fonction_precision, fonction_recall, fonction_f1_score, fonction_f1_score_Arthur

def compute_isolation_forest(df_total,unique_values,variable_textuelle):
    """Compute isolation forest
    df_total : DataFrame for the prediction,
    unique_values = The name of all the values of the columns
    crises = Les types de gravités pris. Si mineures non inclues choisir 1
    """
    df_isolation = pd.get_dummies(df_total, columns=["jour_semaine","time"])
    
    for i in variable_textuelle:#Drop for each columns previously computed for means
        for k in unique_values[f'{i}_mean']:
            df_isolation = df_isolation.drop( columns = k )
            
    df_isolation= df_isolation.drop(columns = {'jour' , 'jour_hhmm', 'nb', 'Gravité' })#Drop useless columns
    
    #Set the number of anomalies that isolation forest needs to find.
    outliers_fraction = len(df_total[(df_total['Gravité']>1)])/len(df_total)

    #Scaling of the dataset
    scaler = StandardScaler()
    np_scaled = scaler.fit_transform(df_isolation.values)
    data = pd.DataFrame(np_scaled)

    #Calculation of the algorithm
    model = IsolationForest(contamination=outliers_fraction)
    model.fit(data)
    anomaly = model.predict(data)
    
    #For an easier manipulation of the Data : create a column in the original data set
    df_total['ISO'] = anomaly
    df_total['ISO'] = np.where(df_total['ISO'] == -1, 2, df_total['ISO']) #If used to create a graph, the condition used to define a crisis needs to be >1.
    
    precision = fonction_precision(df_total,'ISO', 1)
    recall = fonction_recall(df_total,'ISO', 1)
    f1_score = fonction_f1_score(precision,recall)
    f1_score_Arthur = fonction_f1_score_Arthur(precision, recall)
    
    
    return df_total['ISO'] ,precision, recall, f1_score, f1_score_Arthur