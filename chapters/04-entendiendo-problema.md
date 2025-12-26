# 4. Entendiendo el Problema

> El mayor desperdicio en software es construir algo que nadie necesita.

## Objetivos de Aprendizaje

Al finalizar este capítulo, serás capaz de:
- Distinguir entre lo que el usuario pide y lo que realmente necesita
- Aplicar técnicas de elicitación para descubrir requerimientos ocultos
- Escribir user stories efectivas y especificaciones técnicas claras
- Hacer las preguntas correctas antes de escribir una línea de código

---

## El problema del problema

Imagina esta conversación:

> **Cliente**: "Necesito un botón que exporte los datos a Excel."
>
> **Desarrollador**: "Ok, lo hago."
>
> *Tres días después...*
>
> **Cliente**: "Esto no es lo que necesitaba. Yo quería poder filtrar antes de exportar, y que el formato fuera específico para contabilidad."

¿Quién falló aquí? Ambos. El cliente asumió que el desarrollador entendería el contexto. El desarrollador asumió que entendía el problema.

📖 **Concepto**: La mayoría de los proyectos de software no fallan por código mal escrito. Fallan porque **resuelven el problema equivocado** o resuelven el problema correcto de la manera incorrecta.

### El iceberg de los requerimientos

Lo que el usuario dice es solo la punta del iceberg:

```
                    ┌─────────────────┐
     Visible        │  "Quiero un     │
     (lo que dice)  │   botón de      │
                    │   exportar"     │
════════════════════╪═════════════════╪════════════════════
                    │                 │
                    │  • ¿Exportar qué datos exactamente?
                    │  • ¿En qué formato?
     Oculto         │  • ¿Quién lo va a usar?
     (lo que        │  • ¿Con qué frecuencia?
      necesita      │  • ¿Qué hacen con el archivo después?
      realmente)    │  • ¿Hay restricciones de seguridad?
                    │  • ¿Qué pasa si son millones de filas?
                    │  • ¿Necesitan realmente Excel o solo
                    │     una forma de analizar los datos?
                    │
                    └─────────────────┘
```

Tu trabajo no es solo implementar lo que piden. Es **descubrir lo que necesitan**.

---

## Del pedido al requerimiento

Un **pedido** es lo que alguien te dice que quiere. Un **requerimiento** es lo que realmente necesita el sistema para resolver el problema de negocio.

### Ejemplo: "Necesitamos login con Google"

**Pedido**: Implementar autenticación con Google.

**Preguntas que deberías hacer**:
- ¿Por qué Google específicamente? ¿Los usuarios tienen cuentas de Google?
- ¿También necesitan poder registrarse con email/password?
- ¿Qué pasa con usuarios que no tienen Google?
- ¿Necesitan single sign-on con otras plataformas (Microsoft, Apple)?
- ¿Hay requisitos de seguridad específicos (2FA, sesiones)?
- ¿Qué datos del perfil de Google necesitamos?

**Requerimiento real** (después de investigar):
> Los usuarios son empleados de empresas que usan Google Workspace. Necesitan autenticarse con su cuenta corporativa de Google. No necesitan registro manual. Debemos capturar nombre, email y foto de perfil. Las sesiones deben expirar después de 8 horas de inactividad.

¿Ves la diferencia? El pedido era vago. El requerimiento es específico y accionable.

### El framework de las 5 W + H

Una técnica simple pero poderosa:

| Pregunta | Propósito |
|----------|-----------|
| **What** (Qué) | ¿Qué problema estamos resolviendo? ¿Qué funcionalidad específica? |
| **Who** (Quién) | ¿Quién va a usar esto? ¿Quién se beneficia? |
| **Why** (Por qué) | ¿Por qué es necesario? ¿Qué pasa si no lo hacemos? |
| **When** (Cuándo) | ¿Cuándo lo necesitan? ¿Con qué frecuencia se usa? |
| **Where** (Dónde) | ¿En qué contexto? ¿Móvil, desktop, ambos? |
| **How** (Cómo) | ¿Cómo debería funcionar? ¿Cómo medimos el éxito? |

💡 **Insight**: El "Why" es la pregunta más importante y la que menos se hace. Entender *por qué* alguien necesita algo te permite proponer mejores soluciones—a veces completamente diferentes a lo que pidieron.

---

## Técnicas de elicitación

"Elicitación" es el proceso de descubrir y documentar requerimientos. No es solo preguntar "¿qué quieres?"—es usar técnicas específicas para extraer información que el usuario no sabe que tiene.

