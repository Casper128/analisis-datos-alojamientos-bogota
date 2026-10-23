"""
Utilidades compartidas por los notebooks del proyecto BI Airbnb Bogotá.

Este módulo centraliza funcionalidades comunes para evitar repetir código
entre los notebooks del proyecto.

Incluye:
- Rutas y constantes del proyecto.
- Lectura y escritura de archivos CSV.
- Validaciones de integridad.
- Registro de decisiones de limpieza.
- Filtro por tamaño mínimo de muestra.
- Carga de las bases procesadas.
- Pruebas estadísticas reutilizables.
- Estadísticos descriptivos.
- Configuración básica de visualizaciones.

Los notebooks 01-04 contienen la lógica propia de cada fase.

Proyecto:
Evento Evaluativo 3 - Análisis de Datos
Airbnb Bogotá
"""

# ================================================================
# IMPORTACIONES
# ================================================================

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


# ================================================================
# RUTAS DEL PROYECTO
# ================================================================

# Carpeta raíz: ubicación de este archivo y de los notebooks.
RAIZ = Path(__file__).resolve().parent

# Dataset original.
ENTRADA = RAIZ / "datos" / "listings_bogota.csv"

# Salidas de la fase de preparación y modelado.
DIR_FASE3 = RAIZ / "salida_fase3"

# Resultados utilizados por análisis posteriores y Tableau.
DIR_RESULTADOS = RAIZ / "resultados"

# Archivos principales generados por la fase 3.
ARCHIVO_ANALITICO = DIR_FASE3 / "airbnb_bogota_analitico.csv"
ARCHIVO_ANFITRIONES = DIR_FASE3 / "anfitriones_resumen.csv"


# ================================================================
# CONSTANTES
# ================================================================

# Nivel de significancia estadística.
ALPHA = 0.05

# Semilla utilizada para garantizar reproducibilidad.
SEED = 20261018

# Número mínimo de observaciones permitido por grupo.
MIN_N = 30

# Número de iteraciones utilizado por los análisis de sensibilidad.
N_ITER_SENSIBILIDAD = 100


# ================================================================
# UTILIDADES GENERALES
# ================================================================

def guardar_csv(frame, carpeta, nombre):
    """
    Guarda un DataFrame como archivo CSV.

    Utiliza UTF-8 con BOM para conservar correctamente caracteres
    especiales y facilitar su apertura en Excel, Power BI y Tableau.

    Parámetros
    ----------
    frame : pandas.DataFrame
        DataFrame que se desea guardar.

    carpeta : str o pathlib.Path
        Carpeta de destino.

    nombre : str
        Nombre del archivo CSV.
    """

    carpeta = Path(carpeta)

    # Crea la carpeta si todavía no existe.
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / nombre

    frame.to_csv(
        ruta,
        index=False,
        encoding="utf-8-sig"
    )


def exigir(condicion, mensaje):
    """
    Valida una condición necesaria para continuar el procesamiento.

    Si la condición no se cumple se genera un ValueError.

    Parámetros
    ----------
    condicion : bool
        Expresión que debe cumplirse.

    mensaje : str
        Mensaje mostrado si la validación falla.
    """

    if not condicion:
        raise ValueError(mensaje)


# ================================================================
# BITÁCORA DE LIMPIEZA
# ================================================================

class Registro:
    """
    Bitácora de decisiones realizadas durante la limpieza de datos.

    Cada llamada registra:
    - paso;
    - detalle;
    - cantidad de registros afectados.

    La información puede guardarse posteriormente como CSV.
    """

    def __init__(self):
        self.filas = []

    def __call__(self, paso, detalle, n=None):

        self.filas.append(
            {
                "paso": paso,
                "detalle": detalle,
                "registros_afectados": n
            }
        )

        mensaje = f"[{paso}] {detalle}"

        if n is not None:
            mensaje += f": {n}"

        print(mensaje)

    def guardar(
        self,
        carpeta,
        nombre="registro_limpieza.csv"
    ):
        """
        Guarda la bitácora completa como archivo CSV.
        """

        resultado = pd.DataFrame(self.filas)

        guardar_csv(
            resultado,
            carpeta,
            nombre
        )


# ================================================================
# FILTRO POR TAMAÑO DE MUESTRA
# ================================================================

