# Universidad del Desarrollo  
## Magíster en Data Science – Facultad de Ingeniería  
### Asignatura: Visualización de Datos y Storytelling  
**Profesor:** Carlos Elías Pérez Pizarro  
**Tarea Intermedia 1 – Dinámicas Globales de Población**  
**Fecha de entrega:** viernes 7 de noviembre de 2025  
**Modalidad:** Trabajo grupal (3–4 personas)  
**Formato de entrega:** Presentación ppt + carpeta técnica comprimida (.zip)

---

## 🎯 Objetivo general

Aplicar los conceptos de **percepción visual**, **marcas**, **canales** y **efectividad de codificación** para explorar y comunicar hallazgos significativos a partir de datos demográficos globales.  

El foco está en el **análisis visual riguroso** y la **justificación técnica de decisiones de diseño**, no en la estética ni en la narrativa final.

---

## 📊 Datasets

Los grupos trabajarán con **dos datasets de Our World in Data**, ambos basados en la base *UN World Population Prospects (2024)*:

1. **Birth rate vs. Death rate (1950–2023)**  
   - Variables: tasa de natalidad, tasa de mortalidad y población total.  
   - Unidad: nacimientos o muertes por cada 1.000 personas.

2. **Population growth rate with and without migration (1950–2023)**  
   - Variables: tasa de crecimiento total (%) y tasa de crecimiento natural (%).  
   - Diferencia entre ambas = impacto neto de la migración.

Cada fila corresponde a un país o región por año.

---

## 🧩 Desafío

A partir de los datasets entregados, cada grupo deberá desarrollar un **análisis visual comparativo y justificado** que cumpla con los siguientes requisitos:

1. **Exploración visual de los datos**  
   - Analicen las relaciones entre natalidad, mortalidad y crecimiento poblacional (con y sin migración).  
   - Exploren tendencias, quiebres o patrones regionales y temporales.  
   - Comparen regiones o países de interés (por ejemplo: Europa vs África, 1970–2020).  

2. **Identificación de hallazgos relevantes**  
   - El objetivo no es contar una historia, sino **detectar y explicar un fenómeno observable** con base en los datos.  
   - Ejemplo: “Desde XXXX, el crecimiento natural de XXXX es negativo, pero el total sigue positivo por XXXX.”

3. **Visualizaciones clave**  
   - Elaboren al menos **dos visualizaciones distintas y complementarias** que, en conjunto, sustenten la misma relación o insight detectado.  
   - Las visualizaciones deben **apoyarse entre sí**, mostrando diferentes facetas o niveles de detalle del fenómeno analizado (por ejemplo, una visión temporal y otra geográfica, o una general y otra comparativa).  
   - Deben variar al menos uno de los siguientes aspectos:  
     - tipo de **marca** (punto, línea, barra, área, etc.)  
     - **canal visual** dominante (posición, color, tamaño, longitud, etc.)  
     - **composición** visual (mapa, serie temporal, gráfico comparativo, etc.)  
   - Cada visualización debe incluir una **justificación técnica breve**:
     - Qué canal y marca se utilizaron.  
     - Por qué esa elección es perceptualmente efectiva.  
     - Qué precisión o saliencia aporta, y qué limitaciones tiene.  
   - Se evaluará la **coherencia y complementariedad** entre ambas, no la repetición de un mismo gráfico con cambios cosméticos.

4. **Visualización incorrecta o engañosa**  
   - Diseñen una visualización **intencionalmente problemática**, por ejemplo:  
     - eje truncado,  
     - paleta de color inapropiada,  
     - área o volumen mal utilizados,  
     - escalas inconsistentes o sin contexto.  
   - Expliquen **por qué podría inducir a error** o manipular la interpretación.  
   - Este punto mide la comprensión ética de las buenas prácticas de visualización.

5. **Síntesis analítica**  
   - Cierren con una frase o idea interpretativa concisa basada en evidencia, por ejemplo:  
     > “En los países XXXXX, el crecimiento poblacional actual XXXX.”  
   - No se espera aún una narrativa extensa ni recomendación política: solo una **observación clara y fundamentada**.

---

## 📁 Entregables

### 1. Presentación PPT
Debe tener entre **8 y 10 diapositivas** y seguir la siguiente estructura:

