# Apéndice A. Glosario

Este glosario define los términos como se usan en el libro. No intenta
reemplazar especificaciones. Cuando una palabra posee varios significados, se
explicita el que importa para aplicaciones web.

Los términos ingleses se conservan cuando son la forma habitual en código,
documentación o conversación técnica.

---

## A

**Accesibilidad:** propiedad de un producto que permite a personas con
capacidades, dispositivos y contextos diversos percibirlo, comprenderlo y
operarlo. No es sinónimo de compatibilidad con un único lector de pantalla.

**ACID:** conjunto de propiedades asociadas a transacciones: atomicidad,
consistencia, aislamiento y durabilidad. No garantiza por sí solo que las reglas
del negocio estén bien modeladas.

**Actor:** persona, sistema o proceso que interactúa con una aplicación. En
seguridad, puede ser legítimo, accidental o hostil.

**Agente:** sistema que recibe un objetivo, observa contexto, decide acciones,
usa herramientas y evalúa resultados dentro de límites definidos.

**API (Application Programming Interface):** contrato mediante el cual un
componente ofrece capacidades a otro. Puede ser una API HTTP, una función, una
interfaz de lenguaje o una herramienta para agentes.

**API idempotente:** operación que puede repetirse con la misma intención sin
aplicar varias veces el mismo efecto. Idempotencia no significa que todas las
respuestas deban ser idénticas.

**Artefacto:** salida versionable de un proceso de build, como una imagen de
contenedor, un binario, un paquete o archivos estáticos.

**Asincronía:** modelo en el que una tarea puede suspenderse mientras espera y
permitir que avance otro trabajo. No implica necesariamente paralelismo.

**Autenticación:** proceso para establecer o verificar una identidad.

**Autorización:** decisión sobre qué operación puede realizar una identidad
sobre un recurso en un contexto.

**Availability / disponibilidad:** proporción o condición en la que un sistema
puede atender una operación válida. Debe definirse con población, ventana y
criterios concretos.

---

## B

**Backpressure:** mecanismo mediante el cual un consumidor o dependencia
comunica que no puede aceptar trabajo al ritmo actual.

**Backend:** parte del sistema que ejecuta lógica fuera del navegador, coordina
datos y aplica políticas. Puede ser un monolito, una función o varios servicios.

**Backend for Frontend (BFF):** capa de servidor diseñada para las necesidades
de una interfaz concreta. No reemplaza automáticamente todos los servicios.

**Baseline:** medición o comportamiento de referencia contra el cual se evalúa
un cambio.

**Branch / rama:** línea de desarrollo en control de versiones que referencia
una secuencia de commits.

**Build:** proceso que transforma código y dependencias en artefactos
ejecutables o publicables.

**Bundle:** conjunto de módulos y recursos empaquetados para su entrega, con
frecuencia al navegador.

---

## C

**Caché:** copia reutilizable de un resultado para evitar trabajo posterior.
Necesita clave, política de frescura, invalidación y comportamiento ante fallos.

**Capacidad:** cantidad de carga que un sistema puede atender respetando sus
objetivos de servicio.

**CDN (Content Delivery Network):** red distribuida que entrega contenido desde
ubicaciones cercanas o conectadas eficientemente con los usuarios.

**CI (Continuous Integration):** práctica de integrar cambios frecuentemente y
verificarlos mediante un pipeline reproducible.

**CD (Continuous Delivery/Deployment):** capacidad de mantener cambios
publicables o desplegarlos automáticamente después de verificarlos. El
significado exacto debe aclararse.

**Cliente:** componente que inicia una interacción con otro. Un navegador es un
cliente HTTP; un backend también puede ser cliente de otro servicio.

**Commit:** objeto de control de versiones que registra un estado y sus padres.

**Componente:** unidad con una responsabilidad y una interfaz. Puede ser visual,
de dominio o de infraestructura.

**Concurrencia:** progreso de varias tareas durante un intervalo solapado. No
requiere que se ejecuten simultáneamente en distintos núcleos.

**Consistencia:** término dependiente del contexto. Puede referirse a invariantes
válidas en una transacción o a qué versiones de datos observan nodos
distribuidos.

**Contenedor:** proceso aislado mediante capacidades del sistema operativo y
empaquetado con filesystem y metadata. No es una máquina virtual completa.

**Contrato:** expectativas observables entre partes: entradas, salidas, errores,
invariantes, tiempos o compatibilidad.

**Cookie:** dato que el navegador almacena y asocia a reglas de dominio, path y
otros atributos, y que puede enviar en requests HTTP.

**CORS (Cross-Origin Resource Sharing):** protocolo de headers mediante el que
un servidor permite que ciertos orígenes lean respuestas desde scripts del
navegador. No es autenticación ni firewall.

