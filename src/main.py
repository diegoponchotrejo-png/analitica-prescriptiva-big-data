from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = BASE_DIR / "data" / "inventario.csv"
OUTPUT_DIR = BASE_DIR / "docs" / "evidencias"
OUTPUT_PATH = OUTPUT_DIR / "resultado_recomendaciones.csv"

# Política del ejemplo: después de cubrir el tiempo de reposición,
# buscamos conservar 7 días adicionales de demanda.
DIAS_COBERTURA_EXTRA = 7


def cargar_datos(ruta: Path) -> pd.DataFrame:
    """Carga un CSV de inventario."""
    return pd.read_csv(ruta)


def validar_y_limpiar_datos(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Valida estructura, nulos, duplicados y valores imposibles."""
    requeridas = {
        "producto",
        "stock_actual",
        "ventas_ultimos_30_dias",
        "stock_minimo",
        "tiempo_reposicion_dias",
    }

    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {sorted(faltantes)}")

    limpio = df.copy()
    reporte = {
        "registros_iniciales": len(limpio),
        "nulos_detectados": int(limpio[list(requeridas)].isna().sum().sum()),
        "duplicados_detectados": int(limpio.duplicated(subset=["producto"]).sum()),
    }

    # Quitamos filas sin datos indispensables y productos duplicados.
    limpio = limpio.dropna(subset=list(requeridas))
    limpio = limpio.drop_duplicates(subset=["producto"], keep="last")

    numericas = [
        "stock_actual",
        "ventas_ultimos_30_dias",
        "stock_minimo",
        "tiempo_reposicion_dias",
    ]

    for columna in numericas:
        limpio[columna] = pd.to_numeric(limpio[columna], errors="coerce")

    limpio = limpio.dropna(subset=numericas)

    # No tienen sentido inventarios, ventas o tiempos negativos.
    mascara_valida = (
        (limpio["stock_actual"] >= 0)
        & (limpio["ventas_ultimos_30_dias"] >= 0)
        & (limpio["stock_minimo"] >= 0)
        & (limpio["tiempo_reposicion_dias"] > 0)
    )
    registros_invalidos = int((~mascara_valida).sum())
    limpio = limpio.loc[mascara_valida].copy()

    reporte["registros_invalidos_eliminados"] = registros_invalidos
    reporte["registros_finales"] = len(limpio)

    return limpio, reporte


def analizar_inventario(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores y aplica reglas prescriptivas de inventario."""
    resultado = df.copy()

    # Promedio simple de demanda diaria con base en 30 días.
    resultado["demanda_diaria"] = (
        resultado["ventas_ultimos_30_dias"] / 30
    ).round(2)

    # Demanda estimada mientras llega un nuevo pedido.
    resultado["demanda_durante_reposicion"] = (
        resultado["demanda_diaria"] * resultado["tiempo_reposicion_dias"]
    ).round(2)

    # Fórmula clásica:
    # Punto de reorden = demanda durante lead time + stock de seguridad.
    # En este proyecto, stock_minimo funciona como stock de seguridad.
    resultado["punto_reorden"] = (
        resultado["demanda_durante_reposicion"] + resultado["stock_minimo"]
    ).round(0).astype(int)

    # Nivel objetivo: cubrir el lead time + una semana adicional de demanda
    # + el stock mínimo. La semana extra es una política explícita y configurable,
    # no un porcentaje arbitrario.
    resultado["nivel_objetivo"] = (
        resultado["stock_minimo"]
        + resultado["demanda_diaria"]
        * (resultado["tiempo_reposicion_dias"] + DIAS_COBERTURA_EXTRA)
    ).round(0).astype(int)

    recomendaciones = []
    cantidades = []
    razones = []

    for _, fila in resultado.iterrows():
        stock = int(fila["stock_actual"])
        punto = int(fila["punto_reorden"])
        objetivo = int(fila["nivel_objetivo"])
        ventas = int(fila["ventas_ultimos_30_dias"])

        if stock <= punto:
            cantidad = max(objetivo - stock, 1)
            recomendaciones.append("REPONER")
            cantidades.append(cantidad)
            razones.append(
                f"Stock ({stock}) <= punto de reorden ({punto}); "
                f"se sugieren {cantidad} unidades para acercarse al nivel objetivo ({objetivo})."
            )
        elif stock > max(objetivo * 2, ventas * 1.5):
            recomendaciones.append("REVISAR SOBRESTOCK")
            cantidades.append(0)
            razones.append(
                f"Stock ({stock}) es alto frente al nivel objetivo ({objetivo}) "
                "y a la demanda reciente."
            )
        else:
            recomendaciones.append("MANTENER")
            cantidades.append(0)
            razones.append(
                f"Stock ({stock}) está por encima del punto de reorden ({punto}) "
                "y dentro de un rango razonable."
            )

    resultado["recomendacion"] = recomendaciones
    resultado["cantidad_sugerida"] = cantidades
    resultado["justificacion"] = razones

    prioridad = {"REPONER": 1, "MANTENER": 2, "REVISAR SOBRESTOCK": 3}
    resultado["prioridad"] = resultado["recomendacion"].map(prioridad)
    resultado = resultado.sort_values(
        ["prioridad", "stock_actual"]
    ).drop(columns="prioridad")

    return resultado


def generar_graficas(resultado: pd.DataFrame) -> None:
    """Genera gráficas sencillas como evidencia del análisis."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    conteo = resultado["recomendacion"].value_counts()
    plt.figure(figsize=(8, 5))
    conteo.plot(kind="bar")
    plt.title("Cantidad de productos por recomendación")
    plt.xlabel("Recomendación")
    plt.ylabel("Número de productos")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grafica_recomendaciones.png", dpi=150)
    plt.savefig(OUTPUT_DIR / "grafica_recomendaciones.svg")
    plt.close()

    muestra = resultado.head(20).copy()
    x = range(len(muestra))

    plt.figure(figsize=(12, 6))
    plt.bar(x, muestra["stock_actual"], label="Stock actual")
    plt.plot(x, muestra["punto_reorden"], marker="o", label="Punto de reorden")
    plt.xticks(x, muestra["producto"], rotation=70, ha="right")
    plt.title("Stock actual vs. punto de reorden")
    plt.ylabel("Unidades")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "grafica_stock_vs_reorden.png", dpi=150)
    plt.savefig(OUTPUT_DIR / "grafica_stock_vs_reorden.svg")
    plt.close()


def imprimir_resumen(resultado: pd.DataFrame, reporte_calidad: dict) -> None:
    print("\n=== CALIDAD DE DATOS ===")
    for clave, valor in reporte_calidad.items():
        print(f"{clave}: {valor}")

    print("\n=== SISTEMA PRESCRIPTIVO DE INVENTARIO ===")
    print(f"Productos analizados: {len(resultado)}")
    print(f"Reponer: {(resultado['recomendacion'] == 'REPONER').sum()}")
    print(f"Mantener: {(resultado['recomendacion'] == 'MANTENER').sum()}")
    print(
        "Revisar sobrestock: "
        f"{(resultado['recomendacion'] == 'REVISAR SOBRESTOCK').sum()}"
    )

    columnas = [
        "producto",
        "stock_actual",
        "punto_reorden",
        "nivel_objetivo",
        "recomendacion",
        "cantidad_sugerida",
    ]

    # Para datasets grandes mostramos una muestra, no miles de filas.
    print("\nPrimeras recomendaciones:\n")
    print(resultado[columnas].head(20).to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sistema prescriptivo para reposición de inventario."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Ruta del archivo CSV de inventario.",
    )
    args = parser.parse_args()

    df = cargar_datos(args.data)
    df_limpio, reporte = validar_y_limpiar_datos(df)
    resultado = analizar_inventario(df_limpio)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(OUTPUT_PATH, index=False)
    generar_graficas(resultado)
    imprimir_resumen(resultado, reporte)

    print(f"\nResultado completo: {OUTPUT_PATH}")
    print(f"Gráficas generadas en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
