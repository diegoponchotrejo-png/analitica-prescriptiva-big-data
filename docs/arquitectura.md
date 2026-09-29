# Arquitectura del proyecto

## Flujo general

```text
┌───────────────────────┐
│  Dataset inventario   │
│   data/inventario.csv │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Lectura y validación  │
│      con pandas       │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│      Análisis         │
│ demanda diaria        │
│ punto de reorden      │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Reglas de decisión    │
│ REPONER / MANTENER /  │
│ REVISAR SOBRESTOCK    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Recomendación y       │
│ cantidad sugerida     │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Resultado CSV +       │
│ salida en terminal    │
└───────────────────────┘
```

Este flujo representa la idea solicitada en la actividad:

**Datos → Análisis → Resultado → Recomendación → Acción**
