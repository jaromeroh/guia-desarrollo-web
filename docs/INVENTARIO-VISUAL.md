# Inventario visual del manuscrito

> Corte editorial: 3 de agosto de 2026. Este documento inventaría y prioriza
> oportunidades visuales; no autoriza todavía la generación ni el reemplazo
> masivo de imágenes.

## Objetivo

Determinar dónde una imagen mejora de forma material la comprensión y dónde el
contenido debe seguir siendo texto, código o una tabla semántica. El inventario
cubre la introducción, los 31 capítulos, los cinco apéndices, los recursos ya
publicados y las exploraciones visuales existentes.

La unidad de inventario es la **función pedagógica**, no cada caja dibujada. Si
cinco bloques ASCII explican variaciones del mismo concepto, pueden resolverse
mediante una sola lámina comparativa.

## Resultado del barrido

Se localizaron **216 bloques cercanos a una representación visual** en 18 de
los 31 capítulos:

| Clasificación inicial | Cantidad | Tratamiento esperado |
|---|---:|---|
| Diagramas ASCII claros | 148 | Evaluar conversión, consolidación o rediseño |
| Esquemas compactos | 42 | Preferir tabla, árbol de texto o diagrama pequeño según el caso |
| Secuencias textuales | 18 | Mantener como texto salvo que el orden o los actores sean esenciales |
| Fragmentos de código detectados por sus flechas | 8 | Mantener como código; son falsos positivos |
| **Total detectado** | **216** | **No equivale a 216 imágenes** |

No se encontraron caracteres de cajas fuera de bloques de código. Esto facilita
el reemplazo posterior sin alterar párrafos narrativos.

### Distribución por parte

| Parte | Bloques detectados | Observación |
|---|---:|---|
| I. Fundamentos | 1 | Los capítulos 2–5 explican procesos visuales sin ASCII |
| II. Nuevo paradigma | 21 | Alta concentración en pensamiento sistémico e IA |
| III. Antes | 92 | Mayor densidad; arquitectura y APIs requieren consolidación |
| IV. Durante | 59 | Predominan flujos técnicos, protocolos y persistencia |
| V. Después | 27 | Testing, CI/CD y despliegue concentran los ASCII |
| VI. Stacks en práctica | 0 | Conviene una gramática común para comparar los tres stacks |
| VII. Futuro | 16 | Todos pertenecen al capítulo 30 |
| Apéndices | 0 válidos | Un resultado del apéndice B fue un falso positivo del detector |

## Recursos visuales existentes

El manuscrito de la edición 1.0 publica **185 SVG y un PNG**. El directorio de
producción contiene además dos PNG técnicos de respaldo; las exploraciones y
los recursos descartados se conservan fuera del contenido publicado:

| Grupo | Estado | Acción recomendada |
|---|---|---|
| 9 SVG del capítulo 1 | Publicados; seis funciones y tres variantes móviles | Conservar y verificar en cada salida del libro |
| 16 SVG de los capítulos 2–3 | Publicados; ocho funciones con variante móvil | Conservar y verificar en cada salida del libro |
| 10 SVG de los capítulos 4–5 | Publicados; cinco funciones con variante móvil | Conservar y verificar en cada salida del libro |
| 1 PNG y 2 SVG del capítulo 6 | Publicados; dos funciones, una con variante móvil | Conservar y verificar en cada salida del libro |
| 18 SVG de los capítulos 7–9 | Publicados; nueve funciones con variante móvil | Consolidados y verificados |
| 38 SVG de los capítulos 10–16 | Publicados; diecinueve funciones con variante móvil | Consolidados y verificados |
| 36 SVG de los capítulos 17–20 | Publicados; dieciocho funciones con variante móvil | Consolidados y verificados |
| 24 SVG de los capítulos 21–23 | Publicados; doce funciones con variante móvil | Segunda pasada cerrada |
| 12 SVG de los capítulos 24–29 | Publicados; seis funciones con variante móvil | Incluye la serie comparable de stacks |
| 20 SVG de los capítulos 30–31 y el apéndice C | Publicados; diez funciones con variante móvil | Segunda pasada y cierre verificados |
| 2 PNG técnicos de respaldo | No publicados | Mantener para inspección y compatibilidad |
| 15 PNG de exploración | Referenciados desde documentos de diseño | Conservar como historial; no publicarlos directamente |
| 9 SVG fuente de las exploraciones | Conservados en el historial | Mantener como originales editables |
| 8 PNG en `assets/images/descartadas` | Descartados de forma explícita | Excluir del manuscrito; conservar hasta cerrar la dirección visual |

Los 185 SVG finales referenciados incluyen `role="img"`,
`<title>` y `<desc>`, además de texto alternativo o explicación equivalente en
el manuscrito.

