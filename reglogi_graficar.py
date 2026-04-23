import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_grid_dims(n):
    """Calcula las dimensiones (filas, cols) para una cuadrícula que contenga n gráficos."""
    # Intentamos mantener una forma más o menos cuadrada
    if n <= 1:
        return 1, 1
    elif n == 2:
        return 1, 2
    elif n <= 4:
        return 2, 2
    elif n <= 6:
        return 2, 3
    elif n <= 9:
        return 3, 3
    else:
        # Para más de 9, podrías necesitar una lógica más compleja o simplemente
        # aceptar que la figura será más alta o ancha. Usaremos 3 columnas como límite
        # para mantener los gráficos visibles, si es posible.
        cols = 3
        rows = int(np.ceil(n / cols))
        return rows, cols

def graficar_multiples_regrelogis(
        model, 
        df_modelo, 
        feature_list, 
        out_name, 
        feature_cols,
        holgura=0
        ):
    """
    Genera un subplot para cada característica, mostrando su efecto en la probabilidad 
    de regresión logística, manteniendo otras variables en su media.
    
    Args:
        model (LogisticRegression): El modelo ya entrenado.
        df_modelo (pd.DataFrame): DataFrame con todas las variables.
        feature_list (list): Lista de nombres de las características a graficar.
        out_name (str): Nombre de la variable de salida (binaria).
        feature_cols (list): Lista de todas las columnas usadas para entrenar el modelo.
    """
    
    # Obtener el número de gráficos y la cuadrícula
    num_features = len(feature_list)
    rows, cols = get_grid_dims(num_features)
    
    # Crear la figura y la cuadrícula de ejes
    # Aumentamos el tamaño de la figura en función del número de subplots
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    
    # Asegurarse de que 'axes' es un array plano para la iteración
    # Esto maneja casos donde rows=1 o cols=1
    if num_features == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    # Calcular los valores promedio de las características para mantenerlas constantes
    X_train = df_modelo[feature_cols]
    mean_values = X_train.mean()
    
    # ----------------------------------------------------------------------
    # Iterar y graficar cada característica
    # ----------------------------------------------------------------------
    for i, feature_name in enumerate(feature_list):
        ax = axes[i] # Seleccionar el eje actual
        
        # 1. Preparar el rango de la característica
        # Si la característica es binaria (0/1), usamos solo esos puntos, si no, usamos linspace
        if len(df_modelo[feature_name].unique()) <= 2:
            x_range = np.array([0, 1])
            num_points = 2
        else:
            x_min = df_modelo[feature_name].min()-holgura
            x_max = df_modelo[feature_name].max()+holgura
            x_range = np.linspace(x_min, x_max, 100)
            num_points = 100

        # 2. Crear el DataFrame de predicción (manteniendo otras variables en la media)
        X_pred = pd.DataFrame(np.tile(mean_values.values, (num_points, 1)), columns=feature_cols)
        X_pred[feature_name] = x_range
        
        # 3. Calcular las probabilidades
        probabilities = model.predict_proba(X_pred)[:, 1]
        
        # 4. Trazar la curva de probabilidad
        ax.plot(x_range, probabilities, color='navy', linewidth=2, 
                label=f'Probabilidad de {out_name}')
        
        # 5. Trazar los datos reales (puntos dispersos)
        # Solo mostrar los datos si la columna de la característica no es binaria,
        # o si la queremos superponer a los puntos 0 y 1.
        ax.scatter(df_modelo[feature_name], df_modelo[out_name], alpha=0.05, color='red', 
                   label=f'Datos Reales (0 o 1)')
        
        # 6. Configurar el gráfico
        ax.axhline(0.5, color='gray', linestyle='--', linewidth=1, label='Umbral de 0.5')
        ax.set_title(f'Probabilidad vs. {feature_name}', fontsize=8)
        # ax.set_xlabel(feature_name, fontsize=6)
        ax.set_xlabel(feature_name, fontsize=6)
        ax.tick_params(axis='x', labelsize=4)
        ax.set_ylabel('Probabilidad Estimada', fontsize=6)
        ax.grid(True, linestyle=':', alpha=0.5)
        # ax.legend(loc='upper right')
        ax.legend(loc='upper right', bbox_to_anchor=(1.0, 0.90), fontsize=8)

    # 7. Eliminar los ejes vacíos si el número de gráficos es menor que el número total de subplots
    for j in range(num_features, rows * cols):
        fig.delaxes(axes[j])
        
    # Ajustar el diseño para evitar la superposición de títulos y etiquetas
    plt.suptitle(f'Regresión Logística - Efecto de las Características en {out_name}', fontsize=12)
    # fig.tight_layout(rect=[0, 0, 1, 0.96]) # Deja espacio para suptitle
    fig.tight_layout(rect=[0, 0, 1, 0.96], h_pad=2.0) 
    plt.show()