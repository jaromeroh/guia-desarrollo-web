# 26. La Nueva Capa de Abstracción

> "I've never felt this much behind as a programmer. The profession is being dramatically refactored... There's a new programmable layer of abstraction to master involving agents, subagents, their prompts, contexts, memory, modes, permissions, tools, plugins, skills, hooks, MCP, LSP, slash commands, workflows, IDE integrations, and a need to build an all-encompassing mental model for fundamentally stochastic, fallible, unintelligible and changing entities suddenly intermingled with what used to be good old fashioned engineering."
>
> — Andrej Karpathy, Diciembre 2025

---

## Objetivos de Aprendizaje

Al terminar este capítulo podrás:

- Entender qué es la "nueva capa de abstracción" y por qué representa un cambio de paradigma
- Conocer los componentes del ecosistema agentico: agents, MCP, hooks, skills
- Desarrollar el modelo mental necesario para trabajar con entidades estocásticas
- Configurar tu entorno de desarrollo para trabajo agentico efectivo
- Reconocer patrones y antipatrones en el uso de agentes de IA

---

## El Terremoto de Magnitud 9

Karpathy no exagera cuando habla de un terremoto. Pero para entenderlo, necesitamos ver qué ha cambiado.

### Las capas que ya conocíamos

Como desarrolladores, siempre hemos trabajado con capas de abstracción:

```
┌─────────────────────────────────────────┐
│         Código de aplicación            │
├─────────────────────────────────────────┤
│         Frameworks / Librerías          │
├─────────────────────────────────────────┤
│         Lenguaje de programación        │
├─────────────────────────────────────────┤
│         Sistema operativo               │
├─────────────────────────────────────────┤
│         Hardware                        │
└─────────────────────────────────────────┘
```

Cada capa oculta complejidad. No necesitas saber cómo funcionan los transistores para escribir JavaScript. No necesitas entender el kernel para usar un framework web.

### La nueva capa

Ahora hay una capa adicional **encima** de tu código:

```
┌─────────────────────────────────────────┐
│    ★ NUEVA CAPA: Agentes y contexto     │  ← Esto es nuevo
├─────────────────────────────────────────┤
│         Código de aplicación            │
├─────────────────────────────────────────┤
│         Frameworks / Librerías          │
├─────────────────────────────────────────┤
│         Lenguaje de programación        │
├─────────────────────────────────────────┤
│         Sistema operativo               │
├─────────────────────────────────────────┤
│         Hardware                        │
└─────────────────────────────────────────┘
```

Esta nueva capa incluye:

| Componente | Qué hace |
|------------|----------|
| **Agentes** | Ejecutan tareas de forma autónoma |
| **Subagentes** | Agentes especializados para subtareas |
| **Contexto** | Lo que el agente "sabe" en cada momento |
| **Memoria** | Información persistente entre sesiones |
| **Modos** | Estados de operación (plan, auto, etc.) |
| **Permisos** | Qué puede y qué no puede hacer el agente |
| **Herramientas** | Capacidades que el agente puede usar |
| **MCP** | Protocolo para conectar agentes con sistemas |
| **Hooks** | Automatización de eventos |
| **Skills** | Conocimiento reutilizable |

### Por qué esto es diferente

Las capas anteriores eran **deterministas**. Si escribías `2 + 2`, obtenías `4`. Siempre. Sin excepciones.

La nueva capa es **estocástica**. Pides "escribe una función que sume dos números" y obtienes algo diferente cada vez. A veces mejor que lo que esperabas. A veces peor. A veces incorrecto.

> 📖 **Concepto**: **Estocástico** significa que hay aleatoriedad involucrada. Los LLMs no son máquinas deterministas; son sistemas probabilísticos que generan la respuesta más probable dada una entrada, pero esa probabilidad tiene varianza.

Esta diferencia fundamental requiere un cambio en cómo pensamos sobre desarrollo de software.

---

## Anatomía de la Nueva Capa

### Agents y Subagents

Un **agente** es un sistema de IA que puede:
- Recibir instrucciones en lenguaje natural
- Analizar contexto (archivos, código, estado)
- Decidir qué acciones tomar
- Ejecutar esas acciones
- Evaluar resultados e iterar

