import pandas as pd, os, datetime, sys
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT
import copy

#########
######### Saving datasets and variables
#########


def save_df(xx_final,n,t,w,a):
    """Save a final dataframe cointaining all the basic mathematical formulas (means, rolling means) and textual encoding."""
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    return xx_final.to_csv(os.path.join(DATA_ROOT,'Clean', f'data_messagerie_cleaned_{n}_{t}_{w}_{a}.csv'))

def save_cleaning_strings_df(xx_final):
    """Save a dataframe used to be modify on the textual parts after analysis of the textual tresholds."""
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    return xx_final.to_csv(os.path.join(DATA_ROOT,'Clean', f'data_messagerie_cleaning_strings.csv'))

def save_unique_values(unique_values,n,t,w,a,contact,info,sujet,solution,types):
    """Save a dictionnary with all the textual columns and the text category higher than the treshold. This dictionnary is strings only. Is used for For loops that target the textual columns"""
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    f = open(os.path.join(DATA_ROOT, 'Clean', f"unique_values_{n}_{t}_{w}_{a}_Co_{contact}_In_{info}_Su_{sujet}_So_{solution}_Ty_{types}.pkl"),"wb")
    pickle.dump(unique_values,f)
    f.close()
    return f

def save_variable_textuelle(variable_textuelle):
    """Save a dictionnary with all the textual columns. This dictionnary is strings only. Is used for For loops that target the textual columns"""
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    f = open(os.path.join(DATA_ROOT, 'Clean', f"variable_textuelle.pkl"),"wb")
    pickle.dump(variable_textuelle,f)
    f.close()
    return f

def save_format_textuel(format_textuel,n,t,w,a,contact,info,sujet,solution,types):
    """Save a dictionnary with all the strings of the textual columns by treshold. This dictionnary has all the strings in inntergers. The NaN values are not taken into account. Is used for graphs and basic maths to understand the distribution of textual data by tickets"""
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    f = open(os.path.join(DATA_ROOT, 'Clean', f"format_textuel_{n}_{t}_{w}_{a}_Co_{contact}_In_{info}_Su_{sujet}_So_{solution}_Ty_{types}.pkl"),"wb")
    pickle.dump(format_textuel,f)
    f.close()
    return f

def save_df_mise_en_forme(xx):
    """Save a dataframe cointaining all the right columns ready for data cleaning."""
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    return xx.to_csv(os.path.join(DATA_ROOT,'Clean', f'data_mise_en_forme.csv'))

def save_variable_dataframe_to_convert(variable_dataframe_to_convert):
    """Save a list that contain every names of a divided Dataset. It goes from 0 to 200 000 rows."""
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    f = open(os.path.join(DATA_ROOT, 'Clean', f"variable_dataframe_to_convert.pkl"),"wb")
    pickle.dump(variable_dataframe_to_convert,f)
    f.close()
    return f

#########
######### Loading datasets and variables
#########



def get_data(n,t,w,a):
    """Return a final dataframe cointaining all the basic mathematical formulas (means, rolling means) and textual encoding."""
    return pd.read_csv(os.path.join(DATA_ROOT, 'Clean', f'data_messagerie_cleaned_{n}_{t}_{w}_{a}.csv'), index_col=0, parse_dates=True)

def get_data_cleaning_strings():
    """Return a dataframe used to be modify on the textual parts after analysis of the textual tresholds."""
    return pd.read_csv(os.path.join(DATA_ROOT,'Clean', f'data_messagerie_cleaning_strings.csv'), index_col=0, parse_dates=True)

def get_unique_values(n,t,w,a,contact,info,sujet,solution,types):
    """Return a dictionnary with all the textual columns and the text category higher than the treshold. This dictionnary is strings only. Is used for For loops that target the textual columns"""
    return pd.read_pickle(os.path.join(DATA_ROOT,'Clean', f"unique_values_{n}_{t}_{w}_{a}_Co_{contact}_In_{info}_Su_{sujet}_So_{solution}_Ty_{types}.pkl"))

def get_variable_textuelle():
    """Return a dictionnary with all the textual columns. This dictionnary is strings only. Is used for For loops that target the textual columns"""
    return pd.read_pickle(os.path.join(DATA_ROOT,'Clean', f"variable_textuelle.pkl"))
     
def get_format_textuel(n,t,w,a,contact,info,sujet,solution,types):
    """Return a dictionnary with all the strings of the textual columns by treshold. This dictionnary has all the strings in inntergers. The NaN values are not taken into account. Is used for graphs and basic maths to understand the distribution of textual data by tickets"""
    return pd.read_pickle(os.path.join(DATA_ROOT,'Clean', f"format_textuel_{n}_{t}_{w}_{a}_Co_{contact}_In_{info}_Su_{sujet}_So_{solution}_Ty_{types}.pkl"))

def get_df_mise_en_forme():
    """Return a dataframe cointaining all the right columns ready for data cleaning."""
    return pd.read_csv(os.path.join(DATA_ROOT, 'Clean', f'data_mise_en_forme.csv'), index_col=0, parse_dates=True)

def get_variable_dataframe_to_convert():
    """Return list of strings that enable to read in a loop the necessary dataframes"""
    return pd.read_pickle(os.path.join(DATA_ROOT,'Clean', f"variable_dataframe_to_convert.pkl"))