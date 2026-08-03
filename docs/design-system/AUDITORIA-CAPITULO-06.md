# Auditoría visual del capítulo 6

## Alcance

Capítulo auditado: **La Evolución del Desarrollador Web**.

## Recursos existentes

### Evolución del trabajo web

La ilustración `cap06-evolucion-rol.png` se conserva. Su lenguaje editorial,
paleta y nivel de abstracción coinciden con la dirección aprobada. Al no
contener texto indispensable, la composición panorámica puede reducirse sin
perder una instrucción que el lector necesite recuperar.

### Ciclo Antes–Durante–Después

El PNG heredado se reemplaza porque:

- usa una paleta y una tipografía ajenas al sistema visual;
- conserva la numeración anterior de las partes del libro;
- fija una distribución 40/20/40 que el texto rechaza explícitamente como
  regla universal;
- representa tres columnas, pero no el aprendizaje que vuelve desde
  producción hacia las decisiones siguientes.

## Decisión

Crear una composición editorial en SVG y una variante móvil. La nueva lámina
debe presentar:

1. **Antes — Parte III:** reducir incertidumbre.
2. **Durante — Parte IV:** convertir intención en software verificable.
3. **Después — Parte V:** observar la realidad y aprender.
4. **Retorno de evidencia:** los hallazgos del uso alimentan el siguiente ciclo.

No se mostrarán porcentajes de esfuerzo.

## Resultado y verificación

- Se integraron `cap06-ciclo-desarrollo.svg` y su composición móvil.
- Ambos archivos son XML válido e incluyen `role="img"`, `<title>` y `<desc>`.
- La composición refleja la numeración vigente: Parte III, Parte IV y Parte V.
- La inspección a 770 y 420 px confirmó que las etiquetas esenciales permanecen
  legibles y que la versión móvil reordena las fases verticalmente.
- HonKit compila las 37 páginas y carga los recursos nuevos.