### 1. Entrevistas estructuradas

Conversaciones guiadas con stakeholders clave.

**Preparación**:
- Define objetivos claros para la entrevista
- Prepara preguntas abiertas (no sí/no)
- Identifica a las personas correctas (usuarios reales, no solo gerentes)

**Durante**:
- Escucha más de lo que hablas (regla 80/20)
- Toma notas textuales, no interpretaciones
- Pregunta "¿por qué?" al menos 3 veces
- Pide ejemplos concretos

**Preguntas útiles**:
- "Cuéntame cómo haces [tarea] hoy, paso a paso"
- "¿Qué es lo más frustrante de ese proceso?"
- "Si pudieras cambiar una sola cosa, ¿cuál sería?"
- "¿Qué pasa cuando algo sale mal?"
- "Muéstrame un ejemplo de cuando esto funcionó bien/mal"

### 2. Observación (shadowing)

Observar a usuarios reales haciendo su trabajo.

```
Lo que dicen que hacen    vs.    Lo que realmente hacen
─────────────────────────────────────────────────────────
"Uso el sistema todos           En realidad lo usan 2
los días"                       veces por semana

"El proceso es simple"          Tienen 5 post-its con
                                trucos para que funcione

"Exporto y lo mando             Exportan, abren en Excel,
por email"                      borran columnas, reformatean,
                                guardan como PDF, y luego
                                envían por email
```

⚠️ **Advertencia**: Las personas no mienten intencionalmente. Simplemente no son conscientes de todo lo que hacen. El comportamiento automatizado es invisible para quien lo ejecuta.

### 3. Análisis de documentos existentes

Revisa lo que ya existe:
- Reportes actuales (¿qué datos importan?)
- Emails de soporte (¿qué problemas tienen?)
- Flujos de trabajo documentados
- Sistemas legacy que vas a reemplazar
- Hojas de cálculo que usan como "sistema"

💡 **Insight**: Las hojas de Excel de una empresa son una mina de oro. Te muestran qué datos manipulan, qué cálculos hacen, y cómo estructuran su pensamiento.

### 4. Prototipos de baja fidelidad

A veces es más fácil mostrar que explicar.

```
┌─────────────────────────────────────┐
│  Pantalla de exportación (boceto)   │
├─────────────────────────────────────┤
│                                     │
│  Filtros:                           │
│  ┌─────────────┐ ┌─────────────┐    │
│  │ Fecha desde │ │ Fecha hasta │    │
│  └─────────────┘ └─────────────┘    │
│                                     │
│  ┌─────────────┐                    │
│  │ Departamento│                    │
│  └─────────────┘                    │
│                                     │
│  Formato: ○ Excel  ○ CSV  ○ PDF     │
│                                     │
│  [  Exportar  ]                     │
│                                     │
└─────────────────────────────────────┘

"¿Es esto lo que tenías en mente?"
```

Un boceto en papel o una herramienta simple (Figma, Excalidraw, incluso PowerPoint) puede aclarar más que 30 minutos de conversación.

### 5. Talleres de requisitos

Reuniones facilitadas con múltiples stakeholders.

**Cuándo usarlo**:
- Hay múltiples perspectivas que reconciliar
- Hay conflictos entre lo que diferentes personas quieren
- Necesitas consenso rápido

**Formato típico**:
1. Presentar el problema (10 min)
2. Lluvia de ideas individual (5 min, post-its)
3. Compartir y agrupar ideas (15 min)
4. Priorizar juntos (15 min)
5. Definir siguiente pasos (5 min)

---

## User Stories vs Especificaciones Técnicas

Hay dos formas principales de documentar requerimientos, y sirven para propósitos diferentes.

### User Stories

Describen funcionalidad desde la perspectiva del usuario.

**Formato clásico**:
```
Como [tipo de usuario]
Quiero [hacer algo]
Para [lograr algún objetivo]
```

**Ejemplo**:
```
Como contador del departamento de finanzas
Quiero exportar las transacciones del mes a Excel
Para poder hacer la conciliación bancaria mensual
```

**Criterios de aceptación** (el "cómo sabemos que está listo"):
```
- Puedo filtrar por rango de fechas
- Puedo filtrar por tipo de transacción
- El Excel incluye: fecha, descripción, monto, categoría
- Las fechas están en formato DD/MM/YYYY
- Los montos usan separador de miles con punto
- El archivo se descarga en menos de 5 segundos para 10,000 registros
```

### Especificaciones Técnicas

Describen cómo se implementará la solución.