**CSP (Content Security Policy):** política que restringe fuentes y capacidades
de contenido en una página para reducir impacto de ciertas inyecciones.

**CSRF (Cross-Site Request Forgery):** ataque que induce a un navegador a enviar
una request autenticada no deseada a otro sitio.

**Cursor:** valor opaco o compuesto que representa una posición estable para
continuar una colección paginada.

---

## D

**Data Access Layer (DAL):** frontera que centraliza consultas, selección de
campos y, cuando corresponde, autorización cercana a los datos.

**Deadline:** instante máximo hasta el que una operación puede continuar. Es
preferible a sumar timeouts inconexos porque expresa un presupuesto total.

**Degradación controlada:** reducción intencional de funcionalidad o calidad
para conservar operaciones prioritarias durante fallos o sobrecarga.

**Denegación por defecto:** política según la cual una operación no permitida
explícitamente se rechaza.

**Dependency injection:** técnica para entregar a un componente sus
colaboradores desde fuera, en lugar de construirlos dentro.

**Deployment / despliegue:** proceso que lleva un artefacto y su configuración a
un ambiente de ejecución.

**DNS (Domain Name System):** sistema distribuido que resuelve nombres y
publica otros registros. Resolver un dominio es solo una parte del camino hacia
una aplicación.

**DOM (Document Object Model):** representación en objetos de un documento que
el navegador expone a scripts y herramientas.

**DTO (Data Transfer Object):** estructura diseñada para transportar datos por
una frontera, no necesariamente para representar todo el dominio.

**Durabilidad:** propiedad según la cual los efectos confirmados sobreviven a
los fallos cubiertos por el sistema.

---

## E

**Edge:** ubicación de cómputo o entrega distribuida cerca de usuarios o redes
de acceso. No garantiza baja latencia si los datos o efectos están lejos.

**Endpoint:** combinación expuesta de método, ruta y comportamiento en una API.

**Entidad:** objeto de dominio cuya identidad persiste aunque cambien sus
atributos.

**Error budget:** cantidad tolerada de incumplimiento de un objetivo de
fiabilidad durante una ventana.

**Escalabilidad:** capacidad de sostener más carga mediante recursos,
distribución o cambios arquitectónicos sin incumplir objetivos.

**Esquema:** descripción de la estructura de datos, sus tipos y restricciones.
Puede pertenecer a una base, mensaje o API.

**Estado:** información que influye en resultados futuros. Puede vivir en
memoria, cookies, una base, una cola o un sistema externo.

**Evaluación (eval):** conjunto de casos, criterios y mediciones usado para
comparar comportamiento, especialmente de sistemas de IA.

---

## F

**Fallback:** alternativa que conserva una experiencia útil cuando una
capacidad principal no está disponible.

**Feature flag:** decisión de configuración que habilita o cambia comportamiento
sin requerir necesariamente otro artefacto.

**Frontend:** parte del sistema responsable de la experiencia del usuario,
frecuentemente ejecutada en el navegador.

**Frontera de confianza:** punto donde datos o acciones pasan entre contextos
con distintas garantías o privilegios.

**Función pura:** función cuyo resultado depende solo de sus argumentos y que no
produce efectos observables externos.

---

## G

**Garbage collector (GC):** mecanismo que recupera memoria de objetos que ya no
son alcanzables.

**Goroutine:** unidad ligera de ejecución concurrente gestionada por el runtime
de Go.

**Graceful shutdown:** terminación que deja de aceptar trabajo, drena operaciones
en curso y cierra recursos dentro de un plazo.

---

## H

**Hash criptográfico:** función unidireccional que produce una salida de tamaño
fijo. No equivale a cifrado y no todos los hashes sirven para contraseñas.

**Header HTTP:** campo de metadata de una request o respuesta. Su semántica
depende de la especificación y del contexto.

**HTML semántico:** uso de elementos según el significado y la estructura del
contenido, no solo según su apariencia.

**HTTP:** protocolo de aplicación basado en requests y respuestas, con métodos,
status, headers, representación y caché.

**HTTPS:** HTTP protegido mediante TLS. Protege el transporte bajo su modelo de
confianza; no vuelve correcta ni segura toda la aplicación.

---

## I

**IA generativa:** sistema que produce contenido a partir de contexto e
instrucciones. Su salida puede variar y necesita verificación proporcional al
riesgo.

**Índice de base de datos:** estructura que acelera ciertos accesos a cambio de
espacio y coste en escrituras y mantenimiento.

**Infraestructura como código (IaC):** definición versionable de recursos y
configuración de infraestructura.

**Invariante:** condición que debe mantenerse válida en los estados relevantes
del sistema.

**Idempotency key:** identificador de un intento lógico que permite reconocer
repeticiones de una operación.

