import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import leer_datos

def crea_df():
    df = leer_datos.leer_csv()
    df_trabajo = leer_datos.crear_df_trabajo(df)

    df_estres = df_trabajo[[
        'ROL',
        'PROGRAMA',
        'EDAD',
        'EDAD_PUNTOS',
        'SEXO',
        'ESTRASOCI',
        'NIVEDU',
        'ZONARESI',
        'AFRONTAR_PUNTOS', 
        'ALCOFRECU_PUNTOS', 
        'BIEN_PUNTOS', 
        'CONTROL_PUNTOS', 
        'DIFICUVIDA_PUNTOS',
        'ENFADADO_PUNTOS', 
        'ESTRES_PUNTOS',  
        'NERVIOSO_PUNTOS', 
        'PROBLPERSO_PUNTOS',
        'SUPERAR_PUNTOS',
        'SUSTAN_PUNTOS',
        'TODOCONTROL_PUNTOS'
    ]]

    df_estres['score_neurodiab'] = (
        df_estres['AFRONTAR_PUNTOS'] + 
        df_estres['ALCOFRECU_PUNTOS'] +    
        df_estres['BIEN_PUNTOS'] + 
        df_estres['CONTROL_PUNTOS'] + 
        df_estres['DIFICUVIDA_PUNTOS'] +
        df_estres['ENFADADO_PUNTOS'] + 
        df_estres['ESTRES_PUNTOS'] + 
        df_estres['NERVIOSO_PUNTOS'] +
        df_estres['PROBLPERSO_PUNTOS'] +
        df_estres['SUPERAR_PUNTOS'] +
        df_estres['SUSTAN_PUNTOS'] +
        df_estres['TODOCONTROL_PUNTOS']
    )

    print(df_estres.head(10))
    suma = df_estres['score_neurodiab'].sum()
    print('Suma Neuropatia Diatetica ->',suma)

    # columnas_a_excluir = [col for col in df_estres.columns if 'puntos' in col or 'score' in col]
    # print(columnas_a_excluir)
    columnas_numericas = df_estres.select_dtypes(include=np.number).columns
    # print(columnas_numericas)

    columnas_excluidas = [col for col in columnas_numericas if 'puntos' in col or 'score' in col]
    columnas_a_plotear = [col for col in columnas_numericas if col not in columnas_excluidas]
    df_seleccionado = df_estres[columnas_a_plotear]
    # print(df_seleccionado)

    df_largo = pd.melt(df_seleccionado, 
                    value_vars=columnas_a_plotear,
                    var_name='variable', 
                    value_name='valor')
    graficar_mapa_calor(df_estres)

    print("Fin Crear")
    return df_largo

def graf_boxplot(df_largo):
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

def graficar_mapa_calor(df):

    columnas_analisis = [
        'AFRONTAR_PUNTOS', 'ALCOFRECU_PUNTOS', 'BIEN_PUNTOS', 
        'CONTROL_PUNTOS', 'DIFICUVIDA_PUNTOS', 'ENFADADO_PUNTOS', 
        'ESTRES_PUNTOS', 'NERVIOSO_PUNTOS', 'PROBLPERSO_PUNTOS', 
        'SUPERAR_PUNTOS', 'SUSTAN_PUNTOS', 'TODOCONTROL_PUNTOS'
    ]
    
    cols_presentes = [c for c in columnas_analisis if c in df.columns]
    corr_matrix = df[cols_presentes].corr()

    plt.figure(figsize=(8, 6))
    
    sns.heatmap(
        corr_matrix, 
        annot=True,                # Mostrar los valores numéricos
        fmt=".2f",                 # Formato con dos decimales
        cmap='RdYlGn_r',           # Escala de Rojo (Alto) a Verde (Bajo) invertida
        linewidths=0.5,            # Líneas divisorias entre celdas
        annot_kws={"size": 7},     # Tamaño de letra de los números internos
        square=True,               # Celdas cuadradas
        cbar_kws={"shrink": .7}    # Tamaño de la barra de color lateral
    )

    plt.title("Mapa de Calor: Correlaciones de Estrés y Factores de Riesgo", fontsize=8, pad=20)
    plt.xticks(fontsize=6, rotation=45, ha='right')
    plt.yticks(fontsize=6)
    
    # Ajustar diseño para que no se corten las etiquetas
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
  df_largo = crea_df()
  graf_boxplot(df_largo)