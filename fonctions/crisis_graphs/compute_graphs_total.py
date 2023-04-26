import pandas as pd, os, datetime
import altair as alt
from altair_saver import save as altair_saver
import numpy as np
import sys

from fonctions.param import DATA_ROOT


def graphs_variables_totales_crise(df_total, df_crisis, unique_values, variable_textuelle, n, t, c = 1, crisis_column = 'Gravité', date = "whole"):
    """Un dictionnaire qui doit être appelé : nomdelavariable['periode'][1]
    df_total : Dataframe du projet, avec chaque valeur encodée
    df_crisis : Dataframe des crises avant le passage à la minute
    n : Valeur numérique du pas de temps sélectionné
    t : Valeur temporelle ddu pas de temps sélectionné
    c : Le niveau de crises sélectionné. 4 = Crise Jaune, 3 Majeur, 2 Grave 1 Mineur. Valeur par défaut >1
    crisis_column : Colonne du dataframe du projet prise pour la sélection des crises. ajoutée avec comme idée de choisir quel algorithme observé. Valeur par défaut = Gravité
    date : Sélection d'une date précise ou non. Valeur par défaut 'whole' correspondant à toutes les dates de crises du DF. Pour la sélection des date, l'orthographe doit absolument être du type "YYYY-MM-DD". Peut s'arrêter au mois, a la dizaine de jour, a l'années. Altaïr refuse plus de 5000 entrées
    """
    
    
    if date == "whole":
#        df_total = df_total.drop(columns = ['time'])#obligé de drop pour utiliser Altaïr
        panel_graphique = {} #Dictionnaire qui recoupe tous les jours de crises et tous les models demandés
        hist = {}#Dictionnaire qui recoupe tous les diagrames

        
        crisis_df = df_total[df_total[f'{crisis_column}']>c]#Défini la colonne qui sert à montrer les crises et le niveau de crise. A été pensé pour switcher avec les crises trouvées par les algorithmes
        #Implique le besoin dans les retours d'algorithme que les crises soient > 1 dans l'annotation
        crisis_unique_date = pd.unique(crisis_df["jour"])#Remonte les jours des crises

        df_crisis = df_crisis[df_crisis.Gravité_num > c] #Dataframe de crise encodées, sélection des crises au dessus de mineur

        for i in crisis_unique_date:#Pour chaque date

            #Sources et principes des conditions
            source = df_total.filter(like=i,axis=0) #x[0:1000] #x.filter(like="2022-03-22",axis=0) Pour date précise. Pour une période utiliser l'expression suivante x[0:5000] - Ne marche que sur un Frame de 5000 périodes
            source2 = df_crisis[(df_crisis["Début"].between(source.loc[source.index[0],'jour_hhmm'],source.loc[source.index[-1],'jour_hhmm'])) | (df_crisis["Fin"].between(source.loc[source.index[0],'jour_hhmm'],source.loc[source.index[-1],'jour_hhmm']))] #Prend les périodes de crises se trouvant dans les périodes de tickets
            selection = alt.selection_multi(fields=['Gravité'], bind='legend') #Pour la légende intéractive ; les champs qui seront pris en compte pour l'intéraction
            resize = alt.selection_interval(bind='scales') #Pour le graphique intéractif - Notamment zooms
            
            #Pour chaque date créer sa liste de graphqiue
            i_periode = []

            #Pour chaque sujet créer son graphique
            for j in variable_textuelle: #Chaque données textuelle qui a été compute
                if len(unique_values[f'{j}']) > 11:#bug de altaïr si plus de 11 variables
                    continue
                
                line = alt.Chart(source).transform_fold(
                    unique_values[f'{j}'],#Les valeurs utilisées sur l'axis Y
                ).mark_line().encode(
                    alt.X('jour_hhmm:T', axis=alt.Axis(format=("%H %M %a %d %b"))),
                    alt.Y(f'value:Q'),
                    alt.Color('key:N',scale=alt.Scale(scheme='accent'), legend=alt.Legend(title=f'{j}', orient="top-right",labelFontSize=12,titleFontSize=12)),
                )

                #Les périodes de crises
                rect = alt.Chart(source2).mark_rect().encode(
                    x= "Début:T",
                    x2="Fin:T",
                    color=alt.Color('Gravité_num:Q',
                                    sort=["4", "3", "2"],
                                    legend=alt.Legend(title="Gravité crise",orient="top-left",labelFontSize=12,titleFontSize=12),
                                    scale=alt.Scale(
                                        domain=["4", "3", "2"], 
                                        range=["black", "red", "orange"]
                                    )
                                   ),
                    opacity=alt.condition(selection, alt.value(0.4), alt.value(0.1))
                ).interactive().add_selection(
                    selection
                )
                
                #Les moyennes des variables
                rule = alt.Chart(source).transform_fold(
                    unique_values[f'{j}_mean'],
                ).mark_line(opacity=0.5).encode(
                    alt.X('jour_hhmm:T', title=f"Heure / Jour Période de {n}{t} ", axis=alt.Axis(format=("%H %M %a %d %b"))),
                    alt.Y('value:Q',title=f"Nombre de requêtes ouvertes selon {j}"),
                    alt.Color('key:N', scale=alt.Scale(scheme='accent'), legend=alt.Legend(title=f'{j}_mean', orient="top-right",labelFontSize=12,titleFontSize=12)),
                )
                
                #Concatenation des courbes précédentes sur un même graphique
                j_alt = alt.layer(rect ,line, rule).properties(
                    width=750,
                    height=500,
                    title = alt.TitleParams(text = f'{j}', 
                                                            font = 'Ubuntu Mono', 
                                                            fontSize = 22, 
                                                            color = '#3E454F', 
                                                            subtitleFont = 'Ubuntu Mono',
                                                            subtitleFontSize = 16, 
                                                            subtitleColor = '#3E454F'
                              )
                ).resolve_scale(color='independent').add_selection(resize)
                
