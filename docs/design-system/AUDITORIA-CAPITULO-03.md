# Auditoría visual del capítulo 3

> Capítulo: *CSS, Layout Adaptable y Sistema Visual*. Corte: 2 de agosto de
> 2026. Esta auditoría aplica el
> [sistema visual aprobado](./SISTEMA-VISUAL.md).

## Estado inicial

El capítulo no contiene imágenes publicadas ni diagramas ASCII. Los ejemplos
CSS, la tabla de unidades y las listas de verificación deben permanecer como
texto semántico y copiable.

## Necesidades visuales

La lectura completa identifica cuatro relaciones espaciales o de decisión que
el texto obliga a reconstruir mentalmente:

1. **Resolución de la cascada:** las declaraciones candidatas se comparan por
   relevancia, origen e importancia, capa, especificidad y orden de aparición.
2. **Caja y desbordamiento:** contenido, padding y borde participan en el tamaño;
   un mínimo intrínseco mayor que el espacio disponible rompe el contrato.
3. **Elección del modelo de layout:** el flujo normal conserva el orden de
   lectura, Flexbox distribuye en un eje y Grid coordina dos ejes.
4. **Entorno frente a contenedor:** las media queries expresan decisiones de
   página o preferencias; las container queries expresan decisiones locales del
   componente.

## Contenido que seguirá siendo texto

- Declaraciones CSS y ejemplos de selectores: deben conservarse copiables.
- Unidades, tokens y estados de componente: sus tablas y listas ya son la forma
  más precisa y buscable.
- Preferencias de color y movimiento: los ejemplos de código son la evidencia
  principal.
- Checklist y ejercicios: deben continuar como elementos operables.

## Conjunto de producción

Se produjeron cuatro funciones pedagógicas:

| Recurso | Función | Composición móvil |
|---|---|---|
| `cap03-cascada-resolucion.svg` | Secuencia de desempate de la cascada | Sí |
| `cap03-caja-desbordamiento.svg` | Composición de la caja y diagnóstico de overflow | Sí |
| `cap03-eleccion-layout.svg` | Árbol de decisión entre flujo, Flexbox y Grid | Sí |
| `cap03-media-container.svg` | Comparación de alcance entre queries | Sí |

Cada SVG incluye `role="img"`, `<title>` y `<desc>`. Las relaciones también
están explicadas en el texto cercano y ninguna regla que el lector necesite
copiar queda atrapada únicamente en la imagen.

## Resultado de integración

- Los cuatro recursos se insertaron junto a la explicación que amplían, sin
  reemplazar código, tablas, checklists ni ejercicios.
- Cada función dispone de una composición horizontal y otra vertical. El
  elemento `<picture>` cambia a la variante móvil hasta 820 px.
- Los textos alternativos resumen la relación pedagógica; los SVG añaden
  `role="img"`, `<title>` y `<desc>` coherentes.
- El terracota se reserva para el desbordamiento, que representa un contrato de
  tamaño roto; las alternativas neutras de layout no dependen de esa señal.

## Verificación local

- [x] Los ocho SVG son XML válido y permanecen dentro de su `viewBox`.
- [x] HonKit genera correctamente las 37 páginas y carga los ocho recursos.
- [x] A 1280 px se publican las composiciones horizontales dentro de una
      columna de 770 px, sin desbordamiento horizontal.
- [x] A 759 y 420 px se publican las composiciones verticales, sin
      desbordamiento horizontal.
- [x] Flechas, márgenes, contraste y texto esencial se revisaron visualmente en
      la versión local.
