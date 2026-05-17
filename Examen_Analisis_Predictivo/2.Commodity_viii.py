import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import t

# 1. Cargar y preparar datos
df = pd.read_excel('Ejemplo Datos commodities.xlsx')
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.replace('M', ''), format='%Y%m')
df.set_index('Date', inplace=True)
df = df.loc['1999-09-01':]
vars_all = ['CHILE', 'AUSTRALIA', 'COPPER', 'ALUMINUM', 'LMEX']
returns = np.log(df[vars_all]).diff().dropna()

commodities = ['COPPER', 'ALUMINUM', 'LMEX']
tcs = ['CHILE', 'AUSTRALIA']
# 3. Función Test de Diebold-Mariano (1 paso adelante)
def dm_test(e_benchmark, e_modelo):
    d = np.array(e_benchmark) ** 2 - np.array(e_modelo) ** 2
    mean_d = np.mean(d)
    var_d = np.var(d, ddof=1)
    if var_d == 0: return 0, 1
    stat = mean_d / np.sqrt(var_d / len(d))
    p_val = 2 * (1 - t.cdf(abs(stat), df=len(d) - 1))
    return stat, p_val
resultados_oos = []
# 4. Ejercicio Predictivo Fuera de Muestra
for c in commodities:
    y = returns[c]
    y_lag1 = y.shift(1)

    for tc in tcs:
        tc_lag1 = returns[tc].shift(1)
        tc_lag2 = returns[tc].shift(2)

        # Alinear data y definir el tamaño de la ventana (50-50)
        data = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1, 'TC_lag1': tc_lag1, 'TC_lag2': tc_lag2}).dropna()

        T = len(data)
        R = int(T * 0.5)  # Ventana de Estimación (50%)

        err_ar1, err_ph, err_hist, err_zero = [], [], [], []

        # BUCLE RECURSIVO (Expanding Window)
        for t_eval in range(R, T):
            train = data.iloc[:t_eval]  # Set de información disponible hasta T
            test = data.iloc[t_eval]  # Realidad en T+1

            actual = test['Y']

            # 1. AR(1) Benchmark
            X_ar1_train = sm.add_constant(train['Y_lag1'])
            mod_ar1 = sm.OLS(train['Y'], X_ar1_train).fit()
            pred_ar1 = mod_ar1.params['const'] + mod_ar1.params['Y_lag1'] * test['Y_lag1']

            # 2. Modelo Propuesto (PH con 2 rezagos)
            X_ph_train = sm.add_constant(train[['Y_lag1', 'TC_lag1', 'TC_lag2']])
            mod_ph = sm.OLS(train['Y'], X_ph_train).fit()
            pred_ph = mod_ph.params['const'] + mod_ph.params['Y_lag1'] * test['Y_lag1'] + \
                      mod_ph.params['TC_lag1'] * test['TC_lag1'] + mod_ph.params['TC_lag2'] * test['TC_lag2']

            # 3. Benchmark Promedio Histórico
            pred_hist = train['Y'].mean()

            # 4. Benchmark Zero Forecast
            pred_zero = 0.0

            # --- Errores de Pronóstico ---
            err_ar1.append(actual - pred_ar1)
            err_ph.append(actual - pred_ph)
            err_hist.append(actual - pred_hist)
            err_zero.append(actual - pred_zero)

        # --- Cálculo de Métricas Finales ---
        mse_ar1 = np.mean(np.array(err_ar1) ** 2)
        mse_ph = np.mean(np.array(err_ph) ** 2)
        mse_hist = np.mean(np.array(err_hist) ** 2)
        mse_zero = np.mean(np.array(err_zero) ** 2)

        # R2 OOS (Modelo PH vs Benchmark AR1)
        r2_oos_ar1 = 1 - (mse_ph / mse_ar1)

        # Test de Diebold-Mariano (Modelo PH vs Benchmark AR1)
        dm_stat, dm_pval = dm_test(err_ar1, err_ph)

        resultados_oos.append({
            'Commodity': c, 'TC': tc,
            'MSE AR(1)': round(mse_ar1, 6),
            'MSE PH': round(mse_ph, 6),
            'MSE Hist': round(mse_hist, 6),
            'MSE Zero': round(mse_zero, 6),
            'R2 OOS (%)': round(r2_oos_ar1 * 100, 3),
            'P-val DM': round(dm_pval, 4)
        })

print("--- Resultados Predicción Out-Of-Sample (50% / 50%) ---")
df_res_oos = pd.DataFrame(resultados_oos)
print(df_res_oos.to_string(index=False))