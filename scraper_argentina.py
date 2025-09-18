import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
from datetime import datetime

# Crear base de datos
conn = sqlite3.connect('datos_argentina.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS noticias_argentina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    fuente TEXT NOT NULL,
    fecha TEXT NOT NULL,
    categoria TEXT,
    url TEXT UNIQUE
)
''')


# Scraper de noticias sociales
def scrapear_pagina12():
    try:
        url = "https://www.pagina12.com.ar/secciones/sociedad"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        noticias = []
        for articulo in soup.find_all('article', limit=10):
            titulo = articulo.find('h2')
            if titulo:
                noticias.append({
                    'titulo': titulo.text.strip(),
                    'fuente': 'Página12',
                    'fecha': datetime.now().strftime('%Y-%m-%d'),
                    'categoria': 'Sociedad',
                    'url': url
                })

        return noticias
    except Exception as e:
        print(f"Error scraping Página12: {e}")
        return []


# Scraper de datos del gobierno
def scrapear_datos_gobierno():
    try:
        url = "https://datos.gob.ar/dataset"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        datasets = []
        for dataset in soup.find_all('div', class_='dataset', limit=10):
            titulo = dataset.find('h3')
            if titulo:
                datasets.append({
                    'titulo': titulo.text.strip(),
                    'fuente': 'Datos Argentina',
                    'fecha': datetime.now().strftime('%Y-%m-%d'),
                    'categoria': 'Dataset',
                    'url': 'https://datos.gob.ar' + dataset.find('a')['href']
                })

        return datasets
    except Exception as e:
        print(f"Error scraping Datos Argentina: {e}")
        return []


# Ejecutar scrapers y guardar en SQLite
def main():
    print("Iniciando scraping de datos argentinos...")

    # Ejecutar ambos scrapers
    datos_p12 = scrapear_pagina12()
    datos_gob = scrapear_datos_gobierno()

    todos_datos = datos_p12 + datos_gob

    # Insertar en SQLite
    for dato in todos_datos:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO noticias_argentina 
                (titulo, fuente, fecha, categoria, url)
                VALUES (?, ?, ?, ?, ?)
            ''', (dato['titulo'], dato['fuente'], dato['fecha'],
                  dato['categoria'], dato['url']))
        except Exception as e:
            print(f"Error insertando dato: {e}")

    conn.commit()
    print(f"Datos guardados: {len(todos_datos)} registros")

    # Mostrar datos
    df = pd.read_sql_query("SELECT * FROM noticias_argentina", conn)
    print(df.head())

    print("\n--- Contenido completo de la base de datos ---")
    df_completo = pd.read_sql_query("SELECT * FROM noticias_argentina", conn)
    print(df_completo)


if __name__ == "__main__":
    main()
    conn.close()