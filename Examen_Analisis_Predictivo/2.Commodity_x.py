import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import binomtest

df = pd.read_excel('data/Ejemplo Datos commodities.xlsx')
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.replace('M', ''), format='%Y%m')
df.set_index('Date', inplace=True)
df = df.loc['1999-09-01':]

vars_all = ['CHILE', 'AUSTRALIA', 'COPPER', 'ALUMINUM', 'LMEX']
returns = np.log(df[vars_all]).diff().dropna()

commodities = ['COPPER', 'ALUMINUM', 'LMEX']
tcs = ['CHILE', 'AUSTRALIA']

resultados_mda = []

for c in commodities:
    y = returns[c]
    y_lag1 = y.shift(1)

    for tc in tcs:
        tc_lag1 = returns[tc].shift(1)
        tc_lag2 = returns[tc].shift(2)

        data = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1, 'TC_lag1': tc_lag1, 'TC_lag2': tc_lag2}).dropna()
        # Volvemos al 50%
        T = len(data)
        R = int(T * 0.5)

        dir_ar1, dir_ph, dir_hist = [], [], []

        for t_eval in range(R, T):
            train = data.iloc[:t_eval]
            test = data.iloc[t_eval]
            actual = test['Y']

            # Predicciones
            X_ar1_train = sm.add_constant(train['Y_lag1'])
            mod_ar1 = sm.OLS(train['Y'], X_ar1_train).fit()
            pred_ar1 = mod_ar1.params['const'] + mod_ar1.params['Y_lag1'] * test['Y_lag1']

            X_ph_train = sm.add_constant(train[['Y_lag1', 'TC_lag1', 'TC_lag2']])
            mod_ph = sm.OLS(train['Y'], X_ph_train).fit()
            pred_ph = mod_ph.params['const'] + mod_ph.params['Y_lag1'] * test['Y_lag1'] + \
                      mod_ph.params['TC_lag1'] * test['TC_lag1'] + mod_ph.params['TC_lag2'] * test['TC_lag2']

            pred_hist = train['Y'].mean()

            # Guardar 1 si el signo coincide (producto > 0), 0 si falla
            dir_ar1.append(1 if (actual * pred_ar1) > 0 else 0)
            dir_ph.append(1 if (actual * pred_ph) > 0 else 0)
            dir_hist.append(1 if (actual * pred_hist) > 0 else 0)

        # Calcular MDA (Porcentaje de aciertos direccionales)
        P = len(dir_ar1)
        mda_ar1 = np.mean(dir_ar1)
        mda_ph = np.mean(dir_ph)
        mda_hist = np.mean(dir_hist)

        # Test Binomial (H0: P = 0.5 vs H1: P > 0.5)
        pval_ar1 = binomtest(sum(dir_ar1), P, p=0.5, alternative='greater').pvalue
        pval_ph = binomtest(sum(dir_ph), P, p=0.5, alternative='greater').pvalue
        pval_hist = binomtest(sum(dir_hist), P, p=0.5, alternative='greater').pvalue

        resultados_mda.append({
            'Commodity': c, 'TC': tc,
            'MDA AR1 (%)': round(mda_ar1 * 100, 2), 'P-val AR1': round(pval_ar1, 4),
            'MDA PH (%)': round(mda_ph * 100, 2), 'P-val PH': round(pval_ph, 4),
            'MDA Hist (%)': round(mda_hist * 100, 2), 'P-val Hist': round(pval_hist, 4)
        })

print("--- Evaluación de Precisión Direccional (MDA) ---")
print(pd.DataFrame(resultados_mda).to_string(index=False))