def filtrar_min_n(
    data,
    columna,
    min_n=MIN_N
):
    """
    Conserva únicamente categorías con al menos `min_n` observaciones.

    Se utiliza principalmente antes de comparar grupos mediante
    pruebas estadísticas.

    Parámetros
    ----------
    data : pandas.DataFrame
        Base de datos.

    columna : str
        Variable categórica que define los grupos.

    min_n : int
        Tamaño mínimo requerido por grupo.

    Retorna
    -------
    pandas.DataFrame
        Datos correspondientes solamente a grupos válidos.
    """

    if columna not in data.columns:
        raise KeyError(
            f"La columna '{columna}' no existe en el DataFrame."
        )

    conteo = data[columna].value_counts()

    grupos_validos = conteo[
        conteo >= min_n
    ].index

    return data[
        data[columna].isin(grupos_validos)
    ].copy()


# ================================================================
# CARGA DE DATOS
# ================================================================

def cargar_base():
    """
    Carga las bases procesadas generadas por la fase 3.

    Devuelve:
    - todos los registros procesados;
    - muestra analítica;
    - resumen de anfitriones.

    También ejecuta validaciones de integridad.
    """

    # Verificar archivos requeridos.
    for ruta in (
        ARCHIVO_ANALITICO,
        ARCHIVO_ANFITRIONES
    ):

        if not ruta.exists():

            raise FileNotFoundError(
                f"No existe {ruta}. "
                "Ejecute primero 01_preparacion_datos.ipynb"
            )

    # Cargar base completa.
    todo = pd.read_csv(
        ARCHIVO_ANALITICO,
        dtype={
            "id_anuncio": str,
            "id_host": str
        }
    )

    exigir(
        "incluido_analisis" in todo.columns,
        "No existe la columna 'incluido_analisis'."
    )

    # Seleccionar muestra analítica.
    analitico = todo.loc[
        todo["incluido_analisis"].eq(True)
    ].copy()

    # Cargar resumen de anfitriones.
    anfitriones = pd.read_csv(
        ARCHIVO_ANFITRIONES,
        dtype={
            "id_host": str
        }
    )

    # ------------------------------------------------------------
    # VALIDACIONES
    # ------------------------------------------------------------

    exigir(
        analitico["id_anuncio"].is_unique,
        "Existen identificadores de anuncios duplicados."
    )

    exigir(
        anfitriones["id_host"].is_unique,
        "Existen identificadores de anfitriones duplicados."
    )

    exigir(
        analitico["precio_cop"].notna().all(),
        "La muestra analítica contiene precios nulos."
    )

    exigir(
        (analitico["precio_cop"] > 0).all(),
        "La muestra analítica contiene precios no positivos."
    )

    exigir(
        analitico["id_host"].nunique()
        == len(anfitriones),
        (
            "La cantidad de anfitriones de la base analítica "
            "no coincide con anfitriones_resumen.csv."
        )
    )

    return todo, analitico, anfitriones


def cargar_resultado(nombre):
    """
    Carga un archivo previamente generado en DIR_RESULTADOS.

    Evita repetir análisis ya realizados por notebooks anteriores.

    Parámetros
    ----------
    nombre : str
        Nombre del archivo CSV.

    Retorna
    -------
    pandas.DataFrame
    """

    ruta = DIR_RESULTADOS / nombre

    if not ruta.exists():

        raise FileNotFoundError(
            f"No existe {ruta}. "
            "Ejecute primero los notebooks correspondientes."
        )

    return pd.read_csv(ruta)


def anfitriones_unicos(data):
    """
    Genera una tabla con un registro por anfitrión.

    Conserva:
    - id_host;
    - número de anuncios.

    Se utiliza, entre otros propósitos, para calcular
    el KPI de anfitriones con varios anuncios.
    """

    columnas = [
        "id_host",
        "n_anuncios"
    ]

    faltantes = [
        columna
        for columna in columnas
        if columna not in data.columns
    ]

    if faltantes:

        raise KeyError(
            f"Faltan columnas requeridas: {faltantes}"
        )

    return (
        data[columnas]
        .drop_duplicates()
        .copy()
    )


# ================================================================
# AJUSTE DE HOLM
# ================================================================

def holm(valores_p):
    """
    Ajusta múltiples valores p mediante el método de Holm.

    El ajuste reduce el riesgo de falsos positivos cuando se
    realizan varias comparaciones estadísticas.

    Parámetros
    ----------
    valores_p : iterable
        Valores p originales.

    Retorna
    -------
    numpy.ndarray
        Valores p ajustados.
    """

    p = np.asarray(
        valores_p,
        dtype=float
    )

    if len(p) == 0:
        return np.array([], dtype=float)

    if np.isnan(p).any():
        raise ValueError(
            "Los valores p no pueden contener NaN."
        )

    orden = np.argsort(p)

    p_ordenados = p[orden]

    multiplicadores = np.arange(
        len(p),
        0,
        -1
    )

    ajustados_ordenados = np.maximum.accumulate(
        p_ordenados * multiplicadores
    )

    ajustados_ordenados = np.minimum(
        ajustados_ordenados,
        1
    )

    ajustados = np.empty(
        len(p)
    )

    ajustados[orden] = ajustados_ordenados

    return ajustados


