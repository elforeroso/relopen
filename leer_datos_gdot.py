import pandas as pd
import os

def renombrar_columnas(df):
    df_convertida = df.rename(
        columns={'Unnamed: 5': 'EDAD_PUNTOS',
                 'Unnamed: 14': 'IMC_PUNTOS', # Indice Masa Corporal
                 'Unnamed: 16': 'PERIABDO_PUNTOS',  # Perimetro abdominal
                 'Unnamed: 18': 'ANCADI_PUNTOS',   # Antecedentes cardiacos y diabetes
                 'Unnamed: 20': 'ENRECRO_PUNTOS', # Enfermedad Renal Cronica
                 'Unnamed: 22': 'COLESTEROL_PUNTOS', # Colesterol mayor a 310
                 'Unnamed: 24': 'PRESIARTE_PUNTOS', # Presion arterial mayor
                 'Unnamed: 26': 'TRESCONDI_PUNTOS', # Tres o mas condiciones
                 'Unnamed: 28': 'RENALSINDI_PUNTOS', # Enfermedad renal crónica sin diálisis
                 'Unnamed: 30': 'INFLAMA_PUNTOS', # Enfermedad inflamatoria crónica
                 'Unnamed: 32': 'PRECLAMP_PUNTOS', # Mujeres con: embarazo con preeclampsia
                 'Unnamed: 34': 'FAMIECV_PUNTOS', # Antecedente familiar de ECV
                 'Unnamed: 36': 'DIABE10A_PUNTOS', # Diabetes menor de 10 años
                 'Unnamed: 38': 'EJERCI_PUNTOS', # Realiza normalmente al menos 30 minutos
                 'Unnamed: 40': 'FRUTAS_PUNTOS', #Con qué frecuencia come frutas, verduras y hortalizas
                 'Unnamed: 42': 'HIPER_PUNTOS', # Le han recetado alguna vez medicamentos contra la Hipertensión arterial
                 'Unnamed: 44': 'GLUCOSA_PUNTOS', # Le han detectado alguna vez niveles altos de glucosa en sangre
                 'Unnamed: 46': 'DIABEFAMI_PUNTOS', # Ha habido algún diagnóstico de Diabetes en su familia
                 'Unnamed: 49': 'ALCOFRECU_PUNTOS', # Con qué frecuencia consume alguna bebida alcoholica y Tabaco
                 'Unnamed: 51': 'SUSTAN_PUNTOS', # Tranquilizantes o pastillas para dormir
                 'Unnamed: 53': 'FAMIPROBLE_PUNTOS', # Me satisface la ayuda que recibo de mi familia 
                 'Unnamed: 55': 'FAMIPARTI_PUNTOS', # Me satisface la participación que mi familia brinda
                 'Unnamed: 57': 'FAMIACTI_PUNTOS', # Me satisface cómo mi familia acepta y apoya mis deseos
                 'Unnamed: 59': 'FAMIAFEC_PUNTOS', # Me satisface cómo mi familia expresa afectos
                 'Unnamed: 61': 'FAMITIEMPO_PUNTOS', # Me satisface cómo compartimos en familia: El tiempo
                 'Unnamed: 63': 'DEPRIMI_PUNTOS', # Durante los ultimos 30 días se ha sentido a menudo desanimado
                 'Unnamed: 65': 'INTERES_PUNTOS', # Durante los ultimos 30 días ha sentido a menudo poco interés
                 'Unnamed: 67': 'ESTRES_PUNTOS', # Con qué frecuencia ha estado afectado por algo
                 'Unnamed: 69': 'CONTROL_PUNTOS', ### Con qué frecuencia se ha sentido incapaz de controlar
                 'Unnamed: 71': 'NERVIOSO_PUNTOS', # Con qué frecuencia se ha sentido nervioso o estresado
                 'Unnamed: 73': 'PROBLPERSO_PUNTOS', # Con qué frecuencia ha estado seguro sobre su capacidad
                 'Unnamed: 75': 'BIEN_PUNTOS', # Con qué frecuencia ha sentido que las cosas le van bien
                 'Unnamed: 77': 'AFRONTAR_PUNTOS', # Con qué frecuencia ha sentido que no podía afrontar todas las cosas
                 'Unnamed: 79': 'DIFICUVIDA_PUNTOS', # Con qué frecuencia ha podido controlar las dificultades de su vida
                 'Unnamed: 81': 'TODOCONTROL_PUNTOS', # Con qué frecuencia se ha sentido que tenía todo bajo control
                 'Unnamed: 83': 'ENFADADO_PUNTOS', # Con qué frecuencia ha estado enfadado porque las cosas
                 'Unnamed: 85': 'SUPERAR_PUNTOS', # Con qué frecuencia ha sentido que las dificultades
                }
        )

    return df_convertida

