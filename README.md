# Análisis de Airbnb Bogotá

El proyecto conserva **cuatro notebooks** y un módulo compartido, `bi_airbnb.py`. El archivo que alimenta el dashboard es **`resultados/anuncios_dashboard.csv`**. La refactorización mantiene las rutas, nombres y columnas de los CSV y JSON existentes; las imágenes ya no se exportan.

## Objetivo y preguntas de análisis

Transformar la captura de Airbnb Bogotá en información reproducible para comparar precios publicados y señales de actividad entre alojamientos semejantes. La solución combina ETL, seis KPIs, contrastes estadísticos y Tableau; no estima precios óptimos ni rentabilidad.

1. ¿Cómo difieren los precios entre localidades?
2. ¿Qué diferencias hay según tipo de alojamiento?
3. ¿Cómo se relacionan capacidad y precio?
4. ¿Qué asociación existe entre calificación y precio?
5. ¿Qué diferencias se observan entre anfitriones con uno y con varios anuncios?

## Hipótesis contrastadas

| Contraste | Hipótesis nula | Alternativa |
| --- | --- | --- |
| H1 | Las distribuciones de precio son iguales entre localidades incluidas | Al menos una difiere |
| H2 | Las distribuciones de precio son iguales entre tipos incluidos | Al menos una difiere |
| H3 | Rho de Spearman capacidad-precio = 0 | Rho ≠ 0 |
| H4 | Rho de Spearman calificación-precio = 0 | Rho ≠ 0 |
| H5, por indicador | La distribución del indicador es igual entre anfitriones con uno y con 2+ anuncios | Las distribuciones difieren |

H5 compara cuatro indicadores con Holm dentro de cada umbral; 5+ frente a uno es sensibilidad. Los contrastes se formularon para las variables disponibles, sin afirmar causalidad. H1/H2 incluyen grupos con n ≥ 30.

## Resultados e interpretación

La base completa contiene 19.505 anuncios y 8.497 anfitriones. Se conservaron 17.998 anuncios para análisis, pertenecientes a 7.795 anfitriones; 711 no tenían precio y 796 se marcaron como atípicos. No se borraron de la base completa.

| KPI | Resultado sin filtros | Utilidad y alcance |
| --- | --- | --- |
| K1 Precio mediano por noche | COP 160.000 | Referencia de tarifas ofertadas; comparar localidad y tipo semejantes |
| K2 Precio mediano por huésped | COP 60.000 | Relacionar tarifa con capacidad anunciada; no es precio por huésped efectivamente ocupado |
| K3 Calificación promedio | 4,704 / 5; n = 14.549 | Describir valoración disponible; no imputar los 3.449 faltantes |
| K4 Anuncios con reseñas en 12 meses | 67,18 % | Señal de actividad reciente; no equivale a ocupación |
| K5 Ocupación estimada mediana | 6,58 %; 24 días | Estimación de la fuente, no reservas verificadas |
| K6 Anfitriones con varios anuncios | 30,51 %; 2.378 de 7.795 | Describir escala por anfitrión distinto; no acredita gestión profesional |

- **H1:** H = 2.304,1; p < 0,001; η²_H = 0,128; n = 17.945. Dunn-Holm identifica 50 de 120 pares significativos. Chapinero y Usaquén tienen medianas COP 190.531 y COP 190.000; su diferencia estadística (p ajustado ≈ 0,019) no implica una gran diferencia práctica. Bosa no integra H1 por tamaño insuficiente.
- **H2:** H = 4.159,8; p < 0,001; η²_H = 0,231; n = 17.971. Vivienda completa tiene mediana COP 179.332, privada COP 93.000 y compartida COP 52.181. Completa frente a privada: δ = 0,623. Se observan precios publicados diferentes, no disposición a pagar demostrada.
- **H3:** ρ = 0,480; p < 0,001; n = 17.998. La asociación capacidad-precio es positiva; no prueba retorno de ampliar una propiedad.
- **H4:** ρ = 0,046; p < 0,001; n = 14.549. La asociación es muy débil pese a ser significativa; no se estudió el algoritmo de Airbnb.
- **H5:** delta de Cliff de 2+ frente a un anuncio: precio 0,075; ocupación 0,185; reseñas 0,213; calificación −0,199. Todos tienen p ajustado < 0,001. Calificación utiliza 6.171 anfitriones (2.198 frente a 3.973); los demás indicadores, 7.795. La diferencia en precio es despreciable y las otras pequeñas bajo el criterio descriptivo utilizado.
- **Sensibilidad:** un anuncio por anfitrión en 100 selecciones: H1–H3 tienen p < 0,05 en las 100 y H4 en 96. Los efectos medianos son 0,083, 0,266, 0,501 y 0,036, respectivamente, con medidas distintas entre contrastes. No son intervalos de confianza.