| Bloque | Contenido esperado |
|--------|---------------------|
| 1 | Introducción breve: contexto del tema y enfoque del grupo |
| 2 | Descripción básica de los datos (fuente, años, variables, unidades) |
| 3 | Visualizaciones exploratorias (EDA visual con observaciones iniciales) |
| 4 | Dos visualizaciones principales + justificación técnica |
| 5 | Una visualización incorrecta + explicación del error perceptual o ético |
| 6 | Síntesis analítica final (hallazgo más relevante) |

### 2. Carpeta técnica comprimida (.zip)
Debe contener:
- Todos los **notebooks, scripts, planillas o dashboards** usados para generar las visualizaciones.  
- Archivos derivados (si agregaron o transformaron datos).  
- Un **README.txt** breve que indique:
  - Herramientas utilizadas.  
  - Pasos realizados (EDA → visualización → exportación).  
  - Si se usó IA, describir exactamente **en qué parte** y cómo se validaron los resultados.  

---

### 🖍️ Rúbrica de Evaluación (1–100 puntos)

La nota total de la tarea se calcula sobre 100 puntos.  
Cada criterio tiene una ponderación específica.  
Dentro de cada criterio hay 3 niveles de desempeño:

- **Insuficiente:** el trabajo no cumple con las expectativas mínimas.  
- **Adecuado:** el trabajo cumple con lo esencial, pero con debilidades claras.  
- **Sólido:** el trabajo demuestra dominio del criterio, con justificación técnica clara y sin problemas importantes.

> Nota: “Sólido” no significa “bonito”, significa “correcto, claro y defendible”.

#### 1. Rigor analítico (20 puntos)

**Qué evalúa:**  
Capacidad para explorar los datos de forma seria, identificar patrones reales y respaldar afirmaciones con evidencia visual.

| Nivel | Descripción | Puntos |
|-------|-------------|--------|
| Insuficiente | La exploración es superficial o anecdótica. Se muestran gráficos sueltos sin una pregunta clara detrás ni interpretación concreta. No hay diferenciación entre ruido y patrón. | 0–10 |
| Adecuado | Se muestran comparaciones relevantes (por país, región o periodo) y se identifican tendencias o quiebres. La interpretación es razonable pero a veces ambigua o poco focalizada. | 11–16 |
| Sólido | Se identifican hallazgos claros, específicos y bien justificados (por ejemplo, quiebres temporales, diferencias sistemáticas entre regiones, dependencia de migración, etc.). Se entiende el “por qué esto importa”. | 17–20 |

---

#### 2. Diseño y coherencia visual (20 puntos)

**Qué evalúa:**  
Calidad de las **visualizaciones clave**. Cómo las dos visualizaciones seleccionadas se complementan para explicar el mismo fenómeno desde ángulos distintos (temporal, espacial, comparativo, etc.).

| Nivel | Descripción | Puntos |
|-------|-------------|--------|
| Insuficiente | Las visualizaciones son redundantes (la segunda es básicamente la misma con cosmética distinta). No hay complementariedad ni aporte adicional. Hay elecciones gráficas que entorpecen la lectura. | 0–10 |
| Adecuado | Hay dos visualizaciones distintas y ambas son entendibles. Muestran distintos aspectos del mismo fenómeno, pero la conexión entre ellas es parcialmente débil o no se explica bien. | 11–16 |
| Sólido | Las visualizaciones se refuerzan mutuamente: cada una aporta una capa diferente de comprensión (por ejemplo, magnitud temporal vs. localización geográfica). La relación entre ambas está explícita y justificada. | 17–20 |

#### 3. Uso de marcas y canales (20 puntos)

**Qué evalúa:**  
La calidad técnica de las decisiones de codificación visual: marcas usadas (punto, barra, línea…), canales usados (posición, área, color…), su adecuación al tipo de variable y su efectividad perceptual.

| Nivel | Descripción | Puntos |
|-------|-------------|--------|
| Insuficiente | El gráfico usa canales mal elegidos para el tipo de dato (ej. color como continuo para categorías sin orden, área para comparar valores muy cercanos sin escala clara, etc.). No se justifica la elección visual. | 0–10 |
| Adecuado | Se eligen marcas y canales razonables en la mayoría de los casos. Hay una justificación básica (“usamos línea porque es una serie temporal”), pero sin discutir precisión perceptual o limitaciones. | 11–16 |
| Sólido | Se eligen marcas y canales adecuados y se argumenta técnicamente: precisión de comparación, saliencia, discriminabilidad, limitaciones perceptuales conocidas. Se nota comprensión de efectividad y expresividad. | 17–20 |