No es simplemente "autocompletado inteligente". Es un sistema que **actúa**.

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Instrucción: "Agrega tests para el módulo de auth"      │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────────┐      │
│  │                    AGENTE                      │      │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐   │      │
│  │  │ Analizar │→│ Planear  │→│  Ejecutar    │   │      │
│  │  │ contexto │ │ acciones │ │  acciones    │   │      │
│  │  └──────────┘ └──────────┘ └──────────────┘   │      │
│  │                      │                         │      │
│  │                      ▼                         │      │
│  │               ┌──────────┐                     │      │
│  │               │ Evaluar  │←─────────┐          │      │
│  │               │ y repetir│          │          │      │
│  │               └──────────┘          │          │      │
│  └─────────────────────────────────────┘          │      │
│                          │                               │
│                          ▼                               │
│  Resultado: Tests creados, ejecutados, pasando           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

Los **subagentes** son agentes especializados que el agente principal puede invocar:

| Tipo | Especialización | Cuándo se usa |
|------|-----------------|---------------|
| **Explore** | Búsqueda rápida en código | Encontrar archivos, patrones |
| **Plan** | Análisis y diseño | Antes de cambios complejos |
| **General** | Tareas multi-paso | Implementación autónoma |

La clave es que los subagentes tienen **contexto aislado**. Un subagente que busca archivos no contamina el contexto del agente principal con información irrelevante.

### Contexto y Memoria

El **contexto** es todo lo que el agente "sabe" en un momento dado:

- Tu prompt actual
- Los archivos que ha leído
- El historial de la conversación
- Las instrucciones del proyecto (CLAUDE.md)
- El resultado de herramientas ejecutadas

Hay un límite físico: la **ventana de contexto**. Cuando se llena, el agente "olvida" información anterior.

```
┌─────────────────────────────────────────────────┐
│              VENTANA DE CONTEXTO                │
│  ┌───────────────────────────────────────────┐  │
│  │ Instrucciones del sistema                 │  │
│  ├───────────────────────────────────────────┤  │
│  │ CLAUDE.md del proyecto                    │  │
│  ├───────────────────────────────────────────┤  │
│  │ Historial de conversación                 │  │
│  ├───────────────────────────────────────────┤  │
│  │ Archivos leídos                           │  │
│  ├───────────────────────────────────────────┤  │
│  │ Resultados de herramientas                │  │
│  ├───────────────────────────────────────────┤  │
│  │ Tu prompt actual                          │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ████████████████████░░░░░░░ 75% usado         │
└─────────────────────────────────────────────────┘
```

La **memoria** es información que persiste entre sesiones:
- Archivos CLAUDE.md que se cargan automáticamente
- Configuraciones guardadas
- Historial de conversaciones anteriores

> 📖 **Concepto**: El agente no tiene memoria perfecta. Cada sesión empieza casi desde cero. La "memoria" viene de archivos externos que se cargan en el contexto.

### Modos y Permisos

Los **modos** definen cómo opera el agente:

| Modo | Permisos | Uso |
|------|----------|-----|
| **Plan** | Solo lectura | Analizar antes de actuar |
| **Normal** | Pide permiso | Operación estándar |
| **Auto** | Ejecuta sin pedir | Tareas confiables |

Los **permisos** controlan qué herramientas puede usar:

```
Permitido: Leer archivos, ejecutar tests
Preguntar: Escribir archivos, hacer commits
Denegado: Eliminar archivos, push a main
```

Esta configuración es tu **superficie de control**. Defines los límites dentro de los cuales el agente puede operar.

---

## MCP: El Protocolo que Conecta Todo

### El problema N×M

Imagina que tienes N herramientas de IA y M sistemas que quieres conectar:

```
Sin MCP:
Claude ──┬── GitHub
         ├── Slack
         ├── Postgres
         └── Sentry

Cursor ──┬── GitHub
         ├── Slack
         ├── Postgres
         └── Sentry

Copilot ─┬── GitHub
         ├── Slack
         ├── Postgres
         └── Sentry

= N × M integraciones (12 en este caso)
```

