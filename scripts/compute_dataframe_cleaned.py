import argparse, os, sys
import pandas as pd, os, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fonctions.nb_df.encoding_dataset import * 
from fonctions.nb_df.build_dataset import *
from fonctions.nb_df.add_crisis import * 
from fonctions.nb_df.save_df import *
from fonctions.crisis_df.save_crisis_df import get_crisis

from fonctions.param import DATA_ROOT

parser = argparse.ArgumentParser(description='Compute clean Dataset for Algorithms.')
#n et t définissent les pas de temps
parser.add_argument('--n', help='n et t définissent les pas de temps. n correspond à la valeur numérique', required=True)
parser.add_argument('--t', help='n et t définissent les pas de temps. t correspond à la valeur de temps', required=True)

#Parameters related to the precision of the encoding of textual data
parser.add_argument('--contact', help='[contact] int. The following informations are the number of identical "contact" in ["Nb"] column. >=1 = 347 | >=2 = 175| >=10 = 51 | >=50 = 21 | >=100 = 14 | >=500 = 6', required=True, type=int)
parser.add_argument('--info', help='[info] int. The following informations are the number of identical "info" in ["Nb"] column. >=1 = 26514 | >=2 = 8837| >=10 = 629 | >500= 18 | >1000 = 14 | >5000 = 9', required=True, type=int)
parser.add_argument('--sujet', help='[sujet] int. The following informations are the number of identical "sujet" in ["Nb"] column. >=1 = 114 | >=2 = 69 | >=10 = 34 | >=100 = 20 | >=150 = 17 | >=500 = 11 | >=1000 = 9', required=True, type=int)
parser.add_argument('--solution', help='[solution] int. The following informations are the number of identical "solution" in ["Nb"] column. >=2 = 69438 | >=10 = 1796 | >=50 = 250 | >=100 = 104 | >=200 = 42 | >=450 = 14 | >=750 = 9', required=True, type=int)
parser.add_argument('--types', help='[types] int. The following informations are the number of identical "types" in ["Nb"] column. >=2 = 26 | >=10 = 20 | >=50 = 16 | >=100 = 16 | >=200 = 15 | >=450 = 11 | >=750 = 10', required=True, type=int)

#Parameters for the rolling window
parser.add_argument('--w', help='Parameters for the rolling window - int. Number of column it will roll on', required=True, type=int)
parser.add_argument('--a', help='Parameters for the rolling window - int. The penalty used on the column used', required=True, type=int)

#Parameters for get_holiday
parser.add_argument('--periode_start', help='Parameters for get_holiday - int. First year to get the holidays', required=True, type=int)
parser.add_argument('--periode_end', help='Parameters for get_holiday - int. Last year to get the holidays', required=True, type=int)

args = parser.parse_args()

if __name__ == '__main__':
    n = args.n
    t = args.t
    contact = args.contact
    info = args.info
    sujet = args.sujet
    solution= args.solution
    types = args.types
    w = args.w
    a = args.a
    periode_start = args.periode_start
    periode_end = args.periode_end
    
    #Charger les valeurs nécessaires
    xx_cleaned = get_data_cleaning_strings()
    crisis = get_crisis()
    variable_textuelle = get_variable_textuelle()
    
    #Encoding du dataset
    h, unique_values = encoding_sous_motifs(xx_cleaned,n,t)
    xx_final, unique_values, format_textuel = encoding_textual_data(xx_cleaned,h,unique_values,n,t,contact,info,sujet,solution,types)
    save_format_textuel(format_textuel,n,t,w,a,contact,info,sujet,solution,types)
    
    #Mise en forme par heures / Moyenne pondérées / Crises
    xx_final, unique_values = build_dataset(xx_final,periode_start,periode_end,w,a, unique_values,variable_textuelle)
    save_unique_values(unique_values,n,t,w,a,contact,info,sujet,solution,types)
    
    #Ajout des crises selon le resample souhaité
    xx_final = add_crisis(xx_final,crisis)
    save_df(xx_final,n,t,w,a)
    