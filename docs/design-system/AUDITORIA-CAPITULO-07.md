# Auditoría visual del capítulo 7

## Alcance

Capítulo auditado: **Pensamiento en Sistemas**.

## Hallazgos

El capítulo contiene ocho diagramas ASCII y varios esquemas de texto. Convertir
cada bloque produciría repetición y fragmentaría la lectura. Se consolidan en
cuatro funciones pedagógicas:

1. **Frontera de un componente:** contrato visible frente a implementación oculta.
2. **Calidad del diseño:** bajo acoplamiento y alta cohesión como objetivos
   complementarios, no absolutos.
3. **Trade-offs contextualizados:** prioridades, restricciones, coste y
   reversibilidad sustituyen el triángulo de «elige dos».
4. **Flujo de carrito:** actores, fronteras, fallos en conexiones y retorno de
   confirmación o error.

## Tratamiento del texto

- La comparación entre pensamiento local y pensamiento sistémico pasa a tabla.
- El ejemplo PostgreSQL/MongoDB pasa a tabla para mantener alternativas y
  razonamiento buscables.
- La secuencia completa de carrito permanece también como lista numerada junto
  a la lámina.
- La fórmula «bajo acoplamiento + alta cohesión» permanece como síntesis, con la
  advertencia de que dividir sin límite aumenta la complejidad.

Cada función visual tendrá una composición horizontal y una variante móvil.

## Resultado y verificación

- Los ocho bloques ASCII se eliminaron: cuatro relaciones pasaron a SVG y las
  comparaciones restantes a tabla, lista o prosa.
- Se integraron ocho SVG con `role="img"`, `<title>` y `<desc>`.
- El triángulo «elige dos» se reemplazó por un marco contextual que evita
  presentar una heurística como ley universal.
- El ejemplo PostgreSQL/MongoDB ya no afirma que MongoDB carezca de capacidades
  transaccionales; documenta el ajuste al contexto.
- Las composiciones se inspeccionaron a 770 y 420 px y HonKit compila las 37
  páginas sin errores.
