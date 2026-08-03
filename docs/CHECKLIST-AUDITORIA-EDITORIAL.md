# Checklist de auditoría editorial

Este documento registra el trabajo de revisión del manuscrito. Una casilla solo
se marca cuando el texto fue corregido, contrastado con una fuente primaria
cuando corresponde y revisado dentro del libro compilado.

**Estado al 3 de agosto de 2026:** auditoría técnica, editorial, visual y de referencias
completada sobre la introducción, los 31 capítulos y los apéndices A–E. Los
capítulos 27–29 integran los conocimientos mediante el mismo slice vertical en
Next.js, FastAPI y Go; el capítulo 31 cierra el recorrido con un radar de
tendencias. HonKit generó las 37 páginas; la auditoría comprobó 407 referencias,
375 enlaces y 185 SVG. La fase visual está cerrada para la edición 1.0.

## Criterios de cierre

- [x] Las afirmaciones técnicas distinguen fundamento, práctica y estado del
      ecosistema.
- [x] Las reglas contextuales no se presentan como leyes universales.
- [x] Las cifras y comparativas volátiles tienen fuente, fecha y contexto, o se
      eliminan.
- [x] Los ejemplos conceptuales se identifican como tales.
- [x] Los ejemplos ejecutables incluyen una forma razonable de verificar su
      comportamiento.
- [x] Los ejemplos de seguridad, autenticación, datos y despliegue reciben una
      revisión específica.
- [x] Cada capítulo conserva una progresión clara y evita repeticiones.
- [x] El libro compila sin errores y los recursos locales existen.

## Prioridad 1 — Seguridad y datos

### Capítulo 13. Modelado de datos

- [x] Distinguir instantes, fechas civiles y horarios asociados a una zona.
- [x] Corregir el ejemplo de `TIMESTAMPTZ` y `AT TIME ZONE`.
- [x] Usar una única conexión al demostrar una transacción SQL.
- [x] Explicar que UUID no sustituye autorización ni control de acceso.
- [x] Sustituir reglas absolutas sobre índices por decisiones basadas en
      consultas, selectividad y medición.
- [x] Matizar la comparación entre bases relacionales y NoSQL.

### Capítulo 17. Autenticación y autorización

- [x] Diferenciar sesión, cookie, token y credencial.
- [x] Corregir el alcance real de `HttpOnly`, `Secure` y `SameSite`.
- [x] Reemplazar el hash ficticio usado para igualar tiempos.
- [x] Hacer segura la comparación constante de tokens de distinta longitud.
- [x] Reemplazar el ejemplo basado en `csurf`.
- [x] Presentar limitación por IP y por cuenta como controles complementarios.
- [x] Actualizar almacenamiento de contraseñas con parámetros vigentes y
      calibración por hardware.
- [x] Presentar OAuth 2.1 como borrador y RFC 9700 como práctica vigente.
- [x] Revisar que los ejemplos no se presenten como producción sin requisitos
      adicionales.

### Capítulo 19. Persistencia y bases de datos

- [x] Explicar con precisión qué garantiza y qué no garantiza ACID.
- [x] Evitar recomendar niveles de aislamiento por categoría de industria.
- [x] Corregir el ejemplo de transferencia y su afirmación sobre bloqueos.
- [x] Añadir validación de importe, restricción de saldo e idempotencia.
- [x] Mostrar reintentos acotados para errores de serialización.
- [x] Corregir la afirmación sobre `HAVING` en Prisma.
- [x] Separar consistencia de caché de disponibilidad y rendimiento.

### Capítulo 20. Tareas asíncronas

- [x] Explicar la ventana entre commit de base de datos y publicación del job.
- [x] Introducir el patrón transactional outbox.
- [x] Enseñar consumidores idempotentes y entrega al menos una vez.
- [x] Añadir publisher confirms al ejemplo de RabbitMQ.
- [x] Clasificar errores antes de reintentar y respetar presupuesto, cancelación
      y `Retry-After`.
- [x] Corregir la clasificación de circuit breaker, credenciales y certificados.
- [x] Eliminar afirmaciones de popularidad y recomendaciones fechadas.

## Prioridad 2 — Ejemplos y runtimes desactualizados

- [x] Capítulo 1: separar FaaS, edge runtimes y contenedores administrados.
- [x] Capítulo 12: actualizar Apollo Server y los headers de deprecación.
- [x] Capítulo 16: actualizar manejo de promesas a Express 5.
- [x] Capítulo 18: presentar WebTransport como alternativa especializada.
- [x] Capítulo 22: actualizar Node y GitHub Actions; corregir la explicación de
      caché.