# ================================================================
# KRUSKAL-WALLIS
# ================================================================

# ================================================================
# KRUSKAL-WALLIS
# ================================================================

def kruskal(data, grupo, variable="precio_cop", min_n=MIN_N):
    """Kruskal-Wallis entre grupos y cálculo de tamaño de efecto."""

    datos = data[[grupo, variable]].dropna().copy()
    datos = filtrar_min_n(datos, grupo, min_n)

    muestras = [
        subgrupo[variable].to_numpy()
        for _, subgrupo in datos.groupby(grupo, sort=True)
    ]

    if len(muestras) < 2:
        raise ValueError("Se requieren al menos dos grupos válidos.")

    estadistico_h, valor_p = stats.kruskal(*muestras)

    n = len(datos)
    k = len(muestras)

    if n <= k:
        raise ValueError(
            "No hay suficientes observaciones para calcular el tamaño de efecto."
        )

    eta2 = max(
        0.0,
        (estadistico_h - k + 1) / (n - k)
    )

    return (
        datos,
        float(estadistico_h),
        float(valor_p),
        float(eta2),
        k
    )

# ================================================================
# POST-HOC DE DUNN
# ================================================================

def dunn(
    data,
    grupo,
    variable="precio_cop"
):
    """
    Prueba post-hoc de Dunn.

    Se utiliza después de Kruskal-Wallis para identificar
    específicamente cuáles pares de grupos presentan diferencias.

    Incluye:
    - corrección por empates;
    - ajuste de Holm para comparaciones múltiples.
    """

    columnas = [
        grupo,
        variable
    ]

    faltantes = [
        columna
        for columna in columnas
        if columna not in data.columns
    ]

    if faltantes:

        raise KeyError(
            f"Faltan columnas requeridas: {faltantes}"
        )

    datos = (
        data[columnas]
        .dropna()
        .copy()
    )

    if datos[grupo].nunique() < 2:

        raise ValueError(
            "Dunn requiere al menos dos grupos."
        )

    # Rangos globales.
    datos["rango"] = stats.rankdata(
        datos[variable]
    )

    n = len(datos)

    if n <= 1:

        raise ValueError(
            "No existen suficientes observaciones."
        )

    # ------------------------------------------------------------
    # Corrección por empates
    # ------------------------------------------------------------

    empates = (
        datos[variable]
        .value_counts()
        .to_numpy(dtype=float)
    )

    varianza = (
        n * (n + 1) / 12
        -
        (
            (empates ** 3 - empates).sum()
            /
            (12 * (n - 1))
        )
    )

    if varianza <= 0:

        raise ValueError(
            "No es posible calcular Dunn: "
            "la varianza de rangos es cero."
        )

    resumen_grupos = (
        datos
        .groupby(grupo)["rango"]
        .agg(
            ["mean", "count"]
        )
    )

    resultados = []

    # Todas las combinaciones de pares posibles.
    for grupo_a, grupo_b in combinations(
        resumen_grupos.index,
        2
    ):

        media_a = resumen_grupos.loc[
            grupo_a,
            "mean"
        ]

        media_b = resumen_grupos.loc[
            grupo_b,
            "mean"
        ]

        n_a = resumen_grupos.loc[
            grupo_a,
            "count"
        ]

        n_b = resumen_grupos.loc[
            grupo_b,
            "count"
        ]

        denominador = np.sqrt(
            varianza
            *
            (
                1 / n_a
                +
                1 / n_b
            )
        )

        z = (
            media_a - media_b
        ) / denominador

        p_bruto = 2 * stats.norm.sf(
            abs(z)
        )

        resultados.append(
            [
                grupo_a,
                grupo_b,
                z,
                p_bruto
            ]
        )

    resultado = pd.DataFrame(
        resultados,
        columns=[
            "grupo_a",
            "grupo_b",
            "z",
            "p_bruto"
        ]
    )

    resultado["p_holm"] = holm(
        resultado["p_bruto"]
    )

    resultado["rechaza_h0"] = (
        resultado["p_holm"] < ALPHA
    )

    return resultado


