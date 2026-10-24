# Análisis de Airbnb Bogotá --- Evento Evaluativo 3

**Institución:** Institución Universitaria ITM\
**Programa:** Ingeniería de Sistemas\
**Asignatura:** Análisis de Datos\
**Semestre:** 2026-2\
**Equipo:** 10\
**Fuente de datos:** Inside Airbnb --- captura del 16 de septiembre de
2026

**Integrantes:** - Franyelica Valentina Garcia Fernandez - Darwin Osorio
Ospina - Dario Giovanny Montoya - Santiago Pabón Acevedo

## 1. Objetivo

### Descripción general

Proyecto de análisis de datos y Business Intelligence sobre la oferta de
alojamientos de Airbnb en Bogotá, con datos de Inside Airbnb
correspondientes a la captura del 16 de septiembre de 2026. El propósito
es convertir los datos en información útil para comprender el mercado
mediante preparación y modelado de datos, indicadores clave (KPIs),
estadística descriptiva, correlación de Spearman y un dashboard en
Tableau.

### Problema de análisis

La oferta presenta diferencias en precio, ubicación, capacidad, tipo de
alojamiento, calificación, actividad reciente y características del
anfitrión. Observar estas variables por separado dificulta identificar
cuáles se asocian con el precio y cómo resumirlas para apoyar
decisiones. El proyecto aborda estas preguntas mediante análisis
descriptivos y asociaciones estadísticas, sin atribuir causalidad.

### Objetivo general

Analizar los alojamientos de Airbnb en Bogotá mediante técnicas de
Business Intelligence y estadística descriptiva para identificar
patrones, diferencias y asociaciones entre el precio y variables del
alojamiento y del anfitrión, comunicando los resultados mediante KPIs y
dashboards interactivos.

### Objetivos específicos

1.  Preparar, limpiar y transformar el conjunto de datos para construir
    una base analítica consistente.
2.  Estructurar los datos en dimensiones, métricas y tablas orientadas
    al análisis.
3.  Definir indicadores clave que resuman el comportamiento de la
    oferta.
4.  Describir el precio por localidad y por tipo de alojamiento.
5.  Evaluar la asociación del precio con la capacidad y con la
    calificación.
6.  Comparar descriptivamente a los anfitriones con un solo anuncio y a
    los que tienen varios anuncios.
7.  Construir un dashboard en Tableau que comunique los resultados.
8.  Formular conclusiones, limitaciones y posibles decisiones basadas en
    la evidencia.

### Preguntas de análisis

| ID | Pregunta | Tratamiento |
|---|---|---|
| P1 | ¿Cómo se distribuye el precio entre las localidades de Bogotá? | Descriptivo |
| P2 | ¿Cómo varía el precio según el tipo de alojamiento? | Descriptivo |
| H3 | ¿Existe asociación entre la capacidad y el precio? | Correlación de Spearman |
| H4 | ¿Existe asociación entre la calificación y el precio? | Correlación de Spearman |
| P5 | ¿Cómo se comportan los anfitriones con varios anuncios frente a los de un solo anuncio en precio, ocupación, reseñas y calificación? | Descriptivo |

## 2. Metodología

El proyecto se desarrolló a partir del conjunto de datos de Inside
Airbnb correspondiente a una captura del 16 de septiembre de 2026, que
contiene inicialmente **19.505 anuncios y 90 columnas**.

### 2.1. Preparación y modelado de datos

La preparación se implementó en el notebook
`01_preparacion_datos.ipynb`, mediante las siguientes actividades:

-   Selección de variables relevantes y revisión de la calidad de los
    datos.
-   Conversión y validación de los precios publicados en pesos
    colombianos (COP).
-   Identificación de valores no válidos y valores atípicos mediante el
    criterio de 1,5 veces el rango intercuartílico (RIQ) aplicado al
    logaritmo del precio.
-   Normalización de categorías, construcción de métricas derivadas y
    conservación de las calificaciones faltantes sin imputarlas.
-   Registro de exclusiones y generación del diccionario de datos y los
    archivos de trazabilidad.
-   Construcción de un modelo analítico compuesto por una tabla de
    hechos (`fact_anuncios`) y dimensiones de localidad, tipo de
    alojamiento y anfitrión.

Después de aplicar los criterios de preparación establecidos, se obtuvo
una muestra analítica de **17.998 anuncios y 7.795 anfitriones**. Los
registros excluidos se conservan en los archivos de control para
facilitar la trazabilidad del proceso.

