# 2. Anatomía de una Aplicación Web Moderna

> ¿Qué sucede realmente entre el momento en que un usuario hace clic y ve el resultado en pantalla?

## Objetivos de Aprendizaje

Al finalizar este capítulo, serás capaz de:
- Identificar los componentes fundamentales de una aplicación web
- Entender la diferencia entre cliente, servidor y servicios en la nube
- Comparar arquitecturas: monolitos, microservicios y serverless
- Trazar el flujo completo de una petición desde el navegador hasta la base de datos y de vuelta

---

## El mapa del territorio

Antes de profundizar en técnicas específicas, necesitas un mapa mental de cómo encajan todas las piezas. Este capítulo te da ese mapa.

Una aplicación web moderna no es un programa que corre en una computadora. Es un **sistema distribuido**: múltiples programas, corriendo en múltiples computadoras, comunicándose a través de la red.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INTERNET                                      │
└─────────────────────────────────────────────────────────────────────┘
        │                    │                      │
        ▼                    ▼                      ▼
   ┌─────────┐         ┌──────────┐          ┌──────────┐
   │ Usuario │         │ Usuario  │          │ Usuario  │
   │ (Chile) │         │ (México) │          │ (España) │
   └────┬────┘         └────┬─────┘          └────┬─────┘
        │                   │                     │
        └───────────────────┼─────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │      CDN      │    ← Contenido estático
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Load Balancer│    ← Distribuye tráfico
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Servidor │  │ Servidor │  │ Servidor │
        │    #1    │  │    #2    │  │    #3    │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
              └─────────────┼─────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Base de Datos │
                    └───────────────┘
```

No te preocupes si esto parece complejo. Vamos a desarmarlo pieza por pieza.

---

## Cliente y Servidor: la división fundamental

📖 **Concepto**: En la web, hay dos roles fundamentales: el **cliente** (quien pide) y el **servidor** (quien responde). Esta división existe desde los orígenes de Internet y sigue siendo el modelo mental más importante.

### El Cliente

El cliente es cualquier programa que inicia una petición. En el contexto web, típicamente es:

- **El navegador** (Chrome, Firefox, Safari)
- **Una app móvil** que consume APIs
- **Otro servidor** que necesita datos de tu servicio

El cliente vive en el dispositivo del usuario. Tú no controlas ese ambiente:

```
Lo que controlas:          Lo que NO controlas:
──────────────────────────────────────────────────
El código que envías       El navegador del usuario
                           La velocidad de conexión
                           El tamaño de pantalla
                           Si tiene JavaScript habilitado
                           Las extensiones instaladas
                           Si está en modo avión
```

⚠️ **Advertencia**: Nunca confíes en el cliente. Todo lo que viene del navegador puede ser manipulado. La validación en el cliente es para UX; la validación real ocurre en el servidor.

### El Servidor

El servidor es un programa que escucha peticiones y responde. A diferencia del cliente, el servidor está bajo tu control total:

- Decides qué hardware usar
- Controlas el sistema operativo
- Instalas las dependencias exactas que necesitas
- Manejas los secretos (API keys, contraseñas de BD)

```javascript
// Ejemplo conceptual de un servidor minimalista
const server = createServer((request, response) => {
  // 1. Recibe la petición
  const { url, method, headers, body } = request;

  // 2. Procesa (lógica de negocio, base de datos, etc.)
  const result = processRequest(url, method, body);

  // 3. Envía respuesta
  response.send(result);
});

server.listen(3000); // Escucha en puerto 3000
```

### La comunicación: HTTP

Cliente y servidor hablan a través de **HTTP** (HyperText Transfer Protocol). Es un protocolo de petición-respuesta:

```
┌──────────┐                              ┌──────────┐
│  Cliente │                              │ Servidor │
└────┬─────┘                              └────┬─────┘
     │                                         │
     │  ────── Petición HTTP ──────────────▶  │
     │         GET /api/users                  │
     │         Headers: { auth: "token" }      │
     │                                         │
     │                                         │ (procesa)
     │                                         │
     │  ◀────── Respuesta HTTP ─────────────  │
     │          Status: 200 OK                 │
     │          Body: [{ id: 1, name: "Ana" }] │
     │                                         │
