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

# Lista para guardar los resultados
resultados = []

# 3. Iterar y correr regresiones
for c in commodities:
    y = returns[c]
    y_lag1 = y.shift(1)  # Rezago 1 del commodity (rho)

    # Modelo Base: AR(1) sin Tipo de Cambio
    df_base = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1}).dropna()
    X_base = sm.add_constant(df_base['Y_lag1'])
    model_base = sm.OLS(df_base['Y'], X_base).fit()
    r2_base = model_base.rsquared

    for tc in tcs:
        # Rezago 1 del Tipo de Cambio (beta)
        tc_lag1 = returns[tc].shift(1)

        # Modelo Aumentado: AR(1) + TC
        df_aug = pd.DataFrame({'Y': y, 'Y_lag1': y_lag1, 'TC_lag1': tc_lag1}).dropna()
        X_aug = sm.add_constant(df_aug[['Y_lag1', 'TC_lag1']])
        model_aug = sm.OLS(df_aug['Y'], X_aug).fit()

        # Extraer estadísticos
        r2_aug = model_aug.rsquared
        p_rho = model_aug.pvalues['Y_lag1']
        p_beta = model_aug.pvalues['TC_lag1']

        resultados.append({
            'Commodity': c,
            'Tipo Cambio': tc,
            'P-value Rho (AR1)': round(p_rho, 4),
            'P-value Beta (TC)': round(p_beta, 4),
            'R2 Base': round(r2_base, 4),
            'R2 Aumentado': round(r2_aug, 4),
            'Aumento R2': round(r2_aug - r2_base, 4)
        })

# Mostrar la tabla de resultados
df_resultados = pd.DataFrame(resultados)
print(df_resultados.to_string(index=False))