# 🌍 Dashboard Global de Emisiones de CO₂

## 📌 Descripción
Aplicación web interactiva desarrollada en **Streamlit** que permite explorar la evolución histórica de las emisiones de dióxido de carbono (CO₂) a nivel global, regional y nacional. Incluye visualizaciones dinámicas basadas en datos de **Our World in Data** y geometrías de **Natural Earth**.

## 🚀 Demo en línea
[Accede a la app aquí](https://viztestapp-fetixpmymkxks3qup4uhpb.streamlit.app)

## 📂 Estructura del repositorio
```
├── streamlit_app_v4.py           # Script principal de la aplicación (Dashboard)
├── requirements.txt              # Lista de dependencias (streamlit, geopandas, plotly, etc.)
├── README.md                     # Documentación del proyecto
└── Data/                         # Directorio principal de datos
    ├── 50m_cultural/             # Subcarpeta con archivos geográficos (Shapefiles)
    │   ├── ne_50m_admin_0_countries.shp  # Geometría (Mapas)
    │   ├── ne_50m_admin_0_countries.shx  # Índice
    │   ├── ne_50m_admin_0_countries.dbf  # Atributos
    │   └── ne_50m_admin_0_countries.prj  # Proyección
    │
    └── emissions_per_country/    # Subcarpeta con datos numéricos
        └── annual-co2-emissions-per-country.csv # Dataset de emisiones (Our World in Data)
```

## 🔍 Fuentes de datos
- **Emisiones CO₂:** [Our World in Data](https://ourworldindata.org/co2-emissions)
- **Geometrías:** [Natural Earth](https://www.naturalearthdata.com/)

## ⚙️ Requisitos
- Python 3.9+
- Librerías:
  - `streamlit`
  - `pandas`
  - `geopandas`
  - `plotly`

Instalación rápida:
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución local
```bash
streamlit run streamlit_app_v4.py
```

## 📊 Visualizaciones incluidas
1. **Mapa mundial interactivo** (slider por año, proyecciones).
2. **Tendencias históricas** por país (líneas).
3. **Composición regional** (área apilada).
4. **Responsabilidad histórica** (treemap acumulado).

## 🧠 Decisiones de diseño
- Escala de color fija en mapa para mostrar evolución real.
- Agregación por continente para análisis macro.
- Treemap con porcentajes relativos para comparación histórica.

## ⚠️ Limitaciones
- Cobertura incompleta antes de 1900.
- Cambios territoriales (ej. URSS) afectan visualización.
- Datos reflejan emisiones territoriales, no consumo ajustado.

---
**Autores:** Juan José Torres, Cristián Vargas, Christian Vásquez, Claudio Ballerini

**Profesor:** Carlos Elías Pérez Pizarro  
**Curso:** Magíster en Data Science – UDD
