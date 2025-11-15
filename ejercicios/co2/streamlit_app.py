import os

import geopandas as gpd
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================
# configuración de la app
# ============================
st.set_page_config(
    page_title='mapa de emisiones de co₂',
    layout='wide'
)

BASE_DIR = os.path.dirname(__file__)
SHP_PATH = os.path.join(BASE_DIR, '50m_cultural', 'ne_50m_admin_0_countries.shp')
CSV_PATH = os.path.join(BASE_DIR, 'emissions_per_country', 'annual-co2-emissions-per-country.csv')


# ============================
# carga y preparación de datos
# ============================
@st.cache_data
def load_world(shp_path: str):
    """
    carga el shapefile de países y construye:
    - world_master: maestro de países indexado por iso3
    - geojson_world: geometría en formato geojson para plotly
    """
    if not os.path.exists(shp_path):
        raise FileNotFoundError(f'no se encontró el shapefile: {shp_path}')

    world = gpd.read_file(shp_path)

    # estandarizar columna iso3
    world = world.rename(columns={'ISO_A3': 'code'})
    world['code'] = world['code'].str.upper()

    # maestro de países: una sola fila por code
    world_master = (
        world[['code', 'NAME', 'geometry']]
        .drop_duplicates(subset=['code'])
        .rename(columns={'NAME': 'country'})
        .set_index('code')
    )

    geojson_world = world_master['geometry'].__geo_interface__

    return world_master, geojson_world


@st.cache_data
def load_emissions(csv_path: str) -> pd.DataFrame:
    """
    carga el csv de emisiones y lo deja listo para usar
    con columnas: country, code, year, co2
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f'no se encontró el csv de emisiones: {csv_path}')

    df = pd.read_csv(csv_path)

    df = df.rename(columns={'Entity': 'country', 'Code': 'code', 'Year': 'year'})
    df['code'] = df['code'].str.upper()

    # filtrar a códigos iso válidos
    df = df[df['code'].str.len() == 3]

    # quedarnos con la columna de emisiones (asumimos una métrica principal)
    value_col = [c for c in df.columns if c not in ['country', 'code', 'year']]
    if not value_col:
        raise ValueError('no se encontró ninguna columna de emisiones distinta de country/code/year')

    df = df.rename(columns={value_col[0]: 'co2'})

    return df[['country', 'code', 'year', 'co2']]


# ============================
# lógica de visualización
# ============================
def make_co2_map(df_co2: pd.DataFrame,
                 world_master: gpd.GeoDataFrame,
                 geojson_world: dict,
                 year: int):
    """
    genera el mapa de emisiones de co₂ por país para un año dado.
    respeta tu lógica original, pero preparado para streamlit.
    """
    # emisiones del año seleccionado, agregadas por país
    co2_year = (
        df_co2[df_co2['year'] == year][['code', 'co2']]
        .groupby('code', as_index=False)
        .agg({'co2': 'sum'})
        .set_index('code')
    )

    # unir al maestro: aquí nunca se pierden países
    world_y = world_master.join(co2_year, how='left')

    # países con dato vs sin dato
    g_with = world_y[world_y['co2'].notna()].reset_index()
    g_no = world_y[world_y['co2'].isna()].reset_index()

    # capa 1: países con dato → escala continua
    fig = px.choropleth(
        g_with,
        geojson=geojson_world,
        locations='code',            # usa el iso3
        color='co2',
        hover_name='country',
        projection='natural earth',
        color_continuous_scale='Reds'
    )

    # capa 2: países sin dato → gris, sin leyenda
    if not g_no.empty:
        fig_grey = px.choropleth(
            g_no,
            geojson=geojson_world,
            locations='code',
            color_discrete_sequence=['#d0d0d0'],
            hover_name='country',
            projection='natural earth'
        )
        for trace in fig_grey.data:
            trace.showlegend = False
            fig.add_trace(trace)

    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(
        title_text=f'emisiones de co₂ por país en {year}',
        title_x=0.5,
        height=600
    )

    return fig


# ============================
# app principal
# ============================
def main():
    st.title('mapa interactivo de emisiones de co₂')
    st.markdown(
        """
        esta aplicación muestra las emisiones anuales de co₂ por país usando datos de our world in data.
        puedes explorar distintos años y comparar cómo cambia el mapa a lo largo del tiempo.
        """
    )

    # cargar datos
    world_master, geojson_world = load_world(SHP_PATH)
    df_co2 = load_emissions(CSV_PATH)

    # panel lateral de control
    st.sidebar.header('controles')

    min_year = int(df_co2['year'].min())
    max_year = int(df_co2['year'].max())

    # años que usabas en el notebook como casos de estudio
    años_destacados = [1751, 1851, 1951, 2024]
    años_destacados = [a for a in años_destacados if min_year <= a <= max_year]

    preset = st.sidebar.selectbox(
        'años destacados',
        options=['ninguno'] + [str(a) for a in años_destacados],
        index=0
    )

    if preset != 'ninguno':
        year_default = int(preset)
    else:
        year_default = max_year

    year = st.sidebar.slider(
        'año',
        min_value=min_year,
        max_value=max_year,
        value=year_default,
        step=1
    )

    st.sidebar.markdown(
        """
        usa el slider para moverte año a año y el selector de
        años destacados para saltar rápidamente a hitos históricos.
        """
    )

    # generar mapa
    if year < min_year or year > max_year:
        st.warning(f'no hay datos para el año {year}. el rango válido es {min_year}–{max_year}.')
        return

    fig = make_co2_map(df_co2, world_master, geojson_world, year)
    st.plotly_chart(fig, use_container_width=True)

    # tabla resumen opcional
    st.markdown('---')
    st.subheader('tabla de emisiones por país en el año seleccionado')

    df_year = (
        df_co2[df_co2['year'] == year][['country', 'code', 'co2']]
        .groupby(['country', 'code'], as_index=False)
        .agg({'co2': 'sum'})
        .sort_values('co2', ascending=False)
    )

    st.dataframe(df_year, use_container_width=True)


if __name__ == '__main__':
    main()
