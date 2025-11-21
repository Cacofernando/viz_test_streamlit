# %%
import geopandas as gpd
import pandas as pd
import plotly.express as px

# %%
# cargar shapefile natural earth
shp_path = '50m_cultural/ne_50m_admin_0_countries.shp'
world = gpd.read_file(shp_path)

# estandarizar columna iso3
world = world.rename(columns={'ISO_A3': 'code'})
world['code'] = world['code'].str.upper()

# cargar emisiones
df = pd.read_csv('emissions_per_country/annual-co2-emissions-per-country.csv')
df = df.rename(columns={'Entity': 'country', 'Code': 'code', 'Year': 'year'})
df['code'] = df['code'].str.upper()

# filtrar a códigos iso válidos
df = df[df['code'].str.len() == 3]

# quedarnos con la columna de emisiones
value_col = [c for c in df.columns if c not in ['country', 'code', 'year']]
df = df.rename(columns={value_col[0]: 'co2'})
df

# %%
# maestro de países: una sola fila por code, como base para todos los años
world_master = (
    world[['code', 'NAME', 'geometry']]
    .drop_duplicates(subset=['code'])
    .rename(columns={'NAME': 'country'})
    .set_index('code')
)

# geojson fijo indexado por code (iso3)
geojson_world = world_master['geometry'].__geo_interface__
geojson_world

# %%
world_master.crs

# %%
def make_co2_map(df_co2, year):
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
        title_text=f'CO₂ emissions by country in {year}',
        title_x=0.5,
        width=900,
        height=600
    )

    return fig

# %%
fig_1751 = make_co2_map(df, 1751)
fig_1751.show()

fig_1851 = make_co2_map(df, 1851)
fig_1851.show()

fig_1951 = make_co2_map(df, 1951)
fig_1951.show()

fig_2024 = make_co2_map(df, 2024)
fig_2024.show()

# %% [markdown]
# ### **2. adaptar y extender el código base de streamlit**

# %%
# Importación de Librerías
!pip install ipywidgets --quiet
import ipywidgets as widgets
from IPython.display import display, clear_output
import plotly.express as px

# %%
# --- 1. CONFIGURACIÓN DE CONTROLES (SIDEBAR) ---

# Título del sidebar
lbl_titulo = widgets.HTML("<h2>🎛️ Panel de Control</h2>")

# Selector de Año (Slider)
slider_year = widgets.IntSlider(
    value=2020,
    min=df['year'].min(),
    max=df['year'].max(),
    step=1,
    description='📅 Año:',
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='95%')
)

# Selector de Proyección (Tipo de vista)
dd_projection = widgets.Dropdown(
    options=['natural earth', 'orthographic', 'mercator', 'equirectangular'],
    value='natural earth',
    description='🌍 Proyección:',
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='95%')
)

# Selector de Escala de Color
dd_color = widgets.Dropdown(
    options=['Reds', 'Plasma', 'Viridis', 'Magma', 'Turbo'],
    value='Reds',
    description='🎨 Colores:',
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='95%')
)

# Filtro: Mínimo de emisiones (para ocultar países con poco CO2)
slider_min_co2 = widgets.FloatLogSlider(
    value=0,
    base=10,
    min=0, # max se ajustará dinámicamente si quisieras, aquí fijo por simplicidad
    max=4, # 10^4 = 10,000 Mt
    step=0.1,
    description='🏭 Min CO₂ (Mt):',
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='95%')
)

# Botón de Reset (opcional, para limpiar filtros)
btn_reset = widgets.Button(
    description='Restablecer Filtros',
    icon='refresh',
    layout=widgets.Layout(width='95%')
)

# Agrupamos todo en una "Caja Vertical" (VBox) para simular el Sidebar
# Le damos un borde y ancho fijo para que parezca una barra lateral
sidebar = widgets.VBox(
    [lbl_titulo, slider_year, dd_projection, dd_color, widgets.HTML("<hr>"), slider_min_co2, btn_reset],
    layout=widgets.Layout(width='300px', border='1px solid #ddd', padding='10px', margin='0 20px 0 0')
)

# --- 2. ÁREA DE VISUALIZACIÓN (MAIN) ---

out_map = widgets.Output()
main_area = widgets.VBox([out_map])

# --- 3. LÓGICA DE ACTUALIZACIÓN ---

