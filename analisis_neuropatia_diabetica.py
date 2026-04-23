import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt

from scipy.stats import norm
import leer_datos

def crea_df_neuropatia():
    df = leer_datos.leer_csv()
    df_trabajo = leer_datos.crear_df_trabajo(df)

    df_neuropatia_dia = df_trabajo[[
        'ROL',
        'PROGRAMA',
        'EDAD',
        'EDAD_PUNTOS',
        'SEXO',
        'ESTRASOCI',
        'NIVEDU',
        'ZONARESI',
        'IMC_PUNTOS', # Indice Masa Corporal
        'FRUTAS_PUNTOS', #Con qué frecuencia come frutas, verduras y hortalizas
        'HIPER_PUNTOS', # Le han recetado alguna vez medicamentos contra la Hipertensión arterial
        'GLUCOSA_PUNTOS', # Le han detectado alguna vez niveles altos de glucosa en sangre
        'DIABEFAMI_PUNTOS', # Ha habido algún diagnóstico de Diabetes en su familia
        'PERIABDO_PUNTOS',  # Perimetro abdominal
        'EJERCI_PUNTOS', # Realiza normalmente al menos 30 minutos
    ]]

    df_neuropatia_dia['score_neurodiab'] = (
        df_neuropatia_dia['IMC_PUNTOS'] + 
        df_neuropatia_dia['FRUTAS_PUNTOS'] +    
        df_neuropatia_dia['HIPER_PUNTOS'] + 
        df_neuropatia_dia['GLUCOSA_PUNTOS'] + 
        df_neuropatia_dia['DIABEFAMI_PUNTOS'] + 
        df_neuropatia_dia['PERIABDO_PUNTOS'] + 
        df_neuropatia_dia['EJERCI_PUNTOS']
    )

    print(df_neuropatia_dia.head(10))
    suma_neuropatia_dia = df_neuropatia_dia['score_neurodiab'].sum()
    print('Suma Neuropatia Diatetica ->',suma_neuropatia_dia)

    # columnas_a_excluir = [col for col in df_neuropatia_dia.columns if 'puntos' in col or 'score' in col]
    # print(columnas_a_excluir)
    columnas_numericas = df_neuropatia_dia.select_dtypes(include=np.number).columns
    # print(columnas_numericas)

    columnas_excluidas = [col for col in columnas_numericas if 'puntos' in col or 'score' in col]
    columnas_a_plotear = [col for col in columnas_numericas if col not in columnas_excluidas]
    df_seleccionado = df_neuropatia_dia[columnas_a_plotear]
    # print(df_seleccionado)

    df_largo = pd.melt(df_seleccionado, 
                    value_vars=columnas_a_plotear,
                    var_name='variable', 
                    value_name='valor')
    
    # digrama_distribucion(df_neuropatia_dia)
    # graficar_matriz_correlacion(df_neuropatia_dia)
    graficar_mapa_calor(df_neuropatia_dia)
    
    print("Fin Crear")
    return df_largo

def graf_boxplot_neuropatia(df_largo):
    plt.figure(figsize=(9, 5))
    sns.boxplot(
        y='variable', 
        x='valor', 
        data=df_largo, 
        color="skyblue", 
        saturation=0.6,
        showfliers=False,
        ) 
    plt.yticks(fontsize=8)
    fig = plt.gcf()
    fig.subplots_adjust(
        left=0.2, 
        right=0.98, 
        bottom=0.1, 
        top=0.9
    )

    plt.show()


