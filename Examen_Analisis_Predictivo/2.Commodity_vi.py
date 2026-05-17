import pandas as pd
import numpy as np
import statsmodels.api as sm

# 1. Cargar y preparar datos
df = pd.read_excel('Ejemplo Datos commodities.xlsx')
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.replace('M', ''), format='%Y%m')
df.set_index('Date', inplace=True)
df = df.loc['1999-09-01':]

vars_all = ['CHILE', 'COPPER', 'ALUMINUM', 'LMEX'] 
returns = np.log(df[vars_all]).diff().dropna()

commodities = ['COPPER', 'ALUMINUM', 'LMEX']
tc = 'CHILE'

resultados_ph = []

# 3. Iterar y correr regresiones con la especificación de Pincheira y Hardy
for c in commodities:
    y = returns[c]
    y_lag1 = y.shift(1)

    # Dos rezagos del tipo de cambio
    tc_lag1 = returns[tc].shift(1)
    tc_lag2 = returns[tc].shift(2)

    # Alinear data (se pierden 2 observaciones por los rezagos)
    df_ph = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1, 'TC_lag1': tc_lag1, 'TC_lag2': tc_lag2}).dropna()
    X_ph = sm.add_constant(df_ph[['Y_lag1', 'TC_lag1', 'TC_lag2']])

    # Ajustar modelo OLS
    model = sm.OLS(df_ph['Y'], X_ph).fit()

    # TEST DE HIPÓTESIS CONJUNTA (Test F de Wald)
    # H0: TC_lag1 = 0 y TC_lag2 = 0
    hypothesis = '(TC_lag1 = 0), (TC_lag2 = 0)'
    f_test = model.f_test(hypothesis)

    resultados_ph.append({
        'Commodity': c,
        'P-value Beta 1': round(model.pvalues['TC_lag1'], 4),
        'P-value Beta 2': round(model.pvalues['TC_lag2'], 4),
        'Estadistico F': round(f_test.fvalue, 4),
        'P-value Test F': round(f_test.pvalue, 4)
    })

print("--- Test de Hipótesis Conjunta (H0: Beta1 = Beta2 = 0) ---")
df_res_ph = pd.DataFrame(resultados_ph)
print(df_res_ph.to_string(index=False))