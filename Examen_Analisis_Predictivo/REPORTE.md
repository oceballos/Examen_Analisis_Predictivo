# EXÁMEN ANALISIS PREDICTIVO EN FINANZAS
Autores: Osvaldo Ceballos, Yerko Fuentes, Paloma San Martin.

## PARTE 3 METODOLOGÍA BOX-JENKINS 
Se usa el archivo gdp_uk que contiene observaciones trimestrales del 
producto interno bruto de UK para el período 1980-1998 (trimestral) 


### a. ANALISIS PRELIMINAR DE ESTACIOANRIEDAD
Se grafica la serie de `GDP UK` y luego se construyen los gráficos de 
autocorrelacion (ACF) y autocorrelacion parcial (PACF). 
Se observa que la serie no es estacionaria y que se comporta como una 
serie de raíz unitaria (Random Walk). Esto queda claro al observar que PACF 
cae abruptamente tendiendo a 0 en el lag 1 y ACF cae lentamente de forma lineal, 
ambos casos consistentes con lo revisado para series simuladas no estacionarias 
de raiz unitaria.

### b. ANÁLISIS EN 1ERAS DIFERENCIAS (LOG)
La serie dlog(GDP) fluctúa alrededor de una media constante positiva.
La ACF cae rápida y abruptamente hacia cero desde el lag 1.
Este patron es consistente con un proceso estacionario (posiblemente ruido blanco).
La primera diferencia logarÍtmica elimina la tendencia y la serie resulta estacionaria.
Esto sugiere que la serie en niveles es integrada de orden 1: I(1).

### c. ORDEN DE INTEGRACIÓN DE LA SERIE PARA MODELOS ARIMA(p,d,q)

Para analizar el orden de integración de la serie se usa el test ADF (ADF de Dickey-Fuller), el cual nos permite 
determinar si la serie es estacionaria o no. Se compara la serie dlog(GDP) con la serie log(GDP) para determinar si (d=1) 
permite rechazar H0 en el test ADF.


CONCLUSION SOBRE EL ORDEN DE INTEGRACION:

  log(GDP UK) NO es estacionario en niveles.
  dlog(GDP UK) SI es estacionario.
   - La serie es integrada de orden 1: I(1).
   - Se modela con d=1 en el ARIMA(p,1,q).

Especificaciones de modelos ARIMA candidatos (con d=1)

  La ACF de dlog(GDP) muestra autocorrelación significativa en lag 1 y/o 2,
  mientras que la PACF muestra un corte abrupto tras el lag 1 o 2.
  Esto sugiere que la parte AR y MA de bajo orden son razonables, 
  además permiten mantener parsimonía en los parámetros.

  Modelos candidatos:

   1. ARIMA(1,1,0): La PACF tiene un pico en lag 1 -> componente AR(1) domina.
                   Equivalente a un AR(1) sobre la primera diferencia.

   2. ARIMA(0,1,1): La ACF tiene un pico en lag 1 y cae -> componente MA(1).
                   Equivalente al modelo IMA(1,1).

   3. ARIMA(1,1,1): Combina AR(1) y MA(1) para mayor flexibilidad.
                   Permite capturar patrones mixtos en la autocorrelación.

   4. ARIMA(2,1,0): AR(2) sobre la primera diferencia, si la PACF muestra
                   autocorrelación significativa hasta el lag 2.

### d. MODELOS ARIMA(p,d,q) y discusión sobre indicadores de calidad.

Según lo definido en [3.c] se realizan pruebas con todas las especificaciones candidatas. 
Utilizando el test AIC y BIC se selecciona el modelo ARIMA(1,1,1) con el mejor 
indicador de calidad (AIC). Además se muestra  el valor de DW (o test F de Durbin-Watson).

