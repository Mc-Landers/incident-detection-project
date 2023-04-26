import pandas as pd, os, datetime
import altair as alt
from altair_saver import save as altair_saver
import sys

from fonctions.param import DATA_ROOT

def compute_histogramme_total(df_initial,format_textuel):
    """Construit les diagrammes nécessaires à l'étude des strings textuels sur l'ensemble du dataset.
    df_initial : Dataset inital des tickets. n'a normalement subit qu'une modification des strings
    format_textuel : Dictionnaire comprennant les données intergers des données textuelles"""
    hist = {}
    for j in format_textuel:
        alt_j = pd.DataFrame(format_textuel[f'{j}'], columns=[f'{j}']).value_counts()
        taille = len(df_initial)

        base2 = alt.Chart(alt_j.reset_index().rename(columns={0:'counts'})).transform_joinaggregate(
            TotalTicket=f'sum(counts)',
        ).transform_calculate(
            PercentOfTotal=f"datum.counts / datum.TotalTicket"
        ).encode(
        x=alt.X(f'{j}:N', title=f'Variable textuelle - {j} - ', axis=alt.Axis(labelAngle = 300)),
        y=alt.Y("PercentOfTotal:Q",  title='Part de la variable dans le dataset', axis=alt.Axis(format=".1%")),
        # The highlight will be set on the result of a conditional statement
        color=alt.Color("PercentOfTotal:Q", 
                            legend=alt.Legend(title="%",format=".1%"), 
                            scale=alt.Scale(scheme='yelloworangered')
                           )
        ).properties(title={"text" : [f'% de la part des thématiques pour - {j} - ']}, width=600)

        bar = base2.mark_bar()
        text = base2.mark_text(radius=10,size=13, stroke="#000").encode(text=alt.Text("PercentOfTotal:Q",format=".1%"))

        AB = alt.layer(bar,text).properties(
                    width=400,
                    height=350)
        hist[f'{j}'] = AB
    
    return hist