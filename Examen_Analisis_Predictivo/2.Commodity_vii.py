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

# Diccionario para guardar el R2 del modelo no restringido (Punto G) para Chile
r2_no_restringido_chile = {}
for c in commodities:
    y, y_lag1 = returns[c], returns[c].shift(1)
    tc_lag1, tc_lag2 = returns['CHILE'].shift(1), returns['CHILE'].shift(2)
    df_temp = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1, 'TC_lag1': tc_lag1, 'TC_lag2': tc_lag2}).dropna()
    X = sm.add_constant(df_temp[['Y_lag1', 'TC_lag1', 'TC_lag2']])
    r2_no_restringido_chile[c] = sm.OLS(df_temp['Y'], X).fit().rsquared

resultados_h = []

# 3. Correr la regresión de PH (Predictor Sumado)
for c in commodities:
    y = returns[c]
    y_lag1 = y.shift(1)

    for tc in tcs:
        # Sumar los rezagos 1 y 2
        tc_lag1 = returns[tc].shift(1)
        tc_lag2 = returns[tc].shift(2)
        tc_sum = tc_lag1 + tc_lag2

        df_ph2 = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1, 'TC_sum': tc_sum}).dropna()
        X_ph2 = sm.add_constant(df_ph2[['Y_lag1', 'TC_sum']])

        model_ph2 = sm.OLS(df_ph2['Y'], X_ph2).fit()
        r2_restringido = model_ph2.rsquared
        p_beta = model_ph2.pvalues['TC_sum']

        # Calcular cuánto baja el R2 solo para el caso de Chile
        baja_r2 = r2_no_restringido_chile[c] - r2_restringido if tc == 'CHILE' else None

        resultados_h.append({
            'Commodity': c,
            'Tipo Cambio': tc,
            'P-value Beta (Suma)': round(p_beta, 4),
            'R2 Modelo Suma': round(r2_restringido, 4),
            'Caída de R2 vs Pt(g)': round(baja_r2, 6) if baja_r2 is not None else '-'
        })

print("--- Resultados Especificación Predictor Sumado (PH) ---")
df_res_h = pd.DataFrame(resultados_h)
print(df_res_h.to_string(index=False))