### 2.2. Indicadores y análisis estadístico

En `02_kpis_dashboard.ipynb` se calcularon seis indicadores para resumir
el comportamiento de la oferta: precio mediano por noche, precio mediano
por huésped, calificación promedio, proporción de anuncios con reseñas
recientes, ocupación estimada mediana y proporción de anfitriones con
varios anuncios.

En `03_contrastes_hipotesis.ipynb` se desarrollaron los análisis
descriptivos de precios por localidad y tipo de alojamiento, así como la
comparación descriptiva entre anfitriones con un anuncio y anfitriones
con dos o más anuncios. También se evaluaron dos hipótesis de asociación
mediante el coeficiente de correlación de Spearman:

-   **H3:** relación entre la capacidad del alojamiento y el precio.
-   **H4:** relación entre la calificación del alojamiento y el precio.

Para estas dos pruebas se estableció un nivel de significancia de **α =
0,05**. La interpretación considera tanto el valor p como la magnitud y
dirección del coeficiente de correlación.

Las comparaciones por localidad, tipo de alojamiento y grupo de
anfitriones son descriptivas en el alcance actualizado del proyecto; no
se presentan como pruebas de diferencias estadísticamente
significativas. Finalmente, `04_figuras_resumen.ipynb` permite verificar
las exportaciones, conciliar los indicadores y consolidar las
conclusiones.

### 2.3. Visualización y Business Intelligence

Se construyó un dashboard interactivo en Tableau con tres vistas:

-   **Resumen ejecutivo:** presenta los seis KPIs y una visión general
    de la oferta.
-   **Exploración de precios:** permite examinar la distribución de los
    precios y su relación con la capacidad.
-   **Comparación por segmentos:** presenta los precios medianos según
    la localidad y el tipo de alojamiento.

Los filtros de localidad, tipo de alojamiento y anfitrión permiten
explorar los datos desde diferentes perspectivas. Las visualizaciones se
alimentan de los archivos CSV generados durante el procesamiento.

## 3. Resultados

### 3.1. Indicadores clave (KPIs)

| ID | Indicador | Resultado |
|---|---|---:|
| K1 | Precio mediano por noche | 160.000 COP |
| K2 | Precio mediano por huésped | 60.000 COP |
| K3 | Calificación promedio (14.549 anuncios con calificación) | 4,70 / 5 (4,704) |
| K4 | Anuncios con reseñas en los últimos 12 meses | 67,18 % |
| K5 | Ocupación estimada mediana | 6,58 % |
| K6 | Anfitriones con varios anuncios (2.378 de 7.795) | 30,51 % |

-   Se utiliza la mediana debido a la asimetría de los precios y a la
    influencia que pueden tener los valores extremos.
-   La ocupación es una estimación derivada de la metodología del
    proyecto, no una medición directa de las reservas reales.

### 3.2. Descriptivos de precio (P1 y P2)

**Por localidad (P1).** Las medianas varían entre localidades. Entre las
más altas se encuentran Chapinero (aproximadamente 190.531 COP), Barrios
Unidos (148.749 COP) y Teusaquillo (139.000 COP). Entre las más bajas
figuran Bosa (87.906 COP) y Sumapaz (72.000 COP). Sumapaz tiene pocos
anuncios, por lo que su resultado debe interpretarse con cautela.

**Por tipo de alojamiento (P2).** La oferta se concentra principalmente
en viviendas completas:

| Tipo de alojamiento | Número de anuncios |
|---|---:|
| Vivienda completa | 13.200 |
| Habitación privada | 4.694 |
| Habitación compartida | 77 |
| Habitación de hotel | 27 |

**Por segmentos (localidad y tipo).** Dentro de una misma localidad, los
precios medianos varían según el tipo de alojamiento. Por ejemplo, en
Chapinero, la mediana de la vivienda completa es de aproximadamente
199.000 COP, frente a unos 122.000 COP para la habitación privada. Los
segmentos con menos de 30 anuncios deben interpretarse con cautela.

Estas diferencias son descriptivas: no prueban diferencias poblacionales
ni permiten concluir cuál segmento es más rentable.

### 3.3. Asociaciones entre variables (H3 y H4)

| Hipótesis | Variables | n | ρ de Spearman | Valor p | Decisión |
|---|---|---:|---:|---:|---|
| H3 | Capacidad – precio | 17.998 | 0,480 | < 0,001 | Rechazar H₀ |
| H4 | Calificación – precio | 14.549 | 0,046 | < 0,001 | Rechazar H₀ |