Cada combinación requiere código específico. Esto no escala.

### La solución N+M

MCP (Model Context Protocol) estandariza la comunicación:

```
Con MCP:
                    ┌── GitHub (MCP server)
Claude  ─┐          ├── Slack (MCP server)
Cursor  ─┼── MCP ───├── Postgres (MCP server)
Copilot ─┘          └── Sentry (MCP server)

= N + M integraciones (7 en este caso)
```

Cada herramienta implementa el protocolo MCP una vez. Cada sistema expone un servidor MCP una vez. Todos se conectan automáticamente.

### Los 3 primitivos de MCP

MCP define tres tipos de capacidades:

| Primitivo | Controlado por | Descripción |
|-----------|----------------|-------------|
| **Tools** | El modelo | Acciones que el agente puede ejecutar |
| **Resources** | La aplicación | Datos que la aplicación expone |
| **Prompts** | El usuario | Plantillas predefinidas de instrucciones |

**Tools** son cosas como "crear issue en GitHub", "ejecutar query SQL", "enviar mensaje a Slack".

**Resources** son datos como "lista de issues abiertos", "schema de la base de datos", "mensajes recientes del canal".

**Prompts** son plantillas como "revisa este PR siguiendo estos criterios...".

### Arquitectura

```
┌────────────────┐         ┌────────────────┐
│   MCP Client   │◄───────►│   MCP Server   │
│  (Claude Code) │ JSON-RPC│   (GitHub)     │
└────────────────┘         └────────────────┘
        │
        │ El cliente carga las definiciones
        │ de herramientas en el contexto
        ▼
┌────────────────────────────────────────────┐
│            Contexto del modelo             │
│  ┌──────────────────────────────────────┐  │
│  │ Tool: github.create_issue            │  │
│  │ Tool: github.list_prs                │  │
│  │ Tool: github.merge_pr                │  │
│  │ ...                                  │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

El modelo ve las herramientas disponibles y decide cuándo usarlas basándose en tu instrucción.

### Servidores populares

| Servidor | Funcionalidad |
|----------|---------------|
| **GitHub** | Issues, PRs, repos, acciones |
| **Postgres** | Queries SQL, schema |
| **Slack** | Mensajes, canales |
| **Sentry** | Errores, alertas |
| **Notion** | Páginas, bases de datos |
| **Puppeteer** | Automatización de navegador |

En 2025, el registro de MCP tiene más de 75 conectores oficiales y miles comunitarios.

### Consideraciones de seguridad

MCP introduce nuevos vectores de ataque:

| Riesgo | Descripción | Mitigación |
|--------|-------------|------------|
| **Prompt injection** | Contenido malicioso en datos | Validar inputs, aislar contextos |
| **Tool poisoning** | Servidor MCP malicioso | Usar solo servidores confiables |
| **Privilege escalation** | Combinar herramientas para obtener acceso | Principio de mínimo privilegio |
| **Data exfiltration** | Enviar datos sensibles a servidores | Auditar qué datos fluyen |

> ⚠️ **Importante**: Cada herramienta que conectas es una superficie de ataque potencial. Conecta solo lo necesario y audita regularmente.

---

## Configurando tu Entorno Agentico

### El archivo CLAUDE.md

CLAUDE.md es el "manual" de tu proyecto para la IA. Se carga automáticamente al inicio de cada sesión.

**Qué incluir:**

```markdown
# Proyecto: E-commerce API

## Stack
- Node.js 20 + TypeScript
- PostgreSQL con Prisma
- Jest para tests

## Estructura
/src
  /modules     # Módulos por feature
  /shared      # Código compartido
  /config      # Configuración
/tests
  /unit        # Tests unitarios
  /integration # Tests de integración

## Convenciones
- Usar kebab-case para archivos
- Cada módulo tiene su propio barrel export
- Tests junto al código que prueban (.test.ts)

## Comandos frecuentes
- npm run dev: Desarrollo
- npm run test: Ejecutar tests
- npm run build: Build de producción

