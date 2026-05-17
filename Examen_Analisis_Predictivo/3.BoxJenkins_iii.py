import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import os

# A partir de los ejercicios (i) y (ii), determine el orden de integracion de
# la serie (I(0), I(1) o I(2)). Seleccione 4 posibles especificaciones de modelos
# ARIMA para la serie, argumentando su eleccion.

# Cargar datos
df = pd.read_excel('data/GDP UK.xlsx', header=None, skiprows=2, names=['Date', 'GDP'])
df['Date'] = pd.PeriodIndex(df['Date'], freq='Q').to_timestamp()
df.set_index('Date', inplace=True)
df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')
df.dropna(inplace=True)

gdp = df['GDP']
lgdp = np.log(gdp)
dlgdp = lgdp.diff().dropna()

def adf_test(serie, nombre, maxlag=4):
    resultado = adfuller(serie, maxlag=maxlag, autolag='AIC')
    stat, pval, lags_usados, nobs, valores_criticos, _ = resultado
    print(f"\n--- Test ADF: {nombre} ---")
    print(f"  Estadistico ADF : {stat:.4f}")
    print(f"  P-valor         : {pval:.4f}")
    print(f"  Lags utilizados : {lags_usados}")
    print(f"  Valores criticos:")
    for nivel, val in valores_criticos.items():
        print(f"    {nivel}: {val:.4f}")
    if pval < 0.05:
        print(f"  Conclusion: Se RECHAZA H0 (raiz unitaria) al 5% -> Serie ESTACIONARIA")
    else:
        print(f"  Conclusion: NO se rechaza H0 (raiz unitaria) al 5% -> Serie NO ESTACIONARIA")
    return pval

print("=" * 60)
print("DETERMINACION DEL ORDEN DE INTEGRACION - GDP UK")
print("=" * 60)

pval_niveles = adf_test(lgdp, "log(GDP UK) - Niveles")
pval_diff    = adf_test(dlgdp, "dlog(GDP UK) - Primera Diferencia")

print("\n" + "=" * 60)
print("CONCLUSION SOBRE EL ORDEN DE INTEGRACION:")
print("=" * 60)
if pval_niveles >= 0.05 and pval_diff < 0.05:
    orden = 1
    print("  log(GDP UK) NO es estacionario en niveles.")
    print("  dlog(GDP UK) SI es estacionario.")
    print("  => La serie es integrada de orden 1: I(1).")
    print("  => Se modela con d=1 en el ARIMA(p,1,q).")
elif pval_niveles < 0.05:
    orden = 0
    print("  log(GDP UK) es estacionario en niveles.")
    print("  => La serie es I(0). Se modela con ARMA(p,q) directamente.")
else:
    orden = 2
    print("  dlog(GDP UK) tampoco es estacionario -> posible I(2).")
    print("  => Se requeriria segunda diferencia.")


