import pandas as pd, os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fonctions.param import DATA_ROOT

def create_200000_lines_df(xx_cleaned):#Create files for VisualCRM in the right format (types to type) and separtor ;
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean'))
    if not os.path.exists(os.path.join(DATA_ROOT,'Clean','VisualCRM')):
        os.mkdir(os.path.join(DATA_ROOT,'Clean','VisualCRM'))
    
    variable_dataframe_to_convert = []
    xx_cleaned = xx_cleaned.reset_index().rename(columns={xx_cleaned.index.name:'jour_hhmm'})
    xx_cleaned = xx_cleaned.reset_index().rename(columns={xx_cleaned.index.name:'id'})
    maximum = len(xx_cleaned)
    for i,j in zip(range(1,maximum,200000),range(200000,maximum,200000)):
        if i == 1:
            i = 0
            xx_cleaned.loc[i:j,('bucket')]=1
            xx_cleaned[i:j].rename(columns={'types':"type"}).to_csv(os.path.join(DATA_ROOT, 'Clean', 'VisualCRM', f'VisualCRM_to_convert_{i}_{j}.csv'),sep=";",index=False)
            variable_dataframe_to_convert.append(f'VisualCRM_to_convert_{i}_{j}.csv')
        else:
            xx_cleaned.loc[i:j,('bucket')]=i
            xx_cleaned[i:j].rename(columns={'types':"type"}).to_csv(os.path.join(DATA_ROOT, 'Clean', 'VisualCRM',f'VisualCRM_to_convert_{i}_{j}.csv'),sep=";",index=False)
            variable_dataframe_to_convert.append(f'VisualCRM_to_convert_{i}_{j}.csv')
    j = j+1
    xx_cleaned.loc[i:j,('bucket')]=maximum
    xx_cleaned[j:maximum].rename(columns={'types':"type"}).to_csv(os.path.join(DATA_ROOT, 'Clean', 'VisualCRM',f'VisualCRM_to_convert_{j}_{maximum}.csv'),sep=";",index=False)
    variable_dataframe_to_convert.append(f'VisualCRM_to_convert_{j}_{maximum}.csv')
    
    return variable_dataframe_to_convert