## Conclusiones y decisiones propuestas

Usar los filtros de localidad, tipo y grupo de anfitrión para construir referencias de ofertas semejantes y revisar anuncios alejados de su segmento. Interpretar conjuntamente precio, cobertura de calificaciones y actividad estimada. Las diferencias entre anfitriones pueden orientar revisiones de servicio, pero no demuestran superioridad profesional o atención personalizada.

El estudio no observa costos, reservas verificadas ni ingresos netos: no permite recomendar adquisiciones como rentables, garantizar retornos ni calcular un precio óptimo. Las comparaciones son de una captura y una muestra filtrada; faltan controles multivariables para aislar asociaciones. Los tamaños de efecto ayudan a distinguir significancia de utilidad práctica.

## Entrega y video

El dashboard se entrega en `Dashboard/Airbnb_Bogota.twbx`. Contiene dos vistas y cinco visualizaciones de negocio, además de seis KPIs. Para la sustentación, usar `GUION_VIDEO.md`, con 12 minutos 40 segundos de exposición y participación de los cuatro integrantes. `CHECKLIST_ENTREGA.md` distingue lo verificado de lo pendiente. El equipo administra GitHub y debe incorporar la URL del repositorio y del video cuando existan. No se simula historial de participación ni se afirma que la grabación ya esté realizada.

## Organización y ejecución

Ejecutar todas las celdas de cada notebook, en este orden, desde la carpeta del proyecto:

| Notebook | Responsabilidad | Uso analítico |
| --- | --- | --- |
| `01_preparacion_datos.ipynb` | ETL, validación y modelo dimensional | Definir una población trazable y registrar exclusiones |
| `02_kpis_dashboard.ipynb` | Seis KPIs y tablas para Tableau | Alimentar los indicadores y filtros del dashboard |
| `03_contrastes_hipotesis.ipynb` | H1–H5, comparaciones y sensibilidad | Evaluar diferencias, asociaciones y magnitud de los efectos |
| `04_figuras_resumen.ipynb` | Cierre, validación y resumen de control | Conciliar esquema, población, KPIs y conclusiones |

`bi_airbnb.py` centraliza rutas, escritura CSV, lectura de bases, filtros de tamaño mínimo, pruebas, ajuste de Holm, comparación de anfitriones y selecciones de sensibilidad. El notebook 04 reutiliza las tablas de 03, valida las 51 columnas y los valores exportados y concilia los seis KPIs desde el CSV que consume Tableau. No repite contrastes ni genera gráficas. Las visualizaciones se presentan en Tableau. Los PNG de ejecuciones anteriores son históricos y no se actualizan.

La numeración de notebooks corresponde al orden de ejecución. En la guía, la Fase 5 es el dashboard y la Fase 6 incluye contrastes, validación y storytelling.

Dependencias: Python, NumPy, pandas, SciPy, Matplotlib, IPython y un entorno Jupyter con ipykernel. Para ejecutar automáticamente también se necesitan nbformat y nbclient. Las rutas se resuelven respecto a `bi_airbnb.py`; los notebooks deben poder importar ese módulo. No requiere descargar nuevamente la fuente.

## ETL practicado

Se aplica un **ETL por lotes de una captura**, ejecutado localmente con pandas. No es una carga incremental ni una serie temporal. La entrada es `datos/listings_bogota.csv`; las fechas efectivas y el SHA-256 de la fuente quedan en `salida_fase3/informe_preparacion.json`.

