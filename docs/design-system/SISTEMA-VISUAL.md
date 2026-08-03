# Sistema visual del libro

> Estado: aprobado para producción el 31 de julio de 2026.

## Propósito

Las imágenes deben hacer visible una relación que el texto obliga a reconstruir
mentalmente: una secuencia, una dependencia, una jerarquía, una comparación, un
estado o una transición. No se añadirá una imagen para decorar cada capítulo ni
para repetir un párrafo.

El libro utiliza un único lenguaje: **editorial técnico luminoso**. El blueprint
y el cuaderno técnico se conservan únicamente como exploraciones históricas
descartadas.

## Dos modos, una sola identidad

### Ilustración conceptual

Se utiliza en aperturas o transiciones cuando una escena narrativa ayuda a
orientar al lector. Se produce como imagen rasterizada, evita texto incrustado y
debe mantener una composición simple. Los iconos sin función pedagógica se
eliminan.

### Diagrama técnico

Se utiliza para procesos, secuencias, arquitecturas, decisiones, estados y
datos. Se construye como SVG determinista para conservar precisión, edición,
accesibilidad y buena impresión. El PNG es un respaldo de inspección, no la
fuente principal.

## Paleta

| Token | Valor | Función principal |
|---|---|---|
| Papel | `#F2EEE6` | Fondo exterior de la lámina |
| Superficie | `#FFFDFA` | Área principal y tarjetas |
| Tinta | `#20262E` | Texto y estructura principal |
| Azul petróleo | `#31536A` | Flujo principal y elementos técnicos |
| Terracota | `#B95736` | Riesgo, error o transición crítica |
| Ocre | `#C59132` | Datos, decisión o estado intermedio |
| Borde ocre | `#B68125` | Contornos que requieren mayor contraste |
| Gris cálido | `#A9A49B` | Contexto, bordes y relaciones secundarias |
| Texto secundario | `#59636D` | Explicaciones y conectores secundarios |

El color nunca será el único portador de significado. Debe reforzarse mediante
texto, forma, posición o patrón de línea.

## Tipografía y jerarquía

- Tipografía principal: `system-ui`, con alternativas del sistema.
- Monoespaciada solo para código, protocolos, nombres literales o valores.
- Títulos breves; una etiqueta de familia puede aparecer dentro de la lámina,
  pero no debe duplicar el encabezado del capítulo.
- Oraciones y explicaciones extensas permanecen en el cuerpo del libro.
- Las mayúsculas sostenidas se reservan para etiquetas pequeñas de orientación.

## Gramática de formas y conectores

- Rectángulos redondeados: componentes, etapas o responsabilidades.
- Círculos: estados o ciclos, no componentes arbitrarios.
- Contenedores: fronteras del sistema, del proceso o de confianza.
- Línea continua: flujo o transición principal.
- Línea discontinua: trabajo programado, retorno o relación secundaria, siempre
  acompañada por una etiqueta o leyenda.
- Terracota: excepción o fallo; no se utiliza para decorar.
- Flechas: expresan dirección. Las líneas sin dirección representan asociación.

Cada familia conserva su notación. Un modelo de datos no debe parecer un flujo
y una máquina de estados no debe reducirse a una lista de pasos.

## Composición y respuesta a distintos anchos

- Lienzo horizontal de referencia: entre 1000 y 1200 unidades de ancho.
- La versión de escritorio debe verificarse a 760 px de ancho real.
- A 420 px deben seguir legibles el concepto y las etiquetas esenciales.
- Si el texto secundario deja de ser legible, se crea una composición móvil
  simplificada o se divide el contenido en dos láminas; no basta con encogerlo.
- Las escenas conceptuales pueden conservar una proporción panorámica si no
  contienen texto indispensable.

## Accesibilidad

- Cada referencia Markdown incluye texto alternativo que expresa la función de
  la imagen, no una lista exhaustiva de formas.
- Cada SVG contiene `role="img"`, `<title>` y `<desc>` coherentes.
- Las relaciones complejas se explican también en el texto cercano.
- Se verifica contraste, escala de grises y orden de lectura.
- Ningún dato necesario para copiar, buscar o ejecutar queda atrapado en una
  imagen.

## Archivos

- Producción: `assets/diagrams/capNN-concepto.svg` o `.png`.
- Fuente principal de diagramas: SVG.
- Respaldo de inspección: PNG con el mismo nombre base.
- Exploraciones y versiones rechazadas: `assets/diagrams/explorations/`.
- No se eliminan los recursos sustituidos hasta cerrar la auditoría visual.

## Flujo editorial

1. Confirmar que la imagen resuelve una necesidad del inventario.
2. Reducir el contenido a una pregunta pedagógica concreta.
3. Construir una primera composición con la plantilla apropiada.
4. Revisar exactitud técnica, ortografía y accesibilidad.
5. Probar a 760 px y 420 px.
6. Integrar en un único capítulo y compilar la versión local.
7. Aprobar antes de producir el siguiente lote.

## Recursos iniciales aprobados

