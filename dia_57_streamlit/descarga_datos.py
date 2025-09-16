# descarga_datos.py
import requests
import pandas as pd
import sqlite3
import io
from zipfile import ZipFile

# --- Configuración ---
# URL del archivo ZIP del INDEC.
# ¡IMPORTANTE! Esta URL puede cambiar. Si vuelve a fallar, busca la más reciente.
url_indec_eph = "https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_usu_1_Trim_2025_xls.zip"

# Posibles nombres de archivos Excel dentro del ZIP.
# Hemos priorizado el archivo de base individual (usu_individual)
# Basado en tu log anterior: ['EPH_usu_1er_Trim_2025_xlsx/usu_hogar_T125.xlsx', 'EPH_usu_1er_Trim_2025_xlsx/usu_individual_T125.xlsx']
posibles_nombres_excel = [
    "EPH_usu_1er_Trim_2025_xlsx/usu_individual_T125.xlsx",  # ¡Este es el que queremos para análisis individual!
    "EPH_usu_1er_Trim_2025_xlsx/usu_hogar_T125.xlsx",
    # Si no encuentra el individual, lee este (aunque no es lo ideal para ingresos/educación)
    "base_individual.xls",
    "base_individual.xlsx",
    "usu_individual.xls",
    "usu_individual.xlsx",
    # Otros nombres comunes que podrían aparecer en otros trimestres o versiones
    "EPH_T12025_individual.xls",
    "EPH_T12025_individual.xlsx",
]

# Nombre de la tabla en SQLite donde se guardarán estos datos
nombre_tabla_db = 'datos_eph_indec'

# --- Lógica de Descarga y Procesamiento ---
# Conectar a la base de datos SQLite existente
conn = sqlite3.connect('datos_sociales.db')

try:
    print(f"Intentando descargar datos de: {url_indec_eph}")
    response = requests.get(url_indec_eph)
    response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx
    print("Descarga exitosa. Procesando ZIP...")

    df = None  # Inicializamos el DataFrame como None

    with ZipFile(io.BytesIO(response.content)) as zfile:
        print("Archivos dentro del ZIP:", zfile.namelist())  # ¡Esta línea es clave para depuración!

        excel_file_found = None
        for possible_name in posibles_nombres_excel:
            if possible_name in zfile.namelist():
                excel_file_found = possible_name
                break  # Encontramos uno, salimos del bucle

        if excel_file_found:
            print(f"Intentando leer el archivo Excel: '{excel_file_found}'.")
            with zfile.open(excel_file_found) as excel_file:
                # pd.read_excel puede necesitar 'header' si los datos no empiezan en la fila 0
                # y 'sheet_name' si el Excel tiene múltiples hojas y queremos una específica.
                # Para el INDEC, a menudo la primera hoja es la que tiene los datos.
                df = pd.read_excel(excel_file, engine='openpyxl')
                print(f"Archivo '{excel_file_found}' leído correctamente.")
        else:
            # Si no encontramos los nombres comunes, buscamos el primer .xls o .xlsx que haya
            excel_files = [f for f in zfile.namelist() if f.endswith(('.xls', '.xlsx'))]
            if excel_files:
                # Tomamos el primer archivo Excel que encontremos
                excel_file_found = excel_files[0]
                print(
                    f"No se encontró un nombre predefinido, intentando leer el primer archivo Excel: {excel_file_found}")
                with zfile.open(excel_file_found) as excel_file:
                    df = pd.read_excel(excel_file, engine='openpyxl')
            else:
                raise ValueError("No se encontraron archivos Excel (.xls/.xlsx) dentro del ZIP.")

    if df is not None:  # Si se pudo cargar el DataFrame
        # Opcional: Mostrar las primeras filas y columnas para verificar
        print("\n--- Primeras 5 filas del DataFrame descargado ---")
        print(df.head())
        print("\n--- Columnas del DataFrame ---")
        print(df.columns)
        print("\n--- Información del DataFrame ---")
        print(df.info())

        # Guardar el DataFrame en la tabla SQLite
        df.to_sql(nombre_tabla_db, conn, if_exists='replace', index=False)
        print(f"\nDatos guardados exitosamente en la tabla '{nombre_tabla_db}' en 'datos_sociales.db'.")
    else:
        print("No se pudo cargar ningún DataFrame desde el ZIP. Revisar el contenido del ZIP.")

except requests.exceptions.RequestException as e:
    print(f"Error al descargar el archivo: {e} (Verifica la URL y tu conexión a internet).")
except ValueError as e:
    print(f"Error al procesar el ZIP: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
finally:
    conn.close()
    print("Conexión a la base de datos cerrada.")