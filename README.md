# Proyecto Big Data — Analítica prescriptiva

## ¿Qué debería hacerse?

Este proyecto es una práctica sencilla para demostrar el concepto de **analítica prescriptiva**. El caso elegido es la **reposición de inventario**.

La idea es que el sistema no solamente muestre lo que pasó con las ventas, sino que analice los datos y recomiende una acción concreta para cada producto.

## Problema

Una tienda tiene diferentes productos y necesita decidir cuáles debe reponer primero. Si únicamente revisamos el stock actual, podemos equivocarnos porque un producto con pocas unidades puede venderse muy lento, mientras otro con más unidades puede agotarse rápido.

Por eso usamos también:

- ventas de los últimos 30 días;
- stock mínimo;
- tiempo de reposición;
- demanda diaria estimada.

## Flujo del proyecto

**Datos → Análisis → Resultado → Recomendación → Acción**

1. **Datos:** se lee el archivo CSV del inventario.
2. **Análisis:** se calcula la demanda diaria y el punto de reorden.
3. **Resultado:** se compara el stock actual contra ese punto.
4. **Recomendación:** el sistema indica `REPONER`, `MANTENER` o `REVISAR SOBRESTOCK`.
5. **Acción:** cuando se recomienda reponer, también se calcula una cantidad sugerida.

## Reglas de decisión

- Si el stock actual es menor o igual al punto de reorden, se recomienda **REPONER**.
- Si existe demasiado inventario comparado con la demanda, se recomienda **REVISAR SOBRESTOCK**.
- En los demás casos se recomienda **MANTENER**.

El punto de reorden se calcula con:

`demanda durante el tiempo de reposición + stock mínimo`

## Estructura

```text
analitica-prescriptiva-big-data/
│
├── README.md
├── requirements.txt
├── src/
│   └── main.py
│
├── data/
│   ├── inventario.csv
│   └── README.md
│
├── docs/
│   ├── arquitectura.md
│   └── evidencias/
│       ├── ejecucion.txt
│       └── resultado_recomendaciones.csv
│
└── .gitignore
```

## Requisitos

- Python 3.10 o superior.
- pip.

## Instalación

```bash
git clone https://github.com/diegoponchotrejo-png/analitica-prescriptiva-big-data.git
cd analitica-prescriptiva-big-data
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python src/main.py
```

El programa muestra las recomendaciones en terminal y genera:

```text
docs/evidencias/resultado_recomendaciones.csv
```

## Demostración para la exposición

1. **Problema:** decidir qué productos se deben reponer.
2. **Datos:** abrir `data/inventario.csv`.
3. **Arquitectura/solución:** mostrar `docs/arquitectura.md`.
4. **Código:** abrir `src/main.py`.
5. **Ejecución:** correr `python src/main.py`.
6. **Resultados:** revisar las recomendaciones y el CSV.
7. **Interpretación:** explicar por qué algunos productos deben reponerse y otros no.

## ¿Dónde está la analítica prescriptiva?

La parte prescriptiva aparece cuando el sistema convierte el análisis en una recomendación concreta. No se queda solamente en “este producto vendió 90 unidades”, sino que indica qué hacer con ese producto.

## Ventajas

- Fácil de entender y ejecutar.
- Las recomendaciones tienen una justificación visible.
- Relaciona datos históricos con una decisión.
- Puede ampliarse con más reglas o modelos.

## Limitaciones

- El dataset es pequeño y didáctico.
- Las reglas son simplificadas.
- No considera promociones, estacionalidad, costos, proveedores o cambios repentinos de demanda.
- En un sistema real se necesitarían más datos y validaciones.

## Conclusión

La analítica prescriptiva sirve para convertir datos en acciones. En este proyecto, los datos de inventario se transforman en recomendaciones concretas para apoyar la decisión de reponer, mantener o revisar productos.

## Integrantes

Agregar aquí los nombres de los integrantes del equipo antes de entregar.

## Conclusiones individuales

Cada integrante debe agregar su propia conclusión antes de la entrega final.
