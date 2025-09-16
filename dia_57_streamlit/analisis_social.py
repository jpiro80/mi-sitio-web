# analisis_social.py
import streamlit as st
import pandas as pd
import sqlite3

# Conectar a SQLite
conn = sqlite3.connect('datos_sociales.db')

# Cargar datos de la tabla 'pobreza'
df = pd.read_sql_query("SELECT * FROM pobreza", conn)

# Cerrar la conexión después de cargar los datos
conn.close()

st.title("Análisis de Datos Sociales en Argentina 🇦🇷")

st.markdown("---") # Esto es una línea divisoria
st.subheader("Datos de Tasa de Pobreza (ejemplo)")
st.dataframe(df) # Muestra el DataFrame completo en una tabla

st.markdown("---") # Otra línea divisoria
st.subheader("Evolución de la Tasa de Pobreza por Año")
# Asegurarse de que la columna 'año' sea el índice para el gráfico de línea
# Esto le dice a Streamlit que 'año' es el eje X
st.line_chart(df.set_index('año')['tasa_pobreza'])

st.markdown("---")
st.info("Este es un dashboard de ejemplo. ¡Puedes añadir más análisis y visualizaciones!")