**Ejemplo** (para la misma funcionalidad):
```markdown
## Endpoint de Exportación

### Request
POST /api/exports/transactions

```json
{
  "startDate": "2025-01-01",
  "endDate": "2025-01-31",
  "transactionTypes": ["income", "expense"],
  "format": "xlsx"
}
```

### Response
- 200: Archivo binario con header Content-Disposition
- 400: Parámetros inválidos
- 413: Demasiados registros (límite: 50,000)

### Implementación
- Usar streaming para archivos grandes
- Cache de 5 minutos para exports idénticos
- Timeout de 30 segundos
- Logging de cada exportación para auditoría
```

### ¿Cuándo usar cada una?

| User Stories | Especificaciones Técnicas |
|--------------|---------------------------|
| Comunicar con stakeholders no técnicos | Comunicar con desarrolladores |
| Definir el "qué" y el "por qué" | Definir el "cómo" |
| Al inicio, para alinear expectativas | Después, para planificar implementación |
| Deben ser entendibles por cualquiera | Pueden ser técnicas |

📖 **Concepto**: Las user stories no reemplazan a las especificaciones técnicas. Son complementarias. La user story dice qué problema resolvemos; la especificación técnica dice cómo lo resolvemos.

---

## El arte de hacer preguntas

Hacer las preguntas correctas es una habilidad que se desarrolla con práctica.

### Preguntas que abren conversaciones

| En lugar de... | Pregunta... |
|----------------|-------------|
| "¿Necesitas filtros?" | "¿Cómo decides qué datos exportar?" |
| "¿Está bien así?" | "¿Qué cambiarías si pudieras?" |
| "¿Lo entendiste?" | "¿Puedes explicarme cómo lo usarías?" |
| "¿Algo más?" | "¿Qué no te he preguntado que debería saber?" |

### La técnica de los 5 "Por qué"

Cuando alguien te pide algo, pregunta "por qué" repetidamente para llegar a la raíz:

```
"Necesito un reporte de ventas diario por email."
  └─ ¿Por qué?
"Para saber cómo van las ventas."
  └─ ¿Por qué necesitas saberlo diariamente?
"Para detectar si hay problemas rápido."
  └─ ¿Por qué? ¿Qué tipo de problemas?
"A veces un producto deja de venderse y no nos damos cuenta."
  └─ ¿Por qué no se dan cuenta?
"Porque hay muchos productos y no tenemos alertas."
  └─ ¿Por qué no tienen alertas?
"Nunca las hemos implementado."

SOLUCIÓN REAL: Sistema de alertas automáticas cuando un
producto cae más del 20% vs. su promedio, no un reporte diario.
```

### Preguntas sobre casos borde

Los casos borde revelan complejidad oculta:

- "¿Qué pasa si el usuario no tiene permiso?"
- "¿Qué pasa si hay 0 resultados? ¿Y si hay 1 millón?"
- "¿Qué pasa si dos personas hacen esto al mismo tiempo?"
- "¿Qué pasa si falla a mitad del proceso?"
- "¿Qué pasa si el usuario cierra el navegador durante la operación?"
- "¿Qué pasa si el dato ya existe?"
- "¿Qué pasa los fines de semana? ¿Y en feriados?"

### Preguntas sobre el contexto

- "¿Quién más usa esto?"
- "¿Qué hacen antes y después de esta tarea?"
- "¿Con qué frecuencia hacen esto?"
- "¿Qué herramientas usan actualmente?"
- "¿Hay regulaciones o políticas que deba conocer?"

---

## Antipatrones comunes

### 1. El "sí a todo"

```
Cliente: "¿Puede hacer X?"
Desarrollador: "Sí"
Cliente: "¿Y también Y?"
Desarrollador: "Sí"
Cliente: "¿Y Z?"
Desarrollador: "Sí"

Resultado: Proyecto inmanejable, nunca termina.
```

**Solución**: Cada "sí" debe venir con un costo explícito (tiempo, complejidad, trade-offs).

### 2. El "ya sé lo que necesitas"

Asumir que entiendes el problema sin validar.

```
"Es obvio que necesitan un dashboard con gráficos."

Realidad: Lo que necesitan es una alerta por email
cuando algo está mal. No quieren monitorear un dashboard.
```

**Solución**: Siempre valida tu entendimiento. "Entonces, si entiendo bien, necesitas X para lograr Y. ¿Es correcto?"

### 3. El "el usuario no sabe lo que quiere"

Descartar lo que dice el usuario porque "no es técnico".

