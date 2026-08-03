# Exploración visual 01: viaje de una petición

## Objetivo

Comparar tres direcciones visuales para los diagramas del libro utilizando el
mismo contenido, la misma geometría y el mismo nivel de detalle. De esta forma,
la decisión se basa en el lenguaje visual y no en diferencias de información.

> Esta exploración conserva valor como registro de la comparación. La decisión
> editorial posterior descartó el blueprint y el cuaderno técnico: no son
> variantes autorizadas para el libro.

El caso elegido es el viaje simplificado de una petición `GET /perfil` entre:

1. Navegador.
2. DNS.
3. Edge o CDN.
4. Aplicación.
5. Servicio de autenticación.
6. Base de datos.

Las tres variantes representan los mismos diez mensajes y separan la secuencia
en red, procesamiento y respuesta.

## Dirección A: editorial técnico luminoso

![Viaje de una petición en estilo editorial técnico luminoso](../../assets/diagrams/explorations/viaje-peticion-editorial.png)

### Lectura

Es la dirección más compatible con el tono didáctico del libro. Los fondos
suaves ayudan a reconocer las fases sin competir con el contenido, mientras que
el azul identifica los pasos y las respuestas utilizan línea discontinua.

### Resultado editorial

- Arquitecturas y mapas de sistema.
- Secuencias y flujos de datos.
- Capas y dependencias.
- Matrices de decisión.
- Modelos de datos.
- Pipelines de CI/CD.

## Dirección B: blueprint de ingeniería

![Viaje de una petición en estilo blueprint de ingeniería](../../assets/diagrams/explorations/viaje-peticion-blueprint.png)

### Lectura

La rejilla, la tipografía monoespaciada y el contraste alto producen una
identidad técnica fuerte. Las llamadas se representan en cian y los retornos en
ámbar.

### Uso recomendado

**Descartado.** El fondo oscuro, la rejilla y la atmósfera de «plano técnico»
disonan con el tono editorial del libro y dificultan su uso continuo e impreso.

## Dirección C: cuaderno técnico

![Viaje de una petición en estilo cuaderno técnico](../../assets/diagrams/explorations/viaje-peticion-sketch.png)

### Lectura

El papel pautado, las pequeñas irregularidades y la anotación final hacen que el
diagrama parezca parte de una sesión de diseño. El estilo comunica exploración
y aprendizaje, no una especificación definitiva.

### Resultado editorial

**Descartado.** La pauta, la irregularidad y la apariencia de boceto introducen
un registro visual distinto que no corresponde con la identidad del libro.

## Comparación

| Criterio | Editorial luminoso | Blueprint | Cuaderno técnico |
|---|---|---|---|
| Legibilidad continua | Alta | Media | Media |
| Precisión técnica | Alta | Alta | Media |
| Integración con GitBook | Alta | Media | Alta |
| Impresión y escala de grises | Alta | Media-baja | Alta |
| Personalidad visual | Media-alta | Alta | Alta |
| Uso en grandes cantidades | Adecuado | No recomendado | Selectivo |
| Función principal | Lenguaje aprobado | Descartado | Descartado |

## Recomendación

Adoptar **editorial técnico luminoso** como único lenguaje visual del libro.
Las necesidades de infraestructura, UX o razonamiento se resolverán mediante
la notación y la composición apropiadas, sin cambiar de estilo.

Todas las imágenes aprobadas deben compartir:

- La misma gramática de flechas y líneas.
- Tipos de nodo consistentes.
- Numeración de pasos.
- Color acompañado siempre por forma, texto o patrón.
- Texto mínimo de 16 px en un lienzo de 1000 px.
- Alternativa textual para diagramas complejos.
- Elementos `<title>` y `<desc>` en cada SVG.

## Decisiones pendientes

Antes de convertir el resto del manuscrito:

1. Probar el lenguaje aprobado en ilustración conceptual y diagramas técnicos.
2. Confirmar la paleta definitiva.
3. Definir plantillas por familia: arquitectura, secuencia, decisión, datos y
   wireframe.
4. Probar la dirección elegida en móvil, modo oscuro e impresión.
5. Documentar los tokens y la gramática de conectores.