def plot_map(change=None):
    # Obtenemos valores actuales de los widgets
    year = slider_year.value
    proj = dd_projection.value
    color_scale = dd_color.value
    min_co2 = slider_min_co2.value
    
    # Limpiamos el output anterior
    with out_map:
        clear_output(wait=True)
        
        # A. FILTRADO DE DATOS
        # Primero por año
        df_year = df[df['year'] == year].copy()
        
        # Verificación 1: ¿Hay datos para este año?
        if df_year.empty:
            display(widgets.HTML(f"<h3 style='color: orange;'>⚠️ No hay registros de emisiones para el año {year}.</h3>"))
            return

        # Segundo, aplicamos filtro de emisiones mínimas
        df_filtered = df_year[df_year['co2'] >= min_co2]
        
        # Verificación 2: ¿Quedan países tras el filtro?
        if df_filtered.empty:
            display(widgets.HTML(
                f"<h3 style='color: #666;'>ℹ️ Hay datos en {year}, pero ningún país supera las {min_co2:.1f} Mt de CO₂.</h3>"
                "<p>Intenta bajar el filtro de 'Min CO₂'.</p>"
            ))
            return

        # B. GENERACIÓN DEL MAPA
        # Usamos un try-except por seguridad ante errores de Plotly
        try:
            # Unimos con el maestro para tener geometrías (como en tu función original)
            # Nota: Para mejor performance en ipywidgets, a veces es mejor pasar el geojson directo a px.choropleth
            # sin hacer el join costoso si ya tienes 'code' en df. 
            # Usaremos tu lógica de geojson que es eficiente.
            
            fig = px.choropleth(
                df_filtered,
                geojson=geojson_world,
                locations='code',
                color='co2',
                hover_name='country',
                projection=proj,
                color_continuous_scale=color_scale,
                # Mantenemos rango fijo visualmente basado en el año actual para ver contraste local
                # O puedes fijarlo globalmente con range_color=[0, df['co2'].max()]
                range_color=[0, df_filtered['co2'].max()], 
                title=f'Emisiones de CO₂ en {year}'
            )
            
            # Ajustes visuales (fondo gris para países sin datos)
            fig.update_geos(
                fitbounds="locations", 
                visible=False,
                showcountries=True, countrycolor="#e0e0e0",
                showland=True, landcolor="#eeeeee"
            )
            
            fig.update_layout(
                margin={"r":0,"t":50,"l":0,"b":0},
                width=800, 
                height=600
            )
            
            fig.show()
            
        except Exception as e:
            display(widgets.HTML(f"<h3 style='color: red;'>Error al generar el gráfico: {str(e)}</h3>"))

# Conectar los controles a la función de actualización
slider_year.observe(plot_map, names='value')
dd_projection.observe(plot_map, names='value')
dd_color.observe(plot_map, names='value')
slider_min_co2.observe(plot_map, names='value')

# Lógica del botón reset
def reset_filters(b):
    slider_min_co2.value = 0
    dd_projection.value = 'natural earth'
    dd_color.value = 'Reds'
    # El cambio de valor disparará automáticamente el observe
btn_reset.on_click(reset_filters)

# --- 4. LAYOUT FINAL Y EJECUCIÓN ---

# Contenedor principal: Sidebar a la izquierda, Mapa a la derecha
app_layout = widgets.HBox([sidebar, main_area])

# Inicializar
plot_map()
display(app_layout)

# %% [markdown]
# ### **3. recrear (o adaptar críticamente) visualizaciones de CO₂ de Our World In Data**

# %%
# 1. Extraemos Continente y Población del shapefile 'world' que cargaste al inicio
# (Asumimos que usas Natural Earth, que suele tener columnas 'CONTINENT' y 'POP_EST')
world_info = world[['code', 'CONTINENT', 'POP_EST']].drop_duplicates(subset='code')

# 2. Unimos esa info a tu dataframe de emisiones
df_extended = df.merge(world_info, on='code', how='left')

# 3. Calculamos emisiones acumuladas por país (para la gráfica histórica)
df_extended['co2_cumulative'] = df_extended.groupby('code')['co2'].cumsum()

# 4. Calculamos per cápita (Nota: Usamos la población actual del mapa como referencia aproximada)
# Si tus datos de CO2 están en Toneladas, la división es directa.
df_extended['co2_per_capita'] = df_extended['co2'] / df_extended['POP_EST']

df_extended.head()

# %% [markdown]
# **Gráfica 1: Tendencias Temporales (Líneas)**
# 
# Ésta gráfica nos permite tener una foto de las emisiones por país de un año en particular, sobre todo si un país está aumentando o disminuyendo la curva de emisiones, es decir, la historia completa de emisiones de los países deseados.

