import pandas as pd, os, datetime
import altair as alt
from altair_saver import save as altair_saver
import sys

from fonctions.param import DATA_ROOT

def hist_totaux(hist):
    hist_totaux = {}
    expr_list = []
    for j in hist:
        expr = hist[f'{j}']
        expr_list.append(expr)
        hist_totaux = expr_list[0]
        for expr in expr_list[1:]:
            hist_totaux &= expr
            
    hist_totaux = hist_totaux.resolve_scale(theta='independent',color='independent')

    return hist_totaux