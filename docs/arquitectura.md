# Arquitectura del proyecto

## Arquitectura de la práctica

```text
Fuentes de datos
├── inventario.csv
├── inventario_sintetico.csv (generado localmente)
└── eventos_ventas.jsonl (generado localmente)
          │
          ▼
Extracción / lectura
├── pandas.read_csv()
└── lectura de eventos JSONL
          │
          ▼
Calidad de datos
├── columnas requeridas
├── nulos
├── duplicados
└── valores negativos o inválidos
          │
          ▼
Transformación
├── demanda diaria
├── demanda durante lead time
├── punto de reorden
└── nivel objetivo
          │
          ▼
Analítica prescriptiva
├── REPONER
├── MANTENER
└── REVISAR SOBRESTOCK
          │
          ▼
Resultados
├── CSV de recomendaciones
├── salida en terminal
└── gráficas
          │
          ▼
Acción
└── apoyar la decisión de compra/reposición
```

## ¿Dónde entra Big Data?

La práctica no pretende construir una infraestructura empresarial completa de Big Data. El objetivo es demostrar el principio con una solución reproducible y escalable a mayor volumen.

Para reforzar el concepto se incluyen:

- un generador capaz de crear 100,000 o más registros sintéticos;
- eventos de venta en formato JSONL para mostrar variedad de formatos;
- procesamiento por bloques o **chunks**, evitando cargar necesariamente todo el archivo de gran tamaño a memoria;
- validación y limpieza de datos antes del análisis;
- separación entre fuentes, procesamiento, analítica y salida.

En una arquitectura real de mayor escala, esta misma lógica podría ejecutarse sobre almacenamiento distribuido, un data lake y motores como Apache Spark. Aquí no se implementan porque la actividad busca primero comprender los principios antes de usar infraestructura especializada.

## Escalamiento conceptual

```text
Fuentes (POS / e-commerce / ERP / APIs / eventos)
                    │
                    ▼
             Data Lake / Storage
                    │
                    ▼
       Procesamiento distribuido (Spark)
                    │
                    ▼
        Datos limpios y consolidados
                    │
                    ▼
        Motor analítico prescriptivo
                    │
                    ▼
      Dashboard / ERP / recomendación
```

El flujo principal solicitado sigue siendo:

**Datos → Análisis → Resultado → Recomendación → Acción**
