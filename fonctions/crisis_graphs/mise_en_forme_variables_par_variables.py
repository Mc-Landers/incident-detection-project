import pandas as pd, os, datetime
import altair as alt
from altair_saver import save as altair_saver
import sys

from fonctions.param import DATA_ROOT

def create_schema(panel_graphique_variables_par_variables, variable,variable_textuelle):
    schema_variables = {}
    for j in variable_textuelle:
        for k in variable[f'{j}']:
            num_plots = len(panel_graphique_variables_par_variables[f'{k}'])
            expr_list = []
            for i in range(0, num_plots, 2):
                if i + 1 < num_plots:
                    expr = panel_graphique_variables_par_variables[f'{k}'][i] | panel_graphique_variables_par_variables[f'{k}'][i+1]
                    expr_list.append(expr)
            schema_variables[f"{k}"] = expr_list[0]
            for expr in expr_list[1:]:
                schema_variables[f"{k}"] &= expr
    return schema_variables