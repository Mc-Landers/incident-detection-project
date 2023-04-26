import copy
from jours_feries_france import JoursFeries
import pandas as pd, os, datetime

def get_holidays(df,periode_start,periode_end):
    """
    Import french metropolitan holidays under a timestamp. 
    
    periode_start=year
    periode_end=year
    df=DataFrame, need to have a df['jour_semaine'] to compare.
    
    In your code, you need to assign a column name to the return function
    EX : df['holiday'] = get_holidays(df,2021,2022)
    df['jour'] needs t obe in format datetime64 
    
    Disclaimer : The library is imported from the french government website. It actually goes up to 2027.
    """
    holidays=[]
    for i in [periode_start,periode_end]:
        s = JoursFeries.for_year(i)
        holidays.append(s)
    holidays = pd.DataFrame.from_dict(holidays, dtype='datetime64[ns]')
    
    jour_semaine = copy.deepcopy(df['jour_semaine'])
    for t in range(len(df)):
        if df.iloc[t]['jour'] in holidays.values:
            jour_semaine[t]=7 #In a normal sate time use of Pandas goes from 0 to 6 for the weekdays. Added 7 for the holidays
    return jour_semaine