from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def generar_inventario(n: int, semilla: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)

    categorias = np.array([
        "Audio", "Computo", "Accesorios", "Telefonia",
        "Almacenamiento", "Video", "Energia"
    ])

    df = pd.DataFrame({
        "producto": [f"Producto_{i:06d}" for i in range(1, n + 1)],
        "categoria": rng.choice(categorias, size=n),
        "stock_actual": rng.integers(0, 250, size=n),
        "ventas_ultimos_30_dias": rng.poisson(lam=80, size=n),
        "stock_minimo": rng.integers(5, 31, size=n),
        "tiempo_reposicion_dias": rng.integers(1, 16, size=n),
    })

    return df


def generar_eventos_jsonl(df: pd.DataFrame, cantidad: int, semilla: int = 42) -> list[dict]:
    rng = np.random.default_rng(semilla + 1)
    indices = rng.integers(0, len(df), size=cantidad)

    eventos = []
    for i, indice in enumerate(indices, start=1):
        fila = df.iloc[indice]
        eventos.append({
            "evento_id": i,
            "producto": fila["producto"],
            "categoria": fila["categoria"],
            "tipo": "venta",
            "unidades": int(rng.integers(1, 6)),
            "canal": str(rng.choice(["web", "tienda", "app"])),
        })

    return eventos


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registros", type=int, default=100000)
    parser.add_argument("--eventos", type=int, default=20000)
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    inventario = generar_inventario(args.registros)
    csv_path = DATA_DIR / "inventario_sintetico.csv"
    inventario.to_csv(csv_path, index=False)

    eventos = generar_eventos_jsonl(inventario, args.eventos)
    jsonl_path = DATA_DIR / "eventos_ventas.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as archivo:
        for evento in eventos:
            archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")

    print(f"CSV generado: {csv_path} ({len(inventario):,} registros)")
    print(f"JSONL generado: {jsonl_path} ({len(eventos):,} eventos)")


if __name__ == "__main__":
    main()
