# Referencias del curso aplicadas al proyecto Airbnb Bogotá

Referencia: *Guía de Análisis de Datos*, docente Daniel Alexis Nieto Mora, Departamento de Sistemas, Ingeniería en Ciencia de Datos, grupo 190304018-1. Se revisaron los PDF proporcionados completos; las lecturas y videos enlazados no se han revisado. Las páginas corresponden a la numeración impresa.

Por instrucción del usuario, el análisis estadístico se limita a las técnicas de estas guías. Los ejercicios Titanic son ejemplos de práctica y no se trasladan como nuevas preguntas a Airbnb. Tampoco se afirma resolver todos los talleres.

| Guía | Contenido aplicado | Implementación |
| --- | --- | --- |
| Semana 4, pp. 1–3 y 6–7 | Media, mediana, varianza, desviación estándar, cuartiles, RIQ y Spearman | Descriptivos en 02/03; correlaciones H3/H4 en 03 |
| Semana 5, pp. 1–3 y 8 | Preparación de variables según el propósito del análisis | 01 conserva unidades y categorías interpretables. No hay un modelo predictivo que requiera PCA, one-hot o escalamiento |
| Semana 6, pp. 1–2 y 5–6 | H0/H1, α, valor p, errores tipo I/II e interpretación | H3/H4: H0 rho = 0, H1 rho ≠ 0; α = 0,05, decisiones por contraste y límites de la inferencia |
| Semanas 7–8, pp. 1–3 y 6 | ETL, modelo analítico, KPIs, filtros y storytelling | 01 prepara; 02 calcula seis KPIs y exporta; 04 verifica y comunica; Tableau presenta las vistas |

## Alcance de las preguntas

P1 (localidad), P2 (alojamiento) y P5 (anfitriones) se describen con conteos, medias, medianas y dispersión según corresponda. No son contrastes y no se declaran diferencias significativas. H3/H4 usan Spearman y conservan su numeración para relacionarlas con los KPIs.

No se ejecutan pruebas post-hoc, correcciones por multiplicidad, pruebas de comparación de grupos ajenas al material, diagnósticos adicionales ni remuestreo. Los resultados y conclusiones de esos métodos se retiraron. La guía 6 introduce t y chi-cuadrado, pero no se añaden artificialmente a preguntas que aquí se presentan como descriptivas.

El valor p se interpreta para cada correlación, sin una afirmación conjunta sobre las dos. Rho indica asociación, no causalidad. Los anuncios pueden compartir anfitrión y la captura no es una muestra aleatoria: las conclusiones inferenciales son exploratorias. No se calculan intervalos de confianza ni se afirma cumplir todos los temas del programa.

## Preparación y presentación

Se mantienen la limpieza y las tablas que alimentan Tableau. La regla existente de atípicos sobre log(precio) es una decisión del ETL previo, no una prueba inferencial ni un requisito atribuido al profesor. Las calificaciones no se imputan. Las claves de dimensiones no se interpretan como distancias. El modelo en CSV es local y de una captura, no un Data Warehouse histórico.

Para la exposición: pregunta, medida, hallazgo observado, decisión acotada y limitación. La guía de semanas 7–8 contempla tendencias solo cuando aplican; una captura no permite demostrar evolución temporal.

## Fuentes y trazabilidad

Los archivos originales permanecen en la carpeta Downloads del usuario; no se duplican en el repositorio. Las dos copias de semana 6 son idénticas byte por byte y cuentan como una única fuente.

| Archivo | Páginas | SHA-256 |
| --- | --- | --- |
| `Análisis_de_datos_Semana_4.pdf` | 7 | `76202dee3e4a05c0c807cb17285f7469f27bde63e5207c595044dee7d3c55168` |
| `Análisis_de_datos_Semana_5.pdf` | 8 | `b97d5f8ed7b55077e1de9e1d090ca0dabdaab726f0d946d9c8a0df47f17acb8d` |
| `Análisis_de_datos_Semana_6.pdf` y `Análisis_de_datos_Semana_6 (1).pdf` | 6 cada uno | `4c70b7ce6bf58102e3a5105933e5c898dd952e91f666c7f54223b382e1228768` |
| `Análisis_de_datos_Semana_7-8.pdf` | 7 | `00b057a8597a6ae18e4b590287b34aa6c7ad95aa83430366d35caaf5c4239f6b` |
