def compute_rolling_mean(column, window_size = 100, alpha = 1):
    """
    Permet de créer une fenêtre roulante à moyenne pondérée
    
    Window size = int. En fonction du Timestamp utilisé permet de sélectionner le nombre de créneaux à sélectionner
    alpha = int. Coefficient a appliquer sur les valeurs
    """
    return column.rolling(window=window_size).apply(lambda x: (1-alpha)*x.mean() + alpha*x[-1])