```

Los métodos HTTP más comunes:

| Método | Propósito | ¿Modifica datos? |
|--------|-----------|------------------|
| GET | Obtener datos | No |
| POST | Crear nuevo recurso | Sí |
| PUT | Reemplazar recurso completo | Sí |
| PATCH | Modificar parcialmente | Sí |
| DELETE | Eliminar recurso | Sí |

---

## Las capas de una aplicación

Una aplicación web moderna tiene múltiples capas, cada una con responsabilidades específicas.

### Vista de capas (de arriba hacia abajo)

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                      │
│  (Lo que el usuario ve e interactúa)                        │
│  ─────────────────────────────────────────────────────────  │
│  HTML, CSS, JavaScript, React/Vue/Svelte                    │
│  Corre en: Navegador del usuario                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────┐
│                      CAPA DE API                             │
│  (El contrato entre cliente y servidor)                      │
│  ─────────────────────────────────────────────────────────  │
│  REST endpoints, GraphQL, tRPC                               │
│  Autenticación, validación de entrada                        │
│  Corre en: Servidor                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  CAPA DE LÓGICA DE NEGOCIO                   │
│  (Las reglas y procesos del dominio)                         │
│  ─────────────────────────────────────────────────────────  │
│  Servicios, casos de uso, validaciones de negocio            │
│  "Un usuario no puede tener más de 3 pedidos pendientes"     │
│  Corre en: Servidor                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE ACCESO A DATOS                     │
│  (Comunicación con bases de datos y servicios externos)      │
│  ─────────────────────────────────────────────────────────  │
│  Repositories, ORMs, clientes de APIs externas               │
│  Corre en: Servidor                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE PERSISTENCIA                       │
│  (Donde viven los datos)                                     │
│  ─────────────────────────────────────────────────────────  │
│  PostgreSQL, MongoDB, Redis, S3                              │
│  Corre en: Servidor de base de datos (o servicio en nube)    │
└─────────────────────────────────────────────────────────────┘
```

💡 **Insight**: Las capas no son una burocracia. Cada una tiene una razón de existir: separar responsabilidades hace que el código sea más fácil de entender, probar y modificar. Cuando todo está mezclado, un cambio en la UI puede romper la base de datos.

---

## Dos decisiones arquitectónicas fundamentales

Cuando diseñas la arquitectura de tu aplicación, no tomas una decisión—tomas **dos decisiones independientes** que se pueden combinar:

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│   DECISIÓN 1: ¿Cómo ORGANIZO el código?                       │
│   ──────────────────────────────────────                       │
│   Monolito ◄─────────────────────────────► Microservicios     │
│   (todo junto)                              (servicios separados)
│                                                                │
│   DECISIÓN 2: ¿Cómo EJECUTO el código?                        │
│   ──────────────────────────────────────                       │
│   Tradicional ◄──────────────────────────► Serverless         │
│   (servidores 24/7)                         (funciones on-demand)
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

Estas dos dimensiones son **ortogonales**: puedes combinarlas de cualquier manera. Veamos cada una.

---

### Decisión 1: Organización del código

Esta decisión responde: *¿Cómo divido las responsabilidades de mi aplicación?*

#### Monolito

Todo el código del servidor vive en una sola aplicación, un solo repositorio, un solo deployment.

```
┌────────────────────────────────────────┐
│              MONOLITO                   │
├────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ Usuarios │ │ Productos│ │ Pagos  │ │
│  └──────────┘ └──────────┘ └────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ Envíos   │ │ Reportes │ │ Admin  │ │
│  └──────────┘ └──────────┘ └────────┘ │
│                                        │
│         Una base de datos              │
│         Un deployment                  │
│         Un repositorio                 │
└────────────────────────────────────────┘
```

**Ventajas:**
- Simple de desarrollar y debuggear
- Una sola base de datos = transacciones ACID fáciles
- Un solo deployment = menos complejidad operacional
- Ideal para equipos pequeños

