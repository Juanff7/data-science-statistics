import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings('ignore')

datos = pd.read_excel('WHO_Limpio.xlsx')


#3 filtrar a europa (año 2010-2022) # Corrected the year range in the comment
datos_europa = datos[(datos["who_region"] == "4_Eur") & (datos["year"].between(2010,2022))]

#4 medidas de tendecias de dispercion
no2 = datos_europa["no2_concentratio"].dropna() # Corrected variable name to datos_europa
print("media: ", no2.mean())
print("mediana: ", no2.median())
print("Moda: ", no2.mode().values)
print("Desviacion estandar", no2.std())
print("Rango intercuartilico: ",  no2.quantile(0.75)-no2.quantile(0.25))






#3 histograma sobre la concentracion de no2 (forma de distribucion)
sns.histplot(datos_europa[datos_europa["no2_concentratio"] < 100]["no2_concentratio"],
             bins=30, kde=True, color="steelblue")
plt.axvline(x=40, color="red", linestyle="--", label="Límite OMS (40 µg/m³)")
plt.title("Histograma de concentración de NO₂ (Europa 2010–2022)")
plt.xlabel("Concentración de NO₂ (µg/m³)")
plt.ylabel("Frecuencia")
plt.legend()
plt.show()



plt.figure(figsize=(10, 6))
sns.boxplot(x='year', y='no2_concentratio',
               data= datos_europa, palette='Set2')
plt.axhline(40, color='red', linestyle='--', label='Límite OMS (40 µg/m³')
plt.ylim(0, 200)   # <-- solo muestra hasta 200 µg/m³
plt.legend()
plt.title('Distribución de Concentración de NO₂ por Año (Europa 2010–2022)')
plt.xlabel('Año')
plt.ylabel('Concentración de NO₂ (µg/m³)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#3 Barra para mostrar las 10 ciudades con las concentraciones medias de no2 mas altas y bajas , durante la ultima decada
# Promedio de NO₂ por ciudad
ciudades_no2 = datos_europa.groupby('city')['no2_concentratio'].mean().dropna()

#obtener ciudades
top10 = ciudades_no2.sort_values(ascending=False).head(10)
bottom10 = ciudades_no2.sort_values(ascending=True).head(10)


#Top 10 ciudades con la concentracion(media) de no2 mas alta
plt.figure(figsize=(12,6))
top10.plot(kind='bar', color='darkred')
plt.axhline(40, color='red', linestyle='--', label='Límite OMS (40 µg/m³)')
plt.title('Top 10 ciudades con mayor concentración media de NO₂ (2012–2022)')
plt.ylabel('Concentración media de NO₂ (µg/m³)')
plt.xlabel('Ciudad')
plt.legend()
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.show()


plt.figure(figsize=(12,6))
bottom10.plot(kind='bar', color='darkgreen')
plt.axhline(40, color='red', linestyle='--', label='Límite OMS (40 µg/m³)')
plt.title('Top 10 ciudades con menor concentración media de NO₂ (2012–2022)')
plt.ylabel('Concentración media de NO₂ (µg/m³)')
plt.xlabel('Ciudad')
plt.legend()
plt.ylim(0, 5)
plt.xticks(rotation=45)
plt.show()


#Medida anual de NO2 en eurpa 2010-2022 su promedio en toda la decada

datos_no2_anuales = datos_europa.groupby('year')['no2_concentratio'].mean()
plt.figure(figsize=(10, 6))
plt.plot(datos_no2_anuales.index ,datos_no2_anuales.values ,color='steelblue',marker='*',markersize=8)
plt.title('Evolución histórica de la concentración promedio de NO₂ (Europa 2010–2022)')
plt.xlabel('Año')
plt.ylabel('Concentración promedio de NO₂ (µg/m³)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


# 1) Filtrar a 2020–2022
df_2020_22 = datos_europa[datos_europa['year'].between(2020, 2022)].copy()

#Agrupar por tipos de estaciones
estacion_no2 = df_2020_22.groupby(['type_of_stations', 'year'])['no2_concentratio'].mean().reset_index()
orden_estaciones = ['Urban', 'Suburban']
estacion_no2['type_of_stations'] = pd.Categorical(estacion_no2['type_of_stations'], categories=orden_estaciones, ordered=True)
#Graficar
# 3) Gráfico de barras agrupadas
plt.figure(figsize=(10,6))
sns.barplot(data=estacion_no2, x='year', y='no2_concentratio',
            hue='type_of_stations', palette='Set2', ci=None)
plt.title('Comparación de NO₂ entre estaciones Urban y Suburban (2020–2022)')
plt.xlabel('Año')
plt.ylabel('Concentración promedio de NO₂ (µg/m³)')
plt.legend()

# Línea guía de la OMS
plt.axhline(40, color='red', linestyle='--', label='Límite OMS (40 µg/m³)')


plt.title('Comparación de NO₂ entre estaciones Urban y Suburban (2020–2022)')
plt.xlabel('Año')
plt.ylabel('Concentración promedio de NO₂ (µg/m³)')
plt.legend()
plt.tight_layout()
plt.show()


plt.figure(figsize=(10,6))

sns.scatterplot(
    data=datos_europa,
    x="population",
    y="no2_concentratio",
    hue="country_name",   # Colorear por país
    alpha=0.7
)

plt.xscale("log")  # escalar población en logaritmo para que no quede aplastado
plt.axhline(40, color="red", linestyle="--", label="Límite OMS (40 µg/m³)")

plt.title("Relación entre concentración de NO₂ y población por ciudad (Europa 2010–2022)")
plt.xlabel("Población de la ciudad (escala logarítmica)")
plt.ylabel("Concentración promedio de NO₂ (µg/m³)")
plt.ylim(0, 100)
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left', title="País")
plt.tight_layout()
plt.show()

df_map = datos_europa.copy()
for c in ['no2_concentratio','latitude','longitude']:
    df_map[c] = pd.to_numeric(df_map[c], errors='coerce')
df_map = df_map.dropna(subset=['latitude','longitude'])

#Filtra rangos razonables de NO2 para evitar outliers raros en el mapa
df_map = df_map[(df_map['no2_concentratio'] > 0) & (df_map['no2_concentratio'] < 200)]

# Agrupar por ciudad y calcular métricas
city_analisis = (
    df_map.groupby('city')
          .agg(no2_count=('no2_concentratio','count'),
               no2_mean =('no2_concentratio','mean'),
               no2_std  =('no2_concentratio','std'),
               latitude =('latitude','first'),
               longitude=('longitude','first'),
               country  =('country_name','first'))
          .round(3)
          .reset_index()
)



# Tamaño mínimo de burbuja para que todas se vean
city_analisis['size'] = np.clip(city_analisis['no2_mean'], 6, 40)

fig = px.scatter_mapbox(
    city_analisis,
    lat='latitude', lon='longitude',
    size='size',                # tamaño según promedio
    color='no2_mean',           # color según promedio
    hover_name='city',
    hover_data={
        'country': True,
        'no2_mean': ':.1f',
        'no2_count': True,
        'no2_std': ':.1f'
    },
    color_continuous_scale='YlOrRd',
    range_color=(0, 60),        # escala útil para NO2
    size_max=40,
    zoom=4,
    center={'lat': 54, 'lon': 15},   # centro aproximado de Europa
    mapbox_style='open-street-map',
    title='Concentración promedio de NO₂ por ciudad (Europa 2010–2022)'
)

fig.update_coloraxes(colorbar_title='NO₂ (µg/m³)')
fig.update_layout(height=600)
fig.show()