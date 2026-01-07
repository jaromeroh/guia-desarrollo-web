# 4. Desarrollo Asistido por IA

> "La IA no reemplaza al programador. Reemplaza al programador que no sabe usar IA."

## Objetivos de Aprendizaje

Al finalizar este capítulo, serás capaz de:
- Entender qué puede y qué NO puede hacer la IA en desarrollo de software
- Aplicar el ciclo efectivo: prompt → revisar → iterar → validar
- Escribir prompts que producen código útil y correcto
- Identificar cuándo confiar en la IA y cuándo verificar manualmente
- Evitar los antipatterns más comunes del desarrollo asistido por IA

---

## El Cambio de Paradigma

Desde 2022, algo fundamental cambió en el desarrollo de software. Herramientas como Claude Code, Codex, GitHub Copilot y Cursor transformaron cómo escribimos código.

```
┌─────────────────────────────────────────────────────────────┐
│              ANTES vs AHORA                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ANTES (2020)                    AHORA (2024+)              │
│  ────────────                    ─────────────              │
│  Buscar en Stack Overflow        Preguntar a la IA          │
│  Copiar snippet, adaptarlo       Describir lo que necesitas │
│  Leer documentación completa     Pedir resumen contextual   │
│  Escribir boilerplate manual     Generarlo en segundos      │
│  Debuggear solo                  "¿Por qué falla esto?"     │
│  Horas buscando soluciones       Minutos iterando prompts   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### El "middle" que desaparece

Karri Saarinen, CEO de Linear, describe este cambio con una metáfora poderosa: **el centro del trabajo de software se está comprimiendo**.

```
┌─────────────────────────────────────────────────────────────┐
│           EL TRABAJO DE SOFTWARE: ANTES vs AHORA            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ANTES (el "middle" era grueso):                            │
│  ───────────────────────────────                            │
│                                                             │
│  ┌─────────┐   ┌─────────────────────────┐   ┌─────────┐   │
│  │ ANTES   │   │        MIDDLE           │   │ DESPUÉS │   │
│  │         │   │                         │   │         │   │
│  │ Idea    │   │  Abrir IDE              │   │ Revisar │   │
│  │ Diseño  │   │  Configurar entorno     │   │ Testear │   │
│  │ Plan    │   │  Escribir código        │   │ Lanzar  │   │
│  │         │   │  Debuggear              │   │         │   │
│  │  10%    │   │  Buscar en StackOverflow│   │  10%    │   │
│  │         │   │         80%             │   │         │   │
│  └─────────┘   └─────────────────────────┘   └─────────┘   │
│                                                             │
│  AHORA (el "middle" se comprime):                           │
│  ──────────────────────────────                             │
│                                                             │
│  ┌───────────────┐   ┌───────────┐   ┌───────────────┐     │
│  │    ANTES      │   │  MIDDLE   │   │    DESPUÉS    │     │
│  │               │   │           │   │               │     │
│  │ Entender      │   │ Promptear │   │ Revisar       │     │
│  │ Diseñar       │   │ Iterar    │   │ Verificar     │     │
│  │ Dar contexto  │   │           │   │ Testear       │     │
│  │ Decidir       │   │   30%     │   │ Validar       │     │
│  │     35%       │   │           │   │     35%       │     │
│  └───────────────┘   └───────────┘   └───────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

El tiempo que antes pasabas escribiendo código ahora se redistribuye hacia los extremos:

- **El antes** absorbe más esfuerzo: entender el problema, diseñar la solución, dar contexto a la IA, tomar decisiones arquitectónicas
- **El después** también crece: revisar output, validar corrección, testear edge cases, asegurar calidad

> 💡 **Insight**: "Writing code is less like constructing a solution and more like setting up the conditions for a good solution to emerge." — Karri Saarinen. Ya no "construyes" código; **creas las condiciones** para que emerja una buena solución.

Esta redistribución tiene consecuencias importantes que veremos a lo largo del libro.

---

Pero este cambio viene con una trampa: **la IA hace que sea muy fácil generar código que no entiendes**.

Y código que no entiendes es código que no puedes:
- Debuggear cuando falla
- Modificar cuando cambian los requisitos
- Optimizar cuando hay problemas de rendimiento
- Mantener cuando crece el proyecto