def digrama_distribucion(df):
   
    # Lista de variables a graficar
    variables = [
        'IMC_PUNTOS', 'FRUTAS_PUNTOS', 'HIPER_PUNTOS', 
        'GLUCOSA_PUNTOS', 'DIABEFAMI_PUNTOS', 
        'PERIABDO_PUNTOS', 'EJERCI_PUNTOS'
    ]
    
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12, 16))
    axes = axes.flatten() # Aplanamos para iterar fácilmente

    for i, var in enumerate(variables):
        data = df[var].dropna()
        
        # 1. Graficar el histograma y la curva de densidad suavizada (KDE)
        # sns.histplot(data, kde=True, stat="density", color="skyblue", ax=axes[i], alpha=0.5)
        sns.histplot(data, kde=False, stat="density", color="skyblue", ax=axes[i], alpha=0.5)
        
        # # 2. Superponer la campana de Gauss teórica (en color rojo)
        # mu, std = norm.fit(data)
        # xmin, xmax = axes[i].get_xlim()
        # x = np.linspace(xmin, xmax, 100)
        # p = norm.pdf(x, mu, std)
        # axes[i].plot(x, p, 'r', linewidth=2, label=f'Gauss (μ={mu:.1f}, σ={std:.1f})')
        
        # Personalización
        # axes[i].set_title(f'Distribución de {var}')
        # axes[i].legend(fontsize='small')
        # axes[i].set_xlabel('Puntos')
        axes[i].set_title(f'Distribución de {var}', fontsize=7) # Título del gráfico
        # axes[i].set_xlabel('Puntos', fontsize=8)               # Etiqueta eje X
        # axes[i].set_ylabel('Density', fontsize=8)              # Etiqueta eje Y
        axes[i].tick_params(axis='both', labelsize=7)          # Números de los ejes
        axes[i].legend(fontsize=7)

    # Eliminar el último subplot si queda vacío (tenemos 7 variables y 8 espacios)
    if len(variables) < len(axes):
        fig.delaxes(axes[-1])

    plt.tight_layout()
    plt.show()

def graficar_matriz_correlacion(df):
    # 1. Seleccionamos las columnas de puntos para comparar
    columnas_puntos = [
        'IMC_PUNTOS', 'FRUTAS_PUNTOS', 'HIPER_PUNTOS', 
        'GLUCOSA_PUNTOS', 'DIABEFAMI_PUNTOS', 
        'PERIABDO_PUNTOS', 'EJERCI_PUNTOS'
    ]
    
    # Opcional: Agregar una variable categórica para dar color (ej. SEXO)
    # columns_to_plot = columnas_puntos + ['SEXO']
    
    # 2. Configurar el estilo
    sns.set_theme(style="ticks")

    # 3. Crear el pairplot
    # diag_kind='kde' crea curvas de densidad en la diagonal (como la campana de Gauss)
    g = sns.pairplot(
        df[columnas_puntos], 
        diag_kind='kde',
        plot_kws={'alpha': 0.5, 's': 30, 'color': 'skyblue'},
        diag_kws={'color': 'red'}
    )

    # 4. Ajustar el tamaño de la letra en los ejes
    for ax in g.axes.flatten():
        if ax is not None:
            ax.xaxis.label.set_size(7)
            ax.yaxis.label.set_size(7)
            ax.tick_params(labelsize=6)

    plt.suptitle("Matriz de Relaciones: Variables de Neuropatía", y=1.02, fontsize=10)
    plt.show()

def graficar_mapa_calor(df):
    # 1. Seleccionamos solo las variables de interés (puntos y score)
    columnas_analisis = [
        'IMC_PUNTOS', 'FRUTAS_PUNTOS', 'HIPER_PUNTOS', 
        'GLUCOSA_PUNTOS', 'DIABEFAMI_PUNTOS', 
        'PERIABDO_PUNTOS', 'EJERCI_PUNTOS'
    ]
    
    # 2. Calculamos la matriz de correlación de Pearson
    corr_matrix = df[columnas_analisis].corr()

    # 3. Configuramos el tamaño del gráfico
    plt.figure(figsize=(8,6))

    # 4. Creamos el mapa de calor
    sns.heatmap(
        corr_matrix, 
        annot=True,                # Muestra los números dentro de los cuadros
        fmt=".2f",                 # Dos decimales
        cmap='coolwarm',           # Color: Rojo (positivo), Azul (negativo)
        linewidths=0.5,            # Espacio entre cuadros
        annot_kws={"size": 8},     # Tamaño de letra de los números internos
        cbar_kws={"shrink": .8}    # Ajusta el tamaño de la barra de color
    )

    # 5. Ajustes de etiquetas y títulos
    plt.title("Mapa de Calor: Correlación de Variables Neuropatía", fontsize=12)
    plt.xticks(fontsize=8, rotation=45)
    plt.yticks(fontsize=8)
    
    # Ajustar para que no se corte el diseño
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
  df_largo = crea_df_neuropatia()
#   graf_boxplot_neuropatia(df_largo)
