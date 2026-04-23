import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# --- 1. Crear un DataFrame de Ejemplo ---
data = {
    'IMC': np.random.uniform(18.5, 35.0, 50),
    'Rol': np.random.choice(['Estudiante', 'Profesor', 'Administrativo'], 50),
    'Edad': np.random.randint(20, 55, 50)
}
df = pd.DataFrame(data)

# Añadir una ligera diferencia de IMC por Rol para hacerlo más interesante
df.loc[df['Rol'] == 'Profesor', 'IMC'] += 2
df.loc[df['Rol'] == 'Administrativo', 'IMC'] -= 1
df['IMC'] = df['IMC'].clip(lower=18.5) # Asegurar que no baja de un límite

# --- 2. Gráfico de Correlación Numérica (IMC vs. Edad) ---

## 📉 Diagrama de Dispersión
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Edad', y='IMC', data=df, hue='Rol', palette='viridis')
plt.title('Diagrama de Dispersión: IMC vs. Edad (Color por Rol)')
plt.xlabel('Edad (Años)')
plt.ylabel('Índice de Masa Corporal (IMC)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# Opcional: Calcular el coeficiente de correlación (solo entre variables numéricas)
correlacion_numerica = df[['IMC', 'Edad']].corr().iloc[0, 1]
print(f"\nCoeficiente de Correlación (Pearson) entre IMC y Edad: {correlacion_numerica:.2f}")
print("Una correlación cercana a 0 indica poca relación lineal.")

# --- 3. Gráfico de Asociación Numérica-Categórica (IMC vs. Rol) ---

## 📦 Gráfico de Caja (Box Plot)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Rol', y='IMC', data=df, palette='Pastel1')
plt.title('Distribución del IMC por Rol')
plt.xlabel('Rol')
plt.ylabel('Índice de Masa Corporal (IMC)')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()

# --- 4. Gráfico de Asociación Numérica-Categórica (Edad vs. Rol) ---

## 🎻 Gráfico de Violín (Muestra la densidad de la distribución)
plt.figure(figsize=(10, 6))
sns.violinplot(x='Rol', y='Edad', data=df, palette='coolwarm')
plt.title('Distribución de la Edad por Rol')
plt.xlabel('Rol')
plt.ylabel('Edad (Años)')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()