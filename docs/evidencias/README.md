# Evidencias del proyecto

Esta carpeta contiene los resultados que utilizamos para comprobar el funcionamiento del análisis.

Al ejecutar:

```bash
python src/main.py
```

se actualizan automáticamente:

- `resultado_recomendaciones.csv`: cálculos y recomendación de cada producto.
- `grafica_recomendaciones.png` y `.svg`: cantidad de productos por tipo de recomendación.
- `grafica_stock_vs_reorden.png` y `.svg`: comparación del stock actual contra el punto de reorden.

Los archivos SVG se conservan en GitHub para poder ver las gráficas directamente desde el README.

Con el dataset de ejemplo se obtienen 6 productos para reponer, 1 para mantener y 3 para revisar por posible sobrestock.

Para hacer una prueba de mayor volumen:

```bash
python src/generar_dataset.py --registros 100000 --eventos 20000
python src/main.py --data data/inventario_sintetico.csv
```

Para probar lectura por bloques:

```bash
python src/procesar_por_chunks.py --data data/inventario_sintetico.csv --chunk 20000
```

El dataset grande se genera localmente y no se guarda en el repositorio para evitar subir archivos pesados.
