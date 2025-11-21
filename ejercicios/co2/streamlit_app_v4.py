import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Dashboard CO2", layout="wide")

st.title("🌍 Dashboard Global de Emisiones de CO₂")
st.markdown("Visualización interactiva de emisiones históricas, tendencias y responsabilidad por regiones.")

# --- 2. CARGA DE DATOS CON RUTAS RELATIVAS SEGURAS ---
@st.cache_data
def load_data():
    # Obtener la ruta del directorio donde está ESTE script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir rutas absolutas a los datos
    shp_path = os.path.join(script_dir, '50m_cultural', 'ne_50m_admin_0_countries.shp')
    csv_path = os.path.join(script_dir, 'emissions_per_country', 'annual-co2-emissions-per-country.csv')

    # Verificar si existen (para dar un error claro si no)
    if not os.path.exists(shp_path):
        st.error(f"❌ No se encontró el archivo: {shp_path}")
        st.stop()
    if not os.path.exists(csv_path):
        st.error(f"❌ No se encontró el archivo: {csv_path}")
        st.stop()

    # A) Cargar Mapa
    world = gpd.read_file(shp_path)
    world = world.rename(columns={'ISO_A3': 'code'})
    world['code'] = world['code'].str.upper()
    
    # B) Cargar Emisiones
    df = pd.read_csv(csv_path)
    df = df.rename(columns={'Entity': 'country', 'Code': 'code', 'Year': 'year'})
    df['code'] = df['code'].str.upper()
    
    # Filtrar códigos válidos
    df = df[df['code'].str.len() == 3]
    # Renombrar columna de valor (asumimos que es la que no es country/code/year)
    value_col = [c for c in df.columns if c not in ['country', 'code', 'year']][0]
    df = df.rename(columns={value_col: 'co2'})

    # C) Unir datos extra (Continente y Población) del mapa al dataframe
    world_info = world[['code', 'CONTINENT', 'POP_EST', 'geometry']].drop_duplicates(subset='code')
    # Para el mapa necesitamos el geojson, pero streamlit prefiere que lo manejemos separado o en el gpd
    # Hacemos el merge para tener 'CONTINENT' en el df principal
    df_extended = df.merge(world_info[['code', 'CONTINENT', 'POP_EST']], on='code', how='left')

    return world_info, df_extended

# Ejecutar carga
try:
    world_master, df = load_data()
except Exception as e:
    st.error(f"Error crítico al cargar datos: {e}")
    st.stop()

# Preparamos el GeoJSON para Plotly (solo una vez)
geojson_world = world_master.set_index('code')['geometry'].__geo_interface__

# --- 3. SIDEBAR: FILTROS GLOBALES ---
st.sidebar.header("🎛️ Panel de Control")

# --- SECCIÓN 1: MAPA MUNDIAL ---
st.header("1. Mapa de Emisiones Anuales")
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### Configuración del Mapa")
    year_map = st.slider("📅 Año:", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=2020)
    proj_map = st.selectbox("🌍 Proyección:", ['natural earth', 'orthographic', 'mercator', 'equirectangular'])
    
    # Filtro de datos para el mapa
    df_map = df[df['year'] == year_map]

with col2:
    if not df_map.empty:
        fig_map = px.choropleth(
            df_map,
            geojson=geojson_world,
            locations='code',
            color='co2',
            hover_name='country',
            projection=proj_map,
            color_continuous_scale='Reds',
            range_color=[0, df['co2'].max()], # Escala fija para comparar años
            title=f'Emisiones de CO₂ en {year_map}'
        )
        fig_map.update_geos(fitbounds="locations", visible=False, showcountries=True, countrycolor="#d0d0d0")
        fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning(f"No hay datos para el año {year_map}")

st.divider()

# --- SECCIÓN 2: TENDENCIAS (LÍNEAS) ---
st.header("2. Tendencias Históricas")
st.markdown("Compara la evolución de emisiones entre países.")

# Widgets específicos
top_countries = ['China', 'United States', 'India', 'United Kingdom', 'Germany', 'Brazil']
avail_countries = sorted(df['country'].unique())
valid_default = [c for c in top_countries if c in avail_countries]

sel_paises = st.multiselect("Selecciona Países:", avail_countries, default=valid_default)
rango_anios = st.slider("Rango de Años:", 
                        min_value=int(df['year'].min()), 
                        max_value=int(df['year'].max()), 
                        value=(1900, 2024))

if sel_paises:
    mask_pais = df['country'].isin(sel_paises)
    mask_anio = (df['year'] >= rango_anios[0]) & (df['year'] <= rango_anios[1])
    df_trend = df[mask_pais & mask_anio].sort_values('year')
    
    fig_trend = px.line(
        df_trend, x='year', y='co2', color='country',
        title='📈 Evolución temporal', template='plotly_white'
    )
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("Selecciona al menos un país para ver la gráfica.")

st.divider()

# --- SECCIÓN 3: REGIONES (ÁREA APILADA) ---
st.header("3. Emisiones por Región")

lista_continentes = sorted([c for c in df['CONTINENT'].dropna().unique()])
sel_regiones = st.multiselect("Selecciona Regiones:", lista_continentes, default=lista_continentes)

if sel_regiones:
    mask_reg = df['CONTINENT'].isin(sel_regiones)
    df_reg = df[mask_reg].groupby(['year', 'CONTINENT'])['co2'].sum().reset_index().sort_values('year')
    
    fig_area = px.area(
        df_reg, x='year', y='co2', color='CONTINENT',
        title='🏭 Composición por Región', template='plotly_white'
    )
    st.plotly_chart(fig_area, use_container_width=True)

st.divider()

# --- SECCIÓN 4: TREEMAP (RESPONSABILIDAD HISTÓRICA) ---
st.header("4. Responsabilidad Histórica (Acumulada)")
st.markdown("¿Quién ha emitido más CO₂ en total hasta la fecha seleccionada?")

year_limit = st.slider("Acumulado hasta el año:", 1900, 2024, 2024)
sel_reg_tree = st.multiselect("Filtrar Regiones (Treemap):", lista_continentes, default=lista_continentes, key="tree_filter")

if sel_reg_tree:
    mask_tree = (df['year'] <= year_limit) & (df['CONTINENT'].isin(sel_reg_tree))
    df_tree = df[mask_tree].groupby(['CONTINENT', 'country'])['co2'].sum().reset_index()
    df_tree = df_tree[df_tree['co2'] > 0] # Eliminar ceros
    
    fig_tree = px.treemap(
        df_tree,
        path=[px.Constant("Total"), 'CONTINENT', 'country'],
        values='co2',
        color='CONTINENT',
        title=f'🏛️ Emisiones Totales (1750 - {year_limit})'
    )
    fig_tree.update_traces(textinfo="label+percent root", root_color="lightgrey")
    st.plotly_chart(fig_tree, use_container_width=True)