Por eso este capítulo existe tan temprano en el libro. La IA es una herramienta poderosa, pero necesitas bases sólidas para usarla bien.

---

## Qué Puede y Qué No Puede Hacer la IA

### Lo que la IA hace bien

```
┌─────────────────────────────────────────────────────────────┐
│           FORTALEZAS DE LA IA PARA CÓDIGO                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ Generar boilerplate y código repetitivo                 │
│     "Crea un componente React con TypeScript para un        │
│      formulario de login con validación"                    │
│                                                             │
│  ✅ Explicar código existente                               │
│     "¿Qué hace esta función? ¿Por qué usa recursión?"       │
│                                                             │
│  ✅ Traducir entre lenguajes/frameworks                     │
│     "Convierte este código Python a JavaScript"             │
│                                                             │
│  ✅ Sugerir soluciones a errores comunes                    │
│     "Tengo este error: TypeError... ¿cómo lo soluciono?"    │
│                                                             │
│  ✅ Generar tests basados en código existente               │
│     "Escribe tests unitarios para esta función"             │
│                                                             │
│  ✅ Documentar código                                       │
│     "Agrega JSDoc a estas funciones"                        │
│                                                             │
│  ✅ Refactorizar siguiendo patrones conocidos               │
│     "Refactoriza esto usando el patrón Repository"          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Lo que la IA hace mal (o no puede hacer)

```
┌─────────────────────────────────────────────────────────────┐
│           LIMITACIONES DE LA IA                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ❌ Entender TU contexto de negocio                         │
│     No sabe que tu empresa tiene reglas específicas         │
│                                                             │
│  ❌ Conocer tu codebase completo                            │
│     Solo ve lo que le muestras en el prompt                 │
│                                                             │
│  ❌ Garantizar que el código funciona                        │
│     Genera código plausible, no necesariamente correcto     │
│                                                             │
│  ❌ Tomar decisiones arquitectónicas complejas              │
│     Puede sugerir, pero tú decides considerando tradeoffs   │
│                                                             │
│  ❌ Saber qué hay en tu base de datos                       │
│     No conoce tus datos reales ni su estado                 │
│                                                             │
│  ❌ Mantenerse actualizada con cambios recientes            │
│     APIs nuevas, breaking changes, versiones recientes      │
│                                                             │
│  ❌ Detectar problemas de seguridad sutiles                  │
│     Puede introducir vulnerabilidades sin saberlo           │
│                                                              │
│  ❌ Optimizar para TU escala específica                      │
│     No sabe si tienes 100 o 10 millones de usuarios         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

💡 **Insight**: La IA es excelente para el "cómo" (implementación) pero limitada para el "qué" y el "por qué" (diseño y decisiones). Tú aportas el contexto, los requisitos y el juicio; la IA acelera la ejecución.

### 📊 El Precipicio de la Complejidad

Estudios recientes muestran un patrón claro en las capacidades de la IA para código:

| Tipo de tarea | Tasa de éxito |
|---------------|---------------|
| Tareas aisladas (un componente, una función) | ~40% |
| Integraciones multi-paso | ~25% |

La IA "funciona bien y luego cae por un precipicio cuando la complejidad aumenta". Este fenómeno se conoce como el **complexity cliff**.

**Implicación práctica**: Descomponer tareas complejas en pasos simples aumenta dramáticamente la tasa de éxito. En lugar de pedir "implementa el sistema de autenticación completo", pide primero el modelo de usuario, luego el hash de passwords, luego el endpoint de login, etc.

### El Divide de Capacidades

Una forma más precisa de entender qué delegar:

| IA Fuerte | IA Débil |
|-----------|----------|
| Lógica y flujo de datos | Decisiones de diseño visual |
| Scaffolding y boilerplate | Juicio estético ("gusto") |
| Convertir specs explícitas en código | Jerarquía visual y decisiones UX |
| Patrones conocidos y documentados | Integraciones multi-paso sin contexto fuerte |
| Refactoring mecánico | Arquitectura de sistemas complejos |

> 💡 **Insight**: "You are still the architect." El éxito depende menos del modelo que uses y más de la especificidad del prompt, los guardrails que establezcas, y cómo estructures el workflow. — Addy Osmani

---

## El Ciclo de Desarrollo con IA

No se trata de pedir código y pegarlo. El desarrollo efectivo con IA sigue un ciclo:

