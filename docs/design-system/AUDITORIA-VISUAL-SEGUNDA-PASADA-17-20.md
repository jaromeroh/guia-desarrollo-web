# Segunda pasada visual de los capítulos 17–20

> Integrada el 3 de agosto de 2026.

## Resultado

La segunda pasada consolidó los esquemas secundarios de cuatro capítulos en
**trece funciones pedagógicas** y **26 SVG**: trece composiciones de escritorio
y trece variantes móviles.

| Cap. | Funciones nuevas | Salida editorial de los demás bloques |
|---:|---|---|
| 17 | Sesión frente a token; passkey; Authorization Code con PKCE; RBAC/ABAC/ReBAC | El flujo offline volvió a una secuencia nativa; JWT y ejemplos permanecen como código |
| 18 | Patrones de conexión; escalado mediante backplane | Comparaciones de HTTP, WebTransport y casos de uso volvieron a tablas; protocolos y payloads permanecen como código |
| 19 | Actualización perdida; MVCC; contratos de caché | Aislamiento, acceso a datos, invalidación y búsqueda volvieron a tablas o prosa |
| 20 | Cola de trabajo; transactional outbox; CQRS; Event Sourcing | Decisión síncrono/asíncrono, fallos, backoff y llamadas frente a eventos volvieron a contenido semántico |

No queda ASCII visual en estos cuatro capítulos. Los bloques monoespaciados que
permanecen son código, payloads o prompts copiables.

## Decisiones de precisión

- OAuth 2.1 se presenta como Internet-Draft revisión 15, no como estándar. RFC
  9700 queda como BCP publicada para OAuth 2.0 y se distinguen sus requisitos de
  los del borrador.
- WebAuthn Level 3 se identifica como Candidate Recommendation Snapshot del 26
  de mayo de 2026.
- Se retiraron promesas de latencia y compatibilidad universal para polling,
  SSE, proxies y CDNs.
- El backplane se separó de la durabilidad: Redis Pub/Sub distribuye mensajes,
  pero no ofrece replay a procesos desconectados.
- Los niveles de aislamiento reflejan la tabla vigente de PostgreSQL 18 e
  incluyen anomalías de serialización.
- Repository y Unit of Work ya no prometen pruebas sin integración ni cambios
  de motor sin coste.
- Se eliminaron umbrales universales para migrar a un motor de búsqueda.
- CQRS se separó de Event Sourcing; ninguno exige automáticamente al otro.

## Validación

- Los 26 SVG superan `validate_diagram.py` sin errores ni advertencias.
- Se renderizaron previsualizaciones de escritorio a 1200 y 736 px y móviles a
  480 y 320 px.
- Las previsualizaciones están en
  `output/diagram-previews/second-pass-17-20/`; los SVG maestros permanecen en
  `assets/diagrams/`.
- La validación web comprueba HTTP 200, selección correcta de variantes móviles,
  imágenes completas y ausencia de desbordamiento horizontal.

## Próximo bloque

La siguiente segunda pasada corresponde a los capítulos 21–23: estrategia de
testing, ramas y feature flags, y despliegue progresivo. Los capítulos 24–29 ya
quedaron sin esquemas secundarios durante la primera pasada.
