import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import leer_datos

def crear_df_grafica(df_trabajo):
    df_grafica = df_trabajo[[
        # 'CEDULA',
        # 'ROL',
        # 'PROGRAMA',
        # 'EDAD',
        'EDAD_PUNTOS',
        'SEXO',
        # 'ESTRASOCI',
        # 'NIVEDU',
        # 'ZONARESI',
        'IMC_PUNTOS', # Indice Masa Corporal
        'PERIABDO_PUNTOS',  # Perimetro abdominal
        'ANCADI_PUNTOS',   # Antecedentes cardiacos y diabetes
        'ENRECRO_PUNTOS', # Enfermedad Renal Cronica
        'COLESTEROL_PUNTOS', # Colesterol mayor a 310
        # 'PRESIARTE_PUNTOS', # Presion arterial mayor
        # 'TRESCONDI_PUNTOS', # Tres o mas condiciones
        # 'RENALSINDI_PUNTOS', # Enfermedad renal crónica sin diálisis
        # 'INFLAMA_PUNTOS', # Enfermedad inflamatoria crónica
        # 'PRECLAMP_PUNTOS', # Mujeres con: embarazo con preeclampsia
        # 'FAMIECV_PUNTOS', # Antecedente familiar de ECV
        # 'DIABE10A_PUNTOS', # Diabetes menor de 10 años
        # 'EJERCI_PUNTOS', # Realiza normalmente al menos 30 minutos
        # 'FRUTAS_PUNTOS', #Con qué frecuencia come frutas, verduras y hortalizas
        # 'HIPER_PUNTOS', # recetado alguna vez medicamentos contra la Hipertensión arterial
        # 'GLUCOSA_PUNTOS', # Le han detectado alguna vez niveles altos de glucosa en sangre
        # 'DIABEFAMI_PUNTOS', # Ha habido algún diagnóstico de Diabetes en su familia
        # 'ALCOFRECU_PUNTOS', # Con qué frecuencia consume alguna bebida alcoholica y Tabaco
        # 'SUSTAN_PUNTOS', # Tranquilizantes o pastillas para dormir
        # 'FAMIPROBLE_PUNTOS', # Me satisface la ayuda que recibo de mi familia 
        # 'FAMIPARTI_PUNTOS', # Me satisface la participación que mi familia brinda
        # 'FAMIACTI_PUNTOS', # Me satisface cómo mi familia acepta y apoya mis deseos
        # 'FAMIAFEC_PUNTOS', # Me satisface cómo mi familia expresa afectos
        # 'FAMITIEMPO_PUNTOS', # Me satisface cómo compartimos en familia: El tiempo
        # 'DEPRIMI_PUNTOS', # Durante los ultimos 30 días se ha sentido a menudo desanimado
        # 'INTERES_PUNTOS', # Durante los ultimos 30 días ha sentido a menudo poco interés
        # 'ESTRES_PUNTOS', # Con qué frecuencia ha estado afectado por algo
        # 'CONTROL_PUNTOS', ### Con qué frecuencia se ha sentido incapaz de controlar
        # 'NERVIOSO_PUNTOS', # Con qué frecuencia se ha sentido nervioso o estresado
        # 'PROBLPERSO_PUNTOS', # Con qué frecuencia ha estado seguro sobre su capacidad
        # 'BIEN_PUNTOS', # Con qué frecuencia ha sentido que las cosas le van bien
        # 'AFRONTAR_PUNTOS', # Con qué frecuencia ha sentido que no podía afrontar todas las cosas
        # 'DIFICUVIDA_PUNTOS', # Con qué frecuencia ha podido controlar las dificultades de su vida
        # 'TODOCONTROL_PUNTOS', # Con qué frecuencia se ha sentido que tenía todo bajo control
        # 'ENFADADO_PUNTOS', # Con qué frecuencia ha estado enfadado porque las cosas
        # 'SUPERAR_PUNTOS' # Con qué frecuencia ha sentido que las dificultades
        ]]

    # df_trabajo.info()
    return df_grafica

df = leer_datos.leer_csv()
df_trabajo = leer_datos.crear_df_trabajo(df)
df_grafica = crear_df_grafica(df_trabajo)
print(df_grafica.head(10))
print(df_grafica.info())

grafica = sns.pairplot(
    df_grafica, 
    hue='SEXO',
    height=8.0,  # <-- Aumenta la altura de cada subgráfico
    aspect=4   # <-- Hace que cada subgráfico sea más ancho que alto
)
plt.suptitle('Grafica comparativa entre variables', y=1.02) # Título general
plt.show()