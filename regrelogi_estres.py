import pandas as pd
import numpy as np
import seaborn as sns
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, confusion_matrix, accuracy_score
import leer_datos
import reglogi_graficar
import reglogi_graficar_odds_forest

df_modelo = None
feature_cols = None
Y_proba = None
auc_score = None
model = None

def calculo_regrelogis_estres():

    global df_modelo, feature_cols, Y_proba, auc_score, model

    print("                                 Leyendo datos...")
    df = leer_datos.leer_csv()
    df_trabajo = leer_datos.crear_df_trabajo(df)

    ################################################################
    #                Opcion 1: Datos con Fuga
    ################################################################


    print("                              Creado DataFrame...")
    df_modelo = df_trabajo[[
        'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
        'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
        'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
        'out_estres'
    ]]

    canti = len(df_modelo)
    canti0 = len(df_modelo[df_modelo['out_estres'] == 0])
    canti1 = len(df_modelo[df_modelo['out_estres'] == 1])
    print("**************************************************")
    print("               Conteo de Casos ESTRES             ")
    print("**************************************************")
    print(f"Cantidad Total.. {canti:>6}")
    print(f"Cantidad 0...... {canti0:>6}")
    print(f"Cantidad 1...... {canti1:>6}")
    print(f"Diferencia...... {canti-(canti0+canti1):>6}")

    print("                                    Calculando...")
    feature_cols = [
        'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
        'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
        'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
    ]
    X_train = df_modelo[feature_cols]

    Y_train = df_modelo['out_estres']

    model = LogisticRegression(solver='liblinear') # 'liblinear' es bueno para datasets pequeños
    model.fit(X_train, Y_train)
    mean_values = X_train.mean()

    print("**************************************************")
    print("           Resultados ESTRES Modelo de    ")
    print("          Regresión Logística Múltiple    ")
    print("**************************************************")
    print(f"Variables Predictoras (X):")
    for feature in feature_cols:
        print(f"  - {feature}")
        print(f"Intercepto (b): {model.intercept_[0]:>8.4f}")

    print("\nPendientes (w) para cada característica:")
    for feature, coef in zip(feature_cols, model.coef_[0]):
        print(f"  - {feature:<24}: {coef:>8.4f}")
    print("................................................")

    # Obtener las probabilidades de predicción para la clase positiva (1)
    Y_proba = model.predict_proba(X_train)[:, 1]

    # .....................................................
    # Calcular el AUC
    auc_score = roc_auc_score(Y_train, Y_proba)

    # Calcular la Predicción de Clase (0 o 1) para otras métricas
    Y_pred = model.predict(X_train)

    # Calcular Accuracy y Matriz de Confusión
    accuracy = accuracy_score(Y_train, Y_pred)
    cm = confusion_matrix(Y_train, Y_pred)
    tn, fp, fn, tp = cm.ravel()
    print("                                      Evaluando...")
    print("**************************************************")
    print("       Evaluación del Pronóstico Estres       ")
    print("**************************************************")

    print(f"1. Área Bajo la Curva (AUC): {auc_score:.4f}")
    print("   - Un valor cercano a 1.0 indica un alto grado")
    print("     de pronóstico.")

    print(f"2. Precisión (Accuracy): {accuracy:.4f}")
    print("   - Proporción de predicciones correctas")
    print("     sobre el total.")

    print("3. Matriz de Confusión:")
    print(f"   [ [TN ({tn})   FP ({fp})] ")
    print(f"   [FN ({fn})   TP ({tp})] ]")
    print("\n------------------------------------------------------")

    ################################################################
    #                Opcion 2: Datos sin Fuga
    ################################################################


    print("                              Creado DataFrame...")
    df_modelo = df_trabajo[[
        'DIFICUVIDA_PUNTOS',
        'ENFADADO_PUNTOS',
        'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
        'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
        'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
        'out_estres_fuga'
    ]]

    canti = len(df_modelo)
    canti0 = len(df_modelo[df_modelo['out_estres_fuga'] == 0])
    canti1 = len(df_modelo[df_modelo['out_estres_fuga'] == 1])
    print("**************************************************")
    print("         Conteo de Casos Estres SIN FUGA          ")
    print("**************************************************")
    print(f"Cantidad Total.. {canti:>6}")
    print(f"Cantidad 0...... {canti0:>6}")
    print(f"Cantidad 1...... {canti1:>6}")
    print(f"Diferencia...... {canti-(canti0+canti1):>6}")

    print("                                    Calculando...")
    feature_cols = [
        'DIFICUVIDA_PUNTOS',
        'ENFADADO_PUNTOS',
        'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
        'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
        'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
    ]
    X_train = df_modelo[feature_cols]

    Y_train = df_modelo['out_estres_fuga']

    model = LogisticRegression(solver='liblinear') # 'liblinear' es bueno para datasets pequeños
    model.fit(X_train, Y_train)
    mean_values = X_train.mean()

    print("**************************************************")
    print("           Resultados ESTRES Modelo de    ")
    print("      Regresión Logística Múltiple SIN FUGA       ")
    print("**************************************************")
    print(f"Variables Predictoras (X):")
    for feature in feature_cols:
        print(f"  - {feature}")
        print(f"Intercepto (b): {model.intercept_[0]:>8.4f}")

    print("\nPendientes (w) para cada característica:")
    for feature, coef in zip(feature_cols, model.coef_[0]):
        print(f"  - {feature:<24}: {coef:>8.4f}")

    print("\nOdds Ratio (OR) para cada característica:")
    for feature, coef in zip(feature_cols, model.coef_[0]):
        # El Odds Ratio es el exponencial del coeficiente (np.exp(coef))
        or_value = np.exp(coef) 
        print(f"  - {feature:<18}: {or_value:>8.4f}")
    print("..................................................")

    # Obtener las probabilidades de predicción para la clase positiva (1)
    Y_proba = model.predict_proba(X_train)[:, 1]


    # ....................................................................
    # Calcular el AUC
    auc_score = roc_auc_score(Y_train, Y_proba)

    # Calcular la Predicción de Clase (0 o 1) para otras métricas
    Y_pred = model.predict(X_train)

    # Calcular Accuracy y Matriz de Confusión
    accuracy = accuracy_score(Y_train, Y_pred)
    cm = confusion_matrix(Y_train, Y_pred)
    tn, fp, fn, tp = cm.ravel()
    print("                                      Evaluando...")
    print("**************************************************")
    print("    Evaluación del Pronóstico Estres SIN FUGA     ")
    print("**************************************************")

    print(f"1. Área Bajo la Curva (AUC): {auc_score:.4f}")
    print("   - Un valor cercano a 1.0 indica un alto grado")
    print("     de pronóstico.")

    print(f"2. Precisión (Accuracy): {accuracy:.4f}")
    print("   - Proporción de predicciones correctas")
    print("     sobre el total.")

    print("3. Matriz de Confusión:")
    print(f"   [ [TN ({tn})   FP ({fp})] ")
    print(f"   [FN ({fn})   TP ({tp})] ]")
    print("\n------------------------------------------------------")


# df_modelo.to_csv('out_estres.csv', index=False)

def grafica_regrelogis_estres():

    reglogi_graficar_odds_forest.graficar_odds_forest(
        df_modelo=df_modelo, 
        feature_cols=feature_cols, 
        target_col='out_estres_fuga',
        Y_proba=Y_proba, 
        auc_score=auc_score,
        titulo_modelo="Modelo Predictivo Estres SIN FUGA Odds Ratio (IC 95%)"
        )

    reglogi_graficar.graficar_multiples_regrelogis(
        model=model, 
        df_modelo=df_modelo, 
        feature_list=feature_cols, 
        out_name='out_estres_fuga',
        feature_cols=feature_cols,
        holgura=0
    )

if __name__ == "__main__":
    calculo_regrelogis_estres()
    grafica_regrelogis_estres()