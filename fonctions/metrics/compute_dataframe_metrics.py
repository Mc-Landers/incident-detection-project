import pandas as pd

def compute_dataframe_metrics(algo, precision, recall, f1_score, f1_score_Arthur):
    """Create a small dataframe with the main metrics precision, recall,f1_score"""
    tableau_metrics = pd.DataFrame({"Algorithm" : f'{algo}',"Précision" : precision , "Recall" : recall , "f1_score_Arthur" : f1_score_Arthur, "f1_score" : f1_score}, index=[0]).set_index('Algorithm')
    return tableau_metrics