# Pregunta 1 Sección 1
import numpy as np
import statsmodels.api as sm
import pandas as pd
import os


# 0. Parámetros iniciales
np.random.seed(42)  # Fijamos semilla para replicabilidad
T = 1000
N_series = 20
a = 1
b = 0.5  # Elegimos 0.5 para cumplir con 0.4 < b < 0.7
Z_0 = 1 / (1 - b)  # Condición inicial t=0

# 1. Simulamos los shocks
shocks = np.random.standard_normal((N_series, T))

# 2. Construir los 20 procesos AR(1)
Z = np.zeros((N_series, T))
for i in range(N_series):
    current_Z = Z_0
    for t in range(T):
        current_Z = a + b * current_Z + shocks[i, t]
        Z[i, t] = current_Z

# 3. Separar en los primeros 10 (Y) y los últimos 10 (X)
Y = Z[:10, :]
X = Z[10:, :]

# 4. Ejecutar las 10 regresiones: Y_i(t) = c + k * X_i(t) + error
ols_rejects = 0
hac_rejects = 0

for i in range(10):
    y_i = Y[i, :]
    x_i = X[i, :]
    X_mat = sm.add_constant(x_i)

    # Especificar el modelo
    model = sm.OLS(y_i, X_mat)

    # Ajuste con errores estándar usuales (OLS)
    results_ols = model.fit()
    if results_ols.pvalues[1] < 0.10:  # Evaluar significancia al 10%
        ols_rejects += 1

    # Ajuste con errores estándar HAC (Newey-West)
    # maxlags se suele fijar por regla empírica, usaremos 6 como base
    results_hac = model.fit(cov_type='HAC', cov_kwds={'maxlags': 6})
    if results_hac.pvalues[1] < 0.10:
        hac_rejects += 1

print(f"Significancia con errores usuales (OLS): {ols_rejects / 10 * 100}%")
print(f"Significancia con errores HAC: {hac_rejects / 10 * 100}%")


# 5. Reordenamos los df para insertarlos en el documento
shocks_t = shocks.T
Y_t = Y.T
X_t = X.T

# 6. Crear los DataFrames de Pandas asignando nombres claros a las columnas
columnas_shocks = [f'Shock_{i+1}' for i in range(20)]
columnas_Y = [f'Y{i+1}' for i in range(10)]
columnas_X = [f'X{i+1}' for i in range(10)]

df_shocks = pd.DataFrame(shocks_t, columns=columnas_shocks)
df_Y = pd.DataFrame(Y_t, columns=columnas_Y)
df_X = pd.DataFrame(X_t, columns=columnas_X)

# 7. Guardamos el archivo
nombre_archivo = 'Examen - Shocks - Analisis Predictivos de Finanzas.xlsx'

# 8. Verificador Si el archivo existe, detenemos el proceso de guardado
if os.path.exists(nombre_archivo):
    print(f"ALERTA: El archivo '{nombre_archivo}' ya existe en este directorio.")

else:
    # 8.1 Si no existe, se crea
    columnas_shocks = [f'Shock_{i+1}' for i in range(20)]
    columnas_Y = [f'Y{i+1}' for i in range(10)]
    columnas_X = [f'X{i+1}' for i in range(10)]

    df_shocks = pd.DataFrame(shocks_t, columns=columnas_shocks)
    df_Y = pd.DataFrame(Y_t, columns=columnas_Y)
    df_X = pd.DataFrame(X_t, columns=columnas_X)

    # 8.2 Guardar
    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
        df_shocks.to_excel(writer, sheet_name='Shocks', index=False)
        df_Y.to_excel(writer, sheet_name='Series_Y', index=False)
        df_X.to_excel(writer, sheet_name='Series_X', index=False)

    print(f"Éxito: Datos exportados y guardados en '{nombre_archivo}'.")
