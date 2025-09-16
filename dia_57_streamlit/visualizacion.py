import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carga los datos del archivo CSV
# Asegúrate de que el nombre del archivo sea exactamente el mismo que el de tu archivo de datos de EPH
df = pd.read_csv('datos.csv')

# Crea el mapa de calor
correlacion = df.corr(numeric_only=True)
sns.heatmap(correlacion, annot=True)

# Guarda el gráfico como un archivo PNG
plt.savefig('correlaciones.png')

print("El mapa de calor de correlaciones se ha guardado como 'correlaciones.png'.")