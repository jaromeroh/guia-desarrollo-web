# Auditoría visual de los capítulos 10–19

> Primera pasada integrada el 2 de agosto de 2026.
>
> Estado actualizado el 3 de agosto de 2026: los capítulos 11–15 completaron
> su segunda pasada en
> `AUDITORIA-VISUAL-SEGUNDA-PASADA-11-15.md`; los capítulos 17–19 la completaron
> en `AUDITORIA-VISUAL-SEGUNDA-PASADA-17-20.md`.

## Alcance del lote

Se revisaron diez capítulos consecutivos y se produjo al menos una función
pedagógica ancla para cada uno. El capítulo 10 recibió dos. Cada función cuenta
con composición horizontal y variante móvil; en total se añadieron **22 SVG**.

La pasada no convierte automáticamente cada bloque monoespaciado en una imagen.
Los árboles de carpetas, contratos, cronologías copiables y tablas permanecen
como texto cuando esa forma ofrece mejor búsqueda y accesibilidad. Los diagramas
secundarios se consolidarán por pregunta pedagógica antes de reemplazarlos.

| Capítulo | Función integrada | Pares SVG | Bloques visuales secundarios por revisar |
|---:|---|---:|---:|
| 10 | Proceso de diseño y estados de interfaz | 2 | 0 |
| 11 | Dependencias, MVC y patrones | 3 | 2 árboles de carpetas conservados |
| 12 | Contrato, API-first y elección de estilo | 3 | 0 |
| 13 | Niveles, ERD e índice B-Tree | 3 | 1 árbol de migraciones conservado |
| 14 | Slice, riesgo, contexto, flujo y ciclo | 4 | 0 |
| 15 | Renderizado, dependencias y estado | 3 | 2 árboles de proyecto conservados |
| 16 | Pipeline de backend | 1 | 0 |
| 17 | Identidad, sesión, passkey, PKCE y autorización | 5 | 1 esquema JWT conservado como código |
| 18 | Elección, patrones y escalado de tiempo real | 3 | 0 |
| 19 | Transacción, concurrencia, MVCC y caché | 4 | 0 |

Los conteos secundarios incluyen árboles y ejemplos de código que probablemente
se conservarán. No representan una cuota de imágenes pendientes.

## Cambios editoriales asociados

- Se reemplazaron los ASCII principales de los capítulos 10–15 y 17–19 por
  imágenes ancla, tablas o prosa semántica.
- Se retiraron cifras universales sobre el costo relativo de un cambio en el
  capítulo 14 y se vinculó el costo con reversibilidad, acoplamiento y alcance.
- Se aclaró en el capítulo 17 que los tokens no eliminan el estado ni la
  autorización.
- Se corrigió en el capítulo 18 la idea de que una solución más compleja es
  necesariamente mejor.
- Se mantuvo el texto alternativo funcional y la descripción interna de cada
  SVG.

## Estado de la segunda pasada

Los capítulos 10–19 están cerrados. Los únicos bloques monoespaciados visuales
que permanecen son árboles de archivos o un esquema compacto de JWT que se
benefician de seguir siendo texto buscable y copiable.