```
┌─────────────────────────────────────────────────────────────┐
│              EL CICLO PROMPT-REVISAR-ITERAR                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────┐◀──────────────────────────────────────┐     │
│  │ 1. PROMPT  │  Describir qué necesitas con contexto │     │
│  └─────┬──────┘                                       │     │
│        │                                              │     │
│        ▼                                              │     │
│  ┌────────────┐     No entiendo                       │     │
│  │ 2. REVISAR │ ──────────────────┐                   │     │
│  │  Entender  │                   │                   │     │
│  └─────┬──────┘                   ▼                   │     │
│        │                   ┌─────────────┐            │     │
│        │                   │  "Explica   │            │     │
│        │ Entiendo          │  esta parte"│            │     │
│        │                   └──────┬──────┘            │     │
│        │                          │                   │     │
│        │◀─────────────────────────┘                   │     │
│        │                                              │     │
│        ▼                                              │     │
│  ┌────────────┐     Necesita ajustes                  │     │
│  │ 3. ITERAR  │ ──────────────────┐                   │     │
│  │  Ajustar   │                   │                   │     │
│  └─────┬──────┘                   ▼                   │     │
│        │                   ┌─────────────┐            │     │
│        │                   │  "Cambia X, │            │     │
│        │ Funciona          │  agrega Y"  │            │     │
│        │                   └──────┬──────┘            │     │
│        │                          │                   │     │
│        │◀─────────────────────────┘                   │     │
│        │                                              │     │
│        ▼                                              │     │
│  ┌────────────┐     No pasa tests ────────────────────┘     │
│  │ 4. VALIDAR │     (volver a PROMPT con el error)          │
│  │   Probar   │                                             │
│  └─────┬──────┘                                             │
│        │                                                    │
│        │ Pasa tests                                         │
│        ▼                                                    │
│  ┌────────────┐                                             │
│  │  ✅ LISTO  │                                             │
│  └────────────┘                                             │
│                                                             │
│  💡 Lo normal es dar varias vueltas. Una iteración          │
│     perfecta es la excepción, no la regla.                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Paso 1: Prompt (Describir)

Escribe un prompt claro con contexto suficiente.

### Paso 2: Revisar (Entender)

**Nunca copies código que no entiendes.** Lee línea por línea. Si algo no está claro, pide explicación.

### Paso 3: Iterar (Ajustar)

El primer resultado rara vez es perfecto. Refina con feedback específico.

### Paso 4: Validar (Probar)

Prueba el código. Escribe tests. Verifica edge cases. La IA no ejecuta tu código — tú sí.

---

## Prompting Efectivo para Código

La calidad del output depende directamente de la calidad del input.

### Context Engineering: La Nueva Habilidad Crítica

No basta con escribir buenos prompts. Necesitas **ingeniar el contexto** — estructurar la información que le das a la IA para maximizar la calidad del output.

```
┌─────────────────────────────────────────────────────────────┐
│           CONTEXT ENGINEERING                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MÁXIMO SIGNAL-TO-NOISE                                  │
│     Solo información relevante, nada superfluo              │
│     ❌ "Aquí está todo el archivo de 2000 líneas"           │
│     ✅ "Aquí está la función relevante y su contexto"       │
│                                                             │
│  2. CODIFICAR CONVENCIONES ANTES                            │
│     Bloquear decisiones antes de pedir código               │
│     ❌ "Haz un componente de login"                         │
│     ✅ "Usamos React + TypeScript + Tailwind + shadcn/ui.   │
│        Los formularios usan React Hook Form con Zod.        │
│        Haz un componente de login."                         │
│                                                             │
│  3. FORZAR TRABAJO INCREMENTAL                              │
│     Pedir planes y pasos, no soluciones monolíticas         │
│     ❌ "Implementa el sistema de pagos"                     │
│     ✅ "Primero, explícame cómo estructurarías el sistema   │
│        de pagos. Luego implementaremos paso a paso."        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> 💡 **Insight**: La calidad del output depende más de cómo estructuras el contexto que del modelo que uses. Un prompt bien estructurado en un modelo menor puede superar a un prompt vago en un modelo superior.

### Anatomía de un buen prompt

