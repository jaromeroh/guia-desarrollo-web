# Auditoría visual · segunda pasada del capítulo 30

> Integración completada el 3 de agosto de 2026.

## Resultado

La pasada añade **5 funciones pedagógicas**, cada una con composición de
escritorio y móvil: **10 SVG** nuevos. El capítulo queda con ocho pares visuales
en total al sumar el ciclo del agente, MCP y el control de autonomía de la
primera pasada.

| Función | Pregunta que responde | Tipología |
|---|---|---|
| Contexto vigente | ¿Cómo reduce la documentación el espacio de búsqueda sin sustituir la verificación? | Proceso con retorno |
| Contratos de ejecución | ¿Qué cambia entre una función, un modelo lingüístico y un agente? | Comparación estructurada |
| Constructor y jardinero | ¿Cuándo controlar directamente y cuándo preparar condiciones? | Comparación estructurada |
| Condiciones organizacionales | ¿Qué debe aportar el sistema de trabajo para producir cambios revisables? | Mapa de sistema |
| Orquestación multiagente | ¿Cuándo paralelizar y cómo vuelven los entregables a una integración verificable? | Mapa de sistema |

## Consolidación del ASCII

De los once bloques monoespaciados detectados:

- Cinco relaciones se convirtieron en diagramas.
- Cuatro ejemplos, listas o comparaciones volvieron a Markdown semántico.
- El árbol de `docs/` y el árbol de una skill permanecen como texto copiable.

También se convirtió la comparación «antes / con agentes» en una tabla. Los
prompts que el lector puede reutilizar se conservaron como texto.

## Decisiones editoriales

- La documentación reduce exploración solo cuando está vigente; una diferencia
  con el código se trata como evidencia que debe investigarse.
- La estocasticidad del modelo no es el único origen de variabilidad: un agente
  incorpora herramientas, permisos, red y estado externo.
- Constructor y jardinero no son identidades excluyentes; el grado de control
  directo depende del riesgo, la reversibilidad y la calidad del oráculo.
- La efectividad de los agentes también depende de convenciones, guardrails y
  prácticas compartidas por la organización.
- El paralelismo multiagente requiere tareas independientes, contratos de
  entrada y salida, y una integración explícita.

## Archivos

- `cap30-contexto-vigente{,-mobile}.svg`
- `cap30-modelos-ejecucion{,-mobile}.svg`
- `cap30-constructor-jardinero{,-mobile}.svg`
- `cap30-condiciones-organizacionales{,-mobile}.svg`
- `cap30-orquestacion-multiagente{,-mobile}.svg`

Las previsualizaciones a 1200, 736, 480 y 320 px están en
`output/diagram-previews-second-pass-30/`.

## Verificación

- 10 de 10 SVG superaron `validate_diagram.py`.
- Todas las composiciones se revisaron a 1200, 736, 480 y 320 px.
- Los dos bloques ASCII restantes son árboles copiables y deliberados.
- `book:audit-references`: 407 referencias, 375 enlaces y 0 fallos.
- `book:build`: 37 páginas; compilación correcta.
- HonKit local respondió HTTP 200 y cargó las variantes móviles a 390 × 844
  sin errores de consola.
