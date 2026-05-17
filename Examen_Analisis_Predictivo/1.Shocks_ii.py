import numpy as np
import pandas as pd
import statsmodels.api as sm
import os

# 0. Parámetros iniciales Cambiamos la semilla
np.random.seed(123)
T = 1000
N_series = 20
a = 1
b = 0.98  # Nuevo valor: 0.95 < b < 0.99
Z_0 = 1 / (1 - b)


shocks = np.random.standard_normal((N_series, T))
Z = np.zeros((N_series, T))

for i in range(N_series):
    current_Z = Z_0
    for t in range(T):
        current_Z = a + b * current_Z + shocks[i, t]
        Z[i, t] = current_Z

Y = Z[:10, :]
X = Z[10:, :]

# 2. Ejecutar regresiones
ols_rejects = 0
hac_rejects = 0

for i in range(10):
    y_i = Y[i, :]
    x_i = X[i, :]
    X_mat = sm.add_constant(x_i)

    model = sm.OLS(y_i, X_mat)

    # OLS usual
    if model.fit().pvalues[1] < 0.10:
        ols_rejects += 1

    # HAC (Newey-West)
    if model.fit(cov_type='HAC', cov_kwds={'maxlags': 6}).pvalues[1] < 0.10:
        hac_rejects += 1

print(f"Significancia OLS (b=0.98): {ols_rejects / 10 * 100}%")
print(f"Significancia HAC (b=0.98): {hac_rejects / 10 * 100}%")

# 3. Exportar el documento
nombre_archivo = 'Examen - Shocks_ii - Analisis Predictivos de Finanzas.xlsx'

if os.path.exists(nombre_archivo):
    print(f"ALERTA: El archivo '{nombre_archivo}' ya existe. Guardado cancelado.")
else:
    df_shocks = pd.DataFrame(shocks.T, columns=[f'Shock_{i + 1}' for i in range(20)])
    df_Y = pd.DataFrame(Y.T, columns=[f'Y{i + 1}' for i in range(10)])
    df_X = pd.DataFrame(X.T, columns=[f'X{i + 1}' for i in range(10)])

    with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
        df_shocks.to_excel(writer, sheet_name='Shocks', index=False)
        df_Y.to_excel(writer, sheet_name='Series_Y', index=False)
        df_X.to_excel(writer, sheet_name='Series_X', index=False)
    print(f"Datos exportados en '{nombre_archivo}'.")