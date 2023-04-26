def changing_visual_crm_values(variable_dataframe_to_convert,variable_textuelle):
    """Une véritable usine à gaz ...
    Return un dataframe avec les nouvelles valeures textuelles.
    variable_dataframe_to_convert = List of strings comportant les noms des df des 200 000 lignes
    variable_textuelle = List of strings comportant le noms des colonnes à variables textuelles
    """
    maximum = len(xx_cleaned)
    ultimate_df = []
    for h, h1, h2 in zip(variable_dataframe_to_convert,range(1,maximum,200000),range(200000,maximum,200000)):
        dataframe_to_convert = pd.read_csv(os.path.join(DATA_ROOT, 'Clean', 'VisualCRM', f'{h}'),sep=";")
        for i in variable_textuelle: 
            if i == 'sous_motif':
                continue
            if h1 == 1:
                h1 = 0
            dataframe_converted = pd.read_csv(os.path.join(DATA_ROOT, 'Clean', 'Retour_visual_CRM', f'df_{i}_{h1}_{h2}.csv'))
            list_col = []
            verbatimes = pd.read_csv(os.path.join(DATA_ROOT, 'Clean', 'Retour_visual_CRM', f'verbatimes_{i}.csv'),sep=";")
            #Récupérer la liste des verbatimes automatiquement
            for j in verbatimes['dataLabel']:
                if j == 'Hors thématiques':
                    list_col.append(j)
                else:
                    list_col.append(f'Thématique : {j}')

            #Pour chaque index valeur dans index trouvé sa contrepartie dans l'autre DF
            for k in range(len(dataframe_to_convert)):
                locked_row = dataframe_converted.loc[(dataframe_to_convert['index'][k] == dataframe_converted['index'])]

                #Dans les colonnes verbatimes si "x" présent alors changer la value de la colonne du data farme initial
                for l in list_col:
                    if (locked_row[f'{l}']=='x').any():
                        dataframe_to_convert.loc[(dataframe_to_convert['index'][k] == dataframe_converted['index']) , f'{i}'] = l
        ultimate_df.append(dataframe_to_convert)


    h2 = h2+1
    h = h[-1]

    dataframe_to_convert = pd.read_csv(os.path.join(DATA_ROOT, 'Clean', 'Visual_CRM', f'{h}'),sep=";")
    for i in variable_textuelle: 
        if i == 'sous_motif':
            continue
        dataframe_converted = pd.read_csv(os.path.join(DATA_ROOT, 'Clean', 'Retour_visual_CRM', f'df_{i}_{h1}_{h2}.csv'))
        list_col = []
        verbatimes = pd.read_csv(os.path.join(DATA_ROOT, 'Clean', 'Retour_visual_CRM', f'verbatimes_{i}.csv'))
        #Récupérer la liste des verbatimes automatiquement
        for j in verbatimes['dataLabel']:
            if j == 'Hors thématiques':
                list_col.append(j)
            else:
                list_col.append(f'Thématique : {j}')

        for k in range(len(dataframe_to_convert)):
                locked_row = dataframe_converted.loc[(dataframe_to_convert['index'][k] == dataframe_converted['index'])]

                #Dans les colonnes verbatimes si "x" présent alors changer la value de la colonne du data farme initial
                for l in list_col:
                    if (locked_row[f'{l}']=='x').any():
                    dataframe_to_convert.loc[(dataframe_to_convert['index'][k] == dataframe_converted['index']) , f'{i}'] = l
            
ultimate_df.append(dataframe_to_convert)
            


    return pd.DataFrame(ultimate_df,index="index")