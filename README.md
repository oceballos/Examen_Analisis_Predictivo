# Examen — Análisis Predictivo de Finanzas
Autores: Osvaldo Ceballos, Yerko Fuentes, Paloma San Martin.

Profesor: Nicolás Hardy

## Requisitos

Python 3.13 · entorno virtual en `.venv/` o puede crear un entorno virtual con `python -m venv .venv/`

Instalar dependencias (solo la primera vez):

```bash
pip install pandas numpy matplotlib statsmodels scipy openpyxl xlsxwriter
```

---

## Estructura del proyecto

```
raiz/
├── data/
│   ├── GDP UK.xlsx                        # Serie trimestral PIB Reino Unido 1980-1998
│   └── Ejemplo Datos commodities.xlsx     # Precios de commodities y tipos de cambio
├── enunciado/
│   └── Examen.pdf                         # Enunciado completo
├── 1. Shocks_i.py                         # Parte 1 — sección i
├── 1.Shocks_ii.py
├── 1.Shocks_iii.py
├── 2.Commodity_i.py  …  2.Commodity_xi.py # Parte 2
├── 3.BoxJenkins_i.py …  3.BoxJenkins_v.py # Parte 3
└── README.md
```

---

## Cómo ejecutar

**Todos los scripts se ejecutan desde la raíz del proyecto.**

```bash
# Ejemplo genérico
python "nombre_script.py"
```

### Parte 1 · Shocks AR(1)

| Script | Qué hace |
|---|---|
| `1. Shocks_i.py` | Simula 20 procesos AR(1), corre 10 regresiones OLS/HAC y exporta datos a Excel |
| `1.Shocks_ii.py` | Análisis complementario de shocks |
| `1.Shocks_iii.py` | Análisis complementario de shocks |

Salida: archivos `Examen - Shocks*.xlsx` en la raíz del proyecto.

---

### Parte 2 · Commodities

| Script | Qué hace |
|---|---|
| `2.Commodity_i.py` | Serie en niveles y logaritmos + ACF/PACF de las 5 variables |
| `2.Commodity_ii.py` | ACF/PACF de retornos a 1 mes vs 12 meses |
| `2.Commodity_iii.py` | Histogramas + test Jarque-Bera de normalidad |
| `2.Commodity_iv.py` | Regresiones OLS con retornos rezagados |
| `2.Commodity_v.py` | … |
| `2.Commodity_vi.py` | … |
| `2.Commodity_vii.py` | … |
| `2.Commodity_viii.py` | Predicción fuera de muestra (ventana expandida 50/50) |
| `2.Commodity_ix.py` | … |
| `2.Commodity_x.py` | … |
| `2.Commodity_xi.py` | Estrategia trading (Anatolyev-Gerko) + test PHB |

Salidas de gráficos:

```
2.Commodity_Graficos_i/    ← imágenes de 2.Commodity_i.py
2.Commodity_Graficos_ii/   ← imágenes de 2.Commodity_ii.py
2.Commodity_Graficos_iii/  ← imágenes de 2.Commodity_iii.py
```

---

### Parte 3 · Box-Jenkins (GDP UK)

Ejecutar en orden secuencial, ya que cada script apoya la respuesta del siguiente:

```bash
python 3.BoxJenkins_i.py    # (i)   Serie en niveles + ACF/PACF
python 3.BoxJenkins_ii.py   # (ii)  Primera diferencia log + ACF/PACF
python 3.BoxJenkins_iii.py  # (iii) Test ADF + selección de 4 modelos ARIMA
python 3.BoxJenkins_iv.py   # (iv)  Estimación, comparación y gráfico del mejor modelo
python 3.BoxJenkins_v.py    # (v)   Discusión OOS — solo imprime en consola
```

Salidas de gráficos:

```
3.BoxJenkins_Graficos_i/    ← gdp_uk_serie.png, gdp_uk_acf_pacf.png
3.BoxJenkins_Graficos_ii/   ← dlgdp_uk_serie.png, dlgdp_uk_acf_pacf.png
3.BoxJenkins_Graficos_iv/   ← arima_mejor_modelo_ARIMA(p,d,q).png
```

> `3.BoxJenkins_v.py` no genera archivos; la respuesta se imprime directamente en la consola.

---

## Dónde encontrar resultados

| Tipo de resultado | Ubicación |
|---|---|
| Gráficos Parte 2 | Carpetas `2.Commodity_Graficos_*/` en la raíz |
| Gráficos Parte 3 | Carpetas `3.BoxJenkins_Graficos_*/` en la raíz |
| Excel Parte 1 | `Examen - Shocks*.xlsx` en la raíz |
| Salida de consola | Terminal al ejecutar cada script |