Las rutas de imagen que aparecen dentro de ejemplos HTML o JSX, como
`/producto.webp`, `/hero.jpg` o `product.image`, **no son recursos rotos del
libro**: forman parte del código mostrado al lector.

## Criterios de decisión

### Convertir o rediseñar como imagen

Una imagen se justifica cuando permite comprender mejor al menos una de estas
relaciones:

- orden temporal entre tres o más actores;
- fronteras, dependencias o dirección del flujo;
- jerarquía o composición de varias capas;
- comparación espacial entre alternativas;
- estados y transiciones;
- cardinalidades o relaciones entre entidades;
- retroalimentación, concurrencia o propagación de fallas.

### Conservar como texto, código o tabla

No se convertirá en imagen:

- una caja que solo encierra un párrafo o una lista;
- un árbol de carpetas que el lector necesita copiar o buscar;
- comandos, solicitudes HTTP, códigos de estado o fragmentos ejecutables;
- una matriz que ya puede expresarse como tabla Markdown accesible;
- una secuencia lineal de dos pasos que se entiende mejor en una oración;
- un resumen que duplica una ilustración anterior.

### Consolidar

Varios ASCII se convertirán en una sola lámina cuando compartan la misma
pregunta. Los primeros casos evidentes son:

- acoplamiento bajo/alto y cohesión baja/alta del capítulo 7;
- estados vacío, carga y error del capítulo 10;
- capas, Clean Architecture y arquitectura hexagonal del capítulo 11;
- familias de almacenamiento del capítulo 13;
- polling, long polling, SSE, WebSocket y WebTransport del capítulo 18;
- concurrencia, niveles de aislamiento y MVCC del capítulo 19;
- pirámide y trofeo de testing del capítulo 21;
- GitFlow y trunk-based development del capítulo 22;
- los tres stacks de los capítulos 27–29.

## Inventario por capítulo

`Otros` agrupa esquemas compactos y secuencias. Los ocho falsos positivos de
código no aparecen en esa columna. Los encabezados se usan como referencia
estable porque los números de línea cambiarán durante la edición.

| Cap. | ASCII claros | Otros | Visuales publicados | Ancla visual recomendada | Decisión inicial |
|---:|---:|---:|---:|---|---|
| 1 | 0 | 0 | 6 | Viaje completo de una petición | Consolidado, integrado y verificado en escritorio y móvil |
| 2 | 0 | 0 | 4 | HTML como contrato, formulario, validación y mejora progresiva | Consolidado, integrado y verificado en escritorio y móvil |
| 3 | 0 | 0 | 4 | Cascada, caja, elección de layout y alcance de queries | Consolidado, integrado y verificado en escritorio y móvil |
| 4 | 0 | 0 | 1 | Event loop: tareas, microtareas y renderizado | Integrado y verificado en escritorio y móvil |
| 5 | 0 | 0 | 4 | URL y origen, diagnóstico por capas, caché y seguridad del navegador | Consolidado, integrado y verificado en escritorio y móvil |
| 6 | 0 | 0 | 2 | Evolución del rol y ciclo antes/durante/después | Consolidado, integrado y verificado; ciclo con variante móvil |
| 7 | 0 | 0 | 4 | Frontera, calidad del diseño, trade-offs y flujo de carrito | ASCII consolidado; integrado y verificado en escritorio y móvil |
| 8 | 0 | 0 | 3 | Redistribución del trabajo, ciclo con evidencia y matriz de riesgo | ASCII consolidado; integrado y verificado en escritorio y móvil |
| 9 | 0 | 0 | 2 | Iceberg del requerimiento y fuentes de descubrimiento | ASCII consolidado; integrado y verificado en escritorio y móvil |
| 10 | 0 | 0 | 2 | Proceso y estados de interfaz | Primera pasada cerrada; ASCII consolidado en imagen, tablas y texto |
| 11 | 2 | 0 | 3 | MVC; Capas, Clean y Hexagonal | Segunda pasada cerrada; solo permanecen árboles de carpetas |
| 12 | 0 | 0 | 3 | API-first y elección entre estilos | Segunda pasada cerrada; ejemplos HTTP conservados como código |
| 13 | 1 | 0 | 3 | Modelo lógico del e-commerce e índices | Segunda pasada cerrada; solo permanece el árbol de migraciones |
| 14 | 0 | 0 | 4 | Riesgo, contexto, flujo y ciclo de planificación | Segunda pasada cerrada; relaciones visuales integradas y listas devueltas a Markdown |
| 15 | 2 | 0 | 3 | Renderizado, fronteras de módulos y propiedad del estado | Segunda pasada cerrada; solo permanecen árboles de proyecto |
| 16 | 0 | 0 | 1 | Pipeline de request, middleware y errores | Integrado desde el texto |
| 17 | 0 | 1 | 5 | Identidad, sesión, passkey, PKCE y autorización | Segunda pasada cerrada; el esquema compacto de JWT permanece como código |
| 18 | 0 | 0 | 3 | Elección, secuencias y escalado del canal | Segunda pasada cerrada; protocolos y payloads permanecen como código |
| 19 | 0 | 0 | 4 | Transacción, concurrencia, MVCC y caché | Segunda pasada cerrada; tablas conservan aislamiento, invalidación y búsqueda |
| 20 | 0 | 0 | 6 | Job, resiliencia, outbox, CQRS y Event Sourcing | Segunda pasada cerrada; código y prompts permanecen copiables |
| 21 | 0 | 0 | 4 | Estrategia de pruebas por riesgo | Segunda pasada cerrada; modelos, niveles y TDD con agente consolidados |
| 22 | 0 | 0 | 4 | Pipeline CI/CD y estrategias de ramas | Segunda pasada cerrada; branching y ciclo de flags consolidados |
| 23 | 0 | 0 | 4 | Espectro de hosting y despliegue sin interrupción | Segunda pasada cerrada; estrategias y promoción consolidadas |
| 24 | 0 | 0 | 1 | Correlación entre logs, métricas y trazas | Integrado desde el texto |
| 25 | 0 | 0 | 1 | Cuello de botella, capacidad y backpressure | Integrado desde el texto |
| 26 | 0 | 0 | 1 | Activos, actores y fronteras de confianza | Integrado desde el texto |
| 27 | 0 | 0 | 1 | Slice vertical en Next.js/Node.js | Integrado con geometría común |
| 28 | 0 | 0 | 1 | Slice vertical en FastAPI | Integrado con geometría común |
| 29 | 0 | 0 | 1 | Slice vertical en Go y comparación final | Integrado con geometría común |
| 30 | 0 | 0 | 8 | Nueva capa, agentes, herramientas y MCP | Segunda pasada cerrada; ocho funciones integradas y árboles copiables conservados como texto |
| 31 | 0 | 0 | 1 | Filtro de adopción y fundamentos durables | Integrado desde el texto |

