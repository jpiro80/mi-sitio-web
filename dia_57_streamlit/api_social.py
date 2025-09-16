# api_social.py
from fastapi import FastAPI
import sqlite3
import pandas as pd # Agregamos pandas para poder leer los datos de la DB

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Análisis Social de Argentina 🇦🇷"}

@app.get("/datos")
def get_datos_pobreza():
    conn = sqlite3.connect('datos_sociales.db')
    # Leer los datos de la tabla 'pobreza'
    df = pd.read_sql_query("SELECT * FROM pobreza", conn)
    conn.close()

    # Convertir el DataFrame a un formato que FastAPI pueda retornar (lista de diccionarios)
    return {"pobreza_argentina": df.to_dict(orient="records")}

@app.get("/datos/{anio}")
def get_datos_por_anio(anio: int):
    conn = sqlite3.connect('datos_sociales.db')
    df = pd.read_sql_query(f"SELECT * FROM pobreza WHERE año = {anio}", conn)
    conn.close()

    if df.empty:
        return {"message": f"No hay datos para el año {anio}"}
    return {"pobreza_argentina_anio": df.to_dict(orient="records")[0]} # Solo el primer resultado