```
┌─────────────────────────────────────────────────────────────┐
│              ESTRUCTURA DE UN PROMPT EFECTIVO               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CONTEXTO                                                │
│     ¿Qué estás construyendo? ¿Qué tecnologías usas?         │
│     "Estoy construyendo una API REST con Node.js y Express" │
│                                                             │
│  2. TAREA ESPECÍFICA                                        │
│     ¿Qué necesitas exactamente?                             │
│     "Necesito un middleware de autenticación con JWT"       │
│                                                             │
│  3. RESTRICCIONES                                           │
│     ¿Qué limitaciones o requisitos hay?                     │
│     "Debe verificar tokens en el header Authorization"      │
│     "Debe manejar tokens expirados con error 401"           │
│                                                             │
│  4. FORMATO ESPERADO (opcional)                             │
│     ¿Cómo quieres la respuesta?                             │
│     "Incluye manejo de errores y comentarios explicativos"  │
│                                                             │
│  5. EJEMPLOS (opcional pero poderoso)                       │
│     Input/output esperado                                   │
│     "Ejemplo de request válido: { header: 'Bearer xxx' }"   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Ejemplo: Prompt malo vs bueno

**❌ Prompt vago:**
```
Haz un login
```

**✅ Prompt específico:**
```
Contexto: Aplicación React con TypeScript, usando React Hook Form
para formularios y Zod para validación.

Tarea: Crear un componente LoginForm que:
1. Tenga campos de email y password
2. Valide email con formato correcto
3. Valide password mínimo 8 caracteres
4. Muestre errores debajo de cada campo
5. Deshabilite el botón mientras se envía
6. Llame a onSubmit(data) cuando el form sea válido

Restricciones:
- Usar solo Tailwind CSS para estilos
- No usar bibliotecas adicionales
- Manejar estado de loading

Incluye tipos TypeScript para las props del componente.
```

### Técnicas avanzadas de prompting

#### 1. Dar ejemplos de código existente

```
Este es mi patrón actual para servicios:

```typescript
// userService.ts
export const userService = {
  async getById(id: string): Promise<User> {
    const response = await api.get(`/users/${id}`);
    return response.data;
  }
};
```

Crea un productService siguiendo el mismo patrón con métodos:
getAll, getById, create, update, delete
```

La IA aprenderá tu estilo del ejemplo.

#### 2. Pedir razonamiento

```
Necesito decidir entre usar Redis o PostgreSQL para
almacenar sesiones de usuario.

Contexto:
- 10,000 usuarios activos diarios
- Sesiones expiran en 24 horas
- Ya tenemos PostgreSQL en producción
- No tenemos Redis configurado

Explica los tradeoffs de cada opción para MI caso específico
y dame tu recomendación con justificación.
```

#### 3. Iterar con feedback específico

```
[Después de recibir código]

El código funciona pero:
1. El manejo de errores es muy genérico, necesito errores
   específicos para "usuario no encontrado" vs "credenciales
   inválidas"
2. Falta validación de que el email no esté vacío antes
   del trim()
3. Prefiero async/await en lugar de .then()

