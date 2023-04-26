import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import copy

from fonctions.param import DATA_ROOT
from fonctions.metrics.fonctions_metrics import fonction_precision, fonction_recall, fonction_f1_score, fonction_f1_score_Arthur

def compute_random_algorithm(df_total,r):

    precision = fonction_precision(df_total, f'rand_{r}', 1)
    recall = fonction_recall(df_total, f'rand_{r}', 1)
    f1_score = fonction_f1_score(precision,recall)
    f1_score_Arthur = fonction_f1_score_Arthur(precision, recall)

    return df_total[f'rand_{r}'], precision, recall, f1_score, f1_score_Arthur