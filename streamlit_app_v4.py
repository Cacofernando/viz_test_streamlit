import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Global de Emisiones CO₂",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título Principal
st.title("🌍 Dashboard Global de Emisiones de CO₂")

# --- 2. CARGA DE DATOS (Actualizada a carpeta 'Data') ---
@st.cache_data
def load_data():
    # Obtener la ruta del directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # --- RUTAS ACTUALIZADAS A LA CARPETA 'Data' ---
    shp_path = os.path.join(script_dir, 'Data', 'ne_50m_admin_0_countries.shp')
    csv_path = os.path.join(script_dir, 'Data', 'annual-co2-emissions-per-country.csv')

    # Validar existencia
    if not os.path.exists(shp_path):
        st.error(f"❌ Archivo Shapefile no encontrado en: {shp_path}")
        st.info("Asegúrate de que los archivos .shp, .shx y .dbf estén dentro de la carpeta 'Data'.")
        st.stop()
    if not os.path.exists(csv_path):
        st.error(f"❌ Archivo CSV no encontrado en: {csv_path}")
        st.stop()

    # Cargar Mapa
    try:
        world = gpd.read_file(shp_path)
    except Exception as e:
        st.error(f"Error leyendo el Shapefile. Verifica que .shx y .dbf estén en la misma carpeta. Detalle: {e}")
        st.stop()

    world = world.rename(columns={'ISO_A3': 'code'})
    world['code'] = world['code'].str.upper()
    
    # Cargar Datos CSV
    df = pd.read_csv(csv_path)
    df = df.rename(columns={'Entity': 'country', 'Code': 'code', 'Year': 'year'})
    df['code'] = df['code'].str.upper()
    df = df[df['code'].str.len() == 3] # Filtrar códigos válidos
    
    # Identificar columna de valor
    value_col = [c for c in df.columns if c not in ['country', 'code', 'year']][0]
    df = df.rename(columns={value_col: 'co2'})

    # Merge para obtener Continente y Población en el DataFrame principal
    world_info = world[['code', 'CONTINENT', 'POP_EST', 'geometry']].drop_duplicates(subset='code')
    df_extended = df.merge(world_info[['code', 'CONTINENT', 'POP_EST']], on='code', how='left')

    return world_info, df_extended

# Ejecutar carga
try:
    world_master, df = load_data()
    # GeoJSON para Plotly
    geojson_world = world_master.set_index('code')['geometry'].__geo_interface__
except Exception as e:
    st.error(f"Error inesperado cargando datos: {e}")
    st.stop()

# --- 3. SIDEBAR GLOBAL ---
with st.sidebar:
    st.header("🎛️ Configuración")
    st.info("Usa los filtros en cada sección para personalizar la vista.")
    
    # Botón de Reset Global
    if st.button("🔄 Restablecer Todo", type="primary"):
        st.rerun()
    
    st.divider()
    st.markdown("Desarrollado con Streamlit y Plotly.")

# --- 4. ESTRUCTURA DE PESTAÑAS ---
tab_dashboard, tab_info = st.tabs(["📊 Dashboard Visual", "ℹ️ Metodología y Datos"])