**Desventajas:**
- Todo escala junto (aunque solo necesites escalar una parte)
- Un error puede tumbar todo el sistema
- El código tiende a acoplarse con el tiempo
- Deployments más riesgosos a medida que crece

#### Microservicios

La aplicación se divide en servicios pequeños e independientes que se comunican por red.

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Usuarios   │   │  Productos   │   │    Pagos     │
│   Service    │   │   Service    │   │   Service    │
├──────────────┤   ├──────────────┤   ├──────────────┤
│  Base Datos  │   │  Base Datos  │   │  Base Datos  │
│   Usuarios   │   │  Productos   │   │    Pagos     │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                    ┌─────┴─────┐
                    │    API    │
                    │  Gateway  │
                    └───────────┘
```

**Ventajas:**
- Escala independiente por servicio
- Equipos pueden trabajar de forma autónoma
- Fallo aislado (un servicio puede caer sin tumbar todo)
- Libertad tecnológica por servicio

**Desventajas:**
- Complejidad operacional masiva
- Latencia de red entre servicios
- Transacciones distribuidas son difíciles
- Debugging es más complicado

⚠️ **Advertencia**: Los microservicios resuelven problemas **organizacionales**, no técnicos. Si tienes un equipo de 5 personas, probablemente no necesitas microservicios. La regla informal: considera microservicios cuando tengas más desarrolladores que los que pueden trabajar efectivamente en un solo repositorio (~10-15 personas).

---

### Decisión 2: Modelo de ejecución

Esta decisión responde: *¿Cómo y dónde corre mi código?*

#### Servidores tradicionales

Tu aplicación corre como un proceso (o varios) en servidores que están encendidos 24/7, esperando peticiones.

```
┌─────────────────────────────────────────────────────┐
│              SERVIDOR TRADICIONAL                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│   ┌─────────────────────────────────────────────┐   │
│   │              Tu aplicación                   │   │
│   │         (proceso corriendo 24/7)             │   │
│   │                                              │   │
│   │   Esperando... → Petición → Respuesta →     │   │
│   │   Esperando... → Petición → Respuesta →     │   │
│   │   Esperando...                               │   │
│   └─────────────────────────────────────────────┘   │
│                                                      │
│   Ejemplos: VPS, EC2, Docker en un servidor,        │
│             Kubernetes, tu laptop corriendo Node     │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Ventajas:**
- Control total sobre el ambiente
- Sin cold starts (siempre listo)
- Costo predecible
- Conexiones persistentes fáciles (WebSockets)
- Sin límites de tiempo de ejecución

**Desventajas:**
- Pagas aunque no haya tráfico
- Tú manejas el escalado
- Mantenimiento de servidores (actualizaciones, seguridad)

#### Serverless (Functions as a Service)

Tu código se empaqueta como funciones que se ejecutan **solo cuando hay una petición**. El proveedor maneja todo lo demás.