#### 4. Detección de malas prácticas (15 puntos)

**Qué evalúa:**  
La visualización “incorrecta/engañosa” y la explicación crítica de por qué es problemática.

| Nivel | Descripción | Puntos |
|-------|-------------|--------|
| Insuficiente | La visualización “mala” no es realmente problemática o no está explicada. Se entrega casi como un meme (“gráfico feo”) sin un análisis serio de por qué podría inducir a error. | 0–7 |
| Adecuado | Se muestra una visualización objetablemente mala (escala truncada, paleta confusa, etc.) y se explican fallas básicas. Sin embargo, la explicación es parcial o genérica (“podría confundir”). | 8–12 |
| Sólido | Se identifica con precisión el mecanismo de engaño (ej. cambio de escala altera percepción de magnitud; uso de área hace parecer enormes diferencias pequeñas; mezcla categorías/ordinales). Se explican consecuencias de interpretación errónea o sesgo comunicacional. | 13–15 |

#### 5. Claridad interpretativa (15 puntos)

**Qué evalúa:**  
La capacidad de cerrar con una observación analítica precisa, sustentada en los datos, sin inventar causalidad.

| Nivel | Descripción | Puntos |
|-------|-------------|--------|
| Insuficiente | El cierre es vago (“los datos son interesantes”, “hay diferencias”) o especulativo (“esto demuestra que las políticas migratorias son malas/buenas”) sin evidencia. | 0–7 |
| Adecuado | Se entrega una afirmación basada en evidencia descriptiva (“el crecimiento natural es negativo en X desde 1995”), pero es demasiado general o poco focalizada. | 8–12 |
| Sólido | Se formula una afirmación concreta, delimitada y respaldada por las visualizaciones presentadas. Se respetan los límites: se distingue descripción de interpretación, y no se fuerza causalidad. | 13–15 |

#### 6. Trazabilidad técnica (10 puntos)

**Qué evalúa:**  
La entrega del material técnico que prueba que el trabajo fue realizado por el grupo: notebooks, planillas, código, transformaciones.

| Nivel | Descripción | Puntos |
|-------|-------------|--------|
| Insuficiente | Faltan notebooks/planillas o el contenido no permite reproducir las visualizaciones. No se evidencia proceso propio. No se declara uso de IA (o se oculta). | 0–4 |
| Adecuado | Se entregan archivos técnicos y son razonablemente consistentes con lo presentado, aunque sin mucho orden o documentación mínima. Uso de IA declarado de manera básica. | 5–8 |
| Sólido | Se entrega todo el material técnico organizado (notebooks, planillas, scripts, dashboards exportables) + README con pasos claros. Si se usó IA, se documenta en qué ayudó y cómo se validó el resultado. | 9–10 |

### Resumen de puntajes

- Rigor analítico: 20 pts  
- Diseño y coherencia visual (visualizaciones complementarias): 20 pts  
- Uso de marcas y canales: 20 pts  
- Detección de malas prácticas: 15 pts  
- Claridad interpretativa: 15 pts  
- Trazabilidad técnica: 10 pts  

**Total: 100 puntos**
---

## 🧠 Propósito pedagógico

Esta primera tarea marca la transición desde la **visualización como herramienta de exploración** hacia la **visualización como razonamiento analítico fundamentado**.  

El énfasis está en:
- Comprender cómo las elecciones gráficas afectan la interpretación.  
- Aplicar la teoría de percepción y codificación visual.  
- Detectar sesgos o manipulaciones visuales.  
- Construir una base técnica sólida para tareas futuras más narrativas.

---

## 📬 Entrega

- Subir la **presentación en PDF** y la **carpeta .zip** al aula virtual antes de las 23:59 del viernes 7 de noviembre de 2025.  
- Un integrante del grupo deberá realizar la entrega en representación de todos.  
- No se aceptarán entregas fuera de plazo salvo casos justificados oficialmente.  
- Revisaremos las presentaciones en clases.  

> **Recordatorio importante:**  
> No se evalúa la “belleza” de los gráficos, sino su **efectividad perceptual y argumentación técnica**.  
> No se busca una historia todavía, sino **claridad analítica y rigor conceptual.**  
> La transparencia en el proceso técnico y la autoría del trabajo son parte esencial de la nota final.