| Capítulo | Recurso | Función |
|---:|---|---|
| 1 | `cap01-mapa-aplicacion.svg` | Mapa de fronteras y responsabilidades |
| 1 | `cap01-html-renderizado.svg` | Proceso técnico |
| 1 | `cap01-http-cliente-servidor.svg` | Intercambio de mensajes |
| 1 | `cap01-capas-aplicacion.svg` | Jerarquía de responsabilidades |
| 1 | `cap01-decisiones-arquitectura.svg` | Comparación en dos dimensiones |
| 1 | `cap01-viaje-peticion.svg` | Secuencia entre actores |
| 2 | `cap02-html-contrato.svg` | Una fuente semántica produce varias capacidades |
| 2 | `cap02-formulario-peticion.svg` | Secuencia de interfaz a protocolo |
| 2 | `cap02-validacion-fronteras.svg` | Responsabilidades y frontera de confianza |
| 2 | `cap02-mejora-progresiva.svg` | Capas acumulativas y degradación útil |
| 3 | `cap03-cascada-resolucion.svg` | Secuencia de desempate de la cascada |
| 3 | `cap03-caja-desbordamiento.svg` | Composición de la caja y diagnóstico de overflow |
| 3 | `cap03-eleccion-layout.svg` | Elección entre flujo normal, Flexbox y Grid |
| 3 | `cap03-media-container.svg` | Alcance de media queries y container queries |
| 4 | `cap04-event-loop.svg` | Proceso técnico |
| 5 | `cap05-url-origen.svg` | Frontera conceptual: componentes de una URL y origen |
| 5 | `cap05-capas-conexion.svg` | Diagnóstico por responsabilidades y evidencia |
| 5 | `cap05-cache-revalidacion.svg` | Árbol de decisión de frescura y validación |
| 5 | `cap05-seguridad-navegador.svg` | Comparación de mecanismos de seguridad del navegador |
| 6 | `cap06-evolucion-rol.png` | Ilustración conceptual |
| 6 | `cap06-ciclo-desarrollo.svg` | Ciclo con retorno de evidencia |
| 7 | `cap07-frontera-componente.svg` | Frontera entre contrato e implementación |
| 7 | `cap07-acoplamiento-cohesion.svg` | Comparación de dos dimensiones del diseño |
| 7 | `cap07-tradeoffs-contexto.svg` | Marco contextual para decisiones técnicas |
| 7 | `cap07-flujo-carrito.svg` | Flujo entre actores, fallos y retorno |
| 8 | `cap08-redistribucion-trabajo.svg` | Comparación de distribución del trabajo |
| 8 | `cap08-ciclo-evidencia.svg` | Ciclo iterativo con evidencia observable |
| 8 | `cap08-verificacion-riesgo.svg` | Matriz de impacto e incertidumbre |
| 9 | `cap09-iceberg-requerimiento.svg` | Capas visibles y ocultas del requerimiento |
| 9 | `cap09-descubrimiento-contraste.svg` | Comparación de fuentes de descubrimiento |
| 10 | `cap10-proceso-diseno.svg` | Proceso iterativo para reducir incertidumbre |
| 10 | `cap10-estados-ui.svg` | Comparación de estados esenciales de interfaz |
| 11 | `cap11-dependencias-arquitectura.svg` | Dirección de dependencias hacia las reglas |
| 11 | `cap11-mvc-flujo.svg` | Coordinación entre usuario, controlador, modelo y vista |
| 11 | `cap11-comparacion-patrones.svg` | Capas, Clean Architecture y arquitectura hexagonal |
| 12 | `cap12-contrato-api.svg` | Coordinación entre necesidad, solicitud, contrato y respuesta |
| 12 | `cap12-api-first-paralelo.svg` | Desarrollo paralelo contra un contrato compartido |
| 12 | `cap12-eleccion-estilo-api.svg` | Comparación entre REST, GraphQL y tRPC |
| 13 | `cap13-niveles-modelado.svg` | Niveles conceptual, lógico, físico y evolución |
| 13 | `cap13-modelo-ecommerce.svg` | Entidades, claves y cardinalidades del e-commerce |
| 13 | `cap13-indice-btree.svg` | Reducción del espacio de búsqueda mediante un índice |
| 14 | `cap14-slice-vertical.svg` | Capacidad completa a través de las capas |
| 14 | `cap14-matriz-riesgos.svg` | Priorización por probabilidad e impacto |
| 14 | `cap14-diagramas-utiles.svg` | Diferencia entre mapa de contexto y flujo |
| 14 | `cap14-ciclo-planificacion.svg` | Planificación como ciclo de aprendizaje |
| 15 | `cap15-estrategias-renderizado.svg` | Distribución de trabajo y frescura por estrategia |
| 15 | `cap15-dependencias-features.svg` | Reglas de composición y dependencia frontend |
| 15 | `cap15-tipos-estado.svg` | Propiedad del estado local, compartido y del servidor |
| 16 | `cap16-pipeline-backend.svg` | Responsabilidades que atraviesa una solicitud |
| 17 | `cap17-flujos-identidad.svg` | Separación entre credencial, sesión y permisos |
| 17 | `cap17-sesion-token-revocacion.svg` | Estado y revocación en sesiones y tokens |
| 17 | `cap17-passkey-desafio.svg` | Desafío y firma de una passkey |
| 17 | `cap17-oauth-pkce.svg` | Secuencia Authorization Code con PKCE |
| 17 | `cap17-modelos-autorizacion.svg` | Comparación RBAC, ABAC y ReBAC |
| 18 | `cap18-eleccion-tiempo-real.svg` | Elección gradual del canal de comunicación |
| 18 | `cap18-patrones-conexion.svg` | Intercambio en polling, long polling, SSE y WebSocket |
| 18 | `cap18-escalado-backplane.svg` | Conexiones distribuidas mediante un backplane |
| 19 | `cap19-transaccion-consistencia.svg` | Invariante, transacción y propagación posterior |
| 19 | `cap19-concurrencia-perdida.svg` | Actualización perdida por lectura concurrente |
| 19 | `cap19-mvcc-snapshots.svg` | Versiones visibles según snapshots e aislamiento |
| 19 | `cap19-patrones-cache.svg` | Comparación de tres contratos de caché |
| 20 | `cap20-ciclo-job-confiable.svg` | Persistencia, ejecución y recuperación de trabajo asíncrono |
| 20 | `cap20-circuit-breaker.svg` | Máquina de estados |
| 20 | `cap20-arquitectura-cola.svg` | Separación entre productor, cola, worker y estado |
| 20 | `cap20-outbox-eventos.svg` | Cambio de dominio y publicación mediante outbox |
| 20 | `cap20-cqrs-proyeccion.svg` | Separación entre escritura y proyección de lectura |
| 20 | `cap20-event-sourcing.svg` | Estado derivado de un stream de eventos |
| 21 | `cap21-estrategia-testing.svg` | Capas de evidencia proporcional al riesgo |
| 22 | `cap22-pipeline-entrega.svg` | Cambio, validación, artefacto, despliegue y liberación |
| 23 | `cap23-despliegue-progresivo.svg` | Exposición gradual con promoción o reversión |
| 24 | `cap24-correlacion-senales.svg` | Investigación correlacionada de un incidente |
| 25 | `cap25-ciclo-capacidad.svg` | Presupuesto, medición, protección y verificación |
| 26 | `cap26-fronteras-confianza.svg` | Controles por frontera de confianza |
| 27 | `cap27-slice-nextjs.svg` | Slice vertical con mecanismos de Next.js |
| 28 | `cap28-slice-fastapi.svg` | El mismo slice con mecanismos de FastAPI |
| 29 | `cap29-slice-go.svg` | El mismo slice con mecanismos de Go |
| 30 | `cap30-ciclo-agente.svg` | Ciclo de intención, acción y verificación |
| 30 | `cap30-mcp-interoperabilidad.svg` | Fronteras entre persona, host, MCP y sistema externo |
| 30 | `cap30-control-autonomia.svg` | Alcance, permisos, aprobaciones y parada |
| 31 | `cap31-filtro-adopcion.svg` | De una novedad a una decisión operable |
| Apéndice C | `apc-ruta-aprendizaje.svg` | Recorrido acumulativo de aprendizaje |