# ================================================================
# ESTADÍSTICOS DESCRIPTIVOS
# ================================================================

def descriptivos(
    data,
    grupo,
    variable="precio_cop"
):
    """
    Genera estadísticas descriptivas de una variable por grupo.

    Calcula:
    - n;
    - mediana;
    - media;
    - primer cuartil;
    - tercer cuartil;
    - rango intercuartílico.
    """

    columnas = [
        grupo,
        variable
    ]

    faltantes = [
        columna
        for columna in columnas
        if columna not in data.columns
    ]

    if faltantes:

        raise KeyError(
            f"Faltan columnas requeridas: {faltantes}"
        )

    datos = (
        data[columnas]
        .dropna()
        .copy()
    )

    resultado = (
        datos
        .groupby(grupo)[variable]
        .agg(
            n="count",
            mediana="median",
            media="mean",
            q1=lambda x: x.quantile(0.25),
            q3=lambda x: x.quantile(0.75)
        )
    )

    resultado["riq"] = (
        resultado["q3"]
        -
        resultado["q1"]
    )

    resultado = (
        resultado
        .sort_values(
            "mediana",
            ascending=False
        )
        .reset_index()
    )

    return resultado


# ================================================================
# MANN-WHITNEY
# ================================================================

def mann_whitney(
    grupo_a,
    grupo_b
):
    """
    Ejecuta Mann-Whitney U bilateral.

    También calcula delta de Cliff como medida
    del tamaño y dirección del efecto.

    Retorna
    -------
    U : float
    p : float
    delta_cliff : float
    """

    a = (
        pd.Series(grupo_a)
        .dropna()
        .to_numpy()
    )

    b = (
        pd.Series(grupo_b)
        .dropna()
        .to_numpy()
    )

    if len(a) == 0 or len(b) == 0:

        raise ValueError(
            "Mann-Whitney requiere observaciones "
            "en ambos grupos."
        )

    u, p = stats.mannwhitneyu(
        a,
        b,
        alternative="two-sided",
        method="asymptotic"
    )

    delta_cliff = (
        2 * u
        /
        (
            len(a)
            *
            len(b)
        )
        - 1
    )

    return (
        float(u),
        float(p),
        float(delta_cliff)
    )


# ================================================================
# CORRELACIÓN DE SPEARMAN
# ================================================================

def spearman(
    data,
    variable_x,
    variable_y="precio_cop"
):
    """
    Calcula la correlación de Spearman entre dos variables.

    Se utiliza para analizar asociaciones monotónicas sin asumir
    normalidad ni una relación estrictamente lineal.

    Retorna
    -------
    n : int
        Número de observaciones válidas.

    rho : float
        Coeficiente de correlación de Spearman.

    p : float
        Valor p.
    """

    columnas = [
        variable_x,
        variable_y
    ]

    faltantes = [
        columna
        for columna in columnas
        if columna not in data.columns
    ]

    if faltantes:

        raise KeyError(
            f"Faltan columnas requeridas: {faltantes}"
        )

    datos = (
        data[columnas]
        .dropna()
        .copy()
    )

    if len(datos) < 2:

        raise ValueError(
            "No existen suficientes observaciones "
            "para calcular Spearman."
        )

    if datos[variable_x].nunique() < 2:

        raise ValueError(
            f"La variable '{variable_x}' "
            "no presenta suficiente variabilidad."
        )

    if datos[variable_y].nunique() < 2:

        raise ValueError(
            f"La variable '{variable_y}' "
            "no presenta suficiente variabilidad."
        )

    rho, p = stats.spearmanr(
        datos[variable_x],
        datos[variable_y]
    )

    return (
        len(datos),
        float(rho),
        float(p)
    )


# ================================================================
# CONFIGURACIÓN DE FIGURAS
# ================================================================

TEAL = "#117C83"
NAVY = "#253449"
GOLD = "#CA773A"


def aplicar_estilo():
    """
    Aplica una configuración visual común a las figuras
    del proyecto.
    """

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,

            "axes.spines.top": False,
            "axes.spines.right": False,

            "axes.labelcolor": NAVY,
            "axes.titlecolor": NAVY,

            "text.color": NAVY,

            "figure.facecolor": "white",
            "axes.facecolor": "white"
        }
    )


def mostrar_figura(fig):
    """
    Muestra una figura dentro de Jupyter.

    No crea archivos automáticamente.

    Al finalizar libera la figura de memoria.
    """

    fig.tight_layout()

    try:

        from IPython.display import display

        display(fig)

    except ImportError:

        plt.show()

    finally:

        plt.close(fig)
