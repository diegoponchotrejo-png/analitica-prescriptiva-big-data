# Evidencias

Al ejecutar:

```bash
python src/main.py
```

se generan automáticamente:

- `resultado_recomendaciones.csv`
- `grafica_recomendaciones.png`
- `grafica_stock_vs_reorden.png`

Para demostrar mayor volumen:

```bash
python src/generar_dataset.py --registros 100000 --eventos 20000
python src/main.py --data data/inventario_sintetico.csv
```

Y para demostrar lectura por bloques:

```bash
python src/procesar_por_chunks.py --data data/inventario_sintetico.csv --chunk 20000
```

No es necesario subir el dataset sintético grande al repositorio; puede generarse siguiendo estas instrucciones.