#####Creation of the second graph : Diagram

                source3 = source.groupby(np.arange(len(source)) // len(source)).sum(numeric_only=True)#Necessary to merge all the lines of a day or the date selection into one line taht will calculate the % of the themes
                base2 = alt.Chart(source3).transform_fold(
                        list(unique_values[f'{j}'])#Imperative to put it in a list format
                        ).transform_calculate(PercentOfTotal="datum.value / datum.nb").encode(
                x=alt.X(f'key:N', title=f'Variable textuelle - {j} - ', axis=alt.Axis(labelAngle = 300)),
                y=alt.Y("PercentOfTotal:Q",  title='Part de la variable dans le dataset', axis=alt.Axis(format=".1%")),
                # The highlight will be set on the result of a conditional statement
                color=alt.Color("PercentOfTotal:Q", 
                                    legend=alt.Legend(title="%",format=".1%"), 
                                    scale=alt.Scale(scheme='yelloworangered')
                                   )
                ).properties(width=600, title={"text" : [f'% de la part des thématiques pour " {j} "'],
                       "subtitle": [f"{i}"]})

                bar = base2.mark_bar()
                text = base2.mark_text(radius=10,size=13, stroke="#000").encode(text=alt.Text("PercentOfTotal:Q",format=".1%"))

                AB = alt.layer(bar,text).properties(
                            width=400,
                            height=350)
                hist[f'{j}'] = AB
                
#####Join the two charts

                i_periode.append(j_alt|hist[f'{j}'])
                panel_graphique[i] = i_periode

                
                
################################################
################################################



    else:#Si une date particulère est passée. L'orthographe doit absolument être du type "YYYY-MM-DD". Peut s'arrêter au mois, a la dizaine de jour, a l'années. Altaïr refuse plus de 5000 entrées
        df_total = df_total.drop(columns = ['time'])#obligé de drop pour utiliser Altaïr
        panel_graphique = {} #Dictionaire qui recoupe tous les jours de crises et tous les models demandés
        hist = {}

        crisis_unique_date = date#Remonte les jours des crises

        df_crisis = df_crisis[df_crisis.Gravité_num > c] #Dataframe de crise encodées, sélection des crises au dessus de mineur

        for i in crisis_unique_date:#Pour chaque date

            #Sources et principes des conditions
            source = df_total.filter(like=i,axis=0) #x[0:1000] #x.filter(like="2022-03-22",axis=0) Pour date précise. Pour une période utiliser l'expression suivante x[0:5000] - Ne marche que sur un Frame de 5000 périodes
            source2 = df_crisis[(df_crisis["Début"].between(source.loc[source.index[0],'jour_hhmm'],source.loc[source.index[-1],'jour_hhmm'])) | (df_crisis["Fin"].between(source.loc[source.index[0],'jour_hhmm'],source.loc[source.index[-1],'jour_hhmm']))] #Prend les périodes de crises se trouvant dans les périodes de tickets
            selection = alt.selection_multi(fields=['Gravité'], bind='legend') #Pour la légende intéractive ; les champs qui seront pris en compte pour l'intéraction
            resize = alt.selection_interval(bind='scales') #Pour le graphique intéractif - Notamment zooms
            
            #Pour chaque date créer sa liste de graphique
            i_periode = []

            #Pour chaque sujet créer son graphique
            for j in variable_textuelle: #Chaque données textuelle qui a été compute
                if len(unique_values[f'{j}']) > 11:#bug de altaïr si plus de 11 variables
                    continue
                    
                line = alt.Chart(source).transform_fold(
                    unique_values[f'{j}'],#Les valeurs utilisées sur l'axis Y
                ).mark_line().encode(
                    alt.X('jour_hhmm:T', axis=alt.Axis(format=("%H %M %a %d %b"))),
                    alt.Y(f'value:Q'),
                    alt.Color('key:N',scale=alt.Scale(scheme='accent'), legend=alt.Legend(title=f'{j}', orient="top-right",labelFontSize=12,titleFontSize=12)),
                )

                #Les périodes de crises
                rect = alt.Chart(source2).mark_rect().encode(
                    x= "Début:T",
                    x2="Fin:T",
                    color=alt.Color('Gravité_num:Q',
                                    sort=["4", "3", "2"],
                                    legend=alt.Legend(title="Gravité crise",orient="top-left",labelFontSize=12,titleFontSize=12),
                                    scale=alt.Scale(
                                        domain=["4", "3", "2"], 
                                        range=["black", "red", "orange"]
                                    )
                                   ),
                    opacity=alt.condition(selection, alt.value(0.4), alt.value(0.1))
                ).interactive().add_selection(
                    selection
                )
                
                #Les moyennes des variables
                rule = alt.Chart(source).transform_fold(
                    unique_values[f'{j}_mean'],
                ).mark_line(opacity=0.5).encode(
                    alt.X('jour_hhmm:T', title=f"Heure / Jour Période de {n}{t} ", axis=alt.Axis(format=("%H %M %a %d %b"))),
                    alt.Y('value:Q',title=f"Nombre de requêtes ouvertes selon {j}"),
                    alt.Color('key:N', scale=alt.Scale(scheme='accent'), legend=alt.Legend(title=f'{j}_mean', orient="top-right",labelFontSize=12,titleFontSize=12)),
                )
                
                #Concatenation des courbes précédentes sur un même graphique
                j_alt = alt.layer(rect ,line, rule).properties(
                    width=1000,
                    height=500,
                    title = alt.TitleParams(text = f'{j}', 
                                                            font = 'Ubuntu Mono', 
                                                            fontSize = 22, 
                                                            color = '#3E454F', 
                                                            subtitleFont = 'Ubuntu Mono',
                                                            subtitleFontSize = 16, 
                                                            subtitleColor = '#3E454F'
                              )
                ).resolve_scale(color='independent').add_selection(resize)
                
#####Creation of the second graph : Diagram

                source3 = source.groupby(np.arange(len(source)) // len(source)).sum(numeric_only=True)#Necessary to merge all the lines of a day or the date selection into one line taht will calculate the % of the themes
                base2 = alt.Chart(source3).transform_fold(
                        list(unique_values[f'{j}'])#Imperative to put it in a list format
                        ).transform_calculate(PercentOfTotal="datum.value / datum.nb").encode(
                x=alt.X(f'key:N', title=f'Variable textuelle - {j} - ', axis=alt.Axis(labelAngle = 300)),
                y=alt.Y("PercentOfTotal:Q",  title='Part de la variable dans le dataset', axis=alt.Axis(format=".1%")),
                # The highlight will be set on the result of a conditional statement
                color=alt.Color("PercentOfTotal:Q", 
                                    legend=alt.Legend(title="%",format=".1%"), 
                                    scale=alt.Scale(scheme='yelloworangered')
                                   )
                ).properties(width=600, title={"text" : [f'% de la part des thématiques pour " {j} "'],
                       "subtitle": [f"{i}"]})

                bar = base2.mark_bar()
                text = base2.mark_text(radius=10,size=13, stroke="#000").encode(text=alt.Text("PercentOfTotal:Q",format=".1%"))

                AB = alt.layer(bar,text).properties(
                            width=400,
                            height=350)
                hist[f'{j}'] = AB
                
#####Join the two charts

                i_periode.append(j_alt|hist[f'{j}'])
                panel_graphique[i] = i_periode
                
    return panel_graphique, crisis_unique_date#Un dictionnaire qui doit être appelé : nomdelavaribale['periode'][1]