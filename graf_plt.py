import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import leer_datos

def histo_edad():
    df_trabajo['EDAD'].hist(bins=8, edgecolor='black') 
    plt.title('Histograma de Frecuencia de Edades')
    plt.xlabel('Edades')
    plt.ylabel('Frecuencia')
    plt.show()  

def histo_edad():
    df_agrupado = df_trabajo.groupby(["PROGRAMA"], as_index=False)[["EDAD"]].count()
    print(df_agrupado)
    programa = df_agrupado["PROGRAMA"].tolist()
    cantidad = df_agrupado["EDAD"].tolist()

    plt.bar(programa, cantidad, color = 'blue')
    plt.title("Cantidad por PROGRAMA")
    plt.xlabel("Programas")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=0)
    plt.show()

def histo_edad_adm_est():
    df_filtrado_adm = df_trabajo[df_trabajo['ROL'] == "Administrativo"]
    df_filtrado_est = df_trabajo[df_trabajo['ROL'] == "Estudiante"]
     
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    sns.histplot(
        data=df_filtrado_adm, 
        x='EDAD', 
        bins=8, 
        edgecolor='black', 
        color='#447ABB',
        kde=True,
        ax=ax[0],
        stat='density',    
        line_kws={
                'color': "#FF0000", 
                'linewidth': 2,
                'alpha': 1
                }
    ) 
    ax[0].set_title('Histograma Edades Administrativos')
    ax[0].set_xlabel('Edad')
    ax[0].set_ylabel('Densidad')
    ax[0].grid(axis='y', alpha=0.5, linestyle='--')

    sns.histplot(
        data=df_filtrado_est, 
        x='EDAD', 
        bins=8, 
        edgecolor='black', 
        color='#1800A3',
        kde=True,
        ax=ax[1],
        stat='density',
        line_kws={
                'color': "#FF0000", 
                'linewidth': 2,
                'alpha': 1
                }
    ) 
    ax[1].set_title('Histograma Edades Estudiantes')
    ax[1].set_xlabel('Edad')
    ax[1].set_ylabel('Densidad')
    ax[1].grid(axis='y', alpha=0.5, linestyle='--')
    
    plt.suptitle('Distribución de Edad por Rol', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

df = leer_datos.leer_csv()
df_trabajo = leer_datos.crear_df_trabajo(df)

# histo_edad()
# barras_programas()
histo_edad_adm_est()





