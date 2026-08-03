# Auditoría visual del capítulo 8

## Alcance

Capítulo auditado: **Desarrollo Asistido por IA**.

## Decisión editorial

Los diez bloques ASCII mezclan relaciones visuales con listas, ejemplos de
prompts y fragmentos que deben seguir siendo copiables. Se consolidan tres
funciones pedagógicas:

1. **Redistribución del trabajo:** la generación mecánica puede comprimirse,
   pero especificar y verificar ganan peso relativo sin imponer porcentajes.
2. **Ciclo basado en evidencia:** especificar, contextualizar, ejecutar,
   observar, evaluar y corregir/revisar hasta reunir evidencia suficiente.
3. **Verificación proporcional:** combinar impacto e incertidumbre para decidir
   permisos, pruebas, revisión y capacidad de recuperación.

Las fortalezas, limitaciones, anatomía de instrucciones, checklist y
antipatrones vuelven a tabla, lista o ejemplo de código. El esquema de MCP pasa
a una relación textual porque su dibujo de dos cajas no añade comprensión
material y el tema se desarrolla visualmente en el capítulo 30.

## Resultado y verificación

- Se integraron seis SVG con `role="img"`, `<title>` y `<desc>`.
- Los bloques de cajas ASCII desaparecieron; los ejemplos de código y prompts
  permanecen como texto copiable.
- La matriz de riesgo ahora combina impacto e incertidumbre, en vez de suponer
  que la familiaridad subjetiva basta para decidir cuánto verificar.
- Las composiciones se inspeccionaron a 770 y 420 px.
- HonKit compila las 37 páginas y carga los recursos nuevos sin errores.
