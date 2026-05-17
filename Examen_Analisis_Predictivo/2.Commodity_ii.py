import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import os

# 1. Definir ruta y cargar datos
ruta_guardado = r".\2.Commodity_Graficos_ii"
if not os.path.exists(ruta_guardado):
    os.makedirs(ruta_guardado)

df = pd.read_excel('Ejemplo Datos commodities.xlsx')
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.replace('M', ''), format='%Y%m')
df.set_index('Date', inplace=True)

# Filtro desde 1999-09-01
df = df.loc['1999-09-01':]
vars_of_interest = ['CHILE', 'AUSTRALIA', 'COPPER', 'ALUMINUM', 'LMEX']

# 2. Calcular logaritmos
log_df = np.log(df[vars_of_interest])

# 3. Calcular retornos a 1 y 12 meses
ret_1m = log_df.diff(1).dropna()
ret_12m = log_df.diff(12).dropna()


# 4. Función para graficar y comparar
def comparar_retornos(var_name):
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle(f'Comparación de Retornos: {var_name}', fontsize=16)

    # Retorno 1 Mes (Fila 1)
    plot_acf(ret_1m[var_name], ax=axes[0, 0], lags=30, title='ACF Retorno 1 Mes')
    plot_pacf(ret_1m[var_name], ax=axes[0, 1], lags=30, title='PACF Retorno 1 Mes', method='ywm')

    # Retorno 12 Meses (Fila 2)
    plot_acf(ret_12m[var_name], ax=axes[1, 0], lags=30, title='ACF Retorno 12 Meses', color='darkred')
    plot_pacf(ret_12m[var_name], ax=axes[1, 1], lags=30, title='PACF Retorno 12 Meses', method='ywm', color='darkred')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])


    ruta_archivo = os.path.join(ruta_guardado, f'3_Comparacion_Retornos_{var_name}.png')
    plt.savefig(ruta_archivo, dpi=300, bbox_inches='tight')
    plt.close()


# 5. Ejecutar para cada variable
for var in vars_of_interest:
    comparar_retornos(var)

print(f"\n¡Gráficos comparativos guardados en:\n{ruta_guardado}")