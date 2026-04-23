import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Crear el DataFrame de Ejemplo (Mismos datos anteriores) ---
np.random.seed(42)  
data = {
    'IMC': np.random.uniform(18.5, 35.0, 50),
    'Rol': np.random.choice(['Estudiante', 'Profesor', 'Administrativo'], 50),
    'Edad': np.random.randint(20, 55, 50)
}
df = pd.DataFrame(data)

# Añadir una ligera diferencia de IMC por Rol (no afecta al cálculo de la matriz general, pero da contexto)
df.loc[df['Rol'] == 'Profesor', 'IMC'] += 2
df.loc[df['Rol'] == 'Administrativo', 'IMC'] -= 1
df['IMC'] = df['IMC'].clip(lower=18.5) 

# --- 2. Calcular la Matriz de Correlación ---
# .corr() calcula la correlación (Pearson por defecto) entre todas las columnas numéricas.
correlacion_matriz = df[['IMC', 'Edad']].corr()

print("Matriz de Correlación (solo IMC y Edad):")
print(correlacion_matriz)

# --- 3. Generar el Diagrama de Calor (Heatmap) ---

plt.figure(figsize=(8, 6))
# Crear el heatmap
sns.heatmap(
    correlacion_matriz, 
    annot=True,         # Muestra el valor numérico de la correlación en cada celda
    cmap='coolwarm',    # Esquema de color: Cool-Warm (ideal para correlación, rojo es negativo, azul es positivo)
    fmt=".2f",          # Formato de los números a dos decimales
    linewidths=.5,      # Líneas para separar las celdas
    cbar=True           # Muestra la barra de color
)

plt.title('Diagrama de Calor de la Correlación entre IMC y Edad')
plt.show()