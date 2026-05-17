import pandas as pd
import numpy as np
import statsmodels.api as sm

# 1. Cargar y preparar datos
df = pd.read_excel('data/Ejemplo Datos commodities.xlsx')
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.replace('M', ''), format='%Y%m')
df.set_index('Date', inplace=True)
df = df.loc['1999-09-01':]

# 2. Calcular retornos
vars_all = ['CHILE', 'AUSTRALIA', 'COPPER', 'ALUMINUM', 'LMEX']
log_df = np.log(df[vars_all])
returns = log_df.diff().dropna()

commodities = ['COPPER', 'ALUMINUM', 'LMEX']
tcs = ['CHILE', 'AUSTRALIA']

resultados_hac = []

# 3. Iterar y correr regresiones con errores HAC
for c in commodities:
    y = returns[c]
    y_lag1 = y.shift(1)

    for tc in tcs:
        tc_lag1 = returns[tc].shift(1)

        # Alinear data
        df_aug = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1, 'TC_lag1': tc_lag1}).dropna()
        X_aug = sm.add_constant(df_aug[['Y_lag1', 'TC_lag1']])

        # Ajuste HAC (Newey-West con 12 rezagos para capturar estacionalidad anual)
        model_hac = sm.OLS(df_aug['Y'], X_aug).fit(cov_type='HAC', cov_kwds={'maxlags': 12})

        # Extraer estadísticos
        p_rho_hac = model_hac.pvalues['Y_lag1']
        p_beta_hac = model_hac.pvalues['TC_lag1']

        resultados_hac.append({
            'Commodity': c,
            'Tipo Cambio': tc,
            'P-value Rho (HAC)': round(p_rho_hac, 4),
            'P-value Beta (HAC)': round(p_beta_hac, 4)
        })

print("--- Regresiones con Errores HAC ---")
df_res_hac = pd.DataFrame(resultados_hac)
print(df_res_hac.to_string(index=False))