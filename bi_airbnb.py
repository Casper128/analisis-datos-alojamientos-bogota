"""Utilidades compartidas por los notebooks del proyecto BI Airbnb Bogotá.

Concentra lo que antes se repetía en los scripts: rutas, constantes, lectura/escritura de CSV,
filtro de muestra mínima, pruebas estadísticas y estilo de figuras.
Los notebooks 01-04 solo contienen la lógica propia de cada fase.
"""
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# ------------------------------------------------------------------ rutas
# Todo es relativo a la carpeta donde viven los notebooks y este módulo.
RAIZ = Path(__file__).resolve().parent
ENTRADA = RAIZ / "datos" / "listings_bogota.csv"

DIR_FASE3 = RAIZ / "salida_fase3"        # salida de la fase 3 (modelo dimensional)
DIR_RESULTADOS = RAIZ / "resultados"     # salida de las fases 4 a 6 (lo que consume Tableau)
ARCHIVO_ANALITICO = DIR_FASE3 / "airbnb_bogota_analitico.csv"
ARCHIVO_ANFITRIONES = DIR_FASE3 / "anfitriones_resumen.csv"

# ------------------------------------------------------------------ constantes
ALPHA = .05
SEED = 20261018
MIN_N = 30          # tamaño mínimo de grupo para H1 y H2
N_ITER_SENSIBILIDAD = 100


# ------------------------------------------------------------------ utilidades generales
def guardar_csv(frame, carpeta, nombre):
    """CSV UTF-8 con BOM (acentos correctos en Excel, Power BI y Tableau)."""
    Path(carpeta).mkdir(parents=True, exist_ok=True)
    frame.to_csv(Path(carpeta) / nombre, index=False, encoding="utf-8-sig")


def exigir(condicion, mensaje):
    if not condicion:
        raise ValueError(mensaje)


class Registro:
    """Bitácora de decisiones de limpieza: imprime cada paso y luego se guarda como CSV."""

    def __init__(self):
        self.filas = []

    def __call__(self, paso, detalle, n=None):
        self.filas.append({"paso": paso, "detalle": detalle, "registros_afectados": n})
        print(f"[{paso}] {detalle}" + (f": {n}" if n is not None else ""))

    def guardar(self, carpeta, nombre="registro_limpieza.csv"):
        guardar_csv(pd.DataFrame(self.filas), carpeta, nombre)


def filtrar_min_n(data, columna, min_n=MIN_N):
    """Conserva solo los grupos de `columna` con al menos `min_n` filas."""
    conteo = data[columna].value_counts()
    return data[data[columna].isin(conteo[conteo >= min_n].index)]


def cargar_base():
    """Lee la salida validada de la fase 3. Devuelve (todo, analitico, anfitriones)."""
    for ruta in (ARCHIVO_ANALITICO, ARCHIVO_ANFITRIONES):
        if not ruta.exists():
            raise FileNotFoundError(f"No existe {ruta}. Ejecute primero 01_preparacion_datos.ipynb")
    todo = pd.read_csv(ARCHIVO_ANALITICO, dtype={"id_anuncio": str, "id_host": str})
    d = todo.loc[todo.incluido_analisis.eq(True)].copy()
    hosts = pd.read_csv(ARCHIVO_ANFITRIONES, dtype={"id_host": str})
    exigir(d.id_anuncio.is_unique and hosts.id_host.is_unique, "Identificadores duplicados")
    exigir((d.precio_cop > 0).all(), "La muestra analítica contiene precios no positivos")
    exigir(d.id_host.nunique() == len(hosts), "Anfitriones del análisis y del resumen no concilian")
    return todo, d, hosts


def anfitriones_unicos(d):
    """Un registro por anfitrión con su cantidad de anuncios (base de K6)."""
    return d[["id_host", "n_anuncios"]].drop_duplicates()


# ------------------------------------------------------------------ estadística
def holm(p):
    p = np.asarray(p, dtype=float)
    orden = np.argsort(p)
    ajustado = np.empty(len(p))
    ajustado[orden] = np.minimum(1, np.maximum.accumulate(p[orden] * np.arange(len(p), 0, -1)))
    return ajustado


def kruskal(data, grupo):
    """Kruskal-Wallis sobre precio_cop. Devuelve (submuestra, H, p, eta²_H, k grupos)."""
    d = filtrar_min_n(data, grupo)
    muestras = [g.precio_cop.to_numpy() for _, g in d.groupby(grupo)]
    h, p = stats.kruskal(*muestras)
    n, k = len(d), len(muestras)
    # Eta cuadrado basada en H. No confundir con epsilon de rangos H/(n-1).
    return d, float(h), float(p), float((h - k + 1) / (n - k)), k


