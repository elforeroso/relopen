import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, confusion_matrix, accuracy_score
import leer_datos
import error_modelo


def graficar_regrelogis(feature_name):
    # Crear un rango de valores para la característica actual
    x_range = np.linspace(df_modelo[feature_name].min()-10, df_modelo[feature_name].max()+10, 100)
    
    # Crear un DataFrame para la predicción, usando las medias para las otras features
    X_pred = pd.DataFrame(np.tile(mean_values.values, (100, 1)), columns=feature_cols)
    
    # Reemplazar la columna de la característica actual con el rango de valores
    X_pred[feature_name] = x_range
    
    # Predecir la probabilidad (Outcome=1) usando el modelo
    probabilities = model.predict_proba(X_pred)[:, 1]
    
    # Crear el gráfico
    plt.figure(figsize=(8, 5))
    plt.plot(x_range, probabilities, color='navy', linewidth=2, 
             label=f'Probabilidad de Diabetes vs. {feature_name}')
    
    # Añadir los datos reales (jitter para visibilidad)
    plt.scatter(df_modelo[feature_name], df_modelo['out_diabetes'], alpha=0.1, color='red', 
                label='Datos Reales (0 o 1)')
    
    plt.axhline(0.5, color='gray', linestyle='--', linewidth=1, label='Umbral de 0.5')
    plt.title(f'Probabilidad de Diabetes vs. {feature_name} (Otras variables en promedio)', fontsize=14)
    plt.xlabel(feature_name, fontsize=12)
    plt.ylabel('Probabilidad Estimada (P(out_diabetes=1))', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend()
    plt.show()


print("                                 Leyendo datos...")
df = leer_datos.leer_csv()
df_trabajo = leer_datos.crear_df_trabajo(df)

print("                              Creado DataFrame...")
df_modelo = df_trabajo[[
    'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
    'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
    'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
    'out_diabetes' # Posibilidad de tener Diabetes
]]

canti = len(df_modelo)
canti0 = len(df_modelo[df_modelo['out_diabetes'] == 0])
canti1 = len(df_modelo[df_modelo['out_diabetes'] == 1])
print("**************************************************")
print("                  Conteo de Casos                 ")
print("**************************************************")
print(f"Cantidad Total.. {canti:>6}")
print(f"Cantidad 0...... {canti0:>6}")
print(f"Cantidad 1...... {canti1:>6}")
print(f"Diferencia...... {canti-(canti0+canti1):>6}")

print("                                     Calculando...")
feature_cols = [
    'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
    'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
    'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
   ]

X_train = df_modelo[feature_cols]

# El output (Y_train) sigue siendo la variable binaria 'Outcome'
Y_train = df_modelo['out_diabetes']

model = LogisticRegression(solver='liblinear') # 'liblinear' es bueno para datasets pequeños
model.fit(X_train, Y_train)
mean_values = X_train.mean()

print("**************************************************")
print("             Resultados Modelo de    ")
print("          Regresión Logística Múltiple    ")
print("**************************************************")
print(f"Variables Predictoras (X):")
for feature in feature_cols:
  print(f"  - {feature}")
print(f"Intercepto (b): {model.intercept_[0]:>8.4f}")

print("\nPendientes (w) para cada característica:")
for feature, coef in zip(feature_cols, model.coef_[0]):
    print(f"  - {feature:<16}: {coef:>8.4f}")
print(".............................................................")

# Obtener las probabilidades de predicción para la clase positiva (1)
Y_proba = model.predict_proba(X_train)[:, 1]

# ....................................................................
# Calculo de verosimilitud R2 McFadden del modelo completo (LN(LM))
# ln_LM = error_modelo.calculo_r2McFadden(Y_train, Y_proba)

# Calculo del Log-Verosimilitud del modelo nulo (LN(L0))
# El modelo nulo predice la media de Y_train para todos
# prob_nula = Y_train.mean() 
# Y_proba_nula = np.full_like(Y_proba, prob_nula)
# ln_L0 = error_modelo.calculo_r2McFadden(Y_train, Y_proba_nula)

# Calculo R2 McFadden
# Pseudo R^2 = 1 - (ln(LM) / ln(L0))
# Usamos -ln(L0) en el denominador para garantizar que sea positivo
# mcfadden_r2 = 1 - (ln_LM / ln_L0)

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
print("             Evaluación del Pronóstico            ")
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

# # df_modelo.to_csv('out_diabetes.csv', index=False)

# for feature in feature_cols:
#   graficar_regrelogis(feature)
