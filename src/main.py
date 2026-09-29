from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "inventario.csv"
OUTPUT_PATH = BASE_DIR / "docs" / "evidencias" / "resultado_recomendaciones.csv"


def cargar_datos(ruta: Path = DATA_PATH) -> pd.DataFrame:
    """Carga el dataset de inventario y valida las columnas necesarias."""
    df = pd.read_csv(ruta)
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
    return df


def analizar_inventario(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica reglas simples de decisión para recomendar una acción."""
    resultado = df.copy()

    resultado["demanda_diaria"] = (
        resultado["ventas_ultimos_30_dias"] / 30
    ).round(2)

    resultado["demanda_durante_reposicion"] = (
        resultado["demanda_diaria"] * resultado["tiempo_reposicion_dias"]
    ).round(2)

    resultado["punto_reorden"] = (
        resultado["demanda_durante_reposicion"] + resultado["stock_minimo"]
    ).round(0).astype(int)

    recomendaciones = []
    cantidades = []
    razones = []

    for _, fila in resultado.iterrows():
        stock = int(fila["stock_actual"])
        punto = int(fila["punto_reorden"])
        ventas = int(fila["ventas_ultimos_30_dias"])

        if stock <= punto:
            objetivo = max(punto + int(round(ventas * 0.35)), punto)
            cantidad = max(objetivo - stock, 1)
            recomendaciones.append("REPONER")
            cantidades.append(cantidad)
            razones.append(
                f"Stock ({stock}) <= punto de reorden ({punto}); hay riesgo de faltante."
            )
        elif stock > max(punto * 2, ventas * 1.5):
            recomendaciones.append("REVISAR SOBRESTOCK")
            cantidades.append(0)
            razones.append(
                f"Stock ({stock}) es alto frente al punto de reorden ({punto}) y la demanda reciente."
            )
        else:
            recomendaciones.append("MANTENER")
            cantidades.append(0)
            razones.append(
                f"Stock ({stock}) se encuentra por encima del punto de reorden ({punto})."
            )

    resultado["recomendacion"] = recomendaciones
    resultado["cantidad_sugerida"] = cantidades
    resultado["justificacion"] = razones

    prioridad = {"REPONER": 1, "MANTENER": 2, "REVISAR SOBRESTOCK": 3}
    resultado["prioridad"] = resultado["recomendacion"].map(prioridad)
    resultado = resultado.sort_values(["prioridad", "stock_actual"]).drop(columns="prioridad")

    return resultado


def imprimir_resumen(resultado: pd.DataFrame) -> None:
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
        "recomendacion",
        "cantidad_sugerida",
    ]
    print("\nRecomendaciones:\n")
    print(resultado[columnas].to_string(index=False))


def main() -> None:
    df = cargar_datos()
    resultado = analizar_inventario(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(OUTPUT_PATH, index=False)

    imprimir_resumen(resultado)
    print(f"\nResultado completo guardado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
