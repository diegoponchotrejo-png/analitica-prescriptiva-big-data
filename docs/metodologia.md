# Metodología del proyecto

La metodología se dividió en cinco etapas.

## 1. Extracción

Los datos se obtienen desde archivos de inventario.

- `data/inventario.csv`: muestra pequeña para explicar el funcionamiento.
- `inventario_sintetico.csv`: dataset de mayor volumen generado por el proyecto.
- `eventos_ventas.jsonl`: eventos simulados para representar otra fuente/formato.

## 2. Limpieza y calidad

Antes del análisis se revisan:

1. columnas requeridas;
2. valores nulos;
3. productos duplicados;
4. valores numéricos inválidos;
5. cantidades negativas;
6. tiempos de reposición menores o iguales a cero.

Los registros inválidos se excluyen del análisis y se genera un resumen de calidad.

## 3. Transformación

Se crean variables derivadas.

### Demanda diaria

```text
demanda_diaria = ventas_ultimos_30_dias / 30
```

### Demanda durante el tiempo de reposición

```text
demanda_lead_time = demanda_diaria × tiempo_reposicion_dias
```

### Punto de reorden

```text
punto_reorden = demanda_lead_time + stock_minimo
```

En esta práctica, `stock_minimo` funciona como stock de seguridad.

### Nivel objetivo

```text
nivel_objetivo =
stock_minimo +
demanda_diaria × (tiempo_reposicion_dias + 7)
```

Los 7 días representan una política explícita de una semana de cobertura adicional después del tiempo de reposición. Está definida en la constante `DIAS_COBERTURA_EXTRA` y puede modificarse.

## 4. Análisis y decisión

Reglas:

- Si `stock_actual <= punto_reorden` → **REPONER**.
- Si el stock es demasiado alto frente al nivel objetivo y la demanda reciente → **REVISAR SOBRESTOCK**.
- En otro caso → **MANTENER**.

Cuando se requiere reposición:

```text
cantidad_sugerida = nivel_objetivo - stock_actual
```

Así se eliminó el porcentaje arbitrario de 35% y se sustituyó por una política de cobertura entendible y configurable.

## 5. Presentación de resultados

El programa produce:

- tabla en terminal;
- CSV con resultados completos;
- gráfica de cantidad de productos por recomendación;
- gráfica de stock actual contra punto de reorden.

Esto permite interpretar el resultado y justificar la acción recomendada.