```
┌─────────────────────────────────────────────────────┐
│              SERVERLESS / FaaS                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│   Sin peticiones:  💤 (nada corriendo, $0)          │
│                                                      │
│   Petición llega:                                    │
│   ┌──────────┐                                       │
│   │ λ función│ ──▶ Respuesta ──▶ 💤                 │
│   └──────────┘     (se apaga)                       │
│                                                      │
│   Muchas peticiones:                                 │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│   │ λ        │ │ λ        │ │ λ        │  (auto)   │
│   └──────────┘ └──────────┘ └──────────┘           │
│                                                      │
│   Ejemplos: AWS Lambda, Vercel Functions,            │
│             Cloudflare Workers, Netlify Functions    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Ventajas:**
- No manejas servidores
- Escala a cero (no pagas si no hay tráfico)
- Escala automáticamente bajo carga
- Menos código de infraestructura

**Desventajas:**
- Cold starts (latencia cuando la función "despierta")
- Límites de tiempo de ejecución (típicamente 10-30 segundos)
- Vendor lock-in
- WebSockets y conexiones persistentes son más difíciles

---

### La matriz: combinando las dos decisiones

Aquí está la clave conceptual: **puedes combinar cualquier organización con cualquier ejecución**.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                           ORGANIZACIÓN                              │
│                                                                     │
│                     Monolito          Microservicios                │
│                 ┌───────────────┬─────────────────────┐             │
│                 │               │                     │             │
│   Tradicional   │  Rails en     │  Kubernetes con     │             │
│   (servidores   │  un VPS       │  Docker             │             │
│    24/7)        │               │                     │             │
│                 │  Django en    │  Cada servicio en   │             │
│ E               │  EC2          │  su contenedor      │             │
│ J               │               │                     │             │
│ E               ├───────────────┼─────────────────────┤             │
│ C               │               │                     │             │
│ U               │  Next.js en   │  Cada servicio      │             │
│ C   Serverless  │  Vercel       │  como Lambdas       │             │
│ I   (funciones  │               │                     │             │
│ Ó    on-demand) │  Remix en     │  Event-driven       │             │
│ N               │  Cloudflare   │  architecture       │             │
│                 │               │                     │             │
│                 └───────────────┴─────────────────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

📖 **Concepto**: Next.js desplegado en Vercel es un **monolito serverless**: organización de monolito (un repo, un proyecto, frontend y API juntos) con ejecución serverless (cada ruta es una función Lambda).

### Ejemplos del mundo real

| Combinación | Ejemplo | Por qué funciona |
|-------------|---------|------------------|
| **Monolito + Tradicional** | Basecamp (Rails), Shopify | Simplicidad, equipo cohesivo, control total |
| **Monolito + Serverless** | Next.js en Vercel, Remix en Cloudflare | Simplicidad de desarrollo + escala automática |
| **Microservicios + Tradicional** | Netflix, Uber (Kubernetes) | Múltiples equipos, escala masiva, control fino |
| **Microservicios + Serverless** | Backend distribuido en AWS Lambda | Escala por servicio, pago granular por uso |

---

### Guía de decisión

Ahora que entiendes que son dos decisiones separadas, aquí está cómo tomar cada una:

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   DECISIÓN 1: ¿Monolito o Microservicios?                          │
│   ─────────────────────────────────────────                         │
│                                                                     │
│   ¿Equipo pequeño (< 10 personas)?                                 │
│       └──▶ MONOLITO                                                 │
│                                                                     │
│   ¿Un solo producto con dominio cohesivo?                          │
│       └──▶ MONOLITO                                                 │
│                                                                     │
│   ¿Múltiples equipos que necesitan autonomía total?                │
│       └──▶ MICROSERVICIOS                                           │
│                                                                     │
│   ¿Partes del sistema con requisitos de escala muy diferentes?     │
│       └──▶ MICROSERVICIOS (o monolito + servicios auxiliares)       │
│                                                                     │
│   ¿No estás seguro?                                                 │
│       └──▶ MONOLITO (siempre puedes extraer servicios después)      │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   DECISIÓN 2: ¿Tradicional o Serverless?                           │
│   ─────────────────────────────────────────                         │
│                                                                     │
│   ¿Tráfico muy variable o impredecible?                            │
│       └──▶ SERVERLESS (escala a cero, escala al infinito)          │
│                                                                     │
│   ¿Necesitas WebSockets o conexiones persistentes?                 │
│       └──▶ TRADICIONAL (o serverless con servicios especializados) │
│                                                                     │
│   ¿Procesos de larga duración (> 30 segundos)?                     │
│       └──▶ TRADICIONAL                                              │
│                                                                     │
│   ¿Quieres mínima operación de infraestructura?                    │
│       └──▶ SERVERLESS                                               │
│                                                                     │
│   ¿Tráfico constante y predecible?                                 │
│       └──▶ TRADICIONAL (puede ser más económico)                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Caso especial: frameworks modernos como Next.js

Los meta-frameworks modernos como **Next.js**, **Nuxt**, **SvelteKit** y **Remix** son interesantes porque:

1. **Organizan como monolito**: Un repositorio, frontend y backend juntos, código compartido fácilmente
2. **Pueden ejecutarse de ambas formas**:
   - `next start` → servidor Node.js tradicional
   - Deploy en Vercel → serverless automático

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PROYECTO NEXT.JS                                │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  /app                                                        │  │
│   │    /page.tsx           (Server Component)                   │  │
│   │    /api/users/route.ts (API Route)                          │  │
│   │    /api/posts/route.ts (API Route)                          │  │
│   │  /components                                                 │  │
│   │  /lib                                                        │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│              ┌───────────────┴───────────────┐                     │
│              ▼                               ▼                      │
│   ┌─────────────────────┐       ┌─────────────────────┐            │
│   │  next start         │       │  Deploy a Vercel    │            │
│   │  (Node.js server)   │       │  (Serverless)       │            │
│   │                     │       │                     │            │
│   │  Un proceso 24/7    │       │  λ /                │            │
│   │  corriendo todo     │       │  λ /api/users       │            │
│   │                     │       │  λ /api/posts       │            │
│   │  TRADICIONAL        │       │  SERVERLESS         │            │
│   └─────────────────────┘       └─────────────────────┘            │
│                                                                     │
│   Mismo código, diferente modelo de ejecución                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

💡 **Insight**: Esta flexibilidad es poderosa. Puedes desarrollar localmente como servidor tradicional (sin cold starts, debugging fácil) y desplegar como serverless en producción (escala automática, cero mantenimiento).

---

## El viaje de una petición

Veamos qué sucede cuando un usuario hace clic en "Ver mi perfil" en una aplicación típica.

### Paso a paso

```
Usuario hace clic en "Mi Perfil"
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. NAVEGADOR (Cliente)                                      │
│    - JavaScript captura el evento click                     │
│    - Muestra un spinner de carga                            │
│    - Prepara la petición HTTP                               │
│    - Añade headers (auth token, content-type)               │
│    - Envía: GET https://api.miapp.com/users/me              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. DNS                                                       │
│    - Convierte "api.miapp.com" → "143.55.32.10"             │
│    - Resultado cacheado para futuras peticiones             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. CDN / EDGE (opcional)                                     │
│    - Si el contenido está cacheado, responde inmediatamente │
│    - Si no, pasa la petición al origen                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. LOAD BALANCER                                             │
│    - Recibe la petición                                      │
│    - Elige un servidor disponible (round-robin, least-conn) │
│    - Reenvía la petición                                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. SERVIDOR DE APLICACIÓN                                    │
│                                                              │
│    5a. Middleware de autenticación                           │
│        - Valida el token JWT                                 │
│        - Extrae user_id del token                            │
│        - Si inválido: responde 401 Unauthorized              │
│                                                              │
│    5b. Router                                                │
│        - Mapea GET /users/me → UserController.getProfile()   │
│                                                              │
│    5c. Controller                                            │
│        - Recibe la petición                                  │
│        - Llama al servicio correspondiente                   │
│                                                              │
│    5d. Service (lógica de negocio)                          │
│        - Aplica reglas de negocio                            │
│        - Decide qué datos necesita                           │
│                                                              │
│    5e. Repository (acceso a datos)                          │
│        - Construye la query SQL                              │
│        - Se comunica con la base de datos                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. BASE DE DATOS                                             │
│    - Recibe: SELECT * FROM users WHERE id = 42               │
│    - Busca en índices                                        │
│    - Retorna el registro del usuario                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. CAMINO DE VUELTA                                          │
│    - Repository recibe datos, los mapea a objeto User        │
│    - Service aplica transformaciones (oculta password hash)  │
│    - Controller serializa a JSON                             │
│    - Servidor envía respuesta HTTP 200                       │
│    - Response: { id: 42, name: "Ana", email: "ana@..." }     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. NAVEGADOR (de vuelta)                                     │
│    - Recibe la respuesta JSON                                │
│    - JavaScript parsea el JSON                               │
│    - Actualiza el estado de la aplicación                    │
│    - React/Vue/Svelte re-renderiza                           │
│    - Usuario ve su perfil                                    │
│    - Spinner desaparece                                       │
└─────────────────────────────────────────────────────────────┘

