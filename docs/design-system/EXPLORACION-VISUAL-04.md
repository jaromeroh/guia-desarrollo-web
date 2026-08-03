# Exploración visual 04: pruebas de producción

## Objetivo

Comprobar que el lenguaje **editorial técnico luminoso** puede cubrir tres
funciones pedagógicas distintas sin fragmentar la identidad del libro:

1. Orientar mediante una ilustración conceptual.
2. Explicar un proceso técnico ordenado.
3. Representar estados y transiciones con precisión.

Estas imágenes nacieron como pruebas y fueron aprobadas como primer lote de
producción. Sus copias definitivas se publican en los capítulos 4, 6 y 20.

## Ilustración conceptual: evolución del rol

![La desarrolladora evoluciona desde la construcción de interfaces hasta el diseño y la supervisión de sistemas asistidos por IA](../../assets/diagrams/explorations/prueba-evolucion-editorial-v1.png)

### Función editorial

Presentar una progresión conceptual de izquierda a derecha: construir una
interfaz, comprender las conexiones del sistema y supervisar un producto con
más señales y automatización. No intenta explicar una arquitectura concreta.

La imagen utiliza composición narrativa y evita texto incrustado. Este modo se
reservaría para aperturas o transiciones donde una escena aporte orientación;
no reemplaza los diagramas técnicos.

## Proceso técnico: un turno del event loop

![Un turno del event loop: tarea, pila de JavaScript, microtareas y oportunidad de renderizado](../../assets/diagrams/explorations/prueba-event-loop-editorial-v1.svg)

### Función editorial

Explicar la secuencia principal y distinguirla del trabajo que programa el
entorno anfitrión. El diagrama hace visibles dos fundamentos que suelen
confundirse: la tarea actual se ejecuta hasta finalizar y la cola de microtareas
se vacía antes de ofrecer una oportunidad de renderizado.

El SVG es la fuente editable y accesible. El PNG del mismo nombre se conserva
únicamente para inspección y compatibilidad.

## Máquina de estados: circuit breaker

![Estados cerrado, abierto y semiabierto de un circuit breaker y sus transiciones](../../assets/diagrams/explorations/prueba-circuit-breaker-editorial-v1.svg)

### Función editorial

Representar estados, responsabilidad y condiciones de transición sin convertir
el patrón en una lista lineal. La forma circular y las flechas hacen evidente
que una prueba fallida vuelve a abrir el circuito y una exitosa restablece el
tráfico normal.

El SVG es la fuente editable y accesible. El PNG del mismo nombre se conserva
únicamente para inspección y compatibilidad.

## Comparación

| Prueba | Tipo | Fortaleza | Riesgo que debe vigilarse |
|---|---|---|---|
| Evolución del rol | Ilustración conceptual | Calidez y orientación narrativa | Añadir iconos sin función pedagógica |
| Event loop | Proceso técnico | Orden, jerarquía y distinción de flujos | Saturar los nodos con excepciones del runtime |
| Circuit breaker | Máquina de estados | Transiciones legibles y notación precisa | Usar color como único portador de significado |

## Criterios de aprobación

- Una sola identidad: papel cálido, superficie clara, tinta, azul petróleo,
  terracota, ocre y gris cálido.
- Sin blueprint, pauta de cuaderno, neón, degradados ni estética genérica de IA.
- Ilustración rasterizada solo cuando la escena narrativa agrega valor.
- SVG determinista para procesos, arquitecturas, secuencias, estados y datos.
- Texto grande, breve y legible al ancho real del contenido de GitBook.
- Color reforzado por etiquetas, formas, posición o patrones de línea.
- Título y descripción accesibles en cada SVG.

## Estado

**Aprobado el 31 de julio de 2026.** Las tres pruebas validan una sola identidad
con dos modos de producción: ilustración conceptual rasterizada y diagrama
técnico en SVG. Las reglas resultantes se documentan en
[Sistema visual del libro](./SISTEMA-VISUAL.md).
