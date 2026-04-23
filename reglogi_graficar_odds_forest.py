from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import statsmodels.api as sm # Importar statsmodels

def graficar_odds_forest(df_modelo, feature_cols, target_col, Y_proba, auc_score, titulo_modelo):
    """
    Genera una figura con dos subgráficos: Forest Plot (OR con IC 95%) y Curva ROC/AUC.

    Args:
        df_modelo (pd.DataFrame): DataFrame con las variables predictoras y objetivo.
        feature_cols (list): Lista de nombres de las variables predictoras (X).
        target_col (str): Nombre de la variable objetivo (Y).
        Y_proba (np.array): Probabilidades predichas para la clase positiva (1).
        auc_score (float): El valor del AUC.
        titulo_modelo (str): Título principal para la figura.
    """
    # --- 1. Ajustar el modelo con statsmodels para obtener IC 95% ---
    X = df_modelo[feature_cols]
    # statsmodels requiere una columna de intercepto ('const') explícita
    X_sm = sm.add_constant(X, prepend=False) 
    Y = df_modelo[target_col]

    logit_model = sm.Logit(Y, X_sm)
    result = logit_model.fit(disp=False)
    
    # --- 2. Preparación de datos para el Forest Plot ---
    
    # Exponenciar coeficientes para obtener OR
    or_values = np.exp(result.params)
    
    # Exponenciar los intervalos de confianza para obtener los límites del OR
    conf = np.exp(result.conf_int())
    conf.columns = ['LCI', 'UCI'] 

    # Combinar en un DataFrame y excluir el intercepto
    df_results = pd.DataFrame({'OR': or_values, 'LCI': conf['LCI'], 'UCI': conf['UCI']})
    df_results = df_results.drop(['const'], errors='ignore')
    
    # Calcular el error (distancia desde el OR a los límites LCI/UCI)
    menor_error = df_results['OR'] - df_results['LCI']
    mayor_error = df_results['UCI'] - df_results['OR']
    errors = np.array([menor_error.values, mayor_error.values])
    y_pos = np.arange(len(df_results))
    y_labels = df_results.index.tolist()

    # --- 3. Preparación para la Curva ROC ---
    fpr, tpr, thresholds = roc_curve(Y, Y_proba)
    roc_auc = auc_score # Usamos el valor pasado

    # =================================================================
    # 4. CREACIÓN DE LA FIGURA CON DOS SUBGRÁFICOS
    # =================================================================
    # plt.style.use('seaborn-v0_8-vif') # Estilo minimalista
    plt.style.use('seaborn-v0_8-white') 
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

    ### SUBGRÁFICO A: FOREST PLOT (OR con IC 95%) ###
    # Usamos ax.errorbar para el Forest Plot
    axes[0].errorbar(
        df_results['OR'],
        y_pos,
        xerr=errors,
        fmt='o', # Marcador central
        color='#4B77BE',
        elinewidth=2, # Grosor de la línea del IC
        capsize=4, # Tamaño de las tapas de los bigotes
        ms=7 # Tamaño del punto
    )
    
    # Línea vertical de referencia en OR = 1.0 
    axes[0].axvline(x=1.0, color='#E74C3C', linestyle='--', linewidth=1.5, alpha=0.7)

    # Ajustes visuales para el Forest Plot
    axes[0].set_yticks(y_pos)
    # Revertir el orden de las etiquetas si deseas que la primera variable esté arriba
    axes[0].set_yticklabels(y_labels, fontsize=8) 
    axes[0].set_title('A. Odds Ratios (IC 95%)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Odds Ratio (OR)', fontsize=12)
    axes[0].set_xscale('log') 
    axes[0].set_xticks([0.1, 0.5, 1, 2, 5, 10]) 
    axes[0].set_xticklabels(['0.1', '0.5', '1.0', '2.0', '5.0', '10.0'])
    axes[0].grid(axis='x', linestyle=':', alpha=0.6)
    axes[0].spines['right'].set_visible(False)
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['left'].set_visible(False)
    axes[0].tick_params(axis='y', length=0) # Ocultar los ticks del eje Y

    ### SUBGRÁFICO B: CURVA ROC / AUC ###
    axes[1].plot(fpr, tpr, color='#1ABC9C', lw=3, label=f'Curva ROC (AUC = {roc_auc:.3f})')
    axes[1].plot([0, 1], [0, 1], color='#34495E', lw=2, linestyle='--', label='Clasificador Aleatorio (0.50)')

    # Ajustes visuales para la Curva ROC
    axes[1].set_title(f'B. Rendimiento Predictivo (Curva ROC)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Tasa de Falsos Positivos (1 - Especificidad)', fontsize=12)
    axes[1].set_ylabel('Tasa de Verdaderos Positivos (Sensibilidad)', fontsize=12)
    axes[1].set_xlim([0.0, 1.0])
    axes[1].set_ylim([0.0, 1.05])
    axes[1].legend(loc='lower right')
    axes[1].grid(linestyle=':', alpha=0.6)
    axes[1].spines['right'].set_visible(False)
    axes[1].spines['top'].set_visible(False)

    # Título general y mostrar la figura
    fig.suptitle(titulo_modelo, fontsize=16, fontweight='heavy', y=1.0)
    #fig.suptitle('Análisis Conjunto: Odds Ratio y Curva ROC (Diabetes Sin Fuga)', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout() # Ajusta automáticamente los subgráficos
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.show()