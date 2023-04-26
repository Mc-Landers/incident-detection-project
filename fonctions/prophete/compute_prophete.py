from prophet import Prophet
import argparse, os, sys
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.metrics.fonctions_metrics import *

def prophete(df_total, interval_width=0.05, changepoint_range=0.8):
    #Interval width Correspond à la taille du Treshold Yhat et Ylow. Les anomalies sont définie par les moyennes que calculent Prophete du DF donné (se traduisant par Yhat et Ylow), si au dessus ou en dessous = Anomalie.
    #La valeur moyenne est 0.95. Mais comme la variance de notre dataset est minime car les crises ne sont pas liées aux changements de tickets. Nous sommes obligé de le désencer à 0.05 pour obtenir des crises comparables.
    
    #Changepoint La précision avec laquelle nous appliquons la prédiction. Influenceras sur la taille du treshold donné
    #La valeur moyenne est 0.8
    
    df_total = df_total.rename(columns = {"jour_hhmm" : "ds", "nb": "y"})
    train = df_total[df_total['ds']<='2022-03-01']#les dates doivent se suivre car Prophete ne comble pas les trous
    test = df_total[(df_total['ds']<='2022-09-01')&(df_total['ds']>='2022-03-01')]

    m = Prophet(
        daily_seasonality=True,
        yearly_seasonality=False,
        weekly_seasonality=True,
        seasonality_mode="additive",
        interval_width=interval_width,
        changepoint_range=changepoint_range,
    )
    m = m.fit(train)
    forecast = m.predict(test)
    forecast["fact"] = test["y"].reset_index(drop=True)

    forecasted = forecast[["ds", "trend", "yhat", "yhat_lower", "yhat_upper", "fact"]].copy()
    forecasted["anomaly"] = 0
    forecasted.loc[forecasted["fact"] > forecasted["yhat_upper"], "anomaly"] = 2
    # forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'], 'anomaly'] = -1 # We don't care about under anomaly
    # anomaly importances
    forecasted["importance"] = 0
    forecasted.loc[forecasted["anomaly"] == 2, "importance"] = (forecasted["fact"] - forecasted["yhat_upper"]) / forecast["fact"]
    forecasted.loc[forecasted["anomaly"] == -1, "importance"] = (forecasted["yhat_lower"] - forecasted["fact"]) / forecast["fact"]
    
    #m.plot(forecasted) #If needed to have a grpahique view of the curve
    
    test = pd.concat([test.reset_index(drop=True),forecasted.reset_index(drop=True)],axis=1)
    test['prophet'] = test['anomaly']#Easier to call it later in the program
    test = test.drop(columns= ["trend", 	"yhat", 	"yhat_lower", 	"yhat_upper", "fact", "anomaly","importance"])#Useless step
    test.rename(columns = {"ds" : "jour_hhmm", "y": "nb"}, inplace = True)#Useless step
    test = test.set_index('jour_hhmm')#Match the rest of the DFs
    
    precision = fonction_precision(test,'prophet',1)
    recall = fonction_recall(test,'prophet',1)
    f1_score = fonction_f1_score(recall,precision)
    f1_score_Arthur= fonction_f1_score_Arthur(recall,precision)
    
    return test['prophet'], precision, recall, f1_score, f1_score_Arthur