1. **Extracción.** Lectura del CSV detallado con identificadores como texto para preservar su precisión. Se seleccionan 35 variables necesarias para el análisis y se audita la calidad de todas las columnas originales. Si falta una variable requerida, la ejecución se detiene.
2. **Limpieza.** Se verifican identificadores nulos y duplicados. Solo se colapsan filas idénticas en las variables seleccionadas; los identificadores repetidos con atributos contradictorios detienen la carga. El precio conserva su texto original y se convierte desde el formato de la fuente: coma de miles, punto decimal y símbolo monetario opcional. Los precios ausentes, malformados o no positivos quedan fuera de la muestra de precios, con motivo registrado.
3. **Atípicos.** Se calculan cuartiles sobre el logaritmo natural de precios positivos. Se marcan valores fuera de `[Q1 − 1,5 × RIQ, Q3 + 1,5 × RIQ]`. El logaritmo atenúa la asimetría de precios y evita aplicar la regla directamente sobre una escala muy sesgada. Los anuncios marcados se conservan en hechos y en la base plana, pero `incluido_analisis` los excluye de KPIs y contrastes. Un atípico no implica necesariamente un error: las conclusiones describen la muestra filtrada.
4. **Transformación.** Normalización de localidades, traducción de tipos de alojamiento, agrupación de propiedades, extracción de baños y conteo de amenidades. Conversión de fechas y cálculo de antigüedad de la última reseña, precio por huésped y ocupación estimada como fracción de 365 días. Segmentación por tamaño del anfitrión, noches mínimas, calificación y cuartiles del precio.
5. **Nulos.** Las calificaciones no se imputan. Solo se reemplazan reseñas por mes faltantes por cero cuando el anuncio no tiene reseñas históricas. El precio por huésped queda nulo si la capacidad no es positiva. Las pruebas por variable utilizan sus observaciones válidas.
6. **Modelado.** Modelo en estrella: `fact_anuncios` tiene un registro por anuncio; `dim_localidad`, `dim_tipo_alojamiento` y `dim_anfitrion` contienen sus atributos. Se validan claves únicas, integridad referencial, atributos consistentes por anfitrión y conservación del número de anuncios después de los cruces. Se crea además una base plana para análisis y un resumen con una observación por anfitrión incluido.
7. **Carga.** Exportación en CSV UTF-8 con BOM, sin índice, a `salida_fase3/` y `resultados/`. Los JSON contienen controles y trazabilidad. El proceso vuelve a generar las salidas al ejecutarse; no modifica la fuente original.

Las claves numéricas de localidad y tipo se reconstruyen en cada carga; no son claves históricas garantizadas entre capturas diferentes. Las dimensiones y hechos deben regenerarse juntos.

## Técnicas y justificación

| Técnica | Aplicación y justificación | Precaución de interpretación |
| --- | --- | --- |
| Mediana, cuartiles y RIQ | Resumir precios asimétricos con menor influencia de extremos | La mediana de medianas no equivale a la mediana global |
| KPIs con denominador explícito | Precio mediano, precio por huésped, calificación promedio, actividad por reseñas, ocupación estimada y proporción de anfitriones con varios anuncios | K6 cuenta anfitriones únicos, no filas de anuncios; las fracciones se multiplican por 100 solo para presentarlas |
| Kruskal–Wallis | H1: precio por localidad; H2: precio por tipo. Comparación de rangos entre varios grupos sin exigir normalidad del precio | Contrasta distribuciones; interpretar solo medianas exige formas comparables. Usa grupos con al menos 30 anuncios, criterio operativo que no garantiza potencia ni independencia |
| Dunn con ajuste Holm | Comparaciones por pares para identificar qué grupos difieren, corrigiendo empates y multiplicidad dentro de H1 o H2 | La corrección no se aplica globalmente a todas las hipótesis del proyecto |
| Eta² basada en H | `(H − k + 1) / (n − k)` para acompañar H1/H2 con magnitud | Es un estimador basado en rangos, no un efecto causal; puede ser negativo en muestras con poco efecto |
| Spearman | H3: capacidad y precio; H4: calificación y precio. Asociación monótona por rangos, adecuada ante asimetría y escalas discretas | No exige linealidad, pero no demuestra causalidad ni controla localidad, tipo u otros factores |
| Mann–Whitney y delta de Cliff | Comparación prevista de vivienda completa vs. habitación privada; H5 compara indicadores agregados por anfitrión | Delta indica dirección y magnitud: positivo significa valores mayores en el primer grupo; no es una diferencia en COP |
| Holm en H5 | Ajuste de cuatro indicadores por umbral: precio, ocupación, reseñas y calificación | El contraste principal usa 2+ anuncios frente a 1; 5+ frente a 1 es sensibilidad y omite anfitriones con 2–4 anuncios |
| Selecciones por anfitrión | 100 selecciones reproducibles de un anuncio por anfitrión, semilla `20261018`, recalculando H1–H4 | Reduce la sobrerrepresentación de anfitriones grandes para explorar estabilidad; no es bootstrap, intervalo de confianza ni inferencia formal con errores agrupados |
| Levene centrado en la mediana | Diagnóstico de dispersión de log(precio) entre localidades en el resumen | No constituye una validación general de los supuestos estadísticos |

