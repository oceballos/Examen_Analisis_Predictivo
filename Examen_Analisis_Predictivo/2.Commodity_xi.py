import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_excel('data/Ejemplo Datos commodities.xlsx')
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.replace('M', ''), format='%Y%m')
df.set_index('Date', inplace=True)
df = df.loc['1999-09-01':]

vars_all = ['CHILE', 'AUSTRALIA', 'COPPER', 'ALUMINUM', 'LMEX']
returns = np.log(df[vars_all]).diff().dropna()

commodities = ['COPPER', 'ALUMINUM', 'LMEX']
tcs = ['CHILE', 'AUSTRALIA']


# 2. Función para el Test de Pincheira, Hardy y Bentancor (2022)
def phb_test(strat_returns):
    strat_returns = np.array(strat_returns)
    X = np.ones(len(strat_returns))

    # Regresión contra una constante usando errores HAC (Newey-West, maxlags=12)
    mod = sm.OLS(strat_returns, X).fit(cov_type='HAC', cov_kwds={'maxlags': 12})

    coef = mod.params[0]
    t_stat = mod.tvalues[0]

    # Test Unilateral: H0: Rentabilidad <= 0 vs H1: Rentabilidad > 0
    p_val = mod.pvalues[0] / 2 if t_stat > 0 else 1 - (mod.pvalues[0] / 2)
    return coef, p_val


resultados_trading = []

# 3. Simulación 50-50 y Estrategia AG (2005)
for c in commodities:
    y = returns[c]
    y_lag1 = y.shift(1)

    for tc in tcs:
        tc_lag1 = returns[tc].shift(1)
        tc_lag2 = returns[tc].shift(2)

        data = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1, 'TC_lag1': tc_lag1, 'TC_lag2': tc_lag2}).dropna()

        T = len(data)
        R = int(T * 0.5)

        strat_ar1, strat_ph, strat_hist = [], [], []

        for t_eval in range(R, T):
            train = data.iloc[:t_eval]
            test = data.iloc[t_eval]
            actual = test['Y']

            # Predicciones de los modelos
            X_ar1_train = sm.add_constant(train['Y_lag1'])
            mod_ar1 = sm.OLS(train['Y'], X_ar1_train).fit()
            pred_ar1 = mod_ar1.params['const'] + mod_ar1.params['Y_lag1'] * test['Y_lag1']

            X_ph_train = sm.add_constant(train[['Y_lag1', 'TC_lag1', 'TC_lag2']])
            mod_ph = sm.OLS(train['Y'], X_ph_train).fit()
            pred_ph = mod_ph.params['const'] + mod_ph.params['Y_lag1'] * test['Y_lag1'] + \
                      mod_ph.params['TC_lag1'] * test['TC_lag1'] + mod_ph.params['TC_lag2'] * test['TC_lag2']

            pred_hist = train['Y'].mean()

            # Estrategia Anatolyev & Gerko
            strat_ar1.append(np.sign(pred_ar1) * actual)
            strat_ph.append(np.sign(pred_ph) * actual)
            strat_hist.append(np.sign(pred_hist) * actual)

        # Evaluar significancia estadística de la rentabilidad (Test PHB)
        mean_ar1, pval_ar1 = phb_test(strat_ar1)
        mean_ph, pval_ph = phb_test(strat_ph)
        mean_hist, pval_hist = phb_test(strat_hist)

        resultados_trading.append({
            'Commodity': c, 'TC': tc,
            'Retorno Med. AR1 (%)': round(mean_ar1 * 100, 3), 'P-val AR1': round(pval_ar1, 4),
            'Retorno Med. PH (%)': round(mean_ph * 100, 3), 'P-val PH': round(pval_ph, 4),
            'Ret. Med. Hist (%)': round(mean_hist * 100, 3), 'P-val Hist': round(pval_hist, 4)
        })

print("--- Evaluación de Rentabilidad (Estrategia AG & Test PHB) ---")
print(pd.DataFrame(resultados_trading).to_string(index=False))