Los capítulos 1–31 trabajados y el apéndice C incluyen variantes `-mobile.svg` para sus diagramas
densos. El corte habitual es 600 px. El viaje de la petición del capítulo 1 y
los recursos de los capítulos 2, 3 y 5–31, además del apéndice C, cambian a una composición vertical hasta
820 px porque sus relaciones horizontales pierden legibilidad antes que el
resto de los recursos.

## Secuencia de producción

La producción conserva una revisión **capítulo por capítulo**, aunque el primer
barrido puede agrupar capítulos consecutivos. Los capítulos 1 a 10 quedan como
casos cerrados y fijan el flujo: auditar todo lo existente, consolidar
funciones, corregir el texto asociado, integrar una única composición por
necesidad y validar localmente antes de abrir el capítulo siguiente.

Los capítulos 11 a 15 completaron su segunda pasada con once funciones nuevas.
Los únicos bloques monoespaciados que permanecen son árboles de carpetas y
migraciones, conservados como texto copiable. Los capítulos 17 a 19 mantienen
la consolidación secundaria registrada en
`AUDITORIA-VISUAL-CAPITULOS-10-19.md`.

Los capítulos 20 a 29 también cuentan con ancla integrada. Los capítulos 20–23
mantienen una segunda pasada de consolidación registrada en
`AUDITORIA-VISUAL-CAPITULOS-20-29.md`. La serie 27–29 comparte geometría,
contrato y orden de responsabilidades para permitir una comparación honesta.

Los capítulos 30–31 y el apéndice C cierran la primera pasada completa del
manuscrito. El capítulo 30 mantiene siete bloques secundarios en revisión; el
resto de la producción pendiente corresponde a consolidación, accesibilidad e
inspección, no a capítulos sin dirección visual.
