from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# =================================================================
# PREPARACIÓN DE DATOS PARA LA GRÁFICA (MODELO 2: SIN FUGA)
# =================================================================
def graficar_odds(model, feature_cols, Y_train, Y_proba, auc_score):
    # 1. Odds Ratios (OR)
    odds_ratios = np.exp(model.coef_[0])
    features = feature_cols
    df_or = pd.DataFrame({'Feature': features, 'Odds Ratio': odds_ratios})

    # 2. Curva ROC / AUC
    fpr, tpr, thresholds = roc_curve(Y_train, Y_proba)
    roc_auc = auc_score # Ya calculado previamente

    # =================================================================
    # CREACIÓN DE LA FIGURA CON DOS SUBGRÁFICOS
    # =================================================================
    plt.style.use('seaborn-v0_8-whitegrid') # Estilo visual más limpio
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

    ### SUBGRÁFICO 1: ODDS RATIO ###
    # Usamos el primer eje (axes[0]) para el gráfico de barras
    sns.barplot(
        x='Odds Ratio', 
        y='Feature', 
        data=df_or.sort_values(by='Odds Ratio', ascending=True), 
        color='#4B77BE',  # Color sobrio y único
        ax=axes[0]
    )

    # Línea vertical de referencia en OR = 1.0 (No Effect)
    axes[0].axvline(x=1.0, color='red', linestyle='--', linewidth=1.5, label='No Efecto (OR = 1)')

    # Ajustes visuales para el Odds Ratio
    axes[0].set_title('Impacto de Variables (Odds Ratio)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Odds Ratio (Escala Logarítmica)', fontsize=12)
    axes[0].set_xscale('log') 
    axes[0].set_xticks([0.1, 0.5, 1, 2, 5, 10]) 
    axes[0].set_xticklabels(['0.1', '0.5', '1', '2', '5', '10'])
    axes[0].legend()


    ### SUBGRÁFICO 2: CURVA ROC / AUC ###
    # Usamos el segundo eje (axes[1]) para la Curva ROC
    axes[1].plot(fpr, tpr, color='darkorange', lw=3, label=f'Modelo (AUC = {roc_auc:.3f})')
    axes[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Clasificador Aleatorio')

    # Ajustes visuales para la Curva ROC
    axes[1].set_title(f'Rendimiento del Modelo (Curva ROC)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Tasa de Falsos Positivos (1 - Especificidad)', fontsize=12)
    axes[1].set_ylabel('Tasa de Verdaderos Positivos (Sensibilidad)', fontsize=12)
    axes[1].set_xlim([-0.05, 1.05])
    axes[1].set_ylim([0.0, 1.05])
    axes[1].legend(loc='lower right')
    axes[1].grid(True)


    # Título general y mostrar la figura
    fig.suptitle('Análisis Conjunto: Odds Ratio y Curva ROC (Diabetes Sin Fuga)', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout() # Ajusta automáticamente los subgráficos
    plt.tight_layout(rect=[0, 0.03, 1, 1.00])
    plt.show()