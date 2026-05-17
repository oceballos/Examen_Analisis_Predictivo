import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.stattools import durbin_watson
import os

# Estime los modelos ARIMA seleccionados en (iii). Evalue: criterios de informacion
# (AIC, BIC), significancia de los parametros, significancia global del modelo,
# estadistico Durbin-Watson y discuta si el R2 es apropiado para seleccionar modelos.
# Elija la mejor especificacion. Genere un grafico con: (i) primera diferencia del gdp,
# (ii) valores ajustados dentro de muestra, (iii) residuos. Discuta el comportamiento
# esperado de los residuos.

ruta_guardado = r".\3.BoxJenkins_Graficos_iv"
if not os.path.exists(ruta_guardado):
    os.makedirs(ruta_guardado)

# Cargar datos
df = pd.read_excel('data/GDP UK.xlsx', header=None, skiprows=2, names=['Date', 'GDP'])
df['Date'] = pd.PeriodIndex(df['Date'], freq='Q').to_timestamp()
df.set_index('Date', inplace=True)
df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')
df.dropna(inplace=True)

gdp = df['GDP']
lgdp = np.log(gdp)
dlgdp = lgdp.diff().dropna()

# 4 especificaciones ARIMA candidatas (d=1 sobre log(GDP))
especificaciones = [
    (1, 1, 0),
    (0, 1, 1),
    (1, 1, 1),
    (2, 1, 0),
]

print("=" * 70)
print("ESTIMACION DE MODELOS ARIMA - GDP UK")
print("=" * 70)

resultados = []
modelos_ajustados = {}

for orden in especificaciones:
    p, d, q = orden
    nombre = f"ARIMA({p},{d},{q})"
    try:
        modelo = ARIMA(lgdp, order=(p, d, q))
        ajuste = modelo.fit()

        # Durbin-Watson sobre residuos
        dw = durbin_watson(ajuste.resid)

        # F-test global (Ljung-Box como proxy de significancia global)
        lb_stat = sm.stats.acorr_ljungbox(ajuste.resid, lags=[10], return_df=True)
        lb_pval = lb_stat['lb_pvalue'].values[0]

        resultados.append({
            'Modelo': nombre,
            'AIC': round(ajuste.aic, 3),
            'BIC': round(ajuste.bic, 3),
            'Log-Lik': round(ajuste.llf, 3),
            'DW': round(dw, 4),
            'LB p-val (lag10)': round(lb_pval, 4),
        })

        modelos_ajustados[nombre] = ajuste

        print(f"\n{'='*50}")
        print(f"Modelo: {nombre}")
        print(f"{'='*50}")
        print(ajuste.summary().tables[1])
        print(f"  AIC : {ajuste.aic:.3f}")
        print(f"  BIC : {ajuste.bic:.3f}")
        print(f"  DW  : {dw:.4f}")
        print(f"  Ljung-Box p-val (lag 10): {lb_pval:.4f}")

    except Exception as e:
        print(f"\nError estimando {nombre}: {e}")

# Tabla resumen
print("\n" + "=" * 70)
print("TABLA RESUMEN - Criterios de Informacion y Diagnostico")
print("=" * 70)
df_res = pd.DataFrame(resultados).sort_values('AIC')
print(df_res.to_string(index=False))

# Mejor modelo por AIC
mejor_nombre = df_res.iloc[0]['Modelo']
mejor_ajuste = modelos_ajustados[mejor_nombre]
print(f"\n=> Mejor modelo por AIC: {mejor_nombre}")

# Discusion R2
print("\n" + "=" * 70)
print("DISCUSION SOBRE EL USO DE R2 EN MODELOS ARIMA:")
print("=" * 70)
print("""
  El R2 NO es un criterio apropiado para seleccionar modelos ARIMA porque:
  1. El R2 aumenta mecanicamente al agregar parametros (sobreajuste).
  2. No penaliza la complejidad del modelo (a diferencia de AIC/BIC).
  3. En modelos con diferenciacion (d>0), el R2 compara con una media trivial
     de la serie diferenciada, no con la serie original, lo que puede ser
     engañoso.
  4. Los criterios AIC y BIC son preferibles: penalizan la log-verosimilitud
     por el numero de parametros estimados (BIC penaliza mas fuertemente).
  5. Adicionalmente, se debe verificar que los residuos sean ruido blanco
     (Ljung-Box) y que el DW sea cercano a 2 (ausencia de autocorrelacion).
""")

# Grafico del mejor modelo: primera diferencia, fitted values, residuos
fitted_en_diff = mejor_ajuste.fittedvalues.diff().dropna()
resid = mejor_ajuste.resid

# Alinear indices
idx_comun = dlgdp.index.intersection(mejor_ajuste.fittedvalues.index)

fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# (i) Primera diferencia de log(GDP)
axes[0].plot(dlgdp.index, dlgdp.values, color='steelblue', linewidth=1.5, label='dlog(GDP UK)')
axes[0].axhline(0, color='gray', linestyle='--', linewidth=0.8)
axes[0].set_title(f'(i) Primera Diferencia Logaritmica del GDP UK')
axes[0].set_ylabel('dlog(GDP)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# (ii) Valores ajustados dentro de muestra (en niveles log(GDP))
axes[1].plot(lgdp.index, lgdp.values, color='steelblue', linewidth=1.5, label='log(GDP UK) Real')
axes[1].plot(mejor_ajuste.fittedvalues.index, mejor_ajuste.fittedvalues.values,
             color='darkorange', linestyle='--', linewidth=1.5, label=f'Fitted {mejor_nombre}')
axes[1].set_title(f'(ii) Valores Ajustados Dentro de Muestra - {mejor_nombre}')
axes[1].set_ylabel('log(GDP)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# (iii) Residuos
axes[2].plot(resid.index, resid.values, color='crimson', linewidth=1.2, label='Residuos')
axes[2].axhline(0, color='gray', linestyle='--', linewidth=0.8)
axes[2].set_title(f'(iii) Residuos del Modelo {mejor_nombre}')
axes[2].set_ylabel('Residuo')
axes[2].set_xlabel('Fecha')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(ruta_guardado, f'arima_mejor_modelo_{mejor_nombre}.png'), dpi=150)
plt.close()

print(f"Grafico guardado en: {ruta_guardado}")
print("\nComportamiento esperado de los residuos:")
print("  - Distribucion aproximadamente normal con media cero.")
print("  - Sin autocorrelacion significativa (ruido blanco).")
print("  - Varianza constante (homocedasticidad).")
print("  - El test de Ljung-Box NO deberia rechazar la hipotesis de no autocorrelacion.")
print("  - El DW deberia ser cercano a 2.")
