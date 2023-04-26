import argparse, os, sys
import pandas as pd, os, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fonctions.nb_df.data_cleaning_strings import * 
from fonctions.nb_df.save_df import *
from fonctions.nb_df.create_200000_lines_df import *
from fonctions.nb_df.changing_visual_crm_values import *

from fonctions.param import DATA_ROOT

if __name__ == '__main__':
    
    #Charger les valeurs nécessaires
    xx = get_df_mise_en_forme()
    variable_textuelle = get_variable_textuelle()
    
    #Clean les colomnes textuelles
    xx_cleaned = data_cleaning_strings(xx,variable_textuelle)
    save_cleaning_strings_df(xx_cleaned)
    
    #For VisualCRM
    variable_dataframe_to_convert = create_200000_lines_df(xx_cleaned)
    save_variable_dataframe_to_convert(variable_dataframe_to_convert)
    
    #After Visual CRM
    new_dataframe = changing_visual_crm_values(xx_cleaned,variable_dataframe_to_convert,variable_textuelle)
    