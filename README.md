# Proyecto Big Data — Analítica prescriptiva

## ¿Qué debería hacerse?

Este proyecto demuestra un caso de **analítica prescriptiva aplicada a inventarios**. El sistema recibe datos de productos, valida su calidad, calcula indicadores de reposición y genera una recomendación concreta para apoyar la decisión de compra.

La idea principal es:

**Datos → Limpieza → Análisis → Resultado → Recomendación → Acción**

## Problema

Una tienda necesita decidir qué productos debe reponer, cuáles puede mantener y cuáles podrían tener exceso de inventario.

Para tomar la decisión usamos:

- stock actual;
- ventas de los últimos 30 días;
- stock mínimo o stock de seguridad;
- tiempo de reposición;
- demanda diaria estimada;
- punto de reorden;
- nivel objetivo de inventario.

## Analítica prescriptiva

La analítica descriptiva responde **qué ocurrió**.

La analítica predictiva responde **qué podría ocurrir**.

La analítica prescriptiva responde **qué debería hacerse**.

En este proyecto, la parte prescriptiva aparece cuando el sistema recomienda una acción:

- **REPONER**
- **MANTENER**
- **REVISAR SOBRESTOCK**

## Fórmulas principales

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

### Cantidad sugerida

Se eliminó el porcentaje arbitrario de 35%. Ahora se utiliza una política explícita de cobertura:

```text
nivel_objetivo =
stock_minimo +
demanda_diaria × (tiempo_reposicion_dias + 7)
```

Los 7 días representan una semana adicional de cobertura y pueden modificarse en `DIAS_COBERTURA_EXTRA`.

Cuando hay que reponer:

```text
cantidad_sugerida = nivel_objetivo - stock_actual
```

## Calidad de datos

Antes de analizar, el programa revisa:

- columnas obligatorias;
- valores nulos;
- productos duplicados;
- valores negativos;
- tiempos de reposición inválidos.

Esto evita generar recomendaciones utilizando datos incorrectos.

## Big Data y las 5 V

El proyecto incluye documentación específica en:

```text
docs/5v_big_data.md
```

Resumen:

- **Volumen:** se puede generar un dataset sintético de 100,000, 500,000 o más registros.
- **Velocidad:** se simulan eventos de ventas que podrían llegar continuamente.
- **Variedad:** se utilizan CSV y JSONL.
- **Veracidad:** se valida y limpia la información antes de analizarla.
- **Valor:** los datos terminan convirtiéndose en recomendaciones de negocio.

Importante: el proyecto es una **demostración académica**. Generar muchos registros no significa que una sola computadora se convierta automáticamente en una plataforma Big Data de producción. La arquitectura está preparada conceptualmente para explicar cómo escalaría.

## Dataset pequeño y dataset grande

Para explicar fácilmente el programa se conserva:

```text
data/inventario.csv
```

con 10 productos.

Para demostrar volumen se puede generar un dataset sintético:

```bash
python src/generar_dataset.py --registros 100000 --eventos 20000
```

Esto genera:

```text
data/inventario_sintetico.csv
data/eventos_ventas.jsonl
```

Los archivos grandes no se suben a GitHub porque pueden volver innecesariamente pesado el repositorio. El código permite recrearlos.

## Procesamiento de mayor volumen

También se incluye un ejemplo de lectura por bloques:

```bash
python src/procesar_por_chunks.py --data data/inventario_sintetico.csv --chunk 20000
```

Esto procesa el archivo en partes en lugar de cargar todos los registros de una sola vez.

No es procesamiento distribuido, pero demuestra una técnica útil cuando aumenta el volumen. En un entorno empresarial, la misma idea podría migrarse a tecnologías como Apache Spark.

## Gráficas

Al ejecutar el proyecto se generan:

- `docs/evidencias/grafica_recomendaciones.png`
- `docs/evidencias/grafica_stock_vs_reorden.png`

Sirven para mostrar visualmente:

- cuántos productos están en cada recomendación;
- cómo se compara el stock actual con el punto de reorden.

## Metodología

La metodología completa está en:

```text
docs/metodologia.md
```

Incluye:

1. extracción;
2. limpieza y validación;
3. transformación;
4. análisis;
5. generación de recomendación;
6. presentación de resultados.

## Arquitectura

La arquitectura se encuentra en:

```text
docs/arquitectura.md
```

Se explica tanto la arquitectura de la práctica como una posible evolución hacia una arquitectura de mayor escala con almacenamiento distribuido y procesamiento tipo Spark.

## Estructura del repositorio

```text
analitica-prescriptiva-big-data/
│
├── README.md
├── requirements.txt
├── src/
│   ├── main.py
│   ├── generar_dataset.py
│   └── procesar_por_chunks.py
│
├── data/
│   ├── inventario.csv
│   └── README.md
│
├── docs/
│   ├── arquitectura.md
│   ├── 5v_big_data.md
│   ├── metodologia.md
│   ├── referencias.md
│   └── evidencias/
│       ├── README.md
│       ├── ejecucion.txt
│       └── resultado_recomendaciones.csv
│
└── .gitignore
```

## Instalación

Requisitos:

- Python 3.10 o superior.
- pip.

Clonar:

```bash
git clone https://github.com/diegoponchotrejo-png/analitica-prescriptiva-big-data.git
cd analitica-prescriptiva-big-data
```

Crear entorno virtual:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar:

```bash
pip install -r requirements.txt
```

## Ejecución básica

```bash
python src/main.py
```

## Ejecución con dataset grande

Primero:

```bash
python src/generar_dataset.py --registros 100000 --eventos 20000
```

Después:

```bash
python src/main.py --data data/inventario_sintetico.csv
```

## Demostración para la exposición

Seguir este orden:

1. **Problema:** decidir qué productos reponer.
2. **Datos:** explicar las columnas del dataset.
3. **Arquitectura/solución:** mostrar `docs/arquitectura.md`.
4. **Código:** explicar `src/main.py`.
5. **Ejecución:** correr el programa.
6. **Resultados:** revisar CSV y gráficas.
7. **Interpretación:** justificar por qué el sistema recomienda cada acción.

## Ventajas

- Recomendaciones justificables.
- Fórmulas más claras y configurables.
- Validación de calidad de datos.
- Dataset sintético para demostrar volumen.
- Soporte de CSV y JSONL para explicar variedad.
- Gráficas para interpretar resultados.
- Procesamiento por chunks para mostrar manejo de archivos grandes.
- Proyecto reproducible desde GitHub.

## Limitaciones

- La práctica no implementa infraestructura Big Data distribuida real.
- El dataset sintético no sustituye datos empresariales reales.
- La demanda diaria se estima mediante un promedio simple.
- No se modelan estacionalidad, promociones, costos de pedido o restricciones de proveedor.
- La regla de sobrestock es una heurística simplificada.

## Referencias

Consultar:

```text
docs/referencias.md
```

Se incluyen referencias de IBM para las 5 V y documentación de Oracle sobre punto de reorden e inventarios.

## Conclusión

El proyecto muestra cómo pasar de datos de inventario a una decisión concreta. También refuerza la relación con Big Data mediante volumen sintético, variedad de formatos, validación de calidad, procesamiento por bloques y una arquitectura conceptual escalable.

## Integrantes

Agregar aquí los nombres de los integrantes del equipo.

## Conclusiones individuales

Cada integrante debe agregar su propia conclusión antes de la entrega final.
