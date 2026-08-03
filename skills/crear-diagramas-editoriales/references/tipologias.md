# Tipologías de diagramas

## Selección

| Pregunta narrativa | Tipología |
|---|---|
| ¿Qué piezas existen y cómo se conectan? | Mapa de sistema |
| ¿Qué ocurre y en qué orden? | Proceso |
| ¿Quién habla con quién y cuándo? | Secuencia |
| ¿Qué opción elegir según dos ejes? | Matriz |
| ¿En qué estado está y qué lo cambia? | Máquina de estados |
| ¿Qué entidades y cardinalidades existen? | Modelo de datos |
| ¿Qué depende de qué? | Capas o jerarquía |
| ¿Qué cambia entre alternativas? | Comparación estructurada |
| ¿Qué verá el usuario? | Wireframe anotado |

No convertir automáticamente cada bloque ASCII en una imagen. Mantener como
contenido nativo de GitBook:

- Listas, checklists y pros/contras.
- Árboles de carpetas.
- Payloads, código y comandos.
- Tablas que no dependen de relaciones espaciales.
- Contenido que se entiende igual de bien en prosa.

## Mapa de sistema

- Dibujar una frontera cuando el alcance sea relevante.
- Diferenciar componentes internos, externos y persistencia.
- Rotular contratos o riesgos en las conexiones.
- Mostrar feedback si explica comportamiento emergente.
- Usar `assets/flujo-sistema.svg` como referencia visual.

## Proceso

- Numerar etapas cuando exista un orden.
- Mostrar bucles únicamente cuando haya una condición de retorno.
- Evitar usar un proceso para representar estados persistentes.
- Mantener entre cuatro y siete pasos por lámina.

## Secuencia

- Colocar actores de izquierda a derecha.
- Representar el tiempo de arriba abajo.
- Usar línea sólida para la petición y discontinua para la respuesta.
- Rotular mensajes con verbos, rutas o eventos.
- Crear una segunda lámina si la secuencia supera doce mensajes.

## Matriz

- Usar solo cuando existan dos ejes independientes.
- Nombrar ambos ejes y su dirección.
- Evitar listas de ventajas disfrazadas de matriz.
- Colocar ejemplos dentro de cuadrantes sin convertirlos en párrafos.

## Máquina de estados

- Usar formas consistentes para todos los estados.
- Rotular transiciones con evento o condición.
- Diferenciar estado inicial o terminal mediante forma además de color.
- No mezclar pasos de proceso con estados.

## Modelo de datos

- Separar modelo conceptual, lógico y físico.
- Mostrar cardinalidades de forma explícita.
- Identificar PK y FK en modelos lógicos o físicos.
- Evitar más de ocho entidades por lámina.
- Extraer subdominios a diagramas separados cuando haya cruces.
- Usar `assets/modelo-datos.svg` como referencia visual.

## Capas y comparación

- Mantener la notación propia de cada patrón.
- Usar círculos concéntricos solo para dependencias hacia un núcleo.
- Usar bandas apiladas para separación horizontal.
- Usar puertos y adaptadores alrededor del núcleo en Hexagonal.
- Conservar la misma escala y densidad al comparar alternativas.
- Usar `assets/comparacion-patrones.svg` como referencia visual.

## Wireframe

- Representar estados de interfaz, no arquitectura.
- Usar baja fidelidad, anotaciones y foco visible.
- Incluir vacío, carga, error y éxito cuando sean parte del concepto.
