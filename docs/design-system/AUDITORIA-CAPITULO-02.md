# Auditoría visual del capítulo 2

> Capítulo: *HTML Semántico, Formularios y Mejora Progresiva*. Corte: 31 de
> julio de 2026. Esta auditoría aplica el
> [sistema visual aprobado](./SISTEMA-VISUAL.md).

## Estado inicial

El capítulo no contiene imágenes publicadas ni diagramas ASCII. Los ejemplos
de HTML y JavaScript son material copiable y deben permanecer como código. Las
tablas expresan decisiones y listas de verificación que seguirán siendo texto
semántico.

## Necesidades visuales

La lectura completa identifica cuatro relaciones que el texto obliga a
reconstruir mentalmente:

1. **HTML como contrato inicial:** la semántica interpretada por el navegador
   alimenta la estructura del documento, el comportamiento nativo y el árbol de
   accesibilidad.
2. **Formulario como interfaz y protocolo:** los controles con `name` se
   convierten en pares de nombre y valor, luego en una petición HTTP que el
   servidor procesa.
3. **Dos responsabilidades de validación:** el cliente ayuda a corregir pronto;
   el servidor analiza, valida y autoriza antes de aceptar cambios.
4. **Mejora progresiva:** HTML conserva la función esencial, CSS mejora la
   presentación y JavaScript amplía la interacción.

## Contenido que seguirá siendo texto

- Enlace frente a botón: dos reglas y ejemplos de código bastan.
- Regiones, listas, tablas y controles: el lector necesita ver la etiqueta HTML
  exacta, no una interpretación gráfica.
- Validar, normalizar, codificar y sanitizar: la comparación textual es más
  precisa y buscable.
- Checklist final: debe continuar como lista operable y copiable.

## Conjunto de producción

Se produjeron cuatro funciones pedagógicas:

| Recurso | Función | Composición móvil |
|---|---|---|
| `cap02-html-contrato.svg` | Una fuente semántica produce varias capacidades | Sí |
| `cap02-formulario-peticion.svg` | Secuencia de interfaz a protocolo | Sí |
| `cap02-validacion-fronteras.svg` | Comparación de responsabilidades y frontera de confianza | Sí |
| `cap02-mejora-progresiva.svg` | Capas acumulativas con degradación útil | Sí |

Cada SVG incluye `role="img"`, `<title>` y `<desc>`. Las relaciones también
están explicadas en el texto cercano y ninguna información copiable queda
atrapada en la imagen.

## Resultado de integración

- Los cuatro recursos se insertaron junto a la explicación que amplían, sin
  reemplazar ejemplos, tablas ni listas operables.
- Cada función dispone de una composición horizontal y otra vertical. El
  elemento `<picture>` cambia a la variante móvil hasta 820 px.
- Los textos alternativos resumen la relación pedagógica; los SVG añaden
  `role="img"`, `<title>` y `<desc>` coherentes.
- La mención «obtener una representación» en la explicación de `GET` se cambió
  por «pedir datos o contenido» para evitar jerga innecesaria en un capítulo
  introductorio.

## Verificación local

- [x] Los ocho SVG son XML válido y permanecen dentro de su `viewBox`.
- [x] HonKit genera correctamente las 37 páginas y carga los ocho recursos.
- [x] A 1280 px se publican las composiciones horizontales dentro de una
      columna de 770 px, sin desbordamiento horizontal.
- [x] A 420 px se publican las composiciones verticales dentro de una columna
      de 390 px, sin desbordamiento horizontal.
- [x] Flechas, márgenes, contraste y texto esencial se revisaron visualmente en
      la versión local.