### Apéndices

| Apéndice | Necesidad visual | Decisión inicial |
|---|---|---|
| A. Glosario | Baja | Mantener búsqueda y texto; no ilustrar términos por decoración |
| B. Herramientas | Baja | Las tablas son más mantenibles que un mapa de logos |
| C. Aprendizaje | Media | Ruta de seis etapas integrada con variante móvil |
| D. Plantillas | Baja | Conservar contenido copiable y accesible |
| E. Bibliografía | Nula | No añadir imágenes |

## Prioridades

### P0 — Validar y preparar los pilotos existentes

- [x] **V-P0-01:** viaje de una petición, estilo editorial técnico luminoso.
- [x] **V-P0-02:** flujo «agregar al carrito» y conexiones del sistema.
- [x] **V-P0-03:** comparación Capas/Clean/Hexagonal.
- [x] **V-P0-04:** ERD del e-commerce.
- [x] Corregir nombres de archivo heredados de la numeración anterior.
- [x] Probar SVG y PNG al ancho real de HonKit/GitBook y en móvil.
- [ ] Verificar la salida impresa antes de preparar una edición para papel.
- [x] Confirmar que título, texto alternativo, `<title>` y `<desc>` no se
      contradicen ni duplican.

### P1 — Diagramas ancla que desbloquean el lenguaje del libro

- [x] HTML, formulario, validación y mejora progresiva — capítulo 2. Cuatro
      funciones integradas con composiciones de escritorio y móvil.
- [x] Cascada, caja, elección de layout y alcance de queries — capítulo 3.
      Cuatro funciones integradas con composiciones de escritorio y móvil.
- [x] Event loop y renderizado — capítulo 4. Integrado con composiciones de
      escritorio y móvil verificadas localmente.
- [x] URL y origen, diagnóstico por capas, caché y seguridad del navegador —
      capítulo 5. Cuatro funciones integradas con composiciones de escritorio
      y móvil.
- [x] Fronteras, acoplamiento/cohesión, trade-offs y flujo de carrito —
      capítulo 7. Cuatro funciones integradas con composiciones de escritorio
      y móvil; los ocho ASCII se consolidaron o devolvieron a texto semántico.
- [x] Ciclo de trabajo con IA y riesgo — capítulo 8. Tres funciones integradas
      con composiciones de escritorio y móvil; listas y prompts permanecen como texto.
- [x] Descubrimiento de requerimientos — capítulo 9. Dos funciones integradas;
      el wireframe y los cinco «por qué» volvieron a texto semántico.