-   **H3 --- Capacidad y precio:** se observa una asociación positiva de
    magnitud moderada. En los datos analizados, los alojamientos con
    mayor capacidad tienden a presentar precios más altos.
-   **H4 --- Calificación y precio:** aunque el valor p es pequeño, el
    coeficiente está muy cerca de cero. La asociación es muy débil y
    tiene poca relevancia práctica. Con muestras grandes, un valor p
    pequeño no implica necesariamente una relación fuerte.
-   Ambos resultados indican asociación, no causalidad.

Los resultados detallados están en `resultados/hipotesis.csv`, que
contiene únicamente H3 y H4, junto con el tamaño de muestra, el
coeficiente rho, el valor p y la decisión estadística.

### 3.4. Anfitriones (P5)

Se comparan descriptivamente los anfitriones con un solo anuncio (5.417)
y aquellos con dos o más anuncios (2.378), considerando precio,
ocupación estimada, reseñas y calificación. En el alcance actualizado no
se afirma significancia estadística entre estos grupos.

Los resultados están en `resultados/descriptivos_anfitriones.csv`. El
nombre técnico `grupo_h5` se conserva por compatibilidad con los datos
existentes y representa la agrupación descriptiva de P5.

## 4. Conclusiones

La oferta de Airbnb en Bogotá está concentrada en dos tipos de
alojamiento: la vivienda completa, con 13.200 anuncios, y la habitación
privada, con 4.694. Las habitaciones compartidas y las de hotel tienen
una participación mucho menor. Esto significa que la mayor parte de los
resultados generales del dashboard está determinada por las dos primeras
categorías. También se observa una concentración de anuncios en ciertos
segmentos: las viviendas completas de Chapinero representan alrededor de
4.083 anuncios y, junto con Usaquén y Teusaquillo, suman 8.356 anuncios,
cerca del 46 % de la muestra.

Los precios cambian entre localidades, por lo que el valor mediano
general de 160.000 COP no describe por igual todos los sectores de
Bogotá. Bosa y Sumapaz presentan medianas bajas, aunque en Sumapaz hay
muy pocos anuncios y el resultado debe tomarse con precaución. El
histograma también muestra que hay muchos anuncios en los rangos de
precios bajos y medios, mientras que los precios más altos aparecen con
menor frecuencia. Esto respalda el uso de la mediana para resumir los
precios.

El tipo de alojamiento también se relaciona con el precio. En
localidades con suficientes anuncios, las viviendas completas suelen
presentar medianas superiores a las habitaciones privadas. Sin embargo,
el comportamiento no es idéntico en todos los segmentos y las
comparaciones con pocas observaciones pueden cambiar considerablemente.
La localidad también importa dentro de un mismo tipo de alojamiento: por
ejemplo, las viviendas completas de Chapinero y Usaquén presentan
medianas cercanas a 200.000 COP, mientras que en Kennedy la mediana es
de aproximadamente 136.698 COP.

La gráfica de dispersión y la correlación de Spearman muestran que los
alojamientos con mayor capacidad tienden a tener precios más altos (ρ =
0,480). Aun así, los puntos están bastante dispersos, por lo que la
capacidad no explica por sí sola las diferencias de precio. En cambio,
la relación entre calificación y precio es muy débil (ρ = 0,046). Aunque
su valor p es inferior a 0,001, el coeficiente cercano a cero indica que
la asociación tiene poca relevancia práctica. Por eso, es importante
interpretar el tamaño de la relación y no solamente la significancia
estadística.

En cuanto a la actividad, el 67,18 % de los anuncios tuvo reseñas
durante los últimos doce meses, mientras que la ocupación estimada
mediana es del 6,58 %. Esta última cifra debe interpretarse teniendo
presente que es una estimación y no un registro de reservas reales.
Además, el 30,51 % de los anfitriones tiene dos o más anuncios, lo que
permite distinguir entre anfitriones con diferentes niveles de presencia
en la plataforma, sin que esto implique necesariamente mayores ingresos
o rentabilidad.

En general, las gráficas y los indicadores permiten observar que la
localidad, el tipo de alojamiento y la capacidad son dimensiones útiles
para comparar los precios publicados en Airbnb Bogotá. Los resultados
describen los anuncios incluidos en la captura del 16 de septiembre de
2026 y no deben interpretarse como tendencias a lo largo del tiempo ni
como evidencia de relaciones causales.