## Decisiones técnicas
- Usamos Zod para validación (no class-validator)
- Prisma sobre TypeORM por simplicidad
- No usamos decoradores de NestJS
```

**Dónde ponerlo:**

| Ubicación | Alcance |
|-----------|---------|
| `~/.claude/CLAUDE.md` | Todos tus proyectos (preferencias globales) |
| `./CLAUDE.md` | Este proyecto específico |
| `./src/auth/CLAUDE.md` | Solo el módulo de auth |

Los archivos se combinan. Puedes tener instrucciones globales y específicas por módulo.

### Hooks: Control determinístico

Los hooks te permiten ejecutar comandos automáticamente en eventos específicos:

**Ejemplo: Formatear código después de cada edición**

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "prettier --write $FILE_PATH"
      }]
    }]
  }
}
```

**Ejemplo: Bloquear cambios a archivos sensibles**

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "if echo $FILE_PATH | grep -q '.env'; then exit 1; fi"
      }]
    }]
  }
}
```

**Eventos disponibles:**

| Evento | Cuándo | Uso común |
|--------|--------|-----------|
| PreToolUse | Antes de ejecutar herramienta | Validar, bloquear |
| PostToolUse | Después de ejecutar herramienta | Formatear, loggear |
| Stop | Cuando termina respuesta | Cleanup, notificar |

### Skills: Conocimiento reutilizable

Una skill es una carpeta con instrucciones que Claude carga automáticamente cuando son relevantes:

```
.claude/skills/
└── pr-review/
    ├── SKILL.md          # Instrucciones
    └── checklist.md      # Referencia
```

**SKILL.md:**

```markdown
---
name: pr-review
description: "Revisa PRs siguiendo estándares del equipo"
---

# Code Review Guidelines

Al revisar código, enfócate en:

1. **Seguridad**: SQL injection, XSS, secrets expuestos
2. **Performance**: N+1 queries, loops innecesarios
3. **Mantenibilidad**: Nombres claros, funciones pequeñas
4. **Tests**: Cobertura de edge cases

Formato de comentarios:
- 🔴 Blocker: Debe arreglarse antes de merge
- 🟡 Sugerencia: Mejora recomendada
- 💭 Pregunta: Necesito entender mejor
```

Cuando pides "revisa este PR", Claude detecta que la skill es relevante y la carga.

### Slash Commands

Comandos personalizados que activas manualmente:

```markdown
# .claude/commands/fix-issue.md
---
description: "Arregla un issue de GitHub"
---

Busca el issue #$1 en GitHub.
Lee el código relacionado.
Implementa la solución.
Crea los tests necesarios.
Abre un PR con la solución.
```

Uso: `/fix-issue 123`

---

## El Modelo Mental

Esta es la sección más importante del capítulo. Sin el modelo mental correcto, usarás las herramientas de forma subóptima.

### Entidades estocásticas

Los LLMs no son funciones puras. Son sistemas probabilísticos.

```
Función tradicional:
suma(2, 3) → 5  (siempre)

LLM:
"suma 2 y 3" → "5"           (probablemente)
             → "2 + 3 = 5"   (a veces)
             → "El resultado es 5" (ocasionalmente)
             → "¿En qué base?" (raramente)
```

Esto significa que:

1. **La misma entrada puede dar diferentes salidas**
2. **No puedes predecir exactamente qué hará**
3. **Necesitas verificar los resultados**

### Falibles pero poderosos

Los agentes cometen errores. También hacen cosas que tomarían horas en minutos.

| Tarea | Humano | Agente |
|-------|--------|--------|
| Escribir función simple | 5 min | 10 seg |
| Refactorizar 50 archivos | 2 horas | 5 min |
| Detectar bug sutil | 30 min | Variable* |
| Decisión arquitectónica | 1 hora | Necesita guía |

*Variable porque puede encontrarlo inmediatamente o no encontrarlo nunca.

La clave es **calibrar tu confianza**:

```
Alta confianza:
- Código boilerplate
- Refactoring mecánico
- Documentación
- Tests de casos comunes

