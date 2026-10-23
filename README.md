# Análisis de Airbnb Bogotá

**Institución:** Institución Universitaria ITM · **Programa:** Ingeniería de Sistemas
**Curso:** Análisis de Datos · **Semestre:** 2026-2 · **Equipo:** 10 · **Entrega:** Evento Evaluativo 3

Proyecto universitario de análisis de datos y BI basado en las guías del profesor Daniel Alexis Nieto Mora, semanas 4, 5, 6 y 7–8. La referencia y sus páginas están en [REFERENCIAS_CURSO.md](REFERENCIAS_CURSO.md).

## Alcance y preguntas

El proyecto utiliza estadística descriptiva, correlación de Spearman, interpretación de hipótesis y BI. No incluye pruebas o análisis estadísticos complementarios.

| Pregunta | Tratamiento |
| --- | --- |
| P1: ¿Cómo se describen los precios por localidad? | Conteo, media, mediana, cuartiles y RIQ |
| P2: ¿Cómo se describen los precios por tipo de alojamiento? | Los mismos descriptivos, sin contrastes entre grupos |
| H3: ¿Existe asociación entre capacidad y precio? | Spearman: H0 rho = 0; H1 rho ≠ 0 |
| H4: ¿Existe asociación entre calificación y precio? | Spearman: H0 rho = 0; H1 rho ≠ 0 |
| P5: ¿Cómo se describen los indicadores de anfitriones con uno y varios anuncios? | Conteos, medias y medianas por grupo, una fila por anfitrión |

Se conserva la numeración H3/H4 para enlazarla con el dashboard. P1, P2 y P5 son preguntas descriptivas: no se afirma significancia estadística entre sus grupos. Los descriptivos incluyen todos los grupos con datos y muestran su tamaño.

Para H3/H4 se usa α = 0,05 y se interpreta cada contraste por separado. El valor p no es la probabilidad de que H0 sea verdadera; no rechazar H0 no demuestra que sea cierta. Rho indica dirección y magnitud de la asociación. Las observaciones de un anfitrión pueden estar relacionadas y la captura no es una muestra aleatoria: la inferencia es exploratoria, sin causalidad ni garantía de generalización.

## Organización y ejecución

Crear un entorno virtual con Python 3.14 e instalar `requirements.txt`. Seleccionar ese intérprete en Jupyter y ejecutar todas las celdas en orden:

| Notebook | Responsabilidad |
| --- | --- |
| `01_preparacion_datos.ipynb` | Limpieza, transformaciones, modelo en estrella y trazabilidad |
| `02_kpis_dashboard.ipynb` | Descriptivos básicos, seis KPIs y exportación para Tableau |
| `03_contrastes_hipotesis.ipynb` | Descriptivos de P1/P2/P5 y correlaciones H3/H4 |
| `04_figuras_resumen.ipynb` | Control de exportaciones, conciliación de KPIs y conclusiones |

`bi_airbnb.py` centraliza rutas, lectura/escritura CSV, registro de limpieza, descriptivos y Spearman. Los notebooks deben ejecutarse desde la raíz del proyecto. Las visualizaciones permanecen en Tableau; no se exportan imágenes desde Python.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Preparación y modelo de datos

La fuente es `datos/listings_bogota.csv`. Se seleccionan las variables útiles, se preservan IDs como texto y se verifica que no haya registros contradictorios. Los precios se convierten respetando el formato de la fuente y se conserva su texto original. Se mantienen las decisiones de limpieza de la base existente: precios no válidos y atípicos marcados mediante RIQ sobre log(precio) quedan fuera de la muestra analítica, sin borrarlos de la base completa. Esta regla es una decisión de preparación del proyecto, no una prueba de hipótesis ni una técnica atribuida como exigencia a las guías suministradas.

Se normalizan nombres de localidades y tipos, se crean métricas interpretables y se conservan las calificaciones faltantes. El modelo contiene `fact_anuncios`, `dim_localidad`, `dim_tipo_alojamiento` y `dim_anfitrion`. Se verifican claves y conservación de filas al cruzar tablas. Las claves numéricas se reconstruyen en cada carga; se regeneran hechos y dimensiones juntos.