Ajusta el código con estos cambios.
```

#### 4. Pedir alternativas

```
Dame 3 formas diferentes de implementar un sistema de
caché en esta aplicación Express, con pros y cons de cada una.
```

---

## Cuándo Confiar y Cuándo Verificar

No todo el código generado por IA requiere el mismo nivel de escrutinio.

### Matriz de riesgo

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    NIVEL DE VERIFICACIÓN                    │
│                                                             │
│       Bajo riesgo                      Alto riesgo          │
│       (confiar más)                    (verificar más)      │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                                                     │   │
│   │  • Boilerplate estándar    • Lógica de negocio      │   │
│   │  • CRUD básico               compleja               │   │
│   │  • Componentes UI          • Autenticación/         │   │
│   │    simples                   Autorización           │   │
│   │  • Formateo de datos       • Manejo de pagos        │   │
│   │  • Utilidades comunes      • Queries SQL complejas  │   │
│   │  • Regex simples           • Criptografía           │   │
│   │  • Tests unitarios         • Concurrencia           │   │
│   │    básicos                 • Validación de          │   │
│   │                              seguridad              │   │
│   │                                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   "Lo he visto mil veces"      "Esto puede salir muy mal"   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Señales de alerta: cuándo desconfiar

🚩 **Desconfía cuando:**

1. **El código es demasiado complejo para lo que pediste**
   - Si pediste algo simple y recibiste 200 líneas, algo está mal

2. **Usa APIs o métodos que no reconoces**
   - Verifica que existan y estén actualizados

3. **Maneja datos sensibles (passwords, tokens, PII)**
   - Siempre revisa el manejo de seguridad manualmente

4. **Hace operaciones destructivas (DELETE, DROP, rm -rf)**
   - Lee cada línea antes de ejecutar

5. **La IA dice "no estoy seguro" o "podría ser"**
   - Esa incertidumbre es información importante

6. **Involucra dependencias externas que no conoces**
   - Verifica que los paquetes existan y sean confiables

### Verificaciones mínimas obligatorias

```
┌─────────────────────────────────────────────────────────────┐
│           CHECKLIST ANTES DE USAR CÓDIGO DE IA              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  □ ¿Entiendo qué hace cada parte del código?                │
│                                                             │
│  □ ¿Las dependencias/imports existen y son correctas?       │
│                                                             │
│  □ ¿Los nombres de métodos/funciones son reales?            │
│    (La IA a veces inventa APIs que no existen)              │
│                                                             │
│  □ ¿Probé el código con datos reales?                       │
│                                                             │
│  □ ¿Probé edge cases? (null, vacío, muy grande)             │
│                                                             │
│  □ ¿El manejo de errores es adecuado?                       │
│                                                             │
│  □ Si hay SQL: ¿está protegido contra inyección?            │
│                                                             │
│  □ Si hay auth: ¿la lógica de permisos es correcta?         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Herramientas del Ecosistema Actual

El panorama de herramientas cambia rápidamente, pero aquí está el estado a 2025:

### IDEs y editores con IA

El rol del IDE está cambiando. Antes era una **herramienta de escritura** — pasabas horas tecleando, navegando código, refactorizando manualmente. Ahora se está convirtiendo en una **herramienta de revisión y navegación** — un visor de código más que un editor.

> 💡 **Insight**: "The IDE becomes more of a code viewer than a writing tool." — Karri Saarinen. Esto no significa que los IDEs sean menos importantes, sino que su función principal cambia: de escribir a supervisar, navegar y validar.

Las herramientas actuales reflejan esta transición:

- **GitHub Copilot** — El más popular. Autocompletado inline en VS Code, JetBrains, etc.
- **Cursor** — Fork de VS Code con IA profundamente integrada (chat + edición)
- **Google Antigravity** — IDE agentico de Google (absorbió a Windsurf). Gratuito en preview
- **JetBrains AI** — IA integrada en IntelliJ, PyCharm, WebStorm
- **Amazon CodeWhisperer** — Alternativa de AWS, gratuito para individuos

### Agentes de coding (autónomos)

Los agentes no solo sugieren código — pueden ejecutar tareas completas: crear PRs, correr tests, modificar múltiples archivos.

- **OpenAI Codex** — Agente cloud que trabaja en paralelo, crea PRs, ejecuta tests
- **Claude Code** — Agente CLI de Anthropic para tareas de desarrollo
- **Google Antigravity** — También funciona como agente con "Artifacts" verificables

### Asistentes conversacionales

Para consultas, explicaciones, y generación de código en chat:

- **Claude** — Razonamiento profundo, código largo, explicaciones claras
- **ChatGPT** — Versatilidad, Code Interpreter para ejecutar código
- **Gemini** — Integración Google, ventana de contexto muy larga

### Herramientas especializadas

- **v0.dev** — Generar componentes React/UI desde descripción (Vercel)
- **Lovable** — Generar aplicaciones web completas desde descripción
- **Warp** — Terminal moderna con IA integrada
- **Replit** — IDE en la nube con Ghostwriter (IA)

### ¿Cuál usar?

- **Quiero sugerencias mientras escribo** → GitHub Copilot o Cursor
- **Necesito generar un archivo/función completa** → Chat con Claude o ChatGPT
- **Quiero que la IA haga cambios en múltiples archivos** → Cursor o Claude Code
- **Necesito entender código existente** → Pegar código en Claude/ChatGPT y preguntar
- **Quiero generar UI rápidamente** → v0.dev para componentes React

💡 **Insight**: Muchos desarrolladores usan múltiples herramientas. Copilot para autocompletado rápido mientras escriben, y Claude/ChatGPT para consultas más complejas o cuando necesitan explicaciones.

---