- [x] Capítulo 23: corregir el workflow de ECR, usar OIDC y retirar límites o
      precios volátiles.
- [x] Capítulo 30: corregir hooks, memoria y convenciones específicas de
      producto.

## Prioridad 3 — Evidencia, vigencia y lenguaje

- [x] Capítulo 6: retirar el reparto 20/80 y las limitaciones absolutas de IA.
- [x] Capítulo 8: retirar porcentajes ilustrativos no medidos.
- [x] Capítulo 9: verificar o retirar la cifra del 47 %.
- [x] Capítulo 10: actualizar la cifra de discapacidad y las listas de
      herramientas.
- [x] Capítulo 11: retirar estadísticas de IA sin contexto.
- [x] Capítulo 14: convertir buffers, cobertura y estimaciones en ejemplos, no
      reglas.
- [x] Capítulo 15: fechar o retirar comparativas, tendencias y porcentajes.
- [x] Capítulo 21: retirar el 81 %, el 70/30 y la idea de que los tests son la
      única defensa.

## Prioridad 4 — Estructura y claridad

- [x] Dividir o reducir el capítulo 11.
  - [x] Añadir una ruta de lectura y delimitarlo frente a backend, datos y
        persistencia.
- [x] Dividir o reducir el capítulo 15.
  - [x] Añadir una ruta de lectura y retirar rankings y prescripciones
        dependientes de moda.
- [x] Revisar la extensión y delimitar el alcance de los capítulos 12, 13 y 17.
- [x] Unificar objetivos, modelo mental inicial, ejercicios y referencias.
- [x] Eliminar duplicaciones entre capítulos de modelado, persistencia,
      arquitectura y seguridad.
  - [x] Documentar límites y referencias cruzadas entre los capítulos 5, 11–13,
        15–17, 19, 21 y 26.
  - [x] Concentrar los fundamentos de estilos en el capítulo 3 y dejar en el 15
        la decisión arquitectónica.
  - [x] Concentrar patrones y dependencias en el capítulo 11 y convertir el 16
        en su aplicación al runtime del backend.
  - [x] Separar el diseño de índices del capítulo 13 de su observación
        operativa en el 19.
  - [x] Mantener los controles HTTP generales en el capítulo 5 y los riesgos
        propios de identidad en el 17.
- [x] Mantener los diagramas ASCII hasta completar la revisión textual.

## Fase visual

- [x] Inventariar los diagramas ASCII, recursos existentes y oportunidades
      visuales en los capítulos sin diagramas.
  - [x] Registrar 216 bloques detectados y separar ocho falsos positivos de
        código.
  - [x] Auditar 45 recursos existentes, incluidos publicados, exploraciones y
        descartados.
  - [x] Definir prioridades P0, P1 y P2 en el
        [inventario visual](./INVENTARIO-VISUAL.md).
- [x] Confirmar **editorial técnico luminoso** como único lenguaje visual y
      descartar blueprint y cuaderno técnico.
