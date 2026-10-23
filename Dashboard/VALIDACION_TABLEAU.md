# Validación de Tableau · 23 de octubre de 2026

Libro de entrega: **Airbnb_Bogota_Validado.twbx**. Se abrió y revisó en Tableau Public para macOS; se guardó localmente. No se publicó en Tableau Public.

## Cambios visuales

- Tres dashboards de 1360 × 740: resumen ejecutivo, exploración de precios y comparación por segmentos.
- Paleta moderada: verde azulado para precios, azul y violeta para grupos de KPIs, histograma ocre y dispersión azul. La composición distingue los cuatro alojamientos por color y por texto.
- Composición ordenada por número de anuncios, sin mezclar cantidades con precios.
- Matriz con mediana en COP y tamaño del grupo en una sola línea. Incluye todos los grupos con datos, incluso los menores de 30 anuncios; las celdas vacías representan combinaciones sin anuncios.
- Etiquetas de cobertura completas, títulos breves, ejes con unidades y puntos de dispersión visibles. Tableau puede omitir etiquetas de barras cercanas para evitar que se superpongan; el valor sigue disponible al consultar la marca.

Los colores de las categorías no indican calidad ni significancia. La matriz conserva una escala gradual para comparar precios. No se añadieron técnicas estadísticas a las previstas en las guías.

## Datos y cálculos

Se ejecutaron completos los cuatro notebooks. Se leyó el extracto Hyper con la API de Tableau y se compararon sus 17.998 filas y 51 columnas contra `resultados/anuncios_dashboard.csv`, ordenando por ID. Los valores coinciden tras normalizar fechas y el campo `precio_texto_original`: Tableau lo interpreta como número, mientras el CSV conserva el texto monetario original. Las variables analíticas coinciden con tolerancia numérica de 1e-10.

Los seis KPIs y la cobertura se contrastaron visualmente con los cálculos de Python. Valores mostrados en Tableau, redondeados:

| Selección | Anuncios | Anfitriones | Precio mediano COP | Por huésped COP | Calificación | Con reseñas 12m | Ocupación estimada | Hosts con 2+ anuncios |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Todas / Todos / Todos | 17.998 | 7.795 | 160.000 | 60.000 | 4,70 | 67,18 % | 6,58 % | 30,51 % |
| Bosa / Todos / Todos | 20 | 18 | 87.906 | 38.053 | 4,80 | 30,00 % | 0,00 % | 22,22 % |
| Todas / Todos / Un anuncio | 5.417 | 5.417 | 147.799 | 56.164 | 4,79 | 57,19 % | 3,84 % | 0,00 % |

En la vista general hay 14.549 calificaciones disponibles; en «Un anuncio», 3.973. El porcentaje de ocupación se almacena como fracción en el CSV y se formatea como porcentaje en Tableau. K6 utiliza anfitriones distintos como denominador.

## Interacciones revisadas

- Apertura de las tres vistas sin errores de carga.
- Filtro Bosa compartido entre resumen, histograma/dispersión y matriz.
- Bosa: 7 habitaciones privadas, mediana 60.500 COP; 13 viviendas completas, mediana 148.700 COP. Ambos grupos aparecen pese a tener menos de 30 anuncios.
- Filtro «Habitación privada»: la matriz conserva solo esa categoría.
- Filtro «Un anuncio»: cobertura y seis KPIs cambian; K6 muestra 0 %.
- Restablecimiento a Todas / Todos / Todos y revisión de la paleta final.

Son comprobaciones representativas; no se recorrieron manualmente todas las combinaciones de filtros. La comparación fila a fila del extracto cubre el conjunto de datos completo.

## Abrir y actualizar

Abrir `Airbnb_Bogota_Validado.twbx`; el extracto incluido permite consultar la captura sin ejecutar Python. El paquete también incluye una copia de `Data/anuncios_dashboard.csv`. Se conservaron las versiones anteriores del libro localmente, excluidas de Git.

Si cambia la fuente:

1. Ejecutar los notebooks 01 → 04 desde la raíz del proyecto.
2. En Tableau, editar la conexión de la fuente «Airbnb Bogotá · anuncios incluidos» y seleccionar el nuevo `resultados/anuncios_dashboard.csv` del proyecto.
3. Actualizar el extracto y comparar los KPIs con `resultados/kpis.csv`; guardar el libro empaquetado localmente.

Ejecutar Python no actualiza automáticamente el extracto. Tableau puede empaquetar solamente el Hyper al guardar y conservar una ruta temporal de la conexión CSV; por eso, para una nueva captura, hay que seleccionar explícitamente el CSV actualizado. La actualización con una captura diferente no formó parte de esta validación.