No se aplica PCA ni escalamiento para modelos predictivos: el objetivo es comparar indicadores en COP, días, huéspedes y puntos. Un ID de dimensión no es una distancia numérica. Los CSV constituyen un modelo analítico local de una captura, no un Data Warehouse histórico desplegado.

## KPIs y dashboard

La muestra actual conserva 17.998 anuncios y 7.795 anfitriones de una base completa de 19.505 anuncios. Las salidas ejecutadas son la fuente para consultar valores vigentes.

| KPI | Medida | Alcance |
| --- | --- | --- |
| K1 | Precio mediano por noche | Precio publicado, no ingreso |
| K2 | Precio mediano por huésped | Tarifa dividida por capacidad anunciada |
| K3 | Calificación promedio | Solo calificaciones disponibles |
| K4 | Proporción de anuncios con reseñas en 12 meses | Señal de actividad, no ocupación verificada |
| K5 | Ocupación estimada mediana | Estimación de la fuente |
| K6 | Proporción de anfitriones con varios anuncios | Cuenta anfitriones distintos, no anuncios |

El dashboard está en `Dashboard/Airbnb_Bogota_Validado.twbx` y consume `resultados/anuncios_dashboard.csv`: una fila por anuncio, 51 columnas e IDs con prefijos `a_` y `h_`. El cambio de alcance estadístico mantiene ese CSV. El extracto Hyper debe actualizarse desde Tableau si cambian sus datos; ejecutar Python no actualiza el libro por sí solo.

El libro validado incluye tres vistas: resumen ejecutivo, exploración de precios y comparación por segmentos. Se corrigieron las unidades de la composición, las etiquetas de cobertura y la exclusión de celdas con menos de 30 anuncios. El paquete incluye el CSV y el extracto.

La historia de presentación es: pregunta → KPI y segmento → hallazgo observado → decisión posible → limitación. Los filtros permiten comparar ofertas semejantes. Las diferencias descriptivas no prueban diferencias poblacionales ni rentabilidad. Una captura no permite afirmar tendencias temporales.

## Salidas actuales

- `salida_fase3/`: hechos, dimensiones, base analítica, resumen por anfitrión, excluidos, calidad, registro, diccionario e informe de preparación.
- `resultados/`: `kpis.csv`, `anuncios_dashboard.csv`, `anfitriones_dashboard.csv`, `descriptivos_P1.csv`, `descriptivos_P2.csv`, `descriptivos_anfitriones.csv`, `hipotesis.csv` y `resumen.json`.

`hipotesis.csv` contiene solo H3 y H4, con n, rho, p y decisión. El resumen de anfitriones conserva el nombre técnico `grupo_h5` por compatibilidad con los datos existentes; representa la agrupación descriptiva de P5. Los resultados de los métodos retirados ya no forman parte de la entrega.

## Validación del alcance actual

Los cuatro notebooks se ejecutaron completos. Los CSV de anuncios y anfitriones para Tableau permanecen idénticos byte por byte; los valores de los seis KPIs se conservan. H3/H4 mantienen sus coeficientes y valores p. Los descriptivos por localidad y alojamiento cubren ahora todos los grupos. Se retiraron las salidas de las pruebas eliminadas y se regeneró el resumen sin diagnósticos ni sensibilidad adicionales.

## Graphify

Graphify es una herramienta de navegación del código, independiente del análisis académico:

```bash
uv tool install graphifyy
graphify install --platform codex --project
graphify extract . --code-only
graphify cluster-only . --no-label
graphify update .
```

El mapa del módulo está en `graphify-out/graph.html`. El mapa conjunto con las celdas de notebooks está en `graphify-out/proyecto_completo/graphify-out/graph.html`; se construye desde copias auxiliares en `graphify-out/proyecto_fuentes/`. Es una instantánea estructural, no una representación completa de operaciones dinámicas de pandas. Editar los notebooks originales, no las copias. Graphify, Codex y los resultados locales están excluidos mediante `.gitignore`.
