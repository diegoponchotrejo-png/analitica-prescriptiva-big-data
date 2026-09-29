# Las 5 V de Big Data aplicadas al proyecto

Este proyecto usa un caso de inventarios para relacionar la analítica prescriptiva con las cinco características comunes de Big Data.

## 1. Volumen

El archivo de demostración contiene pocos productos para que la explicación sea sencilla. Sin embargo, el proyecto incluye `src/generar_dataset.py`, que permite generar 100,000 registros o más.

Ejemplo:

```bash
python src/generar_dataset.py --registros 100000 --eventos 20000
```

La intención es mostrar que la lógica no depende únicamente de los 10 registros de ejemplo.

## 2. Velocidad

En una empresa real, las ventas y movimientos de inventario llegan continuamente desde cajas, aplicaciones o comercio electrónico.

La práctica trabaja principalmente en modo batch, pero el archivo `eventos_ventas.jsonl` representa eventos que podrían llegar de manera continua y actualizar indicadores con mayor frecuencia.

## 3. Variedad

Se contemplan dos formatos:

- CSV para el inventario consolidado.
- JSONL para eventos de venta.

En un entorno empresarial podrían agregarse APIs, bases de datos, archivos de proveedores, sensores o registros de aplicaciones.

## 4. Veracidad

La veracidad se relaciona con la confiabilidad de los datos.

Antes de generar recomendaciones, `main.py` valida:

- columnas obligatorias;
- valores nulos;
- productos duplicados;
- números negativos;
- tiempos de reposición no válidos.

Una recomendación puede ser incorrecta si los datos de entrada también lo son.

## 5. Valor

El valor aparece cuando los datos producen una utilidad concreta.

En este caso, el sistema convierte información de inventario y ventas en acciones sugeridas:

- REPONER;
- MANTENER;
- REVISAR SOBRESTOCK.

Por eso el objetivo no es simplemente almacenar muchos datos, sino utilizarlos para apoyar una decisión.

## Nota importante

Tener 100,000 registros no convierte automáticamente una práctica en una plataforma Big Data real. El dataset sintético se utiliza para demostrar volumen y escalabilidad. Una implementación empresarial podría requerir infraestructura distribuida cuando la escala, velocidad o variedad superaran las capacidades de una sola computadora.
