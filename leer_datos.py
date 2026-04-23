import pandas as pd
import os
import sys
import json
from pathlib import Path
# from config import RUTA_PROYECTO

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

# def leer_csv():
#     carpeta = os.getcwd()
#     os.chdir(carpeta)

#     archivo = "Resultados.csv"
#     df = pd.read_csv(archivo, encoding='latin1')

#     return df

# # ── Configuracion Ruta ───────────────────────────────────────────────────────────────
# def obtener_ruta_config():
#     """Obtiene la ruta donde reside el ejecutable o el script"""
#     if getattr(sys, 'frozen', False):
#         # Si es un .exe creado con PyInstaller
#         base_path = Path(sys.executable).parent
#     else:
#         # Si es un script .py normal
#         base_path = Path(__file__).parent
    
#     archivo_config = base_path / "config.txt"  

#     if archivo_config.exists():
#         with open(archivo_config, "r") as f:
#             return f.read().strip() # Lee la ruta y quita espacios/saltos de línea
#     else:
#         # Ruta por defecto si el archivo no existe
#         return r"C:\Python_scripts\relopen"
def cargar_configuracion():
    
    if getattr(sys, 'frozen', False):
        # Si es un .exe
        base_path = Path(sys.executable).parent
    else:
        # Si es script .py
        base_path = Path(__file__).parent
    
    archivo_config = base_path / "config.json"
    
    # Valores por defecto por si el archivo no existe
    config_defecto = {
        "RUTA_PROYECTO": r"f:\Python_scripts\relopen",
        "NOMBRE_ARCHIVO": "Resultados.csv",
        "USUARIO": "Invitado"
    }

    if archivo_config.exists():
        try:
            with open(archivo_config, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo config.json, usando valores por defecto: {e}")
            return config_defecto
    else:
        with open(archivo_config, "w", encoding="utf-8") as f:
            json.dump(config_defecto, f, indent=4)
        return config_defecto


def leer_csv(ruta_directorio=None):

    config = cargar_configuracion()
    ruta = config.get("RUTA_PROYECTO")
    nombre_archivo = config.get("NOMBRE_ARCHIVO")
    ruta_completa = Path(ruta) / nombre_archivo

    # print("ruta_completa=", ruta_completa)

    if ruta_completa.exists():
        try:
            df = pd.read_csv(ruta_completa, encoding='latin1')
            print(f"Archivo cargado exitosamente desde: {ruta_completa}")
            return df
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return None
    else:
        print(f"Error: No se encontró el archivo en {ruta_completa}")
        return None


def crear_df_trabajo(df):
    df_trabajo = renombrar_columnas(df)

    df_trabajo = df_trabajo[[
        # 'CEDULA',
        'ROL',
        'PROGRAMA',
        'EDAD',
        'EDAD_PUNTOS',
        'SEXO',
        'ESTRASOCI',
        'NIVEDU',
        'ZONARESI',
        'IMC_PUNTOS', # Indice Masa Corporal
        'PERIABDO_PUNTOS',  # Perimetro abdominal
        'ANCADI_PUNTOS',   # Antecedentes cardiacos y diabetes
        'ENRECRO_PUNTOS', # Enfermedad Renal Cronica
        'COLESTEROL_PUNTOS', # Colesterol mayor a 310
        'PRESIARTE_PUNTOS', # Presion arterial mayor
        'TRESCONDI_PUNTOS', # Tres o mas condiciones
        'RENALSINDI_PUNTOS', # Enfermedad renal crónica sin diálisis
        'INFLAMA_PUNTOS', # Enfermedad inflamatoria crónica
        'PRECLAMP_PUNTOS', # Mujeres con: embarazo con preeclampsia
        'FAMIECV_PUNTOS', # Antecedente familiar de ECV
        'DIABE10A_PUNTOS', # Diabetes menor de 10 años
        'EJERCI_PUNTOS', # Realiza normalmente al menos 30 minutos
        'FRUTAS_PUNTOS', #Con qué frecuencia come frutas, verduras y hortalizas
        'HIPER_PUNTOS', # recetado alguna vez medicamentos contra la Hipertensión arterial
        'GLUCOSA_PUNTOS', # Le han detectado alguna vez niveles altos de glucosa en sangre
        'DIABEFAMI_PUNTOS', # Ha habido algún diagnóstico de Diabetes en su familia
        'ALCOFRECU_PUNTOS', # Con qué frecuencia consume alguna bebida alcoholica y Tabaco
        'SUSTAN_PUNTOS', # Tranquilizantes o pastillas para dormir
        'FAMIPROBLE_PUNTOS', # Me satisface la ayuda que recibo de mi familia 
        'FAMIPARTI_PUNTOS', # Me satisface la participación que mi familia brinda
        'FAMIACTI_PUNTOS', # Me satisface cómo mi familia acepta y apoya mis deseos
        'FAMIAFEC_PUNTOS', # Me satisface cómo mi familia expresa afectos
        'FAMITIEMPO_PUNTOS', # Me satisface cómo compartimos en familia: El tiempo
        'DEPRIMI_PUNTOS', # Durante los ultimos 30 días se ha sentido a menudo desanimado
        'INTERES_PUNTOS', # Durante los ultimos 30 días ha sentido a menudo poco interés
        'ESTRES_PUNTOS', # Con qué frecuencia ha estado afectado por algo
        'CONTROL_PUNTOS', ### Con qué frecuencia se ha sentido incapaz de controlar
        'NERVIOSO_PUNTOS', # Con qué frecuencia se ha sentido nervioso o estresado
        'PROBLPERSO_PUNTOS', # Con qué frecuencia ha estado seguro sobre su capacidad
        'BIEN_PUNTOS', # Con qué frecuencia ha sentido que las cosas le van bien
        'AFRONTAR_PUNTOS', # Con qué frecuencia ha sentido que no podía afrontar todas las cosas
        'DIFICUVIDA_PUNTOS', # Con qué frecuencia ha podido controlar las dificultades de su vida
        'TODOCONTROL_PUNTOS', # Con qué frecuencia se ha sentido que tenía todo bajo control
        'ENFADADO_PUNTOS', # Con qué frecuencia ha estado enfadado porque las cosas
        'SUPERAR_PUNTOS' # Con qué frecuencia ha sentido que las dificultades
        ]]
    df_trabajo['ESTRATO'] = df_trabajo.apply(agrupa_estrato, axis=1)
    df_trabajo['SEXO_MASCULI'] = df_trabajo.apply(sexo_numero, axis=1)
    df_trabajo['ZONA_URBANA'] = df_trabajo.apply(zonaresi_numero, axis=1)

    df_trabajo['score_neurodiab'] = (
        df_trabajo['IMC_PUNTOS'] + 
        df_trabajo['FRUTAS_PUNTOS'] +    
        df_trabajo['HIPER_PUNTOS'] + 
        df_trabajo['GLUCOSA_PUNTOS'] + 
        df_trabajo['DIABEFAMI_PUNTOS'] + 
        df_trabajo['PERIABDO_PUNTOS'] + 
        df_trabajo['EJERCI_PUNTOS'] +
        df_trabajo['EDAD_PUNTOS']
        )
    df_trabajo['out_diabetes'] = df_trabajo.apply(calculo_diabetes, axis=1)

    df_trabajo['score_neurodiab_fuga'] = (
        df_trabajo['FRUTAS_PUNTOS'] +    
        df_trabajo['HIPER_PUNTOS'] + 
        df_trabajo['GLUCOSA_PUNTOS'] + 
        df_trabajo['DIABEFAMI_PUNTOS'] + 
        df_trabajo['PERIABDO_PUNTOS'] + 
        df_trabajo['EJERCI_PUNTOS']
        )
    df_trabajo['out_diabetes_fuga'] = df_trabajo.apply(calculo_diabetes, axis=1)

    df_trabajo['score_estres'] = (
        df_trabajo['AFRONTAR_PUNTOS'] + 
        df_trabajo['ALCOFRECU_PUNTOS'] +    
        df_trabajo['BIEN_PUNTOS'] + 
        df_trabajo['CONTROL_PUNTOS'] + 
        df_trabajo['DIFICUVIDA_PUNTOS'] + 
        df_trabajo['ENFADADO_PUNTOS'] + 
        df_trabajo['ESTRES_PUNTOS'] +
        df_trabajo['NERVIOSO_PUNTOS'] +
        df_trabajo['PROBLPERSO_PUNTOS'] +
        df_trabajo['SUPERAR_PUNTOS'] +
        df_trabajo['SUSTAN_PUNTOS'] +
        df_trabajo['TODOCONTROL_PUNTOS']
        )
    df_trabajo['out_estres'] = df_trabajo.apply(calculo_estres, axis=1)
    df_trabajo['score_estres_fuga'] = (
        df_trabajo['AFRONTAR_PUNTOS'] + 
        df_trabajo['ALCOFRECU_PUNTOS'] +    
        df_trabajo['BIEN_PUNTOS'] + 
        df_trabajo['CONTROL_PUNTOS'] + 
        # df_trabajo['DIFICUVIDA_PUNTOS'] + 
        # df_trabajo['ENFADADO_PUNTOS'] + 
        df_trabajo['ESTRES_PUNTOS'] +
        df_trabajo['NERVIOSO_PUNTOS'] +
        df_trabajo['PROBLPERSO_PUNTOS'] +
        df_trabajo['SUPERAR_PUNTOS'] +
        df_trabajo['SUSTAN_PUNTOS'] +
        df_trabajo['TODOCONTROL_PUNTOS']
        )
    df_trabajo['out_estres_fuga'] = df_trabajo.apply(calculo_estres, axis=1)

    df_trabajo['score_dinafami'] = (
        df_trabajo['FAMIACTI_PUNTOS'] + # Me satisface la ayuda que recibo de mi familia
        df_trabajo['FAMIAFEC_PUNTOS'] + # Me satisface la participación que mi familia brinda
        df_trabajo['FAMIPARTI_PUNTOS'] + # Me satisface cómo mi familia acepta y apoya mis deseos
        df_trabajo['FAMIPROBLE_PUNTOS'] + # Me satisface cómo mi familia expresa afectos
        df_trabajo['FAMITIEMPO_PUNTOS']  # Me satisface cómo compartimos en familia: El tiempo
        )
    df_trabajo['out_dinafami'] = df_trabajo.apply(calculo_dinafami, axis=1)
    df_trabajo['score_dinafami_fuga'] = (
        df_trabajo['FAMIACTI_PUNTOS'] + # Me satisface la ayuda que recibo de mi familia
        # df_trabajo['FAMIAFEC_PUNTOS'] + # Me satisface la participación que mi familia brinda
        df_trabajo['FAMIPARTI_PUNTOS'] + # Me satisface cómo mi familia acepta y apoya mis deseos
        df_trabajo['FAMIPROBLE_PUNTOS'] + # Me satisface cómo mi familia expresa afectos
        df_trabajo['FAMITIEMPO_PUNTOS']  # Me satisface cómo compartimos en familia: El tiempo
        )
    df_trabajo['out_dinafami_fuga'] = df_trabajo.apply(calculo_dinafami, axis=1)
    return df_trabajo

def crear_df_trabajo_sinpuntos(df):
    df_trabajo = renombrar_columnas(df)

    df_trabajo_sinpuntos = df_trabajo[[
        # 'CEDULA',
        'ROL',
        'PROGRAMA',
        'EDAD',
        'EDAD_PUNTOS',
        'SEXO',
        'ESTRASOCI',
        'NIVEDU',
        'ZONARESI',
        'IMC', # Indice Masa Corporal
        'PERIABDO',  # Perimetro abdominal
        'ANCADI',   # Antecedentes cardiacos y diabetes
        'ENRECRO', # Enfermedad Renal Cronica
        'COLESTEROL', # Colesterol mayor a 310
        'PRESIARTE', # Presion arterial mayor
        'TRESCONDI', # Tres o mas condiciones
        'RENALSINDI', # Enfermedad renal crónica sin diálisis
        'INFLAMA', # Enfermedad inflamatoria crónica
        'PRECLAMP', # Mujeres con: embarazo con preeclampsia
        'FAMIECV', # Antecedente familiar de ECV
        'DIABE10A', # Diabetes menor de 10 años
        'EJERCI', # Realiza normalmente al menos 30 minutos
        'FRUTAS', #Con qué frecuencia come frutas, verduras y hortalizas
        'HIPER', # recetado alguna vez medicamentos contra la Hipertensión arterial
        'GLUCOSA', # Le han detectado alguna vez niveles altos de glucosa en sangre
        'DIABEFAMI', # Ha habido algún diagnóstico de Diabetes en su familia
        'ALCOFRECU', # Con qué frecuencia consume alguna bebida alcoholica y Tabaco
        'SUSTAN', # Tranquilizantes o pastillas para dormir
        'FAMIPROBLE', # Me satisface la ayuda que recibo de mi familia 
        'FAMIPARTI', # Me satisface la participación que mi familia brinda
        'FAMIACTI', # Me satisface cómo mi familia acepta y apoya mis deseos
        'FAMIAFEC', # Me satisface cómo mi familia expresa afectos
        'FAMITIEMPO', # Me satisface cómo compartimos en familia: El tiempo
        'DEPRIMI', # Durante los ultimos 30 días se ha sentido a menudo desanimado
        'INTERES', # Durante los ultimos 30 días ha sentido a menudo poco interés
        'ESTRES', # Con qué frecuencia ha estado afectado por algo
        'CONTROL', ### Con qué frecuencia se ha sentido incapaz de controlar
        'NERVIOSO', # Con qué frecuencia se ha sentido nervioso o estresado
        'PROBLPERSO', # Con qué frecuencia ha estado seguro sobre su capacidad
        'BIEN', # Con qué frecuencia ha sentido que las cosas le van bien
        'AFRONTAR', # Con qué frecuencia ha sentido que no podía afrontar todas las cosas
        'DIFICUVIDA', # Con qué frecuencia ha podido controlar las dificultades de su vida
        'TODOCONTROL', # Con qué frecuencia se ha sentido que tenía todo bajo control
        'ENFADADO', # Con qué frecuencia ha estado enfadado porque las cosas
        'SUPERAR' # Con qué frecuencia ha sentido que las dificultades
        ]]

    # df_trabajo.info()
    return df_trabajo_sinpuntos

def crea_df_adm_est(df_trabajo):
    df_filtrado_adm = df_trabajo[df_trabajo['ROL'] == "Administrativo"]
    df_filtrado_est = df_trabajo[df_trabajo['ROL'] == "Estudiante"]

def calculo_diabetes(df_trabajo):
    if df_trabajo['score_neurodiab'] >= 13:
        valor = 1
    else:
        valor = 0
    return valor

def agrupa_estrato(df_trabajo):
    valor = ""
    if df_trabajo['ESTRASOCI'] == 1 or df_trabajo['ESTRASOCI'] == 2 :
        valor = 1
    if df_trabajo['ESTRASOCI'] == 3 or df_trabajo['ESTRASOCI'] == 4 :
        valor = 3
    if df_trabajo['ESTRASOCI'] == 5 or df_trabajo['ESTRASOCI'] == 6 :
        valor = 5
    return valor

def sexo_numero(df_trabajo):
    if df_trabajo['SEXO'] == 'Femenino':
        valor = 0
    if df_trabajo['SEXO'] == 'Masculino':
        valor = 1
    return valor

def zonaresi_numero(df_trabajo):
    if df_trabajo['ZONARESI'] == 'Urbana':
        valor = 1
    if df_trabajo['ZONARESI'] == 'Rural':
        valor = 0
    return valor

def calculo_estres(df_trabajo):
    if df_trabajo['score_estres'] >= 14:
        valor = 1
    else:
        valor = 0
    return valor

def calculo_dinafami(df_trabajo):
    if df_trabajo['score_dinafami'] <= 12:
        valor = 1
    else:
        valor = 0
    return valor

def contar_no_numericos(df_trabajo, columna):
    
    columna_coercida = pd.to_numeric(df_trabajo[columna], errors='coerce')
    cuenta_no_numericos = columna_coercida.isna().sum()

    if df_trabajo[columna].dtype == object or df_trabajo[columna].dtype == 'string':
        no_numericos_en_string = pd.to_numeric(df_trabajo[columna], errors='coerce').isna().sum()
        return no_numericos_en_string
    else:
        return df_trabajo[columna].isna().sum()
    
    
# df = leer_csv()
# df_trabajo = crear_df_trabajo(df)
# df_trabajo_sinpuntos = crear_df_trabajo_sinpuntos(df)


