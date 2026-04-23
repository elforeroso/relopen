import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import leer_datos

df = leer_datos.leer_csv()
df_trabajo = leer_datos.crear_df_trabajo(df)
# print(df_trabajo.info())

# correlacion = df_trabajo[[
#     'EDAD_PUNTOS', 
#     'IMC_PUNTOS', #IMC
#     'PERIABDO_PUNTOS', # Perimetro Abdominal
#     'ANCADI_PUNTOS',   # Antecedentes cardiacos y diabetes
#     'ENRECRO_PUNTOS', # Enfermedad Renal Cronica
#     'COLESTEROL_PUNTOS', # Colesterol mayor a 310
#     'DIABETES_PUNTOS', # Sumatoria puntos
#     ]].corr()
# print(correlacion)
# plt.figure(figsize=(8, 6))

# ax = sns.heatmap(
#     correlacion, 
#     annot=True,
#     cmap='RdBu',
#     fmt=".0%",
#     linewidths=.5,
#     cbar=True,
#     annot_kws={"fontsize": 8}
# )
# ax.tick_params(
#     axis='x',
#     labelsize=5,
#     labelrotation=0
# )
# ax.tick_params(
#     axis='y',
#     labelsize=9,
#     labelrotation=0
# )
# plt.subplots_adjust(left=0.25, right=0.95, top=0.9, bottom=0.1)

# plt.title('Diagrama de Correlación para Diabetes')
# plt.show()

# correlacion = df_trabajo[[
#     'IMC_PUNTOS', #IMC
#     'FRUTAS_PUNTOS', # Perimetro Abdominal
#     'HIPER_PUNTOS',   # Antecedentes cardiacos y diabetes
#     'GLUCOSA_PUNTOS', # Enfermedad Renal Cronica
#     'DIABEFAMI_PUNTOS', # Colesterol mayor a 310
#     'PERIABDO_PUNTOS', # Sumatoria puntos
#     'EJERCI_PUNTOS', # Ejercicio

#     ]].corr()
# print(correlacion)
# plt.figure(figsize=(8, 6))

# ax = sns.heatmap(
#     correlacion, 
#     annot=True,
#     cmap='RdBu',
#     fmt=".0%",
#     linewidths=.5,
#     cbar=True,
#     annot_kws={"fontsize": 8}
# )
# ax.tick_params(
#     axis='x',
#     labelsize=5,
#     labelrotation=45
# )
# ax.tick_params(
#     axis='y',
#     labelsize=9,
#     labelrotation=0
# )
# plt.subplots_adjust(left=0.25, right=0.95, top=0.9, bottom=0.1)

# plt.title('Diagrama de Correlación para Diabetes')
# plt.show()

# df_filtrado_adm = df_trabajo[df_trabajo['ROL'] == "Administrativo"]
# correlacion = df_filtrado_adm[[
#     'EDAD_PUNTOS', 
#     'IMC_PUNTOS', #IMC
#     'PERIABDO_PUNTOS', # Perimetro Abdominal
#     'ANCADI_PUNTOS',   # Antecedentes cardiacos y diabetes
#     'ENRECRO_PUNTOS', # Enfermedad Renal Cronica
#     'COLESTEROL_PUNTOS', # Colesterol mayor a 310
#     'DIABETES_PUNTOS', # Sumatoria puntos
#     ]].corr()
# print(correlacion)
# plt.figure(figsize=(8, 6))

# ax = sns.heatmap(
#     correlacion, 
#     annot=True,
#     cmap='RdBu',
#     fmt=".0%",
#     linewidths=.5,
#     cbar=True,
#     annot_kws={"fontsize": 8}
# )
# ax.tick_params(
#     axis='x',
#     labelsize=5,
#     labelrotation=0
# )
# ax.tick_params(
#     axis='y',
#     labelsize=9,
#     labelrotation=0
# )
# plt.subplots_adjust(left=0.25, right=0.95, top=0.9, bottom=0.1)
# plt.title('Diagrama de Correlación para Diabetes Administrativos')
# plt.show()

# df_filtrado_est = df_trabajo[df_trabajo['ROL'] == "Estudiante"]
# correlacion = df_filtrado_est[[
#     'EDAD_PUNTOS', 
#     'IMC_PUNTOS', #IMC
#     'PERIABDO_PUNTOS', # Perimetro Abdominal
#     'ANCADI_PUNTOS',   # Antecedentes cardiacos y diabetes
#     'ENRECRO_PUNTOS', # Enfermedad Renal Cronica
#     'COLESTEROL_PUNTOS', # Colesterol mayor a 310
#     'DIABETES_PUNTOS', # Sumatoria puntos
#     ]].corr()
# print(correlacion)
# plt.figure(figsize=(8, 6))

# ax = sns.heatmap(
#     correlacion, 
#     annot=True,
#     cmap='RdBu',
#     fmt=".0%",
#     linewidths=.5,
#     cbar=True,
#     annot_kws={"fontsize": 8}
# )
# ax.tick_params(
#     axis='x',
#     labelsize=5,
#     labelrotation=0
# )
# ax.tick_params(
#     axis='y',
#     labelsize=9,
#     labelrotation=0
# )
# plt.subplots_adjust(left=0.25, right=0.95, top=0.9, bottom=0.1)
# plt.title('Diagrama de Correlación para Diabetes Estudiantes')
# plt.show()



correlacion = df_trabajo[[
    'SEXO_MASCULI', # Sexo 1=MASCULINO 0=FEMENINO
    'ESTRATO', # Estrato 1=BAJO, 3=MEDIO ALTO, 5=ALTO
    'ZONA_URBANA', # Zona Residencial 1=URBANA 0=RURAL
    'out_diabetes' # Posibilidad de tener Diabetes
    ]].corr()
print(correlacion)
plt.figure(figsize=(8, 6))

ax = sns.heatmap(
    correlacion, 
    annot=True,
    cmap='RdBu',
    fmt=".0%",
    linewidths=.5,
    cbar=True,
    annot_kws={"fontsize": 8}
)
ax.tick_params(
    axis='x',
    labelsize=5,
    labelrotation=45
)
ax.tick_params(
    axis='y',
    labelsize=9,
    labelrotation=0
)
plt.subplots_adjust(left=0.25, right=0.95, top=0.9, bottom=0.1)

plt.title('Diagrama de Correlación para Diabetes')
plt.show()