Confianza media:
- Lógica de negocio estándar
- Integración con APIs conocidas
- Debugging de errores comunes

Baja confianza:
- Decisiones arquitectónicas
- Lógica de negocio compleja
- Código de seguridad crítico
- Optimización de performance
```

### No puedes debuggear el pensamiento

Cuando una función tradicional falla, puedes poner breakpoints, inspeccionar variables, seguir el flujo.

Cuando un LLM "falla", no puedes ver qué "pensó". Solo ves el input y el output.

Esto cambia cómo investigas problemas:

| Debugging tradicional | Debugging de agentes |
|----------------------|---------------------|
| Inspeccionar estado interno | Reformular el prompt |
| Añadir logs | Dar más contexto |
| Seguir el stack trace | Pedir que explique su razonamiento |
| Reproducir exactamente | Intentar variaciones |

### El desarrollador como supervisor

El cambio más importante es en tu rol:

```
Antes:
  Tú escribías código
  Tú decidías cada línea
  Tú ejecutabas y debuggeabas

Ahora:
  El agente escribe código
  Tú guías y validas
  El agente ejecuta, tú supervisas
```

Esto no significa menos trabajo. Significa **trabajo diferente**:

- Más tiempo pensando qué pedir
- Más tiempo revisando output
- Menos tiempo escribiendo caracteres
- Más tiempo entendiendo sistemas

### La nueva habilidad: saber qué delegar

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│    Delegar al agente          │    Hacer tú mismo          │
│    ─────────────────          │    ──────────────          │
│                               │                            │
│    ✓ Código boilerplate       │    ✗ Decisiones de diseño  │
│    ✓ Refactoring mecánico     │    ✗ Arquitectura crítica  │
│    ✓ Tests estándar           │    ✗ Código de seguridad   │
│    ✓ Documentación            │    ✗ Revisión final        │
│    ✓ Búsqueda en codebase     │    ✗ Validación de lógica  │
│    ✓ Prototipado rápido       │    ✗ Deployment a prod     │
│                               │                            │
└────────────────────────────────────────────────────────────┘
```

Con el tiempo, estos límites se mueven. Lo que hoy requiere supervisión cercana, mañana puede ser delegable. Pero el principio permanece: **tú eres responsable del resultado**.

---

## Patrones y Antipatrones

### Patrones efectivos

**1. Dar contexto suficiente**

```
❌ "Arregla el bug"
✓ "Hay un bug en el checkout: cuando el usuario tiene
   cupón de descuento, el total se calcula mal. El error
   está probablemente en calculateTotal() en cart.ts.
   Los tests en cart.test.ts deberían cubrir este caso."
```

**2. Iterar en conversación**

```
Prompt 1: "Crea un componente de login"
→ Revisa lo que genera
Prompt 2: "Agrega validación de email y password mínimo 8 chars"
→ Revisa
Prompt 3: "Ahora agrega manejo de errores del API"
→ Final
```

Cada iteración refina. No intentes especificar todo en un solo prompt.

**3. Pedir explicaciones**

```
"Explica qué hace este código antes de modificarlo"
"¿Por qué elegiste este approach sobre X?"
"¿Qué edge cases podrían fallar?"
```

El agente explicando te ayuda a validar su entendimiento.

**4. Verificar outputs críticos**

Antes de hacer commit:
- Lee el diff completo
- Ejecuta los tests
- Prueba manualmente casos edge
- Revisa por vulnerabilidades de seguridad

### Antipatrones a evitar

**1. Confiar ciegamente**

```
❌ "Refactoriza todo el módulo de auth" → commit sin revisar

Esto es peligroso. El agente puede:
- Cambiar lógica sin querer
- Introducir vulnerabilidades
- Romper edge cases
```

**2. Ignorar los límites del contexto**

```
❌ "Lee los 500 archivos del proyecto y entiende todo"

El contexto tiene límites. Si intentas cargar demasiado,
el agente "olvida" información anterior.
```

**3. No leer lo que produce**

```
❌ "Genera tests" → aceptar sin leer

Los tests generados pueden:
- No cubrir casos importantes
- Ser frágiles
- Probar la implementación, no el comportamiento
```

