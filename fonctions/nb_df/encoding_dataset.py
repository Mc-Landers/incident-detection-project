import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT
import copy

def encoding_sous_motifs(xx,n,t):
    #Encoding of "Sous motifs" by indicated time
    unique_values = {"sous_motif" : pd.unique(xx['sous_motif'])}

    #Permet de créer les colonnes de chaque nb par sous motif en fonction du nombre de fois qu'ils apparaissent
    h = []
    h.append(xx['nb'].resample(f"{n}{t}").sum(numeric_only=True))#Create a column that import the total number of nb
    for i in unique_values['sous_motif']:
        s = copy.deepcopy(xx[xx['sous_motif']==i])#Sélection des colonnes seulement avec un sous-motif particulié (EX: HS049)
        s =s.resample(f"{n}{t}").sum(numeric_only=True) #Permet surtout de créer un index identique pour chaque DF. Met en ordre chronologique et 
        s[f"{i}"] = s['nb'] #Renomme les colonnes nb par le nom du sous motif pour plus de clarté
        s = s.drop(columns = ['nb'])#Lâche les informations superflues
        h.append(s)
    return h, unique_values

def encoding_textual_data(xx,h,unique_values,n,t,contact,info,sujet,solution,types):
    #Encoding of all "textual" data (Sujet, Infos, Type) by indicated time
    treshold = [contact,info,sujet,solution,types]
    format_textuel = {}

    for j,k in zip(['contact','info','sujet','solution','types'], treshold):
        new_j = j

        #Groupby and count each textual Data
        colonne = xx.groupby([f'{j}']).count().sort_values("motif", ascending = False)#Tri les valeurs textuelles par ordre d'apparence
        colonne = colonne.reset_index()

        #Loop that check for the values that are higher than the treshold.
        for i in range(len(colonne)): 
            if colonne.loc[colonne.index[i],"motif"] <= k:#Lock row. If the previously group by is under the the treshold defined by k : and k is defined in the parameters window. 
                colonne.loc[colonne.index[i], f"{j}"] = f"miscellaneous_{new_j}"#Rename the low value by "miscellaneous_"
        colonne = colonne.groupby([f'{j}']).sum()#Regroup and add the new "miscellaneous_" textual data.

        xx_colonne = pd.unique(colonne.index)#list of the appropriate values we need to easily encode the texts
        xx_tmp = copy.copy(xx[f'{j}'])#Creation of a copy of a df
        for i in range(len(xx_tmp)):
            l = xx_tmp[i]
            xx_tmp[i] = f'{j}_{l}' if l in xx_colonne else  f'{j}_miscellaneous'#If the .loc of the column'{j}' is part of the unique values set by the treshold in params then it keeps its name and add {j} infront, else it's renamed {j}_miscellaneous
        format_textuel[f'{j}'] = xx_tmp
        xx[f'{j}'] = xx_tmp#Convert the original Dataet thematique column. Why ? It allow us to keep 'nb' and use it as an encoder;
        unique_values[f'{j}'] = pd.unique(xx[f'{j}'])#The unique values changed, we have to update it.
        #Permet de créer les colonnes de chaque nb par contacts en fonction du nombre de fois qu'ils apparaissent
        for i in unique_values[f'{j}']:
            s = copy.deepcopy(xx[xx[f'{j}']==i])#Sélection des colonnes seulement avec un sous-motif particulié (EX: HS049)
            s =s.resample(f"{n}{t}").sum(numeric_only=True) #Permet surtout de créer un index identique pour chaque DF. Met en ordre chronologique et 
            s[f"{i}"] = s['nb'] #Renomme les colonnes nb par le nom d pour plus de clarté
            s = s.drop(columns = ['nb'])#Lâche les informations superflues
            h.append(s)

    xx_final = pd.concat(h, axis=1)#Création du DataFrame à proprement parlé
    
    return xx_final, unique_values, format_textuel