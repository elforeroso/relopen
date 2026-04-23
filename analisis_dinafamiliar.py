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
        'FAMIACTI_PUNTOS', 
        'FAMIAFEC_PUNTOS', 
        'FAMIPARTI_PUNTOS', 
        'FAMIPROBLE_PUNTOS', 
        'FAMITIEMPO_PUNTOS'
    ]]


    df_estres['score_neurodiab'] = (
        df_estres['FAMIACTI_PUNTOS'] + 
        df_estres['FAMIAFEC_PUNTOS'] +    
        df_estres['FAMIPARTI_PUNTOS'] + 
        df_estres['FAMIPROBLE_PUNTOS'] + 
        df_estres['FAMITIEMPO_PUNTOS']
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
    """
    Genera un mapa de calor compacto para las variables de entorno familiar.
    """
    # 1. Seleccionamos las columnas de la dimensión familiar y el score
    columnas_familia = [
        'FAMIACTI_PUNTOS', 'FAMIAFEC_PUNTOS', 'FAMIPARTI_PUNTOS', 
        'FAMIPROBLE_PUNTOS', 'FAMITIEMPO_PUNTOS'
    ]
    
    # 2. Calculamos la matriz de correlación
    # Filtramos por si alguna columna no existe aún en el df
    cols_existentes = [c for c in columnas_familia if c in df.columns]
    corr_matrix = df[cols_existentes].corr()

    # 3. Configuración de tamaño compacto (8x6 o 6x5 suele ser ideal para pocas variables)
    plt.figure(figsize=(7, 5))

    # 4. Creación del heatmap con recuadros pequeños y exactos
    sns.heatmap(
        corr_matrix, 
        annot=True,                # Valores numéricos visibles
        fmt=".2f",                 # 2 decimales
        cmap='YlGnBu',             # Paleta Azul-Verde-Amarillo (profesional)
        linewidths=1,              # Espacio entre cuadros para que se vean más definidos
        annot_kws={"size": 8},     # Tamaño de letra de los números
        square=True,               # Obliga a que los recuadros sean pequeños y cuadrados
        cbar_kws={"shrink": .6}    # Barra de color lateral pequeña
    )

    # 5. Ajustes de etiquetas
    plt.title("Correlación: Dimensión Dinámica Familiar", fontsize=10, pad=15)
    plt.xticks(fontsize=7, rotation=45, ha='right')
    plt.yticks(fontsize=7)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
  df_largo = crea_df()
  graf_boxplot(df_largo)