**4. Prompts vagos para tareas complejas**

```
❌ "Mejora el performance"
✓ "El endpoint /api/products tarda 2s. Probablemente
   hay un N+1 query. Optimiza la consulta de productos
   con sus categorías."
```

---

## El Futuro Cercano

### Multi-agente

En 2025, herramientas como Claude Squad permiten ejecutar múltiples agentes en paralelo:

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTADOR                          │
│                         │                               │
│         ┌───────────────┼───────────────┐               │
│         ▼               ▼               ▼               │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│    │ Agente 1│    │ Agente 2│    │ Agente 3│           │
│    │ Backend │    │ Frontend│    │ Tests   │           │
│    └─────────┘    └─────────┘    └─────────┘           │
│         │               │               │               │
│         └───────────────┴───────────────┘               │
│                         │                               │
│                    INTEGRACIÓN                          │
└─────────────────────────────────────────────────────────┘
```

Cada agente trabaja en su área. El orquestador resuelve conflictos y integra resultados.

### Agentes especializados

En lugar de un agente generalista, tendrás agentes para tareas específicas:

| Agente | Especialización |
|--------|-----------------|
| **Code reviewer** | Revisa PRs según tus estándares |
| **Test writer** | Genera tests de edge cases |
| **Migrator** | Actualiza dependencias |
| **Documenter** | Mantiene docs sincronizadas |

### La evolución del rol

El desarrollador de 2030 probablemente:

- Pase más tiempo diseñando sistemas que escribiendo código
- Gestione equipos de agentes como hoy gestiona pipelines de CI
- Se especialice en áreas que los agentes no dominan bien
- Sea valorado por juicio y creatividad, no velocidad de tipeo

Pero esto es especulación. Lo único seguro es que el cambio continúa.

---

## Resumen

### La nueva capa en 5 puntos

1. **Hay una nueva capa de abstracción** que incluye agentes, contexto, MCP, hooks, y más

2. **Los agentes son estocásticos y falibles**. No son deterministas como el código tradicional

3. **MCP es el protocolo** que conecta agentes con herramientas externas

4. **Tu rol cambia** de escribir código a supervisar y guiar agentes

5. **El modelo mental importa más** que memorizar comandos específicos

### El principio guía

> La IA amplifica tu capacidad, pero **tú sigues siendo responsable** del resultado. Delega la ejecución, nunca el juicio.

---

## Ejercicios

1. **Escribe un CLAUDE.md** para un proyecto en el que trabajes. Incluye stack, convenciones, y comandos frecuentes. Úsalo por una semana y refínalo basándote en qué preguntas te hace el agente repetidamente.

2. **Identifica tareas delegables**: Haz una lista de 10 tareas que hiciste la semana pasada. Clasifícalas en "delegable al agente", "necesita supervisión", "mejor hacerlo yo". Justifica cada clasificación.

3. **Analiza un MCP server**: Encuentra un servidor MCP open source (GitHub tiene varios en `modelcontextprotocol/servers`). Lee su código y responde: ¿Qué herramientas expone? ¿Qué recursos? ¿Qué permisos necesita?

4. **Ejercicio de calibración**: Pide al agente que resuelva 5 problemas de diferente complejidad. Antes de ver el resultado, predice tu nivel de confianza (alto/medio/bajo). Después, evalúa si tu predicción fue correcta. Esto entrena tu intuición.

---

## Referencias

- Anthropic. (2024). *Introducing the Model Context Protocol*. https://anthropic.com/news/model-context-protocol
- Model Context Protocol. (2025). *MCP Specification*. https://modelcontextprotocol.io/specification
- Karpathy, A. (2025). *On the changing nature of programming*. X/Twitter thread.
- Anthropic. (2025). *Claude Code Documentation*. https://code.claude.com/docs
- Agentic AI Foundation. (2025). *Establishing the AAIF*. Linux Foundation.

---

**Anterior**: [Stack: Go + APIs de Alto Rendimiento](./25-stack-go.md) | **Siguiente**: [Tendencias y Horizontes](./27-tendencias.md)
