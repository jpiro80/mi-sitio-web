import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import sys

# Conectar a la base de datos
conn = sqlite3.connect('datos_argentina.db')

# Análisis 1: Conteo por fuente
df = pd.read_sql_query("SELECT * FROM noticias_argentina", conn)
conteo_fuentes = df['fuente'].value_counts()

print("📊 Análisis de datos scrapeados:")
print(f"Total de registros: {len(df)}")
print("\n📈 Por fuente:")
print(conteo_fuentes)

# Análisis 2: Palabras más comunes en títulos
def analizar_palabras_comunes(titulos):
    palabras = []
    for titulo in titulos:
        palabras.extend(titulo.lower().split())
    
    # Filtrar palabras comunes
    palabras_filtradas = [p for p in palabras if len(p) > 4 and p not in ['sobre', 'desde']]
    return Counter(palabras_filtradas).most_common(10)

palabras_comunes = analizar_palabras_comunes(df['titulo'].tolist())
print("\n🔤 Palabras más comunes en títulos:")
for palabra, count in palabras_comunes:
    print(f"{palabra}: {count}")

# Visualización
plt.figure(figsize=(10, 6))
conteo_fuentes.plot(kind='bar', color=['#007CE0', '#00A0D6'])  # Colores argentinos
plt.title('Noticias por Fuente')
plt.xlabel('Fuente')
plt.ylabel('Cantidad')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('analisis_fuentes.png')
plt.show()

# Guardar análisis en CSV
df.to_csv('datos_analizados.csv', index=False, encoding='utf-8')
print("\n💾 Análisis guardado en 'datos_analizados.csv'")

conn.close()
