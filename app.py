import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title='Panel EDA — vehicles_us.csv', layout='wide')

# Definición de la función de carga de datos con caché


@st.cache_data
def load_data(path):
    """Carga los datos desde la ruta especificada."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f'Error: El archivo {path} no fue encontrado.')
        st.stop()


# Define la ruta del archivo de datos
DATA_PATH = r'C:\Users\damar.hybook-plus\proyecto 7 vehiculos\vehicles_us.csv'
data = load_data(DATA_PATH)

# Encabezado principal usando st.header()
st.header('Análisis Exploratorio del Dataset: vehicles_us')

# Detección y separación de columnas numéricas y categóricas
num_cols = data.select_dtypes(include='number').columns.tolist()
cat_cols = data.select_dtypes(exclude='number').columns.tolist()

if not num_cols:
    st.error('No se encontraron columnas numéricas en el dataset. Asegúrate de que `vehicles_us.csv` contenga datos numéricos para graficar.')
    st.stop()

# Sección para vista previa de datos
with st.expander('Vista previa de datos', expanded=False):
    st.dataframe(data.head(50), use_container_width=True)

st.divider()

# -----------------
# 1. Histograma
# -----------------
st.subheader('Histograma')
col_hist = st.selectbox('Columna numérica para el histograma',
                        options=num_cols, index=0, key='hist_col')
bins = st.slider('Número de barras (bins)', 5, 100, 30)

# Selector de color por categoría
color_hist_by = st.selectbox('Colorear barras por (opcional, columna categórica)',
                             options=['(ninguno)'] + cat_cols,
                             index=0,
                             key='hist_color_by')

# Casilla de verificación para el histograma
hist_checkbox = st.checkbox('Construir histograma',
                            value=False, key='hist_checkbox')

# Generación y visualización del histograma con st.write() y st.plotly_chart()
if hist_checkbox:
    st.write(f'**Creando un histograma para la columna: {col_hist}**')

    # Determinar si se usará color por categoría
    if color_hist_by != '(ninguno)':
        fig_hist = px.histogram(
            data,
            x=col_hist,
            nbins=bins,
            color=color_hist_by,
            title=f'Distribución de {col_hist} (coloreado por {color_hist_by})',
            barmode='overlay'  # Puedes cambiar a 'stack' o 'group' según prefieras
        )
        # Hacer las barras más transparentes para ver superposiciones
        fig_hist.update_traces(opacity=0.75)
    else:
        fig_hist = px.histogram(
            data,
            x=col_hist,
            nbins=bins,
            title=f'Distribución de {col_hist}'
        )

    st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# -----------------
# 2. Gráfico de dispersión (Scatter Plot)
# -----------------
st.subheader('Gráfico de dispersión')

# Determinar selecciones predeterminadas para X e Y
if len(num_cols) >= 2:
    default_x = num_cols[0]
    default_y = num_cols[1]
else:
    default_x = default_y = num_cols[0]

# Encontrar índices para la selección inicial
x_index = num_cols.index(default_x)
y_index = num_cols.index(default_y)
color_index = 0  # (ninguno)

x_scatter = st.selectbox(
    'Eje X (numérico)', options=num_cols, index=x_index, key='scatter_x')
y_scatter = st.selectbox(
    'Eje Y (numérico)', options=num_cols, index=y_index, key='scatter_y')
color_by = st.selectbox('Color por (opcional, columna categórica)', options=[
                        '(ninguno)'] + cat_cols, index=color_index, key='scatter_color')

# Casilla de verificación para el gráfico de dispersión
scatter_checkbox = st.checkbox(
    'Construir gráfico de dispersión', value=False, key='scatter_checkbox')

# Generación y visualización del gráfico de dispersión con st.write() y st.plotly_chart()
if scatter_checkbox:
    st.write(
        f'**Creando un gráfico de dispersión para: {x_scatter} vs {y_scatter}**')

    # Determinar si se usará color
    if color_by != '(ninguno)':
        fig_scatter = px.scatter(
            data,
            x=x_scatter,
            y=y_scatter,
            color=color_by,
            title=f'{x_scatter} vs {y_scatter} (coloreado por {color_by})',
            hover_data=data.columns
        )
    else:
        fig_scatter = px.scatter(
            data,
            x=x_scatter,
            y=y_scatter,
            title=f'{x_scatter} vs {y_scatter}',
            hover_data=data.columns
        )

    st.plotly_chart(fig_scatter, use_container_width=True)
