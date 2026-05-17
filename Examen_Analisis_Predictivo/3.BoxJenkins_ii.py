import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import os

# Repita el ejercicio anterior pero utilizando la primera diferencia logaritmica
# de la serie. ¿Que sugiere esta informacion respecto a la estacionariedad de la
# serie? ¿Que tipo de decaimiento observa en el autocorrelograma?

ruta_guardado = r"..\3.BoxJenkins_Graficos_ii"
if not os.path.exists(ruta_guardado):
    os.makedirs(ruta_guardado)

# Cargar datos
df = pd.read_excel('data/GDP UK.xlsx', header=None, skiprows=2, names=['Date', 'GDP'])
df['Date'] = pd.PeriodIndex(df['Date'], freq='Q').to_timestamp()
df.set_index('Date', inplace=True)
df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')
df.dropna(inplace=True)

gdp = df['GDP']

# Primera diferencia logaritmica: dlgdp = log(GDP_t) - log(GDP_{t-1})
lgdp = np.log(gdp)
dlgdp = lgdp.diff().dropna()

# Grafico de la primera diferencia logaritmica
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(dlgdp.index, dlgdp.values, color='darkgreen', linewidth=1.5)
ax.axhline(0, color='red', linestyle='--', linewidth=0.8)
ax.set_title('Primera Diferencia Logaritmica del PIB UK (Tasa de Crecimiento Trimestral)')
ax.set_xlabel('Fecha')
ax.set_ylabel('dlog(GDP)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(ruta_guardado, 'dlgdp_uk_serie.png'), dpi=150)
plt.close()

# ACF y PACF de la primera diferencia logaritmica
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(dlgdp, lags=20, ax=axes[0], title='ACF - dlog(GDP UK)')
plot_pacf(dlgdp, lags=20, ax=axes[1], title='PACF - dlog(GDP UK)', method='ywm')
plt.tight_layout()
plt.savefig(os.path.join(ruta_guardado, 'dlgdp_uk_acf_pacf.png'), dpi=150)
plt.close()

print("Graficos guardados en:", ruta_guardado)
print("\nEstadisticas de la primera diferencia logaritmica:")
print(f"  Numero de observaciones: {len(dlgdp)}")
print(f"  Media: {dlgdp.mean():.6f} | Std: {dlgdp.std():.6f}")
print(f"  Min: {dlgdp.min():.6f} | Max: {dlgdp.max():.6f}")
print("\nConclusiones:")
print("  - La serie dlog(GDP) fluctua alrededor de una media constante positiva.")
print("  - La ACF cae rapida y abruptamente hacia cero desde el lag 1.")
print("  - Este patron es consistente con un proceso estacionario (posiblemente ruido blanco o ARMA de bajo orden).")
print("  - La primera diferencia logaritmica ELIMINA la tendencia y la serie resulta estacionaria.")
print("  - Esto confirma que la serie en niveles es integrada de orden 1: I(1).")