- [x] Proceso de diseño y estados de interfaz — capítulo 10. Dos funciones
      integradas; ASCII restantes devueltos a tablas o prosa.
- [x] Dirección de dependencias, MVC y comparación de patrones — capítulo 11.
      Segunda pasada cerrada; los dos árboles de carpetas siguen como texto.
- [x] Contrato, API-first y elección de estilo — capítulo 12. Segunda pasada
      cerrada; ejemplos HTTP conservados como código.
- [x] Niveles, ERD e índice B-Tree — capítulo 13. Segunda pasada cerrada; el
      árbol de migraciones sigue como texto.
- [x] Slice, riesgo, contexto, flujo y ciclo — capítulo 14. Segunda pasada
      cerrada sin ASCII visual restante.
- [x] Renderizado, dependencias y propiedad del estado — capítulo 15. Segunda
      pasada cerrada; árboles de proyecto conservados como texto.
- [x] Pipeline backend — capítulo 16. Ancla integrada desde el texto.
- [x] Identidad, sesión, passkey, PKCE y autorización — capítulo 17. Segunda
      pasada cerrada; el JWT compacto permanece como código.
- [x] Protocolos y escalado de tiempo real — capítulo 18. Segunda pasada
      cerrada; payloads y ejemplos permanecen como código.
- [x] Transacción, concurrencia, MVCC y caché — capítulo 19. Segunda pasada
      cerrada; aislamiento, invalidación y búsqueda permanecen como tablas.
- [x] Jobs, resiliencia, outbox, CQRS y Event Sourcing — capítulo 20. Segunda
      pasada cerrada sin ASCII visual restante.
- [x] Estrategia de testing — capítulo 21. Modelos de confianza, elección del
      nivel de prueba y TDD con agente consolidados en la segunda pasada.
- [x] Pipeline CI/CD — capítulo 22. CI/entrega/despliegue, branching y ciclo de
      feature flags consolidados en la segunda pasada.
- [x] Despliegue progresivo — capítulo 23. Estrategias de despliegue y promoción
      del artefacto consolidadas en la segunda pasada.
- [x] Sistema de observabilidad — capítulo 24. Correlación integrada desde el texto.
- [x] Escalabilidad y backpressure — capítulo 25. Ciclo de capacidad integrado.
- [x] Fronteras de confianza — capítulo 26. Controles por frontera integrados.
- [x] Serie comparable Next.js/FastAPI/Go — capítulos 27–29. Misma geometría,
      contrato y orden de responsabilidades.
- [x] Agentes, herramientas y MCP — capítulo 30. Ocho funciones integradas;
      contexto, ejecución, organización y orquestación consolidados en la
      segunda pasada.
- [x] Filtro de adopción técnica — capítulo 31. Integrado desde el texto.

### P2 — Apoyo y navegación

- [ ] Decisiones de caché y búsqueda.
- [ ] Máquinas de estado de tokens, jobs y despliegues.
- [ ] Mapas de estructura solo cuando expliquen dependencias, no carpetas.
- [x] Ruta de aprendizaje del apéndice C. Seis etapas con proyecto y evidencia.
- [ ] Láminas de apertura únicamente si aportan orientación conceptual.

## Alcance de producción estimado

El inventario **no recomienda 216 imágenes**. La primera estimación editorial
es:

- 4 pilotos P0;
- entre 24 y 32 diagramas ancla P1;
- entre 15 y 25 apoyos P2 después de evaluar la lectura;
- entre 45 y 60 imágenes finales para todo el libro, incluyendo las que ya
  existen y sobrevivan la auditoría.

La cifra debe disminuir si una tabla o una consolidación explica mejor el
contenido. No debe crecer para garantizar una cuota por capítulo.

## Reglas para la siguiente fase

1. Confirmar el sistema visual antes de producir en serie.
2. Trabajar primero sobre los cuatro pilotos P0.
3. Conservar SVG como fuente principal y PNG como respaldo de publicación.
4. Mantener el texto relevante fuera de la imagen cuando sea posible.
5. Proporcionar texto alternativo y explicación cercana para relaciones
   complejas.
6. No comunicar significado únicamente mediante color.
7. Usar títulos del documento, no títulos incrustados repetidos en la imagen.
8. Verificar ancho móvil, contraste, modo oscuro e impresión.
9. Sustituir el ASCII solo después de aprobar la imagen en la versión local.
10. No eliminar recursos históricos o descartados sin una decisión separada.

## Próxima decisión

Revisar los pilotos P0 y las pruebas de producción con **editorial técnico
luminoso**, el único lenguaje visual aprobado. El blueprint y el cuaderno
técnico quedan como exploraciones históricas descartadas. Después de validar
las pruebas al ancho real de lectura conviene fijar tokens, plantillas y nombres
definitivos.
