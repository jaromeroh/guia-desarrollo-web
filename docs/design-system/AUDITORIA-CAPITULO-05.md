# Auditoría visual del capítulo 5

## Alcance

Capítulo auditado: **URL, DNS, TLS, HTTP, Caché y Seguridad del Navegador**.

El capítulo es correcto y completo en lo conceptual, pero concentra varias fronteras y procesos que resultan difíciles de retener únicamente como texto. El recorrido integral de una petición ya está representado en el capítulo 1, por lo que repetirlo aquí reduciría el valor editorial de las imágenes.

## Necesidades visuales seleccionadas

1. **URL y origen.** Mostrar qué componentes de una URL definen el origen y cuáles solo ubican un recurso o estado local.
2. **Diagnóstico por capas.** Separar DNS, transporte, TLS, HTTP y aplicación/navegador por responsabilidad y evidencia observable.
3. **Reutilización de caché.** Explicar la diferencia entre frescura, validación y descarga de un nuevo cuerpo.
4. **Seguridad del navegador.** Contrastar política del mismo origen, CORS, CSRF y CSP mediante la pregunta que resuelve cada mecanismo.

Cada necesidad tendrá una composición horizontal y una variante móvil reordenada, no una simple reducción del SVG de escritorio.

## Elementos que permanecen como texto

- Tabla de métodos y códigos HTTP.
- Secuencia completa de una petición.
- Listas de diagnóstico, configuración y ejercicios.

Estas estructuras ya son legibles y no ganan suficiente comprensión al convertirse en ilustraciones.

## Criterios editoriales

- Evitar jerga no explicada en las etiquetas principales.
- Reservar terracota para riesgo o fallo.
- Mantener el azul para flujo y estructura; ocre para caché o autorización explícita.
- Añadir título y descripción accesibles en cada SVG.
- Usar texto mínimo legible en el ancho real del libro.

## Resultado

- Se integraron cuatro funciones pedagógicas, cada una con composición de
  escritorio y móvil.
- La tabla de métodos cambió «obtener representación» por «pedir datos o
  contenido» y «URI conocida» por «URL conocida» para reducir jerga temprana.
- El recorrido completo de una petición permaneció como texto para no repetir
  el diagrama del capítulo 1.

## Verificación

- Los ocho SVG incluyen `role="img"`, `<title>` y `<desc>` y son XML válido.
- HonKit compila las 37 páginas y carga los ocho recursos.
- A 1280 px se seleccionan las cuatro composiciones horizontales, con 770 px
  de ancho real y sin desbordamiento de la página.
- A 420 px se seleccionan las cuatro composiciones móviles, con 390 px de ancho
  real y sin desbordamiento de la página.
- Las variantes móviles de URL y caché se recompusieron tras la inspección
  visual para eliminar cortes y cruces ambiguos.