---

## J

**JSON:** formato textual de intercambio con objetos, arrays, strings, números,
booleanos y null. No expresa por sí solo fechas, UUID ni precisión monetaria.

**JWT (JSON Web Token):** formato compacto de claims protegidos mediante firma o
cifrado según la familia JOSE. Ser JWT no vuelve confiable un token: debe
validarse su contexto criptográfico y semántico.

---

## L

**Latencia:** tiempo entre dos puntos definidos de una operación. Conviene
observar una distribución, no solo un promedio.

**Least privilege / mínimo privilegio:** asignación de solo las capacidades
necesarias, durante el tiempo y alcance necesarios.

**Liveness:** señal de que un proceso sigue vivo y puede requerir reinicio si
falla. No debe confundirse con estar listo para tráfico.

**Lock-in:** coste técnico, económico u organizacional de reemplazar una
tecnología o proveedor.

**Log:** registro discreto de un evento. Debe ser estructurado, útil y respetar
privacidad.

---

## M

**MCP (Model Context Protocol):** protocolo para exponer herramientas, recursos
y otras capacidades a aplicaciones de IA. Interoperabilidad no concede
confianza ni permisos automáticamente.

**Mensaje:** unidad de datos transmitida entre productores y consumidores,
frecuentemente mediante una cola o log.

**Métrica:** serie numérica agregable a lo largo del tiempo. Sus labels deben
tener cardinalidad controlada.

**Middleware:** componente que envuelve o intercepta un recorrido para aplicar
comportamiento transversal.

**Migración:** cambio versionado del esquema o los datos de un sistema vivo.

**Mock:** sustituto programable usado para comprobar interacciones. No reproduce
necesariamente la semántica de la dependencia real.

**Monolito modular:** aplicación desplegada como una unidad, dividida
internamente en módulos con límites explícitos.

---

## O

**OAuth:** familia de protocolos de autorización delegada. No es por sí sola un
protocolo de autenticación del usuario final.

**Observabilidad:** capacidad de investigar el estado interno de un sistema a
partir de sus señales y contexto.

**OIDC (OpenID Connect):** capa de identidad construida sobre OAuth 2.0 que
define, entre otros elementos, un ID Token y endpoints de descubrimiento.

**OpenAPI:** especificación para describir APIs HTTP, sus operaciones y esquemas.

**Origen web:** tupla de esquema, host y puerto usada por el modelo de seguridad
del navegador.

**ORM (Object-Relational Mapper):** herramienta que mapea objetos o estructuras
del lenguaje a datos relacionales. No elimina la necesidad de entender SQL,
transacciones e índices.

**Outbox transaccional:** patrón que guarda el cambio de dominio y un mensaje
pendiente dentro de la misma transacción para publicarlo posteriormente.

---

## P

**Paginación:** división de una colección en partes acotadas mediante offset,
cursor u otra estrategia.

**Paralelismo:** ejecución simultánea de trabajo, normalmente en varios núcleos,
procesos o máquinas.

**Passkey:** credencial basada en claves públicas, normalmente sincronizable o
ligada a un dispositivo, usada mediante WebAuthn/FIDO.

**Pipeline:** secuencia automatizada de etapas que transforma o verifica un
cambio.

**Pool:** conjunto limitado y reutilizable de recursos como conexiones, threads
o workers.

**Progressive enhancement / mejora progresiva:** estrategia que comienza con una
experiencia funcional básica y añade capacidades cuando están disponibles.

**Prompt:** instrucciones y contexto entregados a un modelo. No constituye una
frontera de seguridad.

**Proxy:** intermediario que recibe tráfico y lo reenvía, pudiendo aplicar
routing, TLS, caché, observabilidad o políticas.

---

## Q

**Queue / cola:** estructura o servicio que desacopla productores y consumidores
en el tiempo. La semántica de entrega debe documentarse.

---

## R

**Race condition:** fallo cuyo resultado depende de un orden de ejecución no
controlado entre operaciones concurrentes.

**Rate limit:** límite de operaciones permitido por identidad, origen, recurso o
ventana. Es un control de capacidad y abuso, no autorización.

**Readiness:** señal de que una instancia puede recibir tráfico útil. Puede
depender de inicialización y recursos críticos.

**Reintento:** nueva ejecución después de un fallo. Necesita clasificación de
errores, deadline, backoff, jitter e idempotencia.

**Release:** versión de artefactos y configuración preparada para ser
desplegada.

**Repositorio:** en este libro, componente que encapsula persistencia de una
capacidad. También puede significar el espacio de control de versiones.

**Request:** mensaje HTTP iniciado por un cliente con método, URL, headers y
posible body.

**Response:** mensaje HTTP con status, headers y posible representación.

