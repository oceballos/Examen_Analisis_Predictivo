import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os

# 1. Definir ruta y cargar datos
ruta_guardado = r".\2.Commodity_Graficos_iii"
if not os.path.exists(ruta_guardado):
    os.makedirs(ruta_guardado)

df = pd.read_excel('Ejemplo Datos commodities.xlsx')
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.replace('M', ''), format='%Y%m')
df.set_index('Date', inplace=True)

# Filtro desde 1999-09-01
df = df.loc['1999-09-01':]
vars_of_interest = ['CHILE', 'AUSTRALIA', 'COPPER', 'ALUMINUM', 'LMEX']

# 2. Calcular retornos logarítmicos a 1 mes
log_df = np.log(df[vars_of_interest])
ret_1m = log_df.diff(1).dropna()


# 3. Función para crear el histograma y superponer la Normal teórica
def graficar_histograma(var_name):
    data = ret_1m[var_name]

    plt.figure(figsize=(10, 6))

    # Histograma empírico
    plt.hist(data, bins=30, density=True, alpha=0.7, color='steelblue', edgecolor='black', label='Datos Empíricos')

    # Ajuste de la Normal Teórica
    mu, std = stats.norm.fit(data)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)

    plt.plot(x, p, 'k', linewidth=2, label=f'Curva Normal\n$\mu={mu:.4f}$, $\sigma={std:.4f}$')

    plt.title(f'Distribución de Retornos (1 mes): {var_name}', fontsize=14)
    plt.xlabel('Retorno Logarítmico')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Guardar gráfico
    ruta_archivo = os.path.join(ruta_guardado, f'4_Histograma_{var_name}.png')
    plt.savefig(ruta_archivo, dpi=300, bbox_inches='tight')
    plt.close()


for var in vars_of_interest:
    graficar_histograma(var)
    # Test Jarque-Bera (H0: La serie es Normal)
    jb_stat, jb_pvalue = stats.jarque_bera(ret_1m[var])
    print(
        f"{var}: p-value = {jb_pvalue:.5f} -> {'Rechaza Normalidad' if jb_pvalue < 0.05 else 'No rechaza Normalidad'}")

print(f"\n¡Histogramas guardados en:\n{ruta_guardado}")