| Modelo | AIC | BIC | Log-Lik | DW |
|---|---:|---:|---:|---:|
| ARIMA(1,1,1) | -527.491 | -520.619 | 266.745 | 1.0093 |
| ARIMA(2,1,0) | -523.900 | -517.028 | 264.950 | 1.0094 |
| ARIMA(1,1,0) | -522.667 | -518.086 | 263.333 | 1.0094 |
| ARIMA(0,1,1) | -504.409 | -499.828 | 254.205 | 1.0093 |

El modelo ARIMA(1,1,1) tiene un R2 de 0.81, pero el R2 NO es un criterio apropiado para seleccionar modelos ARIMA porque:
  1. El R2 aumenta por construcción al agregar párametros (sobreajuste).
  2. No penaliza la complejidad del modelo (a diferencia de AIC/BIC).
  3. En modelos con diferenciación (d>0), el R2 compara con una media trivial
     de la serie diferenciada, no con la serie original, lo que puede ser
     engañoso.
  4. Los criterios AIC y BIC son preferibles: penalizan la log-verosimilitud
     por el número de parámetros estimados (BIC penaliza mas fuertemente).

Comportamiento esperado de los residuos:
- Distribución aproximadamente normal con media cero.
- Sin autocorrelación significativa (ruido blanco).
- Varianza constante (homocedasticidad).
- El DW debería ser cercano a 2, en el caso de los modelos propeustos El estadístico DW es prácticamente 
idéntico en todos los modelos (~1.009), lo que sugiere autocorrelación residual positiva moderada en todos los casos.

### e. PROBLEMAS DE LA ESTIMACIÓN DENTRO DE MUESTRA (IN-SAMPLE)

Usar la estimacion dentro de muestra para pronosticar el GDP UK en el
horizonte 2022-2030 presenta varios problemas fundamentales:

a) SOBREAJUSTE (Overfitting):
   Los parametros del modelo ARIMA son estimados minimizando el error
   dentro de la muestra de estimacion (1980-1998). El modelo puede ajustarse
   bien a los datos historicos pero fallar sistematicamente fuera de ese
   rango. Un modelo con mas parametros siempre tendra menor error in-sample,
   aunque no sea el mas apropiado para predecir.

b) BRECHA TEMPORAL EXCESIVA:
   La muestra de estimacion cubre 1980-1998, pero el objetivo es pronosticar
   2022-2030. Esta brecha de mas de 20 anos implica que:
   - Cambios estructurales (crisis 2008, Brexit, COVID-19) no estan
     incorporados en el modelo.
   - Los parámetros estimados en el periodo 1980-1998 pueden no ser
     representativos de la dinámica económica actual.
   - La incertidumbre del pronostico crece exponencialmente con el horizonte.

c) INTERVALOS DE CONFIANZA SUBESTIMADOS:
   La incertidumbre parametrica no se refleja correctamente cuando se
   reportan solo los errores de pronostico in-sample. Los intervalos de
   prediccion tendrian cobertura incorrecta (demasiado angostos).

d) NO HAY EVALUACION REAL DE LA CAPACIDAD PREDICTIVA:
   Un modelo puede tener excelente ajuste in-sample (R2, AIC, BIC) pero
   producir pronosticos de mala calidad. La unica forma de evaluar
   genuinamente la capacidad predictiva es mediante analisis fuera de muestra.

=======================================================================
2. ANALISIS FUERA DE MUESTRA (OUT-OF-SAMPLE)
=======================================================================

El analisis fuera de muestra (OOS) separa los datos en:
   - Muestra de estimacion (in-sample): se estiman los parametros del modelo.
   - Muestra de evaluacion (out-of-sample): se evalua la precision predictiva
     con datos que el modelo NO vio durante la estimacion.

Esto permite una evaluacion genuina de si el modelo tiene valor predictivo
por encima de benchmarks simples.

=======================================================================
3. CONTRIBUCIONES DE LA LITERATURA
=======================================================================

