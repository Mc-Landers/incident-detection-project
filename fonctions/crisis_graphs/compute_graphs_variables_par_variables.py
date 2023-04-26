import pandas as pd, os, datetime
import altair as alt
from altair_saver import save as altair_saver
import sys

from fonctions.param import DATA_ROOT


def graphs_variables_par_variables_crise(df_total, df_crisis, unique_values,variable_textuelle, n, t, c = 1, crisis_column = 'Gravité', date = "whole"):
    """Un dictionnaire qui doit être appelé : nomdelavariable['variable'][1]
    df_total : Dataframe du projet, avec chaque valeur encodée
    df_crisis : Dataframe des crises avant le passage à la minute
    n : Valeur numérique du pas de temps sélectionné
    t : Valeur temporelle ddu pas de temps sélectionné
    c : Le niveau de crises sélectionné. 4 = Crise Jaune, 3 Majeur, 2 Grave 1 Mineur. Valeur par défaut >1
    crisis_column : Colonne du dataframe du projet prise pour la sélection des crises. ajoutée avec comme idée de choisir quel algorithme observé. Valeur par défaut = Gravité
    date : Sélection d'une date précise ou non. Valeur par défaut 'whole' correspondant à toutes les dates de crises du DF. Pour la sélection des date, l'orthographe doit absolument être du type "YYYY-MM-DD". Peut s'arrêter au mois, a la dizaine de jour, a l'années. Altaïr refuse plus de 5000 entrées
    """

    if date == "whole":
        df_total = df_total.drop(columns=['time'])  # obligé de drop pour utiliser Altaïr
        panel_graphique_variables_par_variables = {}  # Dictionaire qui recoupe tous les jours de crises et tous les models demandés

        crisis_df = df_total[df_total[f'{crisis_column}']>c]#Défini la colonne qui sert à montrer les crises et le niveau de crise. A été pensé pour switcher avec les crises trouvées par les algorithmes
        #Implique le besoin dans les retours d'algorithme que les crises soient > 1 dans l'annotation
        crisis_unique_date = pd.unique(crisis_df["jour"])#Remonte les jours des crises

        df_crisis = df_crisis[df_crisis.Gravité_num > c]#Dataframe de crise encodées, sélection des crises au dessus de mineur

        for j in variable_textuelle:#Pour chaque thème qu'il faudrait automatiser dans la création du dataset (en cours)
            for k in unique_values[f'{j}']:#Les valeurs utilisées sur l'axis Y
                k_variable = [] #Pour chaque variable créer sa liste de graphqiue par date
                for i in crisis_unique_date:#Pour chaque date

                    #Sources et principes des conditions
                    source = df_total.filter(like=i,axis=0) #x[0:1000] #x.filter(like="2022-03-22",axis=0) Pour date précise. Pour une période utiliser l'expression suivante x[0:5000] - Ne marche que sur un Frame de 5000 périodes
                    source2 = df_crisis[(df_crisis["Début"].between(source.loc[source.index[0],'jour_hhmm'],source.loc[source.index[-1],'jour_hhmm'])) | (df_crisis["Fin"].between(source.loc[source.index[0],'jour_hhmm'],source.loc[source.index[-1],'jour_hhmm']))] #Prend les périodes de crises se trouvant dans les périodes de tickets
                    selection = alt.selection_multi(fields=['Gravité'], bind='legend') #Pour la légende intéractive ; les champs qui seront pris en compte pour l'intéraction
                    resize = alt.selection_interval(bind='scales')

                    #chaque ligne noire du graphique
                    line = alt.Chart(source).mark_line(color='#000000').encode(
                        alt.X('jour_hhmm:T', axis=alt.Axis(format=("%H %M %a %d %b")), title=f"Pas de temps en {n} {t}"),
                        alt.Y(f'{k}:Q', title=f"Nombre de requêtes ouvertes pour {k}"),
                    )

                    #Chaque période de crises
                    rect = alt.Chart(source2).mark_rect().encode(
                        x= "Début:T",
                        x2="Fin:T",
                        color=alt.Color('Gravité_num:Q',
                                        sort=["4", "3", "2"],
                                        legend=alt.Legend(title="Gravité crise",orient="top-left",labelFontSize=11,titleFontSize=11),
                                        scale=alt.Scale(
                                            domain=["4", "3", "2"], 
                                            range=["black", "red", "orange"]
                                        )
                                       ),
                        opacity=alt.condition(selection, alt.value(0.4), alt.value(0.1))
                    ).interactive().add_selection(
                        selection
                    )

                    #La moyenne associée à la ligne noire
                    rule = line.mark_area(color='purple',opacity=0.3).encode(y=f'{k}_mean')

                    #Concatenation des courbes précédentes sur un même graphique de la période de crise / Ligne noire / Ligne médianne
                    j_alt = alt.layer(rect ,line, rule).properties(
                        width=350,
                        height=250,
                        title = alt.TitleParams(text = f'Noir = {k}, Violet = {k}_mean', 
                                                                font = 'Ubuntu Mono', 
                                                                fontSize = 15, 
                                                                color = '#3E454F', 
                                                                subtitleFont = 'Ubuntu Mono',
                                                                subtitleFontSize = 12, 
                                                                subtitleColor = '#3E454F'
                                  )
                    ).resolve_scale(color='independent').add_selection(resize)

                    k_variable.append(j_alt)

                panel_graphique_variables_par_variables[k] = k_variable

    ###########################
    ###########################

    else:#Si une date particulère est passée. L'orthographe doit absolument être du type "YYYY-MM-DD". Peut s'arrêter au mois, a la dizaine de jour, a l'années. Altaïr refuse plus de 5000 entrées
        df_total = df_total.drop(columns = ['time'])#obligé de drop pour utiliser Altaïr
        panel_graphique_variables_par_variables = {} #Dictionaire qui recoupe tous les jours de crises et tous les models demandés
        crisis_unique_date = date#Remonte les jours des crises

        df_crisis = df_crisis[df_crisis.Gravité_num > c]#Dataframe de crise encodées, sélection des crises au dessus de mineur

        for j in variable_textuelle:#Pour chaque thème qu'il faudrait automatiser dans la création du dataset (en cours)
            for k in unique_values[f'{j}']:#Les valeurs utilisées sur l'axis Y
                k_variable = [] #Pour chaque variable créer sa liste de graphqiue par date
                for i in crisis_unique_date:#Pour chaque date

                    #Sources et principes des conditions
                    source = df_total.filter(like=i,axis=0) #x[0:1000] #x.filter(like="2022-03-22",axis=0) Pour date précise. Pour une période utiliser l'expression suivante x[0:5000] - Ne marche que sur un Frame de 5000 périodes
                    source2 = df_crisis[(df_crisis["Début"].between(source.loc[source.index[0],'jour_hhmm'],source.loc[source.index[-1],'jour_hhmm'])) | (df_crisis["Fin"].between(source.loc[source.index[0],'jour_hhmm'],source.loc[source.index[-1],'jour_hhmm']))] #Prend les périodes de crises se trouvant dans les périodes de tickets
                    selection = alt.selection_multi(fields=['Gravité'], bind='legend') #Pour la légende intéractive ; les champs qui seront pris en compte pour l'intéraction
                    resize = alt.selection_interval(bind='scales')

                    #chaque ligne noire du graphique
                    line = alt.Chart(source).mark_line(color='#000000').encode(
                        alt.X('jour_hhmm:T', axis=alt.Axis(format=("%H %M %a %d %b")), title=f"Pas de temps en {n} {t}"),
                        alt.Y(f'{k}:Q', title=f"Nombre de requêtes ouvertes pour {k}"),
                    )

                    #Chaque période de crises
                    rect = alt.Chart(source2).mark_rect().encode(
                        x= "Début:T",
                        x2="Fin:T",
                        color=alt.Color('Gravité_num:Q',
                                        sort=["4", "3", "2"],
                                        legend=alt.Legend(title="Gravité crise",orient="top-left",labelFontSize=11,titleFontSize=11),
                                        scale=alt.Scale(
                                            domain=["4", "3", "2"], 
                                            range=["black", "red", "orange"]
                                        )
                                       ),
                        opacity=alt.condition(selection, alt.value(0.4), alt.value(0.1))
                    ).interactive().add_selection(
                        selection
                    )

                    #La moyenne associée à la ligne noire
                    rule = line.mark_area(color='purple',opacity=0.3).encode(y=f'{k}_mean')

                    #Concatenation des courbes précédentes sur un même graphique de la période de crise / Ligne noire / Ligne médianne
                    j_alt = alt.layer(rect ,line, rule).properties(
                        width=350,
                        height=250,
                        title = alt.TitleParams(text = f'Noir = {k}, Violet = {k}_mean', 
                                                                font = 'Ubuntu Mono', 
                                                                fontSize = 15, 
                                                                color = '#3E454F', 
                                                                subtitleFont = 'Ubuntu Mono',
                                                                subtitleFontSize = 12, 
                                                                subtitleColor = '#3E454F'
                                  )
                    ).resolve_scale(color='independent').add_selection(resize)

                    k_variable.append(j_alt)

                panel_graphique_variables_par_variables[k] = k_variable

    return panel_graphique_variables_par_variables