```
"Los usuarios no entienden de tecnología.
Yo sé qué es mejor para ellos."
```

**Realidad**: Los usuarios conocen su problema mejor que tú. Tu trabajo es traducir ese problema a una solución técnica, no imponer tu visión.

**Solución**: Escucha el problema, cuestiona la solución propuesta.

### 4. El "requerimiento infinito"

Requerimientos que nunca se terminan de definir.

```
"Necesitamos un sistema de reportes."
"¿Qué reportes?"
"Todos los que puedan necesitar."
```

**Solución**: Forzar priorización. "Si solo pudieras tener un reporte, ¿cuál sería? Ok, empezamos por ese."

---

## Documentando requerimientos

### Estructura mínima viable

Para cada funcionalidad, documenta al menos:

```markdown
## [Nombre de la funcionalidad]

### Problema
¿Qué problema resuelve? ¿Por qué es necesario?

### Usuario
¿Quién lo usa? ¿En qué contexto?

### Descripción
¿Qué hace la funcionalidad?

### Criterios de aceptación
- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Criterio 3

### Fuera de alcance
¿Qué NO incluye esta funcionalidad?

### Preguntas abiertas
¿Qué falta por definir?
```

### Ejemplo completo

```markdown
## Exportación de transacciones a Excel

### Problema
El equipo de contabilidad pasa 2 horas semanales copiando
datos del sistema a Excel para la conciliación bancaria.
Necesitan una forma de exportar directamente.

### Usuario
Contadores del departamento de finanzas (3 personas).
Usan la funcionalidad 4 veces al mes (cierre semanal).

### Descripción
Botón en la pantalla de transacciones que genera un archivo
Excel con las transacciones filtradas según los criterios
actuales de la vista.

### Criterios de aceptación
- [ ] El botón aparece solo para usuarios con rol "contador"
- [ ] Respeta los filtros aplicados en la vista
- [ ] Incluye columnas: fecha, descripción, monto, categoría, estado
- [ ] Formato de fecha: DD/MM/YYYY
- [ ] Formato de montos: separador de miles, 2 decimales
- [ ] Nombre del archivo: transacciones_YYYY-MM-DD.xlsx
- [ ] Funciona para hasta 50,000 registros
- [ ] Muestra barra de progreso para exports > 5 segundos

### Fuera de alcance
- Exportación a otros formatos (CSV, PDF) - fase 2
- Programar exports automáticos - fase 2
- Personalización de columnas - no planificado

### Preguntas abiertas
- ¿Necesitan incluir transacciones anuladas?
- ¿El archivo debe tener algún formato específico para su
  sistema contable?
```

---

## Resumen

- Lo que el usuario **pide** no es lo mismo que lo que **necesita**—tu trabajo es descubrir la diferencia
- Usa las **5 W + H** (What, Who, Why, When, Where, How) para profundizar en cada requerimiento
- Las técnicas de **elicitación** (entrevistas, observación, prototipos) te ayudan a extraer información que el usuario no sabe que tiene
- **User stories** comunican el qué y por qué; **especificaciones técnicas** comunican el cómo
- Haz preguntas que **abran conversaciones**, no que las cierren
- **Documenta** los requerimientos de forma clara, incluyendo lo que está fuera de alcance

---

## Ejercicios

1. **Práctica de entrevista**: Pide a un amigo o colega que te describa un problema de su trabajo. Usa la técnica de los 5 "Por qué" para llegar a la raíz del problema. ¿La solución que pidió inicialmente era la mejor?

2. **Análisis de pedido**: Toma este pedido: "Necesito que la aplicación sea más rápida". Escribe 10 preguntas que harías para convertir esto en requerimientos accionables.

3. **User story completa**: Elige una funcionalidad de una aplicación que uses diariamente. Escribe la user story con el formato completo (Como... Quiero... Para...) más 5 criterios de aceptación.

4. **Casos borde**: Para una funcionalidad de "registro de usuario", lista al menos 10 casos borde que deberían considerarse.

---

## Referencias

- Cohn, M. (2004). *User Stories Applied*. Addison-Wesley. — El libro definitivo sobre user stories
- Patton, J. (2014). *User Story Mapping*. O'Reilly. — Técnica para organizar y priorizar stories
- Gothelf, J. (2013). *Lean UX*. O'Reilly. — Enfoque iterativo para descubrir requerimientos

---

**Anterior**: [Pensamiento en Sistemas](./03-pensamiento-sistemas.md) | **Siguiente**: [Diseño de Producto y UX](./05-diseno-producto-ux.md)
