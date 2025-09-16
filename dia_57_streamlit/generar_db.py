import sqlite3
import pandas as pd

# Conectar o crear la base de datos SQLite
conn = sqlite3.connect('datos_sociales.db')
cursor = conn.cursor()

# Crear tabla 'pobreza' si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pobreza (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        año INTEGER NOT NULL,
        tasa_pobreza REAL NOT NULL
    )
''')

# Datos de ejemplo (¡simulando datos del INDEC para Argentina!) 🇦🇷
data = {
    'año': [2018, 2019, 2020, 2021, 2022, 2023],
    'tasa_pobreza': [32.0, 35.5, 42.0, 40.6, 39.2, 41.7] # Tasas hipotéticas
}
df_pobreza = pd.DataFrame(data)

# Insertar datos en la tabla (o reemplazar si ya existen para este año)
# Usamos replace para facilitar las pruebas
df_pobreza.to_sql('pobreza', conn, if_exists='replace', index=False)

# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos 'datos_sociales.db' creada y poblada con datos de pobreza.")