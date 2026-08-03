# Auditoría visual · segunda pasada de los capítulos 21–23

> Integración completada el 3 de agosto de 2026.

## Resultado

La pasada añade **9 funciones pedagógicas**, cada una con composición de
escritorio y móvil: **18 SVG** en total. Los 27 recuadros ASCII que quedaban en
estos capítulos se consolidaron en estas imágenes o se transformaron en
Markdown nativo cuando su contenido era una lista, una tabla o una advertencia.

| Capítulo | Función | Pregunta que responde | Tipología |
|---:|---|---|---|
| 21 | Modelos de confianza | ¿Cómo cambia el foco entre pirámide, Trophy y una estrategia guiada por riesgo? | Comparación estructurada |
| 21 | Nivel de prueba | ¿Qué nivel conserva la fidelidad necesaria con el menor coste? | Comparación estructurada |
| 21 | TDD con agentes | ¿Cómo se convierte una prueba en evidencia revisable durante el trabajo de un agente? | Proceso con bucle |
| 22 | CI, entrega y despliegue | ¿Dónde termina la automatización y dónde queda la decisión de promoción? | Comparación estructurada |
| 22 | Estrategias de ramas | ¿Cómo cambia el tamaño del lote entre GitFlow, GitHub Flow y trunk-based? | Comparación estructurada |
| 22 | Ciclo de una bandera | ¿Cómo se crea, expone, apaga y retira una feature flag? | Proceso con retorno |
| 23 | Espectro de hosting | ¿Qué responsabilidad conserva el equipo al aumentar la abstracción? | Comparación estructurada |
| 23 | Estrategias de despliegue | ¿Cómo cambian exposición, coste y recuperación entre rolling, blue-green y canary? | Comparación estructurada |
| 23 | Promoción de artefactos | ¿Cómo avanza el mismo artefacto entre ambientes sin reconstruirse? | Proceso |

## Decisiones editoriales

- La pirámide y el Trophy se presentan como modelos históricos de inversión, no
  como cuotas universales de pruebas.
- Las pruebas se eligen por la propiedad y el riesgo que deben comprobar.
- CI, entrega y despliegue continuo se separan por el punto donde queda la
  decisión, no por una simple sucesión de herramientas.
- Branching se explica como control del tamaño del lote y de la coordinación.
- Las feature flags tienen propietario, caducidad y retirada; un *kill switch*
  no revierte datos ni efectos externos.
- Hosting se compara por responsabilidad operativa y requisitos, no por etapa
  de la empresa o prestigio tecnológico.
- Rolling, blue-green y canary no prometen reversión automática de datos.
- Preview y staging validan propiedades diferentes; la paridad no exige que
  todos los ambientes sean idénticos.

## Archivos

Los pares definitivos están en `assets/diagrams/`:

- `cap21-modelos-confianza{,-mobile}.svg`
- `cap21-eleccion-nivel-prueba{,-mobile}.svg`
- `cap21-tdd-agente-evidencia{,-mobile}.svg`
- `cap22-ci-entrega-despliegue{,-mobile}.svg`
- `cap22-branching-lotes{,-mobile}.svg`
- `cap22-ciclo-feature-flag{,-mobile}.svg`
- `cap23-espectro-hosting{,-mobile}.svg`
- `cap23-estrategias-despliegue{,-mobile}.svg`
- `cap23-promocion-artefacto{,-mobile}.svg`

Las previsualizaciones de revisión se generaron a 1200, 736, 480 y 320 px en
`output/diagram-previews-second-pass-21-23/`. Las capturas de HonKit están en
`output/playwright/`.

## Verificación

- 18 de 18 SVG superaron `validate_diagram.py`.
- Las 18 composiciones se revisaron en 1200, 736, 480 y 320 px.
- `book:audit-references`: 407 referencias, 375 enlaces, 0 fallos.
- `book:build`: 37 páginas; compilación correcta.
- HonKit local: capítulos 21, 22 y 23 respondieron HTTP 200.
- Navegador real a 1440 × 1000 y 390 × 844: imágenes cargadas, variantes
  móviles seleccionadas, sin errores de consola.

## Riesgo pendiente

Las comparaciones móviles son deliberadamente largas: priorizan texto legible
sobre una miniatura compacta. Conviene mantener el selector `picture` y no
reemplazar estas variantes por el SVG horizontal en pantallas estrechas.
