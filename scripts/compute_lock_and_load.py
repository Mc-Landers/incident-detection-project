import argparse, os, sys
import pandas as pd, os, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fonctions.nb_df.lock_and_load import *
from fonctions.nb_df.save_df import *
from fonctions.nb_df.extract_data import *
from fonctions.crisis_df.save_crisis_df import get_crisis

from fonctions.param import DATA_ROOT

if __name__ == '__main__':
    
    #Charge le dataset préalablement clean en format csv
    xx = extract_data()
    xx,variable_textuelle = lock_and_load_df(xx)
    save_df_mise_en_forme(xx)
    save_variable_textuelle(variable_textuelle)