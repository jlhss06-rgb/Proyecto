import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Leer el conjunto de datos
car_data = pd.read_csv('../Proyecto7/vehicles_us.csv')

# 2. Aplicar la limpieza y depuración de datos sincronizada
# Rellenar 'is_4wd' con 0
car_data['is_4wd'] = car_data['is_4wd'].fillna(0)

# Rellenar 'paint_color' con 'unknown'
car_data['paint_color'] = car_data['paint_color'].fillna('unknown')

# Imputar 'model_year', 'cylinders' y 'odometer' usando la mediana agrupada por 'model'
for col in ['model_year', 'cylinders', 'odometer']:
    car_data[col] = car_data.groupby('model')[col].transform(lambda x: x.fillna(x.median()))

# Si quedan valores nulos residuales, usar la mediana general
for col in ['model_year', 'cylinders', 'odometer']:
    if car_data[col].isnull().any():
        car_data[col] = car_data[col].fillna(car_data[col].median())

# Asegurar tipos de datos correctos
car_data['model_year'] = car_data['model_year'].astype(int)
car_data['cylinders'] = car_data['cylinders'].astype(int)
car_data['is_4wd'] = car_data['is_4wd'].astype(int)

# Encabezado de la aplicación
st.header('Cuadro de Mando de Análisis de Vehículos (Datos Depurados)')

# --- SECCIÓN: VISUALIZACIÓN INTERACTIVA DEL DATAFRAME ---
st.subheader('Explorador de Datos Interactivo')
show_df = st.checkbox('Mostrar datos limpios en una tabla interactiva')
if show_df:
    st.write("Mostrando los primeros 500 registros del conjunto de datos limpio:")
    st.dataframe(car_data.head(500))

# --- SECCIÓN: FILTROS INTERACTIVOS EN LA BARRA LATERAL ---
st.sidebar.header("Filtros de Búsqueda")

# Extraer modelos únicos y permitir al usuario filtrar la marca/modelo
model_list = sorted(car_data['model'].unique())
selected_models = st.sidebar.multiselect('Selecciona uno o varios modelos de vehículos:', model_list, default=model_list[:5])

# Filtrar el DataFrame según la selección del usuario
filtered_data = car_data[car_data['model'].isin(selected_models)]

# --- SECCIÓN 1: Histogramas interactivos con color ---
st.subheader('Histogramas del Conjunto de Datos')

# Elegir columna para colorear el histograma
color_by_hist = st.selectbox('Selecciona una variable para colorear el histograma:', ['condition', 'transmission', 'fuel'])

# Botón para el histograma
if st.button('Construir Histograma'):
    st.write(f'Creando un histograma del odómetro para los modelos seleccionados coloreado por {color_by_hist}')
    fig = px.histogram(filtered_data, x="odometer", color=color_by_hist, barmode='overlay',
                       title=f'Distribución de Odómetro filtrada y coloreada por {color_by_hist}')
    st.plotly_chart(fig, use_container_width=True)

# --- SECCIÓN 2: Gráficos de Dispersión interactivos por marcas ---
st.subheader('Gráficos de Dispersión Interactivos')

# Botón para el gráfico de dispersión
if st.button('Construir Gráfico de Dispersión'):
    st.write('Creando un gráfico de dispersión de Odómetro vs Precio coloreado por modelo')
    fig_scatter = px.scatter(filtered_data, x="odometer", y="price", color="model",
                             title='Relación entre Odómetro y Precio para los Modelos Seleccionados',
                             labels={'odometer': 'Odómetro', 'price': 'Precio', 'model': 'Modelo'})
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- SECCIÓN 3: Casillas de verificación para construir gráficos alternativos ---
st.subheader('Opciones alternativas mediante Casillas de Verificación')

build_histogram = st.checkbox('Mostrar Histograma Interactiva (Vía Checkbox)')
if build_histogram:
    fig = px.histogram(filtered_data, x="odometer", color=color_by_hist,
                       title=f'Histograma del Odómetro coloreado por {color_by_hist}')
    st.plotly_chart(fig, use_container_width=True)

build_scatter = st.checkbox('Mostrar Gráfico de Dispersión Interactivo (Vía Checkbox)')
if build_scatter:
    fig_scatter = px.scatter(filtered_data, x="odometer", y="price", color="model",
                             title='Gráfico de Dispersión coloreado por Modelo (Filtrado)')
    st.plotly_chart(fig_scatter, use_container_width=True)