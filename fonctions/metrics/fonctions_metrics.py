def fonction_precision(df_total,algorithm,m):
    try:
        precision = (len(df_total[(df_total['Gravité']>m) & (df_total[f'{algorithm}']>m)])/len(df_total[df_total[f'{algorithm}']>m]))
        return precision
    except ZeroDivisionError:
        return 0

def fonction_recall(df_total,algorithm,m):
    try:
        recall = (len(df_total[(df_total['Gravité']>m) & (df_total[f'{algorithm}']>m)])/(len(df_total[(df_total['Gravité']>m) & (df_total[f'{algorithm}']>m)])+(len(df_total[(df_total['Gravité']>m) & (df_total[f'{algorithm}']<m)]))))
        return recall
    except ZeroDivisionError:
        return 0

def fonction_f1_score(precision,recall):
    try:
        f1_score = ((2*(precision*recall)/(precision+recall)))
        return f1_score
    except ZeroDivisionError:
        return 0

def fonction_f1_score_Arthur(precision,recall):
    try:
        f1_score_Arthur = (precision * recall / (precision + recall))
        return f1_score_Arthur
    except ZeroDivisionError:
        return 0