# ==============================================================================
# PESTAÑA 1: DASHBOARD
# ==============================================================================
with tab_dashboard:
    
    # --- SECCIÓN A: MAPA MUNDIAL ---
    st.header("1. Mapa de Emisiones Anuales")
    col_map_ctrl, col_map_viz = st.columns([1, 3])

    with col_map_ctrl:
        st.subheader("Filtros")
        year_map = st.slider("📅 Año:", 
                             min_value=int(df['year'].min()), 
                             max_value=int(df['year'].max()), 
                             value=2020,
                             key="slider_mapa")
        
        proj_map = st.selectbox("🌍 Proyección:", 
                                ['natural earth', 'orthographic', 'mercator', 'equirectangular'],
                                key="proj_mapa")
        
        df_map = df[df['year'] == year_map]

    with col_map_viz:
        if not df_map.empty:
            fig_map = px.choropleth(
                df_map,
                geojson=geojson_world,
                locations='code',
                color='co2',
                hover_name='country',
                projection=proj_map,
                color_continuous_scale='Reds',
                range_color=[0, df['co2'].max()], # Escala fija
                title=f'Emisiones de CO₂ en {year_map} (Mt)'
            )
            fig_map.update_geos(fitbounds="locations", visible=False, showcountries=True, countrycolor="#d0d0d0")
            fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=500)
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning(f"No hay datos registrados para el año {year_map}.")

    st.divider()

    # --- SECCIÓN B: TENDENCIAS Y REGIONES ---
    col_trend, col_region = st.columns(2)

    # GRÁFICA 2: TENDENCIAS (LÍNEAS)
    with col_trend:
        st.header("2. Tendencias Históricas")
        
        top_countries = ['China', 'United States', 'India', 'United Kingdom', 'Germany', 'Brazil']
        avail_countries = sorted(df['country'].unique())
        default_paises = [c for c in top_countries if c in avail_countries]
        
        sel_paises = st.multiselect("Seleccionar Países:", avail_countries, default=default_paises, key="multi_paises")
        
        if sel_paises:
            df_trend = df[df['country'].isin(sel_paises)].sort_values('year')
            fig_trend = px.line(
                df_trend, x='year', y='co2', color='country',
                title='📈 Evolución Temporal', template='plotly_white',
                labels={'co2': 'CO₂ (Ton)', 'year': 'Año'}
            )
            fig_trend.update_layout(legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("Selecciona al menos un país.")

    # GRÁFICA 3: REGIONES (ÁREAS)
    with col_region:
        st.header("3. Emisiones por Región")
        
        lista_continentes = sorted([c for c in df['CONTINENT'].dropna().unique()])
        sel_regiones = st.multiselect("Filtrar Regiones:", lista_continentes, default=lista_continentes, key="multi_regiones")
        
        if sel_regiones:
            mask_reg = df['CONTINENT'].isin(sel_regiones)
            df_reg = df[mask_reg].groupby(['year', 'CONTINENT'])['co2'].sum().reset_index().sort_values('year')
            
            fig_area = px.area(
                df_reg, x='year', y='co2', color='CONTINENT',
                title='🏭 Composición Regional', template='plotly_white',
                labels={'co2': 'Total CO₂', 'year': 'Año'}
            )
            fig_area.update_layout(legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_area, use_container_width=True)
        else:
            st.info("Selecciona al menos una región.")

    st.divider()

    # --- SECCIÓN C: TREEMAP ---
    st.header("4. Responsabilidad Histórica (Acumulada)")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        year_limit = st.slider("Acumulado hasta:", 1900, 2024, 2024, key="slider_tree")
    with c2:
        sel_reg_tree = st.multiselect("Regiones:", lista_continentes, default=lista_continentes, key="multi_tree")

    if sel_reg_tree:
        mask_tree = (df['year'] <= year_limit) & (df['CONTINENT'].isin(sel_reg_tree))
        df_tree = df[mask_tree].groupby(['CONTINENT', 'country'])['co2'].sum().reset_index()
        df_tree = df_tree[df_tree['co2'] > 0]
        
        fig_tree = px.treemap(
            df_tree,
            path=[px.Constant("Total Seleccionado"), 'CONTINENT', 'country'],
            values='co2',
            color='CONTINENT',
            title=f'🏛️ Proporción de Emisiones Totales (1750 - {year_limit})'
        )
        fig_tree.update_traces(textinfo="label+percent root", root_color="lightgrey")
        st.plotly_chart(fig_tree, use_container_width=True)
    else:
        st.warning("Selecciona regiones para ver el gráfico.")


# ==============================================================================
# PESTAÑA 2: INFORMACIÓN Y METODOLOGÍA
# ==============================================================================
with tab_info:
    st.header("ℹ️ Sobre este Proyecto")
    
    st.markdown("""
    Este tablero interactivo permite explorar la evolución histórica de las emisiones de dióxido de carbono (CO₂) 
    a nivel global, regional y nacional. Su objetivo es facilitar la comprensión de las tendencias climáticas mediante visualización de datos.
    """)
    
    st.divider()

    # 1. DATASETS
    st.subheader("📂 1. Fuentes de Datos")
    st.markdown("""
    * **Ubicación de archivos:** Carpeta local `Data/`.
    * **Emisiones de CO₂:** Datos del *Global Carbon Project*, procesados por [Our World in Data](https://ourworldindata.org/co2-emissions).
      * Archivo: `annual-co2-emissions-per-country.csv`
    * **Geometrías:** Fronteras administrativas de [Natural Earth](https://www.naturalearthdata.com/) (1:50m).
      * Archivo: `ne_50m_admin_0_countries.shp`
    """)

    # 2. UNIDADES
    st.subheader("📏 2. Unidades y Periodo")
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("**Unidad:** Toneladas métricas de CO₂ (t).")
    with col_info2:
        st.info(f"**Periodo:** {int(df['year'].min())} - {int(df['year'].max())}.")

    # 3. DISEÑO
    st.subheader("🎨 3. Decisiones de Diseño")
    with st.expander("Ver justificación de diseño", expanded=True):
        st.write("""
        - **Escala de Color Fija:** En el mapa, la escala de rojos se mantiene constante (0 al máximo histórico) para evidenciar el aumento real de emisiones a través de los años.
        - **Agregación Regional:** Se utilizan gráficos de área y treemaps agrupados por continente para facilitar la lectura de tendencias macro-geopolíticas.
        - **Normalización:** En el Treemap, se muestran porcentajes relativos (% root) en lugar de valores absolutos para facilitar la comparación de responsabilidad histórica.
        """)

    # 4. LIMITACIONES
    st.subheader("⚠️ 4. Limitaciones")
    st.warning("""
    - **Datos Históricos:** La cobertura de datos antes de 1900 es limitada para muchos países en desarrollo.
    - **Cambios Territoriales:** Países que ya no existen (ej. URSS) pueden no visualizarse correctamente en el mapa actual.
    - **Alcance:** Los datos reflejan emisiones territoriales, no huella de carbono por consumo (trade-adjusted).
    """)
