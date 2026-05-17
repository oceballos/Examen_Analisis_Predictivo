import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import os

# El archivo gdp_uk en CANVAS contiene observaciones trimestrales del
# producto interno bruto de UK para el periodo 1980-1998 (trimestral). Grafique
# la serie gdp, y luego estudie su ACF y PACF. ¿Que sugiere esta informacion
# respecto a la estacionariedad de la serie? ¿Que tipo de decaimiento observa en
# el autocorrelograma? Argumente en detalle su respuesta.

ruta_guardado = r"..\3.BoxJenkins_Graficos_i"
if not os.path.exists(ruta_guardado):
    os.makedirs(ruta_guardado)

# Cargar datos
df = pd.read_excel('data/GDP UK.xlsx', header=None, skiprows=2, names=['Date', 'GDP'])
df['Date'] = pd.PeriodIndex(df['Date'], freq='Q').to_timestamp()
df.set_index('Date', inplace=True)
df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')
df.dropna(inplace=True)

gdp = df['GDP']

# Grafico de la serie GDP UK
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(gdp.index, gdp.values, color='steelblue', linewidth=1.5)
ax.set_title('PIB Reino Unido (1980-1998) - Trimestral')
ax.set_xlabel('Fecha')
ax.set_ylabel('GDP UK')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(ruta_guardado, 'gdp_uk_serie.png'), dpi=150)
plt.close()

# ACF y PACF de la serie en niveles
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(gdp, lags=20, ax=axes[0], title='ACF - GDP UK (niveles)')
plot_pacf(gdp, lags=20, ax=axes[1], title='PACF - GDP UK (niveles)', method='ywm')
plt.tight_layout()
plt.savefig(os.path.join(ruta_guardado, 'gdp_uk_acf_pacf.png'), dpi=150)
plt.close()

print("Graficos guardados en:", ruta_guardado)
print("\nObservaciones:")
print(f"  Numero de observaciones: {len(gdp)}")
print(f"  Periodo: {gdp.index[0].date()} a {gdp.index[-1].date()}")
print(f"  Media: {gdp.mean():.2f} | Std: {gdp.std():.2f}")