--- West (2006) ---
   Kenneth West en "Forecast Evaluation" (2006) establece los fundamentos
   formales del analisis predictivo fuera de muestra. Sus principales aportes:

   a) Distingue entre tres esquemas de ventana OOS:
      - Ventana fija (Rolling): se estima con ventana de tamano fijo R que
        avanza periodo a periodo.
      - Ventana expandida (Recursive): se usa toda la informacion disponible
        hasta T para predecir T+1.
      - Fija (Fixed): los parametros se estiman una vez y se mantienen fijos.

   b) Deriva la distribucion asintotica de estadisticos de comparacion de
      pronosticos, permitiendo hacer inferencia sobre cual modelo predice
      mejor en el periodo de evaluacion.

   c) Señala que bajo ciertos esquemas de ventana, los errores de pronostico
      OOS son correlacionados en el tiempo, requiriendo correccion de la
      varianza (HAC).

   d) Establece que la evaluacion OOS es el estandar para determinar si un
      modelo tiene valor economico real, no solo ajuste estadistico.

--- Pincheira & Hardy (2019, 2021) ---
   Pablo Pincheira y Nicolas Hardy desarrollan una metodologia de evaluacion
   predictiva especialmente relevante para series macroeconomicas:

   a) Pincheira & Hardy (2019) - "Can we Beat the Random Walk?":
      Proponen el test R2 OOS como medida de habilidad predictiva relativa:

         R2_OOS = 1 - MSE_modelo / MSE_benchmark

      donde MSE es el Error Cuadratico Medio fuera de muestra.
      - Si R2_OOS > 0: el modelo supera al benchmark (ej. caminata aleatoria).
      - Si R2_OOS <= 0: el modelo no agrega valor predictivo.

   b) El benchmark natural para el GDP es la caminata aleatoria (random walk)
      o el modelo de promedio historico, que son dificiles de superar en
      horizontes largos.

   c) Pincheira & Hardy (2021) extienden el analisis a estrategias de trading
      y rentabilidad economica de los pronosticos, mostrando que la
      significancia estadistica no implica necesariamente valor economico.

   d) Proponen el test PHB (Pincheira-Hardy-Bentancor) para evaluar si la
      rentabilidad media de estrategias basadas en pronosticos es
      significativamente positiva, usando errores estandar HAC (Newey-West).

=======================================================================
4. IMPLICANCIAS PARA EL PRONOSTICO DEL GDP UK 2022-2030
=======================================================================

Para pronosticar correctamente el GDP UK hasta 2030 se deberia:

   1. Actualizar la muestra de estimacion con datos recientes (post-1998)
      para capturar cambios estructurales relevantes.

   2. Comparar el modelo ARIMA contra benchmarks simples (caminata aleatoria,
      promedio historico) usando un esquema OOS recursivo o rolling.

   3. Calcular el R2 OOS (Pincheira & Hardy, 2019) para evaluar si el modelo
      agrega valor predictivo real.

   4. Reportar intervalos de prediccion que incorporen tanto la incertidumbre
      del pronostico como la incertidumbre parametrica.

   5. Reconocer que en horizontes muy largos (8 anos), la incertidumbre es
      tan alta que cualquier modelo puntual tendra escasa precision.

# ANEXOS

## ANEXOS PARTE 3:

============================================================
DETERMINACION DEL ORDEN DE INTEGRACION - GDP UK
============================================================

--- Test ADF: log(GDP UK) - Niveles ---
  Estadistico ADF : -1.2371
  P-valor         : 0.6574
  Lags utilizados : 3
  Valores criticos:
    1%: -3.5274
    5%: -2.9038
    10%: -2.5893
  Conclusion: NO se rechaza H0 (raiz unitaria) al 5% -> Serie NO ESTACIONARIA

--- Test ADF: dlog(GDP UK) - Primera Diferencia ---
  Estadistico ADF : -3.8676
  P-valor         : 0.0023
  Lags utilizados : 2
  Valores criticos:
    1%: -3.5274
    5%: -2.9038
    10%: -2.5893
  Conclusion: Se RECHAZA H0 (raiz unitaria) al 5% -> Serie ESTACIONARIA