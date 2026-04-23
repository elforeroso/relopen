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

def calculo_regrelogis_dinafamiliar():

    global df_modelo, feature_cols, Y_proba, auc_score, model

    print("                                 Leyendo datos...")
    df = leer_datos.leer_csv()
    df_trabajo = leer_datos.crear_df_trabajo(df)
    print(df_trabajo[['score_dinafami','out_dinafami']].head(10))
    ################################################################
    #                Opcion 1: Datos con Fuga
    ################################################################


    print("                              Creado DataFrame...")
    df_modelo = df_trabajo[[
        'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
        'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
        'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
        'out_dinafami'
    ]]

    canti = len(df_modelo)
    canti0 = len(df_modelo[df_modelo['out_dinafami'] == 0])
    canti1 = len(df_modelo[df_modelo['out_dinafami'] == 1])
    print("**************************************************")
    print("         Conteo de Casos DINAMICA FAMILIAR        ")
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

    Y_train = df_modelo['out_dinafami']

    model = LogisticRegression(solver='liblinear') # 'liblinear' es bueno para datasets pequeños
    model.fit(X_train, Y_train)
    mean_values = X_train.mean()

    print("**************************************************")
    print("      Resultados DINAMICA FAMILIAR Modelo de    ")
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
    print("   Evaluación del Pronóstico DINAMICA FAMILIAR    ")
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
        'FAMIAFEC_PUNTOS',
        'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
        'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
        'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
        'out_dinafami_fuga'
    ]]

    canti = len(df_modelo)
    canti0 = len(df_modelo[df_modelo['out_dinafami_fuga'] == 0])
    canti1 = len(df_modelo[df_modelo['out_dinafami_fuga'] == 1])
    print("**************************************************")
    print("    Conteo de Casos DINAMICA FAMILIAR SIN FUGA    ")
    print("**************************************************")
    print(f"Cantidad Total.. {canti:>6}")
    print(f"Cantidad 0...... {canti0:>6}")
    print(f"Cantidad 1...... {canti1:>6}")
    print(f"Diferencia...... {canti-(canti0+canti1):>6}")

    print("                                    Calculando...")
    feature_cols = [
        'FAMIAFEC_PUNTOS',
        'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
        'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
        'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
    ]
    X_train = df_modelo[feature_cols]

    Y_train = df_modelo['out_dinafami_fuga']

    model = LogisticRegression(solver='liblinear') # 'liblinear' es bueno para datasets pequeños
    model.fit(X_train, Y_train)
    mean_values = X_train.mean()

    print("**************************************************")
    print("     Resultados DINAMICA FAMILIAR Modelo de    ")
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
    print(".................................................")

    # Obtener las probabilidades de predicción para la clase positiva (1)
    Y_proba = model.predict_proba(X_train)[:, 1]


    # .......................................................
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
    print(" Evaluación Pronóstico DINAMICA FAMILIAR SIN FUGA ")
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


# df_modelo.to_csv('out_dinafami.csv', index=False)

def grafica_regrelogis_dinafamiliar():
    reglogi_graficar_odds_forest.graficar_odds_forest(
        df_modelo=df_modelo, 
        feature_cols=feature_cols, 
        target_col='out_dinafami_fuga',
        Y_proba=Y_proba, 
        auc_score=auc_score,
        titulo_modelo="Modelo Predictivo Dinamica Familiar SIN FUGA Odds Ratio (IC 95%)"
        )

    reglogi_graficar.graficar_multiples_regrelogis(
        model=model, 
        df_modelo=df_modelo, 
        feature_list=feature_cols, 
        out_name='out_dinafami_fuga',
        feature_cols=feature_cols,
        holgura=10
    )

if __name__ == "__main__":
    calculo_regrelogis_dinafamiliar()
    grafica_regrelogis_dinafamiliar()