def dunn(data, grupo):
    """Post-hoc de Dunn con corrección de empates y ajuste de Holm."""
    d = data[[grupo, "precio_cop"]].dropna().copy()
    d["rango"] = stats.rankdata(d.precio_cop)
    n = len(d)
    empates = d.precio_cop.value_counts().to_numpy(dtype=float)
    varianza = n * (n + 1) / 12 - ((empates**3 - empates).sum() / (12 * (n - 1)))
    g = d.groupby(grupo).rango.agg(["mean", "count"])
    filas = []
    for a, b in combinations(g.index, 2):
        z = (g.loc[a, "mean"] - g.loc[b, "mean"]) / np.sqrt(
            varianza * (1 / g.loc[a, "count"] + 1 / g.loc[b, "count"]))
        filas.append([a, b, z, 2 * stats.norm.sf(abs(z))])
    out = pd.DataFrame(filas, columns=["grupo_a", "grupo_b", "z", "p_bruto"])
    out["p_holm"] = holm(out.p_bruto)
    out["rechaza_h0"] = out.p_holm < ALPHA
    return out


def descriptivos(d, grupo):
    out = d.groupby(grupo).precio_cop.agg(
        n="count", mediana="median", media="mean",
        q1=lambda x: x.quantile(.25), q3=lambda x: x.quantile(.75))
    out["riq"] = out.q3 - out.q1
    return out.sort_values("mediana", ascending=False).reset_index()


def mann_whitney(a, b):
    """Devuelve (U, p bilateral asintótico, delta de Cliff)."""
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided", method="asymptotic")
    return float(u), float(p), 2 * u / (len(a) * len(b)) - 1


def spearman(data, variable):
    """Spearman entre `variable` y precio_cop. Devuelve (n, rho, p)."""
    sub = data[[variable, "precio_cop"]].dropna()
    rho, p = stats.spearmanr(sub[variable], sub.precio_cop)
    return len(sub), rho, p


# ------------------------------------------------------------------ figuras
TEAL, NAVY, GOLD = "#117C83", "#253449", "#CA773A"


def aplicar_estilo():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.labelcolor": NAVY, "text.color": NAVY})


def mostrar_figura(fig):
    """Muestra el diagnóstico en el notebook sin crear archivos de imagen."""
    from IPython.display import display
    fig.tight_layout()
    display(fig)
    plt.close(fig)


def cargar_resultado(nombre):
    """Reutiliza las tablas calculadas por 02/03; no repite los contrastes."""
    ruta = DIR_RESULTADOS / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No existe {ruta}. Ejecute los notebooks 02 y 03 primero.")
    return pd.read_csv(ruta)


INDICADORES_H5 = ["precio_mediano", "ocupacion_media_dias", "resenas_12m_media", "calificacion_mediana"]


def comparar_anfitriones(hosts, umbral):
    varios = hosts.loc[hosts.n_anuncios.ge(umbral)]
    uno = hosts.loc[hosts.n_anuncios.eq(1)]
    resultados = []
    for metrica in INDICADORES_H5:
        a, b = varios[metrica].dropna(), uno[metrica].dropna()
        u, p, delta = mann_whitney(a, b)
        resultados.append([umbral, metrica, len(a), len(b), a.median(), b.median(), u, p, delta])
    res = pd.DataFrame(resultados, columns=["umbral_varios", "metrica", "n_varios", "n_uno",
                                            "mediana_varios", "mediana_uno", "u", "p_bruto", "delta_Cliff"])
    res.insert(8, "p_holm", holm(res.p_bruto))
    return res



def sensibilidad_por_anfitrion(d, n_iter=N_ITER_SENSIBILIDAD, seed=SEED):
    """Selecciones reproducibles de un anuncio por host; no es bootstrap."""
    CONTRASTES_GRUPOS = [("H1", "localidad"), ("H2", "tipo_alojamiento")]
    CONTRASTES_CORRELACION = [("H3", "capacidad"), ("H4", "calificacion")]
    rng = np.random.default_rng(seed)
    posiciones = list(d.reset_index(drop=True).groupby("id_host", sort=True).indices.values())
    filas_sens = []
    for iteracion in range(1, n_iter + 1):
        sub = d.iloc[[rng.choice(idx) for idx in posiciones]]
        for hip, campo in CONTRASTES_GRUPOS:
            sub_k, h, p, eta, k = kruskal(sub, campo)
            filas_sens.append([iteracion, hip, len(sub_k), k, eta, p])
        for hip, campo in CONTRASTES_CORRELACION:
            n, rho, p = spearman(sub, campo)
            filas_sens.append([iteracion, hip, n, np.nan, rho, p])
    
    sens = pd.DataFrame(filas_sens, columns=["iteracion", "hipotesis", "n", "grupos", "efecto", "p"])
    return sens