## Antipatterns: Lo que NO Debes Hacer

### 1. Copiar sin entender

```
❌ MAL:
"Funciona, no sé cómo, pero funciona. Siguiente tarea."

✅ BIEN:
"Funciona. Ahora déjame entender por qué funciona antes
de seguir."
```

**El problema**: Cuando algo falle (y fallará), no sabrás por dónde empezar a debuggear.

### 2. Prompts de una sola iteración

```
❌ MAL:
Prompt → Código → Copiar → Siguiente

✅ BIEN:
Prompt → Código → Revisar → "Ajusta X" → Código v2 →
Revisar → "¿Por qué Y?" → Entender → Código final
```

**El problema**: El primer output rara vez es óptimo. La iteración mejora la calidad.

### 3. Confiar en código de seguridad generado

```
❌ MAL:
"La IA generó el hash de passwords, debe estar bien"

✅ BIEN:
"Voy a verificar que use bcrypt con salt apropiado, y voy a
revisar contra OWASP guidelines"
```

**El problema**: Las vulnerabilidades de seguridad no son obvias. La IA puede generar código que "funciona" pero es inseguro.

### 4. No dar contexto

```
❌ MAL:
"Haz un formulario"

✅ BIEN:
"Haz un formulario de registro para una app React con
TypeScript. Usa React Hook Form. Campos: nombre, email,
password. Validación con Zod. Estilos con Tailwind."
```

**El problema**: Sin contexto, la IA asume cosas que probablemente no aplican a tu proyecto.

### 5. Usar IA para todo

```
❌ MAL:
Usar IA para escribir console.log('hello')

✅ BIEN:
Escribir código trivial tú mismo, usar IA para tareas
que realmente te ahorran tiempo
```

**El problema**: Dependencia excesiva atrofia tus habilidades y a veces es más lento que hacerlo tú mismo.

### 6. No versionar el código generado

```
❌ MAL:
Generar código → Pegarlo → Modificarlo → Perder el original

✅ BIEN:
Generar código → Commit → Modificar → Commit con cambios claros
```

**El problema**: Si algo se rompe, no puedes volver atrás ni entender qué cambió.

---

## Mejores Prácticas

### 1. Establece un flujo consistente

```
1. Antes de promptear, define claramente qué necesitas
2. Incluye contexto relevante (stack, restricciones)
3. Revisa el código generado línea por línea
4. Pide explicación de partes que no entiendas
5. Prueba antes de integrar
6. Commitea con mensaje que indique asistencia de IA (opcional)
```

### 2. Usa la IA para aprender, no solo para producir

```
En lugar de solo:
"Genera un hook de React para fetch de datos"

También pregunta:
"Explícame por qué usaste useEffect con ese array de
dependencias"
"¿Qué pasaría si no incluyera el cleanup?"
"¿Hay alternativas a este enfoque? ¿Cuáles son los tradeoffs?"
```

### 3. Mantén el código generado mantenible

Si la IA genera código complejo, simplifica:

```
❌ Código generado:
const result = data.filter(x => x.active).map(x => ({
  ...x,
  fullName: `${x.firstName} ${x.lastName}`,
  age: new Date().getFullYear() - new Date(x.birthDate).getFullYear()
})).sort((a, b) => a.age - b.age).slice(0, 10);

✅ Refactorizado para claridad:
const activeUsers = data.filter(user => user.active);

const usersWithComputedFields = activeUsers.map(user => ({
  ...user,
  fullName: formatFullName(user),
  age: calculateAge(user.birthDate),
}));

const topTenYoungest = usersWithComputedFields
  .sort((a, b) => a.age - b.age)
  .slice(0, 10);
```

### 4. Documenta decisiones, no solo código

Cuando la IA te ayude a tomar una decisión arquitectónica, documenta el razonamiento:

```javascript
// Usamos Redis para sesiones (en lugar de PostgreSQL) porque:
// - Sesiones son efímeras (24h TTL)
// - Necesitamos lecturas muy rápidas en cada request
// - Ya teníamos Redis para caché
// Decisión tomada con análisis de Claude, validada con el equipo.
```

---

## MCP: Conectando la IA con el Mundo

Hasta ahora hemos hablado de la IA como una herramienta que recibe texto y devuelve texto. Pero las herramientas modernas van más allá: pueden interactuar con sistemas externos.

