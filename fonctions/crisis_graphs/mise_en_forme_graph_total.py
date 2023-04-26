import pandas as pd, os, datetime
import altair as alt
from altair_saver import save as altair_saver
import sys

from fonctions.param import DATA_ROOT

def schema_totaux(panel_graphique):
    schema_totaux = {}
    for j in panel_graphique:
        num_plots = len(panel_graphique[f'{j}'])
        expr_list = []
        for i in range(0, num_plots):
            if i + 1 <= num_plots:
                expr = panel_graphique[f'{j}'][i].resolve_scale(theta='independent',color='independent')
                expr_list.append(expr)
        schema_totaux[f"{j}"] = expr_list[0]
        for expr in expr_list[1:]:
            schema_totaux[f"{j}"] &= expr
    return schema_totaux