def leer_csv():
    carpeta = "D:/Documents and Settings/Documents/05-UdeC/08-Investigacion/2025-01 Envejecimiento y Tecnología/12-scripts_envejecimiento" 
    os.chdir(carpeta)

    
    archivo = "Base_Familiar_Año 2022 Gral.csv"
    df_gdot = pd.read_csv(archivo, encoding='latin1')

    return df_gdot

def crear_df_trabajo(df):
    df_trabajo = renombrar_columnas(df)

    df_trabajo = df_trabajo[[
        'Edad',
        'Unidad de medida',
        ' Sexo',
        'Tiene dx hipertension',
        '¿Con que frecuencia consume frutas y verduras',
        'Tiene dx diabetes mellitus'
        ]]
    df_trabajo = df_trabajo.rename(columns={
        'Unidad de medida': 'MEDIDA', 
        'Edad': 'EDAD',
        ' Sexo': 'SEXO',
        'Tiene dx hipertension': 'HIPERTEN',
        '¿Con que frecuencia consume frutas y verduras': 'FRUTAS',
        'Tiene dx diabetes mellitus': 'DIABETES',
        })

    
    df_trabajo['out_diabetes'] = df_trabajo.apply(calculo_diabetes, axis=1)

    # df_trabajo['ESTRATO'] = df_trabajo.apply(agrupa_estrato, axis=1)
    # df_trabajo['SEXO_MASCULI'] = df_trabajo.apply(sexo_numero, axis=1)
    # df_trabajo['ZONA_URBANA'] = df_trabajo.apply(zonaresi_numero, axis=1)

    return df_trabajo



def calculo_diabetes(df_trabajo):
    if df_trabajo['DIABETES'] == "Si":
        valor = 1
    else:
        valor = 0
    return valor


# def agrupa_estrato(df_trabajo):
#     valor = ""
#     if df_trabajo['ESTRASOCI'] == 1 or df_trabajo['ESTRASOCI'] == 2 :
#         valor = 1
#     if df_trabajo['ESTRASOCI'] == 3 or df_trabajo['ESTRASOCI'] == 4 :
#         valor = 3
#     if df_trabajo['ESTRASOCI'] == 5 or df_trabajo['ESTRASOCI'] == 6 :
#         valor = 5
#     return valor


# def sexo_numero(df_trabajo):
#     if df_trabajo['SEXO'] == 'Femenino':
#         valor = 0
#     if df_trabajo['SEXO'] == 'Masculino':
#         valor = 1
#     return valor

# def zonaresi_numero(df_trabajo):
#     if df_trabajo['ZONARESI'] == 'Urbana':
#         valor = 1
#     if df_trabajo['ZONARESI'] == 'Rural':
#         valor = 0
#     return valor



df_gdot = leer_csv()
df_trabajo_gdot = crear_df_trabajo(df_gdot)
print(df_trabajo_gdot.head(10))
# df_trabajo_sinpuntos = crear_df_trabajo_sinpuntos(df)


