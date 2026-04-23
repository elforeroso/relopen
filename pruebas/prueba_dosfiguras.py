import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 1. Preparar los datos de ejemplo
edades = np.random.randint(18, 61, 100)
df = pd.DataFrame({'Edad': edades})
x_line = np.linspace(0, 10, 50)
y_line = np.cos(x_line)

# 2. Crear la Figura y los Ejes (1 Fila, 2 Columnas)
# Esto crea una figura (el lienzo) y una matriz de ejes de 1x2 (ax[0] y ax[1])
fig, ax = plt.subplots(1, 2, figsize=(12, 5)) # figsize controla el tamaño total de la figura

# 3. Dibujar el primer gráfico en el primer eje (ax[0])
ax[0].hist(df['Edad'], bins=10, edgecolor='black', color='skyblue')
ax[0].set_title('Histograma de Edades')
ax[0].set_xlabel('Edad')
ax[0].set_ylabel('Frecuencia')

# 4. Dibujar el segundo gráfico en el segundo eje (ax[1])
ax[1].plot(x_line, y_line, color='red', linestyle='--')
ax[1].set_title('Gráfico de Líneas (Coseno)')
ax[1].set_xlabel('Eje X')
ax[1].set_ylabel('Eje Y')

# 5. Ajustar el espaciado para evitar superposiciones (opcional pero recomendado)
plt.tight_layout()

# 6. Mostrar la figura completa con ambos gráficos
plt.show()