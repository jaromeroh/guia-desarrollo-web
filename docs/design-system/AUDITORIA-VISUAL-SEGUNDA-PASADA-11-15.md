# Segunda pasada visual de los capítulos 11–15

> Integrada y verificada el 3 de agosto de 2026.

## Resultado

La segunda pasada consolidó los esquemas secundarios de cinco capítulos en
**once funciones pedagógicas** y **22 SVG**: once composiciones de escritorio y
once variantes móviles.

| Cap. | Funciones nuevas | Salida editorial de los demás bloques |
|---:|---|---|
| 11 | Flujo MVC; comparación entre capas, Clean y Hexagonal | Comparaciones y señales volvieron a tablas o prosa; se conservan dos árboles de carpetas |
| 12 | Trabajo paralelo API-first; elección entre REST, GraphQL y tRPC | Ejemplos HTTP permanecen como código; estados, compatibilidad y documentación pasaron a tablas o listas |
| 13 | Modelo lógico del e-commerce; búsqueda mediante B-Tree | Modelos NoSQL y normalización pasaron a tablas o prosa; se conserva el árbol de migraciones |
| 14 | Matriz de riesgos; mapa de contexto frente a flujo; ciclo de planificación | Estimación, riesgos y flujo asistido por IA volvieron a contenido semántico |
| 15 | Reglas de dependencia por feature; propiedad del estado | Las secuencias CSR/SSR/SSG volvieron a prosa; se conservan dos árboles de proyecto |

Los cinco bloques monoespaciados que permanecen son árboles de archivos. Son
copiables, buscables y se entienden mejor como texto nativo que como imágenes.

## Decisiones de precisión

- Se eliminó la regla `features → app/store`. `app` queda como raíz de
  composición; las features no dependen de la capa superior ni se importan
  entre sí.
- Se retiraron duraciones universales para migraciones de base de datos y
  cambios de proveedor. Un puerto reduce la superficie del cambio, pero no
  elimina migraciones, diferencias semánticas ni operación.
- El B-Tree se explica como reducción logarítmica del espacio de búsqueda sin
  prometer un número fijo de comparaciones o lecturas.
- El modelo lógico explicita que `Pedido 1:1 Pago` exige una restricción o un
  modelo distinto si existen múltiples intentos.
- Los umbrales de LCP, INP y CLS y el reemplazo de FID se contrastaron con la
  referencia vigente de Web Vitals antes de convertir el ASCII a una tabla.

## Validación

- Los 22 SVG superan `validate_diagram.py` sin errores ni advertencias.
- Se renderizaron previsualizaciones de escritorio a 1200 y 736 px y móviles a
  480 y 320 px.
- HonKit sirve los cinco capítulos y todos los recursos con HTTP 200.
- La comprobación en navegador a 1280 y 420 px confirmó cero imágenes rotas,
  cero desbordamiento horizontal y selección correcta de las once variantes
  `-mobile.svg`.
- Las previsualizaciones están en
  `output/diagram-previews/second-pass/`; los SVG maestros permanecen en
  `assets/diagrams/`.

## Próximo bloque

La siguiente segunda pasada corresponde a los capítulos 17–20: sesión, token y
PKCE; secuencias de tiempo real; concurrencia, MVCC y caché; colas y eventos.