### El protocolo MCP

**MCP** (Model Context Protocol) es un estándar abierto que permite a los agentes de IA conectarse con herramientas externas de forma estandarizada:

```
┌─────────────┐        ┌─────────────┐
│  Tu agente  │◄──────►│  Servidor   │
│  (Claude,   │  MCP   │  (GitHub,   │
│   Cursor)   │        │   Postgres) │
└─────────────┘        └─────────────┘
```

Con MCP configurado, puedes hacer cosas como:
- "Revisa el PR #123 en GitHub"
- "¿Qué errores nuevos hay en Sentry?"
- "Ejecuta esta query en la base de datos"

El agente usa las herramientas sin que tengas que copiar y pegar datos manualmente.

### Por qué importa

Sin MCP, conectar cada herramienta de IA con cada sistema externo requiere código específico. Con MCP:
- Escribes un conector una vez
- Funciona con cualquier herramienta compatible
- El ecosistema crece (miles de servidores disponibles)

### Configuración básica

En Claude Code, los servidores MCP se configuran así:

```bash
# Agregar servidor de GitHub
claude mcp add github

# Agregar servidor de PostgreSQL
claude mcp add postgres --env DATABASE_URL=...
```

Una vez configurados, las herramientas aparecen disponibles automáticamente.

> 📚 **Para profundizar**: El capítulo 26 "La Nueva Capa de Abstracción" explora MCP en detalle, junto con agents, subagents, hooks, skills, y el modelo mental necesario para el desarrollo agentico moderno.

---

## La IA en el resto del libro

A lo largo de los siguientes capítulos, encontrarás notas marcadas con 🤖 que explican cómo aplicar IA en contextos específicos:

- **Diseño de APIs**: Generar documentación OpenAPI, sugerir endpoints
- **Modelado de datos**: Proponer schemas, identificar relaciones
- **Frontend**: Generar componentes, convertir diseños a código
- **Testing**: Crear casos de prueba, generar mocks
- **Debugging**: Analizar errores, sugerir soluciones
- **Code review**: Identificar problemas, sugerir mejoras

Cada nota asumirá que entiendes los principios de este capítulo: la importancia de revisar, iterar y validar.

---

## Resumen

- La IA **acelera** el desarrollo pero **no reemplaza** el entendimiento
- El ciclo efectivo es: **prompt → revisar → iterar → validar**
- La calidad del output depende de la **calidad del prompt** (contexto + especificidad)
- **Confía más** en código de bajo riesgo (boilerplate, CRUD)
- **Verifica más** código de alto riesgo (seguridad, lógica de negocio)
- Evita los antipatterns: copiar sin entender, no iterar, confiar ciegamente
- Usa la IA también para **aprender**, no solo para producir código

---

## Ejercicios

1. **Análisis de prompt**: Toma un prompt que hayas usado recientemente. Reescríbelo aplicando la estructura (contexto, tarea, restricciones, formato). Compara los resultados.

2. **Verificación activa**: Genera código con IA para una función que calcule el precio con descuento de un producto. Luego:
   - Identifica 3 edge cases que podrían fallar
   - Escribe tests para esos casos
   - Verifica si el código pasa los tests

3. **Entendimiento profundo**: Pide a una IA que genere un middleware de rate limiting para Express. Antes de usarlo:
   - Pide explicación de cada línea
   - Identifica qué pasaría si hay múltiples instancias del servidor
   - Pregunta por alternativas y sus tradeoffs

4. **Detección de problemas**: Copia este código generado por IA y encuentra los problemas:
   ```javascript
   app.get('/user/:id', (req, res) => {
     const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
     db.query(query).then(user => res.json(user));
   });
   ```

---

## Referencias

- Simon Willison (2023-2024). Blog posts sobre desarrollo con LLMs. https://simonwillison.net/
- Ethan Mollick (2024). *Co-Intelligence: Living and Working with AI*. Penguin.
- Osmani, A. (2025). *How Good is AI at Coding React Really?* https://addyo.substack.com/
- Documentación oficial de GitHub Copilot, Claude, Cursor
- OWASP Guidelines para seguridad en código generado por IA

---

**Anterior**: [Pensamiento en Sistemas](./03-pensamiento-sistemas.md) | **Siguiente**: [Entendiendo el Problema](./05-entendiendo-problema.md)
