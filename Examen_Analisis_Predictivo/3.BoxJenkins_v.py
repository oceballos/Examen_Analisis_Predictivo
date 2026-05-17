import pandas as pd
import numpy as np

# Explique los problemas de utilizar la estimacion dentro de muestra para pronosticar
# el GDP desde 2022 hasta 2030. Discuta los conceptos de analisis fuera de muestra
# haciendo referencia a Pincheira & Hardy (2019, 2021) y West (2006).

print("=" * 70)
print("PARTE (v): ESTIMACION DENTRO VS FUERA DE MUESTRA")
print("Pronostico del GDP UK 2022-2030 con modelos ARIMA")
print("=" * 70)

print("""
=======================================================================
1. PROBLEMAS DE LA ESTIMACION DENTRO DE MUESTRA (IN-SAMPLE)
=======================================================================

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
   - Los parametros estimados en el periodo 1980-1998 pueden no ser
     representativos de la dinamica economica actual.
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
""")
