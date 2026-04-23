import numpy as np

def calculo_r2McFadden(y_true, y_proba):
    """
    Calcula el log-verosimilitud para un modelo de clasificación binaria (Regresión Logística).
    L = sum[y * ln(p) + (1-y) * ln(1-p)]
    """
    # Se añade una pequeña constante (epsilon) para evitar log(0)
    epsilon = 1e-15 
    y_proba = np.clip(y_proba, epsilon, 1 - epsilon)
    
    return np.sum(y_true * np.log(y_proba) + (1 - y_true) * np.log(1 - y_proba))