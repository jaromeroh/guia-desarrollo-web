# Auditoría visual de los capítulos 20–29

> Primera pasada integrada el 3 de agosto de 2026.
>
> Estado actualizado el 3 de agosto de 2026: los capítulos 20–23 completaron su
> segunda pasada. Véanse `AUDITORIA-VISUAL-SEGUNDA-PASADA-17-20.md` y
> `AUDITORIA-VISUAL-SEGUNDA-PASADA-21-23.md`.
>
> La comparación de los capítulos 27–29 quedó verificada el 3 de agosto de
> 2026, tanto en escritorio como en móvil.

## Alcance del lote

Se integró una nueva función pedagógica en cada capítulo, siempre con una
composición horizontal y otra móvil. El lote añade **20 SVG**. El capítulo 20
conserva además el par existente sobre circuit breaker.

| Capítulo | Función integrada | Pares nuevos | Bloques visuales secundarios por revisar |
|---:|---|---:|---:|
| 20 | Job, cola, outbox, CQRS y Event Sourcing | 5 | 0 |
| 21 | Capas, modelos, niveles y TDD con agentes | 4 | 0 |
| 22 | Pipeline, automatización, branching y feature flags | 4 | 0 |
| 23 | Hosting, despliegue progresivo, estrategias y promoción | 4 | 0 |
| 24 | Correlación de métricas, trazas y logs | 1 | 0 |
| 25 | Ciclo de capacidad y rendimiento | 1 | 0 |
| 26 | Fronteras de confianza | 1 | 0 |
| 27 | Slice vertical con Next.js y Node.js | 1 | 0 |
| 28 | El mismo slice con FastAPI | 1 | 0 |
| 29 | El mismo slice con Go | 1 | 0 |

Los conteos secundarios incluyen comparaciones y secuencias que pueden
consolidarse, pero no árboles o código que deban permanecer copiables. No son
una cuota de imágenes.

## Decisiones del lote

- Los capítulos 27–29 usan la misma secuencia: entrada, caso de uso, dominio,
  persistencia y operación. Solo cambian los mecanismos del stack.
- El capítulo 20 deja claro que una respuesta rápida no vuelve confiable a un
  trabajo: debe persistirse y poder recuperarse antes de confirmarlo.
- Testing se presenta como evidencia proporcional al riesgo, no como una
  cantidad universal de pruebas por nivel.
- CI/CD separa artefacto, despliegue y liberación.
- Deployment conserva explícita la dificultad de revertir datos y efectos
  externos.
- Observabilidad, capacidad y seguridad se explican desde preguntas y
  fronteras, no como catálogos de herramientas.

## Verificación comparativa de los stacks

Los tres capítulos conservan la misma pregunta narrativa: **¿cómo atraviesa
una solicitud de soporte las mismas responsabilidades cuando cambia el
stack?** La tipología elegida es un proceso comparable de cinco etapas.

| Etapa estable | Next.js | FastAPI | Go |
|---|---|---|---|
| Entrada HTTP | Route Handler · Server Action | FastAPI · Pydantic | `net/http` · JSON limitado |
| Caso de uso | TypeScript · puertos | Python · dependencias | interfaces pequeñas |
| Dominio | reglas sin framework | reglas sin framework | reglas y errores |
| Persistencia | consulta · transacción | SQLAlchemy · transacción | `database/sql` · `tx` |
| Operación | tests · logs · deploy | pytest · logs · contenedor | `httptest` · métricas · binario |

La revisión corrigió cuatro aspectos compartidos:

- color terracota fuera de la paleta editorial;
- ausencia de asociación `data-container` entre textos y tarjetas;
- densidad tipográfica excesiva en las tarjetas de escritorio;
- conclusiones cortadas en la composición móvil.

Las seis fuentes SVG pasan el validador sin errores ni advertencias. Se
renderizaron a 1200, 736, 480 y 320 px y se comprobaron dentro de HonKit a
1280 px y 390 px. El navegador cargó la variante móvil correcta y no registró
errores de consola.

Previsualizaciones: `output/diagram-previews-stacks-27-29-v4/`.
Capturas de HonKit: `output/playwright/stacks-27-29/`.

## Siguiente pasada

1. Recorrer las 31 páginas en HonKit para detectar imágenes ausentes,
   desbordamientos y espaciado inconsistente antes de publicar.