# %%
# --- VALORES POR DEFECTO (Para usarlos al resetear) ---
DEFAULT_PAISES = ['China', 'United States', 'India', 'United Kingdom', 'Germany', 'Brazil']


# Validamos que existan
all_countries = sorted(df_extended['country'].unique())
paises_validos_default = [c for c in DEFAULT_PAISES if c in all_countries]
min_year_data, max_year_data = df_extended['year'].min(), df_extended['year'].max()
DEFAULT_RANGO = (1900, max_year_data)

# --- WIDGETS ---
sel_paises = widgets.SelectMultiple(
    options=all_countries,
    value=paises_validos_default,
    description='Países:',
    rows=10,
    layout=widgets.Layout(width='98%')
)

slider_periodo = widgets.IntRangeSlider(
    value=DEFAULT_RANGO,
    min=min_year_data, max=max_year_data,
    step=1,
    description='Periodo:',
    continuous_update=False,
    layout=widgets.Layout(width='98%')
)

# BOTÓN DE RESET
btn_reset = widgets.Button(
    description='Restablecer Filtros',
    icon='refresh',
    button_style='warning', # Color naranja para diferenciarlo
    layout=widgets.Layout(width='98%')
)

# --- LAYOUT ---
panel_lateral = widgets.VBox(
    [
        widgets.HTML("<h3>🛠️ Controles</h3>"),
        slider_periodo,
        widgets.HTML("<hr>"),
        btn_reset, # Agregamos el botón aquí
        widgets.Label("Selecciona países:"),
        sel_paises
    ],
    layout=widgets.Layout(width='250px', padding='10px', border='1px solid #ddd', margin='0 20px 0 0')
)

out_grafica = widgets.Output()

# --- LÓGICA ---
def actualizar_grafica(change=None):
    seleccion = sel_paises.value
    rango = slider_periodo.value
    
    with out_grafica:
        clear_output(wait=True)
        if not seleccion:
            display(widgets.HTML("⚠️ Selecciona al menos un país."))
            return
        
        mask_pais = df_extended['country'].isin(seleccion)
        mask_anio = (df_extended['year'] >= rango[0]) & (df_extended['year'] <= rango[1])
        df_plot = df_extended[mask_pais & mask_anio].sort_values('year')
        
        if df_plot.empty: return

        fig = px.line(
            df_plot, x='year', y='co2', color='country',
            title='📈 Tendencia Histórica de Emisiones',
            template='plotly_white', height=500
        )
        fig.update_xaxes(rangeslider_visible=True)
        fig.show()

# FUNCIÓN DE RESET
def reset_controls(b):
    sel_paises.value = paises_validos_default
    slider_periodo.value = DEFAULT_RANGO
    # Al cambiar los valores, 'actualizar_grafica' se dispara sola gracias a .observe

# CONEXIONES
sel_paises.observe(actualizar_grafica, names='value')
slider_periodo.observe(actualizar_grafica, names='value')
btn_reset.on_click(reset_controls)

# EJECUCIÓN
actualizar_grafica()
display(widgets.HBox([panel_lateral, out_grafica]))

# %% [markdown]
# **2. Emisiones de CO₂ por Región**
# 
# Nos permite visualizar si el problema de la emisión se concentra en ciertas zonas
# 
# 

# %%
# --- DEFAULTS ---
lista_continentes = sorted([c for c in df_extended['CONTINENT'].unique() if isinstance(c, str)])
DEFAULT_REGIONES = lista_continentes # Todas
DEFAULT_RANGO_REG = (1900, df_extended['year'].max())

# --- WIDGETS ---
sel_regiones = widgets.SelectMultiple(
    options=lista_continentes,
    value=DEFAULT_REGIONES,
    description='Regiones:',
    rows=len(lista_continentes),
    layout=widgets.Layout(width='95%')
)

slider_rango_region = widgets.IntRangeSlider(
    value=DEFAULT_RANGO_REG,
    min=df_extended['year'].min(), max=df_extended['year'].max(),
    description='Periodo:',
    continuous_update=False,
    layout=widgets.Layout(width='95%')
)

btn_reset_reg = widgets.Button(
    description='Restablecer Vista',
    icon='refresh',
    button_style='warning',
    layout=widgets.Layout(width='95%')
)

# --- LAYOUT ---
panel_control = widgets.VBox(
    [
        widgets.HTML("<h3>🌍 Filtros Región</h3>"),
        slider_rango_region,
        widgets.HTML("<hr>"),
        btn_reset_reg,
        widgets.Label("Regiones:"),
        sel_regiones
    ],
    layout=widgets.Layout(width='300px', padding='10px', border='1px solid #ddd', margin='0 20px 0 0')
)

