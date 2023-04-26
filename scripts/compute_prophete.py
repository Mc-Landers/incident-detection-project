from prophet import Prophet
import pandas as pd, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fonctions.param import DATA_ROOT
from fonctions.nb_df.save_df import get_data
from fonctions.metrics.compute_dataframe_metrics import *
from fonctions.metrics.fonctions_metrics import *
from fonctions.metrics.save_metrics import *
from fonctions.prophete.compute_prophete import *
from fonctions.prophete.save_prophete import *

parser = argparse.ArgumentParser(description='Compute clean Dataset for Algorithm Isolation Forest.')
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
    
    #Chargement des variables
    df_total = get_data(n,t,w,a)
    
    #Compute prophete
    df_prophete, precision, recall, f1_score, f1_score_Arthur = prophete(df_total)
    save_prediction_prophete(df_prophete,n,t,w,a, contact, info, sujet, solution, types)
    tableau_metrics = compute_dataframe_metrics('prophete',precision, recall, f1_score, f1_score_Arthur)
    save_metrics(tableau_metrics,'prophete',n,t,w,a,contact, info, sujet, solution, types)