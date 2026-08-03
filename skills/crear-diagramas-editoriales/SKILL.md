---
name: crear-diagramas-editoriales
description: Diseña, convierte, revisa y renderiza diagramas SVG para El Arte del Desarrollo Web Moderno con su sistema visual editorial. Usar cuando Codex deba reemplazar diagramas ASCII, crear mapas de arquitectura, procesos, secuencias, matrices, máquinas de estados, modelos de datos, comparaciones, capas o wireframes para el libro, o auditar su coherencia visual, accesibilidad y desbordamientos de texto.
---

# Crear diagramas editoriales

Producir diagramas precisos, editables y accesibles con la paleta y gramática
visual del libro. Conservar SVG como fuente maestra y generar PNG solo para
previsualización o fallback.

## Flujo obligatorio

1. Leer el pasaje completo que rodea al diagrama.
2. Formular la pregunta narrativa que la imagen debe responder.
3. Decidir si una imagen mejora realmente la prosa.
4. Leer [references/tipologias.md](references/tipologias.md) para escoger la
   notación correcta.
5. Leer [references/sistema-visual.md](references/sistema-visual.md) antes de
   crear o modificar cualquier SVG.
6. Copiar `assets/base.svg` o el ejemplo más cercano a un archivo nuevo. No
   modificar las plantillas de la skill durante una tarea de contenido.
7. Reducir el contenido a relaciones, estados, decisiones o flujos esenciales.
8. Crear el SVG con título, descripción accesible y texto asociado a sus
   contenedores mediante `data-container`.
9. Ejecutar el validador y corregir todos los errores.
10. Renderizar previsualizaciones y revisarlas visualmente a varios anchos.
11. Entregar SVG, PNG de revisión y una explicación textual breve.

## Elegir la salida

- Usar `assets/diagrams/<nombre>.svg` como ubicación predeterminada de la fuente
  editable dentro de este repositorio.
- Usar nombres descriptivos, en minúsculas y con guiones.
- Incluir el capítulo cuando el recurso sea definitivo:
  `cap13-oauth-pkce.svg`.
- Generar PNG solo cuando el lector o la aplicación no pueda mostrar el SVG.
- No sobrescribir una imagen existente sin autorización; crear una versión
  nueva durante la exploración.

## Usar las plantillas

- `assets/base.svg`: estructura mínima y tokens.
- `assets/flujo-sistema.svg`: flujo, frontera, riesgos y feedback.
- `assets/comparacion-patrones.svg`: comparación de notaciones arquitectónicas.
- `assets/modelo-datos.svg`: ERD con claves y cardinalidades.

Copiar la plantilla seleccionada al destino y reemplazar su contenido. Mantener
la gramática visual, no los datos ni la geometría exacta del ejemplo.

## Controlar texto y geometría

- Mantener una zona segura de 20–24 px dentro de cada bloque.
- Introducir saltos explícitos con `<tspan>`.
- Limitar etiquetas a dos líneas y tarjetas explicativas a cuatro.
- Ampliar el contenedor o resumir cuando el texto no quepa.
- No reducir tipografía para ocultar un desbordamiento.
- Asociar todo texto interno con `data-container="<id-del-rect>"`.
- Usar superficies de etiqueta para texto colocado sobre conectores.
- Revisar también posiciones entre bloques: el validador no sustituye la
  inspección visual de cruces y colisiones.

## Validar

Ejecutar desde la raíz de la skill:

```bash
python3 scripts/validate_diagram.py /ruta/al/diagrama.svg
```

Tratar los errores como bloqueantes. Revisar las advertencias de tipografía
secundaria y justificar cualquier excepción deliberada con
`data-small-ok="true"`.

El cálculo de desbordamiento es aproximado. Después de validarlo, renderizar:

```bash
python3 scripts/render_preview.py /ruta/al/diagrama.svg \
  /ruta/al/diagrama-preview-1200.png --width 1200
python3 scripts/render_preview.py /ruta/al/diagrama.svg \
  /ruta/al/diagrama-preview-736.png --width 736
python3 scripts/render_preview.py /ruta/al/diagrama.svg \
  /ruta/al/diagrama-preview-480.png --width 480
python3 scripts/render_preview.py /ruta/al/diagrama.svg \
  /ruta/al/diagrama-preview-320.png --width 320
```

Inspeccionar cada PNG. Corregir:

- Texto cortado o fuera de su recuadro.
- Etiquetas que invaden conectores.
- Flechas que atraviesan texto.
- Bloques sin alineación o con espaciado desigual.
- Texto ilegible al ancho real de GitBook.
- Contraste insuficiente o significado dependiente solo del color.

## Preservar precisión editorial

- Mantener la terminología del capítulo.
- No inventar cardinalidades, porcentajes, pasos ni dependencias.
- Señalar discrepancias entre la imagen y el manuscrito antes de corregir el
  contenido.
- Usar un mismo sistema transversal cuando el libro ya comparta un ejemplo,
  como el e-commerce.
- Separar un diagrama denso en dos láminas en vez de comprimirlo.
- Mantener listas, código, árboles de archivos y tablas simples como contenido
  nativo de GitBook.

## Entregar

Informar:

- Qué pregunta responde la imagen.
- Qué tipología se eligió.
- Rutas del SVG y de las previsualizaciones.
- Resultado del validador.
- Riesgos o decisiones editoriales pendientes.

No insertar una exploración en un capítulo hasta recibir aprobación. Si el
usuario pidió explícitamente una imagen definitiva, actualizar la referencia
del capítulo y comprobar el build de GitBook.
