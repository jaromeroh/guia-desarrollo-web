# Auditoría visual de cierre

> Revisión completada el 3 de agosto de 2026 sobre la versión local de HonKit.

## Alcance

La auditoría cubrió la introducción, los 31 capítulos, los cinco apéndices y
todas las fuentes SVG que el manuscrito referencia. Se comprobaron tres
niveles independientes:

1. estructura, paleta, accesibilidad y geometría interna del SVG;
2. renderizado estático a anchos de escritorio y móvil;
3. carga real dentro de HonKit mediante Chromium.

## Resultado

| Control | Cobertura | Resultado |
|---|---:|---:|
| SVG referenciados | 185 | 0 errores y 0 advertencias |
| Páginas de contenido en HonKit | 37 | 37 cargaron correctamente |
| Anchos comprobados | 1280 px y 390 px | 74 cargas de página |
| Imágenes cargadas por el navegador | 190 | 0 rotas |
| Variantes responsive | escritorio y móvil | 0 selecciones incorrectas |
| Texto alternativo | todas las imágenes | 0 ausencias |
| Desbordamiento horizontal de imágenes | todas las imágenes | 0 casos |
| Consola y errores de página | 74 cargas | 0 errores |
| Referencias editoriales | 407 referencias y 375 enlaces | 0 fallos |
| Build de HonKit | 37 páginas | correcto |

Las 190 cargas corresponden a 95 ubicaciones de imagen comprobadas en dos
anchos. Los 185 SVG incluyen las fuentes de escritorio y sus variantes móviles;
el navegador selecciona una sola fuente de cada par en cada carga.

## Correcciones de cierre

- Se normalizaron colores heredados a la paleta editorial aprobada.
- Se corrigieron textos cortados o demasiado próximos al `viewBox` en los
  capítulos 1–8 y 20.
- Se eliminaron etiquetas verticales difíciles de leer en las composiciones
  móviles del event loop y del circuit breaker.
- Se aumentó de 13 a 14 px la tipografía secundaria móvil que aún quedaba en
  varios diagramas de los capítulos 2 y 5–9.
- Se ajustaron saltos de línea en procesos, matrices y conclusiones móviles.
- Se añadió asociación `data-container` a la familia de diagramas generados
  por lotes y se corrigió su densidad tipográfica.
- Se verificó lado a lado la serie de stacks de los capítulos 27–29.
- Se corrigió el renderizador de previsualizaciones para conservar el ancho
  solicitado y usar Quick Look cuando ImageMagick no interpreta un SVG.
- Se ajustó la densidad tipográfica de la ruta de aprendizaje del apéndice C
  para evitar desbordamientos en sus seis etapas.

## Evidencia

- Comparación de stacks: `output/diagram-previews-stacks-27-29-v4/`.
- Capturas de los stacks en HonKit: `output/playwright/stacks-27-29/`.
- Láminas corregidas en la pasada final:
  `output/diagram-previews-final-sweep/`.
- Capturas puntuales del navegador: `output/playwright/`.
- Auditor automático reutilizable: `scripts/playwright_visual_audit.js`.

## Estado editorial

La fase de imágenes del manuscrito actual queda cerrada. No quedan recursos
rotos, gráficos ASCII pendientes de sustitución ni incidencias visuales
conocidas que bloqueen la publicación. Los árboles de archivos, el código, los
payloads y las tablas simples permanecen como contenido nativo y copiable, de
acuerdo con el sistema visual.