Tiempo total: 50-500ms (dependiendo de latencia, carga, etc.)
```

### ¿Dónde puede fallar?

Cada paso es un punto potencial de falla:

| Paso | Posibles fallas |
|------|-----------------|
| DNS | Timeout, dominio expirado |
| Red | Conexión lenta, pérdida de paquetes |
| Load Balancer | Ningún servidor disponible |
| Autenticación | Token expirado, inválido |
| Servidor | Error en código, out of memory |
| Base de datos | Query lenta, conexión agotada |
| Respuesta | Timeout del cliente |

💡 **Insight**: Entender este flujo completo te ayuda a debuggear problemas. Cuando algo falla, puedes preguntarte: "¿En qué paso está fallando?" y acotar el problema rápidamente.

---

## El stack moderno: piezas comunes

Una aplicación web moderna típicamente incluye:

### Frontend
| Categoría | Opciones populares (2025) |
|-----------|---------------------------|
| Framework | React, Vue, Svelte, Solid |
| Meta-framework | Next.js, Nuxt, SvelteKit, Astro |
| Estilos | Tailwind CSS, CSS Modules, Styled Components |
| Estado | Zustand, Jotai, Redux Toolkit, TanStack Query |

### Backend
| Categoría | Opciones populares (2025) |
|-----------|---------------------------|
| Runtime | Node.js, Deno, Bun, Python, Go |
| Framework | Express, Fastify, Hono, FastAPI, Gin |
| ORM | Prisma, Drizzle, SQLAlchemy, GORM |
| Validación | Zod, Yup, Pydantic |

### Datos
| Categoría | Opciones populares (2025) |
|-----------|---------------------------|
| SQL | PostgreSQL, MySQL, SQLite |
| NoSQL | MongoDB, DynamoDB, Firestore |
| Cache | Redis, Memcached |
| Búsqueda | Elasticsearch, Meilisearch, Algolia |

### Infraestructura
| Categoría | Opciones populares (2025) |
|-----------|---------------------------|
| Hosting | Vercel, Railway, Fly.io, AWS, GCP |
| CDN | Cloudflare, Fastly, AWS CloudFront |
| Contenedores | Docker, Kubernetes |
| CI/CD | GitHub Actions, GitLab CI, CircleCI |

⚠️ **Advertencia**: Esta lista cambia constantemente. No intentes aprenderlo todo. Elige un stack, domínalo, y expande gradualmente.

---

## Resumen

- Una aplicación web es un **sistema distribuido**: múltiples programas comunicándose por red
- La división **cliente-servidor** sigue siendo fundamental: cliente pide, servidor responde
- Las aplicaciones tienen **capas** (presentación, API, lógica de negocio, datos) para separar responsabilidades
- Hay tres arquitecturas principales: **monolito** (simple, ideal para empezar), **microservicios** (para grandes equipos), **serverless** (para tráfico variable)
- Una petición atraviesa múltiples componentes; entender este flujo es clave para debuggear
- El stack moderno tiene muchas opciones; elige uno y domínalo antes de explorar otros

---

## Ejercicios

1. **Diagrama mental**: Dibuja en papel el flujo completo de una petición en una aplicación que conozcas (puede ser una que uses diariamente). Identifica cada componente.

2. **Investigación**: Elige una empresa tech que admires. Investiga qué arquitectura usan (monolito, microservicios, híbrida). ¿Por qué crees que eligieron esa opción?

3. **Análisis de stack**: Mira los requisitos de trabajo de 5 ofertas de empleo para desarrollador web en tu región. ¿Qué tecnologías se repiten más?

---

## Referencias

- Fowler, M. (2014). *Microservices* — https://martinfowler.com/articles/microservices.html
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly.
- Newman, S. (2021). *Building Microservices*, 2nd Edition. O'Reilly.

---

**Anterior**: [La Evolución del Desarrollador Web](./01-evolucion-desarrollador.md) | **Siguiente**: [Pensamiento en Sistemas](./03-pensamiento-sistemas.md)