out_region = widgets.Output()

# --- LÓGICA ---
def update_region_chart(change=None):
    seleccion = sel_regiones.value
    rango = slider_rango_region.value
    
    with out_region:
        clear_output(wait=True)
        if not seleccion: return
        
        mask = df_extended['CONTINENT'].isin(seleccion) & \
               (df_extended['year'] >= rango[0]) & (df_extended['year'] <= rango[1])
        df_filtered = df_extended[mask]
        
        if df_filtered.empty: return

        df_grouped = df_filtered.groupby(['year', 'CONTINENT'])['co2'].sum().reset_index().sort_values('year')

        fig = px.area(
            df_grouped, x='year', y='co2', color='CONTINENT',
            title='🏭 Emisiones por Región (Apilado)',
            template='plotly_white', height=500
        )
        fig.show()

# RESET
def reset_regions(b):
    sel_regiones.value = DEFAULT_REGIONES
    slider_rango_region.value = DEFAULT_RANGO_REG

sel_regiones.observe(update_region_chart, names='value')
slider_rango_region.observe(update_region_chart, names='value')
btn_reset_reg.on_click(reset_regions)

update_region_chart()
display(widgets.HBox([panel_control, out_region]))

# %% [markdown]
# **3. Responsabilidad Histórica (Treemap)**
# 
# Visualización de Treemap de acuerdo a quién ha llenado la atmosfera de CO2, desde el inicio de la revolución industrial

# %%
# --- DEFAULTS ---
lista_continentes = sorted([c for c in df_extended['CONTINENT'].unique() if isinstance(c, str)])
DEFAULT_REGIONES_TREE = lista_continentes
max_year_global = df_extended['year'].max()
DEFAULT_ANIO_LIMITE = max_year_global

# --- WIDGETS ---
sel_regiones_tree = widgets.SelectMultiple(
    options=lista_continentes,
    value=DEFAULT_REGIONES_TREE,
    description='Regiones:',
    rows=len(lista_continentes),
    layout=widgets.Layout(width='95%')
)

slider_anio_limite = widgets.IntSlider(
    value=DEFAULT_ANIO_LIMITE,
    min=1900, max=max_year_global,
    description='Hasta año:',
    continuous_update=False,
    layout=widgets.Layout(width='95%')
)

btn_reset_tree = widgets.Button(
    description='Restablecer Todo',
    icon='refresh',
    button_style='warning',
    layout=widgets.Layout(width='95%')
)

# --- LAYOUT ---
panel_tree = widgets.VBox(
    [
        widgets.HTML("<h3>🏛️ Filtros</h3>"),
        slider_anio_limite,
        widgets.HTML("<hr>"),
        btn_reset_tree,
        widgets.Label("Regiones:"),
        sel_regiones_tree
    ],
    layout=widgets.Layout(width='300px', padding='10px', border='1px solid #ddd', margin='0 20px 0 0')
)

out_treemap = widgets.Output()

# --- LÓGICA ---
def update_treemap(change=None):
    seleccion = sel_regiones_tree.value
    anio = slider_anio_limite.value
    
    with out_treemap:
        clear_output(wait=True)
        if not seleccion: return
        
        mask = (df_extended['year'] <= anio) & (df_extended['CONTINENT'].isin(seleccion))
        df_filtered = df_extended[mask]
        
        if df_filtered.empty: return

        df_acum = df_filtered.groupby(['CONTINENT', 'country'])['co2'].sum().reset_index()
        df_acum = df_acum[df_acum['co2'] > 0]

        fig = px.treemap(
            df_acum,
            path=[px.Constant("Total"), 'CONTINENT', 'country'],
            values='co2',
            title=f'🏛️ Proporción Histórica (1750 - {anio})',
            color='CONTINENT',
            template='plotly_white', height=600
        )
        fig.update_traces(textinfo="label+percent root", root_color="lightgrey")
        fig.show()

# RESET
def reset_treemap(b):
    sel_regiones_tree.value = DEFAULT_REGIONES_TREE
    slider_anio_limite.value = DEFAULT_ANIO_LIMITE

sel_regiones_tree.observe(update_treemap, names='value')
slider_anio_limite.observe(update_treemap, names='value')
btn_reset_tree.on_click(reset_treemap)

update_treemap()
display(widgets.HBox([panel_tree, out_treemap]))

# %%



