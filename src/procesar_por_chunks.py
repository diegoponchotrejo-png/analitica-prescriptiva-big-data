from pathlib import Path
import argparse
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA = BASE_DIR / "data" / "inventario_sintetico.csv"


def procesar_por_chunks(ruta: Path, tamano_chunk: int = 20000) -> None:
    total = 0
    suma_stock = 0
    suma_ventas = 0
    chunks = 0

    for bloque in pd.read_csv(ruta, chunksize=tamano_chunk):
        chunks += 1
        total += len(bloque)
        suma_stock += bloque["stock_actual"].sum()
        suma_ventas += bloque["ventas_ultimos_30_dias"].sum()
        print(f"Chunk {chunks}: {len(bloque):,} registros procesados")

    print("\n=== RESUMEN DE PROCESAMIENTO POR CHUNKS ===")
    print(f"Registros procesados: {total:,}")
    print(f"Chunks utilizados: {chunks}")
    print(f"Stock total: {int(suma_stock):,}")
    print(f"Ventas totales 30 días: {int(suma_ventas):,}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--chunk", type=int, default=20000)
    args = parser.parse_args()
    procesar_por_chunks(args.data, args.chunk)


if __name__ == "__main__":
    main()