**Rollback:** retorno a una versión o estado anterior conocido. Revertir código
no siempre revierte datos.

**Runtime:** entorno que ejecuta código y define APIs, memoria, scheduling y
límites.

---

## S

**Sanitización:** transformación de contenido no confiable para conservar solo
una forma permitida. Es distinta de validación y codificación de salida.

**SBOM (Software Bill of Materials):** inventario de componentes incluidos en
un artefacto.

**SDK:** conjunto de bibliotecas y herramientas para integrar una plataforma o
servicio.

**Semántica:** significado observable de una estructura u operación, más allá
de su sintaxis.

**Server Component:** componente que se ejecuta en un entorno de servidor y
produce una representación para el árbol de UI sin enviar necesariamente su
código al navegador.

**Sesión:** asociación entre interacciones y un estado autenticado u otro
contexto. Una cookie puede transportar un identificador de sesión, pero no son
lo mismo.

**SLA (Service Level Agreement):** acuerdo sobre nivel de servicio y
consecuencias entre partes.

**SLI (Service Level Indicator):** medición concreta de un aspecto del servicio.

**SLO (Service Level Objective):** objetivo para un SLI durante una población y
ventana definidas.

**SSR (Server-Side Rendering):** generación de HTML en el servidor para una
request o build.

**SSRF (Server-Side Request Forgery):** abuso de una capacidad del servidor para
realizar requests hacia destinos no autorizados.

**Subagente:** ejecución delegada con tarea, contexto, herramientas y entregable
acotados.

---

## T

**Tenant:** unidad de aislamiento lógico de clientes u organizaciones dentro de
un sistema multi-tenant.

**Throughput:** cantidad de operaciones completadas por unidad de tiempo.

**Timeout:** duración máxima permitida para una fase u operación.

**TLS:** protocolo criptográfico que protege confidencialidad e integridad del
transporte y autentica endpoints según certificados y configuración.

**Token:** representación de claims, identidad, autorización o referencia. Su
significado y seguridad dependen del formato y del emisor.

**Trace / traza:** representación del recorrido de una operación distribuida
mediante spans relacionados.

**Transacción:** unidad de operaciones que el sistema trata con propiedades
definidas de atomicidad y aislamiento.

**Trust boundary:** véase **frontera de confianza**.

---

## U

**URL:** identificador de un recurso que incluye esquema y componentes
dependientes de ese esquema.

**User agent:** software que actúa en nombre del usuario al interactuar con la
web, como un navegador.

**UX (User Experience):** experiencia completa de una persona al intentar
alcanzar un objetivo con el producto.

---

## V

**Validación:** comprobación de que datos cumplen forma, límites y reglas
esperadas. La validación del cliente mejora UX; la del servidor protege la
frontera.

**Vector de ataque:** camino o mecanismo mediante el cual un actor intenta
afectar un activo.

**Versionado semántico:** convención `major.minor.patch` cuya interpretación
depende de que el proyecto defina y respete su API pública.

---

## W

**WASI:** conjunto de interfaces para ejecutar componentes WebAssembly fuera del
navegador mediante capacidades proporcionadas por el host.

**WebAssembly (Wasm):** formato portable de bajo nivel para ejecución eficiente
y compacta dentro de un host.

**WebAuthn:** API web para crear y usar credenciales de clave pública mediante
autenticadores.

**Webhook:** request HTTP que un sistema envía a otro para notificar un evento.
Necesita autenticación, reintentos, idempotencia y protección contra replay.

**WebSocket:** protocolo que establece comunicación bidireccional persistente
después de un handshake HTTP.

**Worker:** proceso, thread o unidad que consume trabajo fuera del recorrido
sincrónico principal.

---

## X

**XSS (Cross-Site Scripting):** inyección que provoca que contenido no confiable
se ejecute como script o markup activo en el contexto de un sitio.

---

## Familias de conceptos

Cuando un término aislado no sea suficiente, consulta la familia:

| Pregunta | Conceptos relacionados |
|----------|------------------------|
| ¿Quién puede hacer qué? | Autenticación, autorización, sesión, token, tenant |
| ¿Cómo viaja una operación? | URL, DNS, TLS, HTTP, request, response |
| ¿Cómo se conserva corrección? | Invariante, transacción, ACID, idempotencia |
| ¿Cómo se comporta bajo carga? | Latencia, throughput, pool, backpressure |
| ¿Cómo se investiga producción? | Log, métrica, traza, SLI, SLO |
| ¿Cómo se publica un cambio? | Build, artefacto, pipeline, release, deployment |
| ¿Cómo se reduce riesgo? | Frontera, mínimo privilegio, validación, rollback |
| ¿Cómo participa la IA? | Prompt, contexto, agente, herramienta, eval, MCP |
