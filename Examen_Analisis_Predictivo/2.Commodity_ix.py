import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import t

df = pd.read_excel('data/Ejemplo Datos commodities.xlsx')
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.replace('M', ''), format='%Y%m')
df.set_index('Date', inplace=True)
df = df.loc['1999-09-01':]

vars_all = ['CHILE', 'AUSTRALIA', 'COPPER', 'ALUMINUM', 'LMEX']
returns = np.log(df[vars_all]).diff().dropna()

commodities = ['COPPER', 'ALUMINUM', 'LMEX']
tcs = ['CHILE', 'AUSTRALIA']


# Función de Diebold-Mariano
def dm_test(e_benchmark, e_modelo):
    d = np.array(e_benchmark) ** 2 - np.array(e_modelo) ** 2
    mean_d = np.mean(d)
    var_d = np.var(d, ddof=1)
    if var_d == 0: return 0, 1
    stat = mean_d / np.sqrt(var_d / len(d))
    p_val = 2 * (1 - t.cdf(abs(stat), df=len(d) - 1))
    return stat, p_val


resultados_oos_30 = []

for c in commodities:
    y = returns[c]
    y_lag1 = y.shift(1)

    for tc in tcs:
        tc_lag1 = returns[tc].shift(1)
        tc_lag2 = returns[tc].shift(2)

        data = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1, 'TC_lag1': tc_lag1, 'TC_lag2': tc_lag2}).dropna()

        T = len(data)

        # 30% Estimación, 70% Evaluación
        R = int(T * 0.3)

        err_ar1, err_ph, err_hist, err_zero = [], [], [], []

        for t_eval in range(R, T):
            train = data.iloc[:t_eval]
            test = data.iloc[t_eval]
            actual = test['Y']

            # AR(1)
            X_ar1_train = sm.add_constant(train['Y_lag1'])
            mod_ar1 = sm.OLS(train['Y'], X_ar1_train).fit()
            pred_ar1 = mod_ar1.params['const'] + mod_ar1.params['Y_lag1'] * test['Y_lag1']

            # PH
            X_ph_train = sm.add_constant(train[['Y_lag1', 'TC_lag1', 'TC_lag2']])
            mod_ph = sm.OLS(train['Y'], X_ph_train).fit()
            pred_ph = mod_ph.params['const'] + mod_ph.params['Y_lag1'] * test['Y_lag1'] + \
                      mod_ph.params['TC_lag1'] * test['TC_lag1'] + mod_ph.params['TC_lag2'] * test['TC_lag2']

            err_ar1.append(actual - pred_ar1)
            err_ph.append(actual - pred_ph)
            err_hist.append(actual - train['Y'].mean())
            err_zero.append(actual - 0.0)

        mse_ar1 = np.mean(np.array(err_ar1) ** 2)
        mse_ph = np.mean(np.array(err_ph) ** 2)

        r2_oos_ar1 = 1 - (mse_ph / mse_ar1)
        dm_stat, dm_pval = dm_test(err_ar1, err_ph)

        resultados_oos_30.append({
            'Commodity': c, 'TC': tc,
            'MSE AR(1)': round(mse_ar1, 5),
            'MSE PH': round(mse_ph, 5),
            'MSE Hist': round(np.mean(np.array(err_hist) ** 2), 5),
            'MSE Zero': round(np.mean(np.array(err_zero) ** 2), 5),
            'R2 OOS (%)': round(r2_oos_ar1 * 100, 3),
            'P-val DM': round(dm_pval, 4)
        })

print("--- Resultados Predicción Out-Of-Sample (30% / 70%) ---")
print(pd.DataFrame(resultados_oos_30).to_string(index=False))