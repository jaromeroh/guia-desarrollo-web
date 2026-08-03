# Sistema visual

## Paleta

Usar únicamente estos colores, además de `none` y `currentColor`:

| Token | Valor | Función |
|---|---|---|
| Tinta | `#20262E` | Títulos, texto y estructura |
| Azul petróleo | `#31536A` | Flujo principal y elementos técnicos |
| Terracota | `#B95736` | Riesgo, excepción y transición crítica |
| Ocre | `#C59132` | Datos, decisión y estado intermedio |
| Gris cálido | `#A9A49B` | Bordes y relaciones secundarias |
| Línea | `#59636D` | Conectores neutrales |
| Texto secundario | `#72706C` | Anotaciones |
| Papel | `#F2EEE6` | Fondo exterior |
| Superficie | `#FFFDFA` | Láminas y tarjetas |
| Azul suave | `#E8EEF1` | Superficie técnica |
| Terracota suave | `#F3E6DF` | Superficie de riesgo |
| Ocre suave | `#F5ECD8` | Superficie de datos |
| Borde suave | `#D8D2C7` | Límites de panel |

No usar violetas, verdes menta, neones, glassmorphism ni degradados.

## Tipografía

- Usar `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
- Usar `ui-monospace, "SFMono-Regular", Consolas, monospace` para código,
  rutas, payloads, claves y nombres físicos.
- Usar 32–36 px para el título de una lámina de 1000–1200 px.
- Usar 18–20 px para títulos de nodo.
- Usar 14–16 px para cuerpo y conectores.
- Reservar 12 px para etiquetas editoriales cortas en mayúsculas.
- No reducir el texto para hacerlo caber. Ampliar el contenedor o resumir.

## Geometría

- Usar radios de 10–18 px.
- Usar bordes de 2–2,5 px.
- Mantener 20–24 px de zona segura dentro de cada recuadro.
- Mantener al menos 24 px entre nodos y 16 px entre texto y conectores.
- Evitar sombras salvo una elevación editorial muy discreta.
- Preferir relaciones de aspecto horizontales; usar vertical cuando la
  secuencia o comparación lo requiera.

## Conectores

- Línea sólida: llamada, dependencia o transición.
- Línea discontinua: respuesta, evento o feedback.
- Terracota: fallo, riesgo o transición crítica.
- Azul petróleo: flujo principal o retorno destacado.
- Rotular el evento o contrato, no repetir los nombres de los nodos.
- Colocar textos largos sobre una superficie de etiqueta.
- No cruzar texto, nodos ni otros conectores.

## Texto dentro de recuadros

SVG no ajusta texto automáticamente. Crear saltos de línea mediante `<tspan>`.

Asociar cada texto contenido con su recuadro:

```xml
<rect id="node-api" x="80" y="160" width="240" height="120" rx="14"/>
<text data-container="node-api" data-padding="24" x="200" y="205"
      text-anchor="middle">
  <tspan x="200">Servicio de API</tspan>
  <tspan x="200" dy="28">Valida la petición</tspan>
</text>
```

El validador usa esta asociación para estimar desbordamientos. Mantener un
máximo de dos líneas en etiquetas y de cuatro líneas en tarjetas explicativas.

## Accesibilidad

- Incluir `role="img"` y `aria-labelledby="title desc"` en `<svg>`.
- Incluir un `<title>` breve y un `<desc>` que explique la relación principal.
- No depender exclusivamente del color; combinarlo con texto, forma o patrón.
- Mantener el orden de lectura del DOM equivalente al orden visual.
- Proporcionar una explicación textual adyacente para diagramas complejos.

## Salida

- Conservar SVG como fuente maestra.
- Generar PNG únicamente como previsualización o fallback.
- No incrustar texto importante en ilustraciones generativas.
- Usar nombres descriptivos con capítulo y concepto cuando el destino sea el
  libro, por ejemplo `cap13-oauth-pkce.svg`.
