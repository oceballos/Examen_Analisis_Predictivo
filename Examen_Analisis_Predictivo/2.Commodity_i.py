#TIN	SOUTHAFRICA	NICKEL	NEWZEALAND	LMEX	LEAD	COPPER	CHILE	CANADA	AUSTRALIA	ALUMINUM
#1994M04

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import os

# 1. Definir la ruta absoluta que indicaste
ruta_guardado = r".\2.Commodity_Graficos_i"

# Crear la carpeta si no existe
if not os.path.exists(ruta_guardado):
    os.makedirs(ruta_guardado)

# 2. Cargar y preparar los datos
df = pd.read_excel('Ejemplo Datos commodities.xlsx')
#Modificamos la variable de Fecha a una con formato más trabajable
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.replace('M', ''), format='%Y%m')
df.set_index('Date', inplace=True)

# FILTRO CRÍTICO: Exclusivamente data desde 1999-09-01 en adelante
df = df.loc['1999-09-01':]

# Seleccionar las 5 variables
vars_of_interest = ['CHILE', 'AUSTRALIA', 'COPPER', 'ALUMINUM', 'LMEX']


# 3. Función para graficar y guardar en la ruta específica
def graficar_y_guardar(serie, titulo, nombre_archivo):
    fig, axes = plt.subplots(1, 3, figsize=(18, 4))

    # Gráfico de la serie
    axes[0].plot(serie.index, serie.values, color='darkblue')
    axes[0].set_title(f'Serie: {titulo}')
    axes[0].grid(True, alpha=0.3)

    # ACF
    plot_acf(serie.dropna(), ax=axes[1], lags=30, title=f'ACF {titulo}')

    # PACF
    plot_pacf(serie.dropna(), ax=axes[2], lags=30, title=f'PACF {titulo}', method='ywm')

    plt.tight_layout()

    # Construir la ruta completa del archivo
    ruta_archivo = os.path.join(ruta_guardado, f'{nombre_archivo}.png')
    plt.savefig(ruta_archivo, dpi=300, bbox_inches='tight')
    plt.close()  # Liberar memoria


# 4. Ejecutar análisis para Niveles y Logaritmos
for var in vars_of_interest:
    # Nivel
    graficar_y_guardar(df[var], f'{var} (Niveles)', f'1_{var}_Niveles')
    # Logaritmo
    log_serie = np.log(df[var])
    graficar_y_guardar(log_serie, f'{var} (Logaritmo)', f'2_{var}_Logaritmo')

print(f"\n¡Proceso finalizado! Revisa la carpeta:\n{ruta_guardado}")