Se usa α = 0,05. Los resultados incluyen tamaño de muestra, p y tamaño del efecto; un resultado significativo puede tener escasa importancia práctica. Los p que subdesbordan a cero se presentan como `< 0,001`. La ocupación y los ingresos estimados proceden de la fuente: no son reservas observadas, ingresos reales ni resultados causados por un tipo de anfitrión. La disponibilidad tampoco equivale automáticamente a ocupación. El análisis es observacional de una captura y no permite afirmar tendencias temporales.

## Contrato de archivos conservado

| Carpeta | Archivos regenerados |
| --- | --- |
| `salida_fase3/` | `fact_anuncios.csv`, `dim_localidad.csv`, `dim_tipo_alojamiento.csv`, `dim_anfitrion.csv` |
| `salida_fase3/` | `airbnb_bogota_analitico.csv`, `anfitriones_resumen.csv`, `muestra_h1_localidad.csv`, `muestra_h2_tipo_alojamiento.csv` |
| `salida_fase3/` | `anuncios_excluidos.csv`, `calidad_variables.csv`, `registro_limpieza.csv`, `diccionario_datos.csv`, `informe_preparacion.json` |
| `resultados/` | **`anuncios_dashboard.csv`**, `anfitriones_dashboard.csv`, `kpis.csv` |
| `resultados/` | `hipotesis.csv`, `descriptivos_H1.csv`, `descriptivos_H2.csv`, `dunn_holm_H1.csv`, `dunn_holm_H2.csv`, `comparaciones_anfitriones.csv` |
| `resultados/` | `sensibilidad_un_anuncio_por_host.csv`, `resumen_sensibilidad.csv`, `resumen.json` |

El contrato de `anuncios_dashboard.csv` conserva una fila por anuncio incluido, los identificadores `a_` y `h_` como texto, y los campos derivados `precio_intervalo_50mil`, `activo_12m` y `grupo_anfitrion`, además de las columnas de la base analítica. No se renombran las variables usadas por Tableau.

`Dashboard/Airbnb_Bogota.twbx` contiene una conexión a este CSV y un extracto Hyper empaquetado. Regenerar el CSV no actualiza por sí solo ese extracto: para visualizar datos nuevos hay que actualizar el extracto desde Tableau y guardar el libro. El archivo TWBX se conserva sin modificaciones.

## Validación de la refactorización

Se ejecutaron los cuatro notebooks completos, en orden, con Python 3.14, NumPy 2.5.4, pandas 3.0.6, SciPy 1.18.1 y Matplotlib 3.11.2. La versión inicial incluía tres figuras diagnósticas; el cierre definitivo las sustituye por controles de exportación y conclusiones sin gráficas.

- `anuncios_dashboard.csv`: **17.998 filas y 51 columnas; idéntico byte por byte al archivo anterior**. SHA-256: `30a9d96eaf7b5bcbfc25a5395dd323a43d00d1ffbd5dadfbe1729a26d84b7f1e`.
- El TWBX permanece idéntico al original. La validación verifica su conexión y la compatibilidad del CSV; no implica una actualización del extracto en Tableau.
- Los 23 CSV mantienen sus columnas y dimensiones. Los valores analíticos coinciden con los anteriores usando tolerancia numérica relativa `1e-10` y absoluta `1e-12`.
- En `calidad_variables.csv`, pandas 3 informa algunas columnas textuales como `str` donde la ejecución anterior informaba `object`. Este cambio corresponde a la representación del tipo, no a cambios de datos.
- Los dos JSON mantienen sus claves. `informe_preparacion.json` coincide íntegramente. En `resumen.json` se actualizó el hash de la base analítica regenerada (cambios de serialización, con valores tabulares equivalentes) y hay una diferencia numérica mínima en el p de Levene por la versión de SciPy, sin cambio de interpretación.

Para comparar futuras ejecuciones, priorizar esquema, identificadores, conteos y valores, además del hash: un cambio de versión puede alterar la serialización de un CSV sin cambiar su contenido analítico.

### Entorno de ejecución

Se incluye `requirements.txt` con las versiones usadas en la validación (Python 3.14). Crear un entorno virtual, activarlo e instalar con `python -m pip install -r requirements.txt`. En el editor, seleccionar ese intérprete como kernel y ejecutar 01 → 02 → 03 → 04. Las versiones fijadas facilitan comparar resultados entre integrantes.

En la ejecución final, los cuatro notebooks terminaron sin errores. El cierre verificó el contrato de 51 columnas, la población y los valores de anuncios/anfitriones y la conciliación de los seis KPIs. `anuncios_dashboard.csv` sigue idéntico byte por byte al archivo previo a la refactorización y el TWBX permanece sin modificaciones.
