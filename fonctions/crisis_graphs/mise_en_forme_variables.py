import pandas as pd, os, datetime
import altair as alt
from altair_saver import save as altair_saver
import sys

from fonctions.param import DATA_ROOT

def create_schema_format(panel_graphique_variable, crisis_unique_date):
    schema = {}
    for j in crisis_unique_date:
        num_plots = len(panel_graphique_variable[f'{j}'])
        expr_list = []
        for i in range(0, num_plots, 2):
            if i + 1 < num_plots:
                expr = panel_graphique_variable[f'{j}'][i] | panel_graphique_variable[f'{j}'][i+1]
                expr_list.append(expr)
        schema[f"{j}"] = expr_list[0]
        for expr in expr_list[1:]:
            schema[f"{j}"] &= expr
    return schema