# -*- coding: utf-8 -*-
# estadisticas.py

import pandas as pd
import numpy as np
import sqlite3
from scipy import stats # Aunque en este ejemplo usaremos numpy.corrcoef, es bueno tenerla para futuros análisis

# Conectar a la base de datos SQLite
conn = sqlite3.connect('datos_sociales.db')

# Cargar los datos de la EPH que descargamos en el Día 59
try:
    df_eph = pd.read_sql_query("SELECT * FROM datos_eph_indec", conn)
    print("Datos de EPH cargados exitosamente.")
    # print(df_eph.head()) # Descomentar para ver las primeras filas y verificar
    # print(df_eph.columns) # Descomentar para ver todas las columnas
except pd.io.sql.DatabaseError:
    print("Error: La tabla 'datos_eph_indec' no existe. Asegúrate de haber ejecutado el Día 59 (descarga_datos.py).")
    conn.close()
    exit() # Salir del script si no hay datos

# --- Identificación de Variables (¡Aquí es donde tu sociología es clave!) ---
# En la EPH, las variables suelen ser números que representan categorías o valores.
# Necesitamos saber qué columnas corresponden a educación e ingresos.
# Si estas columnas no existen o tienen nombres diferentes, deberás ajustarlos aquí.

columna_educacion = 'NIVEL_ED' # Nombre de columna tentativa para Nivel Educativo
columna_ingresos = 'P47T'     # Nombre de columna para Ingreso Total Individual

# Verificar si las columnas existen en el DataFrame
if columna_educacion not in df_eph.columns:
    print(f"Advertencia: La columna '{columna_educacion}' no se encontró. Usando 'ANO4' como proxy de ejemplo para educación.")
    columna_educacion = 'ANO4' # Usar el año como proxy o una columna existente
    # Idealmente, aquí deberías buscar el diccionario de variables del INDEC para tu base EPH.
    # Por ahora, usamos ANO4 para que el script no falle, pero NO es "educación".

if columna_ingresos not in df_eph.columns:
    print(f"Advertencia: La columna '{columna_ingresos}' no se encontró. No se puede calcular correlación de ingresos.")
    print("Finalizando el script de análisis estadístico.")
    conn.close()
    exit()

# --- Limpieza y Preparación de Datos para Correlación ---
# La correlación funciona mejor con datos numéricos limpios.
# - Eliminar valores nulos (NaN)
# - Filtrar valores atípicos o códigos de "no aplica" / "no sabe" (que a menudo son -9, 99, etc. en la EPH)
# Por ahora, haremos una limpieza básica de NaN y de valores negativos (códigos)

# Filtramos valores negativos y nulos en las columnas de interés
df_analisis = df_eph[
    (df_eph[columna_educacion] >= 0) & # Asumimos educación no es negativa
    (df_eph[columna_ingresos] >= 0)    # Los ingresos deben ser >= 0
].dropna(subset=[columna_educacion, columna_ingresos])

if df_analisis.empty:
    print("No hay datos válidos para el análisis de correlación después de la limpieza.")
    conn.close()
    exit()

# --- Cálculo de Correlación ---
# Usaremos el coeficiente de correlación de Pearson, que es el predeterminado de np.corrcoef
# np.corrcoef devuelve una matriz de correlación. Queremos el valor entre las dos variables.
try:
    correlacion_matriz = np.corrcoef(df_analisis[columna_educacion], df_analisis[columna_ingresos])
    correlacion_pearson = correlacion_matriz[0, 1] # El valor de correlación entre las dos variables

    print("\n--- Análisis de Correlación ---")
    print(f"Correlación de Pearson entre '{columna_educacion}' y '{columna_ingresos}': {correlacion_pearson:.2f}")

    # Interpretación básica
    if abs(correlacion_pearson) >= 0.7:
        fuerza = "fuerte"
    elif abs(correlacion_pearson) >= 0.4:
        fuerza = "moderada"
    else:
        fuerza = "débil"

    if correlacion_pearson > 0:
        direccion = "positiva"
    elif correlacion_pearson < 0:
        direccion = "negativa"
    else:
        direccion = "nula"

    print(f"Interpretación: Existe una correlación {fuerza} y {direccion} entre {columna_educacion} y {columna_ingresos}.")
    print("¡Recuerda que correlación no implica causalidad!")

except Exception as e:
    print(f"Error al calcular la correlación: {e}")
    print("Asegúrate que las columnas seleccionadas son numéricas y tienen varianza.")

finally:
    conn.close()
    print("Conexión a la base de datos cerrada.")