- [x] Validar los cuatro pilotos P0 en HonKit/GitBook y móvil.
- [ ] Verificar la salida impresa antes de preparar una edición para papel.
  - [x] Capítulo 1: auditar 15 SVG heredados, consolidar 12 publicaciones en
        seis funciones pedagógicas y preparar tres composiciones móviles.
  - [x] Capítulo 2: crear cuatro funciones pedagógicas desde el texto, preparar
        cuatro composiciones móviles y verificarlas localmente a 1280 y 420 px.
  - [x] Capítulo 3: crear cuatro funciones pedagógicas desde el texto, preparar
        cuatro composiciones móviles y verificarlas localmente a 1280, 759 y
        420 px.
  - [x] Capítulo 5: crear cuatro funciones pedagógicas desde el texto, preparar
        cuatro composiciones móviles y verificar carga, selección responsiva y
        ausencia de desbordamiento a 1280 y 420 px.
  - [x] Capítulo 6: conservar la ilustración conceptual aprobada y reemplazar
        el ciclo heredado por composiciones de escritorio y móvil sin
        porcentajes universales ni numeración obsoleta.
  - [x] Capítulo 7: consolidar ocho ASCII en cuatro funciones visuales y texto
        semántico; corregir el falso universal «elige dos» y actualizar el
        ejemplo de selección de base de datos.
  - [x] Capítulo 8: consolidar diez ASCII en tres funciones visuales y devolver
        fortalezas, límites, instrucciones, checklist y MCP a estructuras de
        texto copiables y buscables.
  - [x] Capítulo 9: consolidar cuatro ASCII en el iceberg del requerimiento y
        el contraste de fuentes de descubrimiento; conservar wireframe y cinco
        «por qué» como texto adaptable.
  - [x] Capítulos 10–19: completar una primera pasada de once funciones
        pedagógicas, generar 22 SVG de escritorio y móvil e integrar cada ancla
        en su contexto. La consolidación secundaria queda registrada en la
        [auditoría del lote](./design-system/AUDITORIA-VISUAL-CAPITULOS-10-19.md).
  - [x] Capítulos 20–29: completar una primera pasada de diez funciones,
        generar 20 SVG de escritorio y móvil y mantener geometría común para
        Next.js, FastAPI y Go. La consolidación secundaria queda registrada en
        la [auditoría del lote](./design-system/AUDITORIA-VISUAL-CAPITULOS-20-29.md).
  - [x] Capítulos 30–31 y apéndice C: completar cinco funciones y diez SVG para
        ciclo agéntico, MCP, control de autonomía, adopción técnica y ruta de
        aprendizaje. El cierre queda registrado en la
        [auditoría del lote](./design-system/AUDITORIA-VISUAL-CAPITULOS-30-31.md).
  - [x] Segunda pasada de los capítulos 11–15: consolidar MVC, patrones,
        API-first, estilos de API, ERD, B-Tree, riesgos, planificación,
        dependencias frontend y propiedad del estado en once funciones y 22
        SVG. El cierre queda registrado en la
        [auditoría de segunda pasada](./design-system/AUDITORIA-VISUAL-SEGUNDA-PASADA-11-15.md).
  - [x] Segunda pasada de los capítulos 17–20: consolidar sesión y token,
        passkeys, PKCE, autorización, canales de tiempo real, concurrencia,
        MVCC, caché, colas, outbox, CQRS y Event Sourcing en trece funciones y
        26 SVG. El cierre queda registrado en la
        [auditoría de segunda pasada](./design-system/AUDITORIA-VISUAL-SEGUNDA-PASADA-17-20.md).
- [x] Reemplazar los ASCII aprobados sin perder contenido buscable.
- [x] Añadir texto alternativo, `<title>` y `<desc>` a los recursos finales.
- [x] Completar la revisión visual de los 31 capítulos y cinco apéndices.

## Fundamentos ya auditados

- [x] Capítulo 1: anatomía de una aplicación web moderna.
- [x] Capítulo 2: HTML semántico, formularios y mejora progresiva.
- [x] Capítulo 3: CSS, layout adaptable y sistema visual.
- [x] Capítulo 4: JavaScript, eventos y runtime del navegador.
- [x] Capítulo 5: URL, DNS, TLS, HTTP, caché y seguridad del navegador.

## Desarrollo del contenido pendiente

- [x] Capítulo 24: Observabilidad.
- [x] Capítulo 25: Escalabilidad y rendimiento.
- [x] Capítulo 26: Seguridad en aplicaciones web.
- [x] Capítulo 27: Stack con Next.js y Node.js.
- [x] Capítulo 28: Stack con Python y FastAPI.
- [x] Capítulo 29: Stack con Go.
- [x] Capítulo 31: Tendencias y horizontes.
- [x] Apéndices A–E.

## Verificación final

- [x] Compilación HonKit sin advertencias de lenguajes desconocidos.
- [x] Enlaces y recursos locales válidos.
- [x] Revisión ortográfica final en español.
  - [x] Ejecutar Aspell sobre el texto narrativo fuera de bloques de código.
  - [x] Corregir préstamos evitables, puntuación, horarios y espacios
        residuales.
- [x] Revisión de referencias primarias y fechas de verificación.
  - [x] Verificar 375 enlaces bibliográficos.
  - [x] Clasificar 407 referencias y registrar el corte del 3 de agosto de 2026 en
        [la auditoría fuente por fuente](./AUDITORIA-REFERENCIAS.md).
- [x] Lectura completa en la versión web local.
  - [x] Revisar la introducción, los 31 capítulos y los cinco apéndices
        renderizados.
  - [x] Confirmar la progresión Fundamentos → Nuevo paradigma → Antes →
        Durante → Después → Integración → Futuro → Apéndices.
  - [x] Corregir tres separadores interpretados como encabezados y cuatro
        identificadores de ancla duplicados.
  - [x] Normalizar los encabezados y retirar la navegación manual redundante de
        los capítulos 17 y 18.
  - [x] Verificar jerarquía de encabezados, recursos, desbordamiento de prosa y
        tablas, y navegación anterior/siguiente.
  - [x] Generar las 37 páginas con HonKit y comprobar que el índice de búsqueda
        contiene las 37 páginas.
