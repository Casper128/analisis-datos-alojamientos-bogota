"""Utilidades compartidas por los notebooks del proyecto BI Airbnb Bogotá.

Concentra lo que antes se repetía en los scripts: rutas, constantes, lectura/escritura de CSV,
descriptivos y correlación de Spearman.
Los notebooks 01-04 solo contienen la lógica propia de cada fase.
"""
from pathlib import Path

import pandas as pd
from scipy import stats

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




def cargar_base():
    """Lee la salida validada de la fase 3. Devuelve (todo, analitico, anfitriones)."""
    todo = pd.read_csv(ARCHIVO_ANALITICO, dtype={"id_anuncio": str, "id_host": str})
    d = todo.loc[todo.incluido_analisis.eq(True)].copy()
    hosts = pd.read_csv(ARCHIVO_ANFITRIONES, dtype={"id_host": str})
    return todo, d, hosts


def anfitriones_unicos(d):
    """Un registro por anfitrión con su cantidad de anuncios (base de K6)."""
    return d[["id_host", "n_anuncios"]].drop_duplicates()


# ------------------------------------------------------------------ estadística


def descriptivos(d, grupo):
    out = d.groupby(grupo).precio_cop.agg(
        n="count", mediana="median", media="mean",
        q1=lambda x: x.quantile(.25), q3=lambda x: x.quantile(.75))
    out["riq"] = out.q3 - out.q1
    return out.sort_values("mediana", ascending=False).reset_index()


def spearman(data, variable):
    """Spearman entre `variable` y precio_cop. Devuelve (n, rho, p)."""
    sub = data[[variable, "precio_cop"]].dropna()
    rho, p = stats.spearmanr(sub[variable], sub.precio_cop)
    return len(sub), rho, p


def cargar_resultado(nombre):
    """Reutiliza las tablas calculadas por 02/03; no repite los contrastes."""
    return pd.read_csv(DIR_RESULTADOS / nombre)
