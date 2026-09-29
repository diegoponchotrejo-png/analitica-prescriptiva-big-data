# Dataset

El proyecto utiliza dos niveles de datos.

## Dataset pequeño

`inventario.csv` contiene 10 registros y se conserva porque facilita explicar cada resultado durante la exposición.

Columnas:

- `producto`: nombre del producto.
- `stock_actual`: unidades disponibles.
- `ventas_ultimos_30_dias`: ventas recientes.
- `stock_minimo`: reserva mínima utilizada como stock de seguridad.
- `tiempo_reposicion_dias`: días que tarda una reposición.

## Dataset sintético de mayor volumen

No se almacena directamente en GitHub para evitar subir archivos innecesariamente grandes.

Se genera con:

```bash
python src/generar_dataset.py --registros 100000 --eventos 20000
```

Esto crea:

- `data/inventario_sintetico.csv`
- `data/eventos_ventas.jsonl`

Se puede cambiar el volumen:

```bash
python src/generar_dataset.py --registros 500000 --eventos 100000
```

El dataset es sintético y se usa únicamente con fines académicos para demostrar escalabilidad y las características de Big Data.
