# Apéndice D. Plantillas y Listas de Verificación

> Una plantilla sirve para hacer visibles decisiones. Si se convierte en un
> formulario que nadie lee, debe reducirse o eliminarse.

Copia y adapta estas plantillas. No todos los campos aplican a todos los
proyectos. El nivel de detalle debe ser proporcional a riesgo, duración,
irreversibilidad y número de personas afectadas.

---

## 1. Brief del problema

Úsalo antes de diseñar una solución.

```text
# Brief: <nombre>

Fecha:
Responsable:
Estado: borrador / validado / descartado

## Problema
¿Qué ocurre hoy?
¿Quién lo experimenta?
¿Con qué frecuencia?
¿Qué evidencia existe?

## Resultado deseado
¿Qué cambio observable buscamos?
¿Cómo sabremos que mejoró?

## Personas y contexto
Usuarios principales:
Usuarios indirectos:
Necesidades de accesibilidad:
Dispositivos, red y ambientes:

## Alcance
Incluye:
No incluye:
Supuestos:

## Restricciones
Tiempo:
Presupuesto:
Regulación o privacidad:
Integraciones:
Capacidad del equipo:

## Riesgos
Riesgo de no hacer:
Riesgo de hacer:
Decisiones irreversibles:

## Evidencia y siguiente paso
Datos disponibles:
Preguntas abiertas:
Experimento más pequeño:
Fecha de revisión:
```

### Lista de verificación

- [ ] Describe una necesidad, no una feature
- [ ] Identifica población y contexto
- [ ] Incluye evidencia o declara que todavía no existe
- [ ] Define resultado observable
- [ ] Separa alcance de exclusiones
- [ ] Expone restricciones reales
- [ ] Permite descartar la idea

---

## 2. Recorrido y criterio de aceptación

```text
# Recorrido: <nombre>

Actor:
Objetivo:
Precondiciones:
Disparador:

## Camino principal
1.
2.
3.

## Alternativas
- Sin datos:
- Entrada inválida:
- Sin permiso:
- Dependencia lenta:
- Operación repetida:
- Usuario abandona:

## Resultado
Estado persistido:
Efectos externos:
Respuesta visible:
Evento o auditoría:

## Criterios de aceptación
- Dado <contexto>, cuando <acción>, entonces <resultado>.
- Dado ...

## Propiedades transversales
Accesibilidad:
Seguridad:
Privacidad:
Rendimiento:
Observabilidad:
```

Evita criterios como “funciona correctamente”. Describe resultados observables
y estados relevantes.

---

## 3. Restricciones y atributos de calidad

```text
# Atributos de calidad

Capacidad principal:
Población:
Ventana:

## Rendimiento
SLI:
Objetivo:
Punto de medición:
Carga esperada:
Comportamiento al saturarse:

## Disponibilidad
Operaciones incluidas:
SLO:
Dependencias críticas:
Degradación:
RTO/RPO si aplica:

## Seguridad
Activos:
Actores:
Fronteras:
Requisitos:

## Privacidad
Datos personales:
Finalidad:
Retención:
Acceso:
Eliminación/exportación:

## Accesibilidad
Estándar objetivo:
Tecnologías de apoyo:
Pruebas manuales:

## Operabilidad
Señales:
Alertas:
Runbook:
Ownership:
```

Un atributo sin población, ventana y punto de medición suele ser una aspiración,
no un requisito verificable.

---

## 4. Registro de decisión arquitectónica (ADR)

```text
# ADR-<número>: <decisión>

Fecha:
Estado: propuesta / aceptada / reemplazada / rechazada
Responsables:
Reemplaza:

## Contexto
¿Qué fuerzas y restricciones requieren una decisión?

## Opciones consideradas

### Opción A
Beneficios:
Costes:
Riesgos:

### Opción B
Beneficios:
Costes:
Riesgos:

## Decisión
¿Qué elegimos?
¿Por qué ahora?

## Consecuencias
Positivas:
Negativas:
Trabajo posterior:

## Evidencia
Experimentos:
Métricas:
Fuentes:

## Reversibilidad
Coste de cambiar:
Señal para reconsiderar:
Fecha de revisión:
```

### Buen ADR

- explica el contexto de su momento;
- conserva alternativas reales;
- registra trade-offs;
- no intenta documentar toda la arquitectura;
- puede ser reemplazado sin reescribir la historia.

---

## 5. Contrato de endpoint HTTP

```text
# <MÉTODO> <ruta>

Propósito:
Consumidores:
Estabilidad: interno / público / experimental
Responsable:

## Identidad
Mecanismo:
Scopes/roles:
Autorización de objeto:

## Request
Path params:
Query params:
Headers:
Content-Type:
Body schema:
Tamaño máximo:

## Validación
Sintáctica:
Semántica:
Reglas de negocio:

## Respuestas
2xx:
4xx:
5xx:
Formato de error:

## Semántica
Idempotencia:
Clave de idempotencia:
Transacción:
Efectos:
Consistencia:

## Operación
Timeout:
Rate limit:
Caché:
Paginación:
Observabilidad:

## Compatibilidad
Versionado:
Deprecación:
Ejemplo:
Prueba de contrato:
```

### Lista de verificación de API

- [ ] Método y status respetan semántica HTTP
- [ ] Entrada y salida tienen esquema
- [ ] Campos internos no se aceptan por mass assignment
- [ ] Autorización incluye recurso y tenant
- [ ] Errores son estables y no filtran detalles
- [ ] Colecciones tienen límite y orden determinista
- [ ] Reintentos e idempotencia están definidos
- [ ] Caché y `Vary` consideran personalización
- [ ] Existe timeout y límite de body
- [ ] Logs excluyen tokens y datos sensibles
- [ ] Cambios incompatibles tienen estrategia

---

## 6. Modelo de datos

```text
# Modelo: <nombre>

Propósito:
Propietario:
Sistema de registro:

## Identidad
Clave primaria:
Claves naturales:
Tenant/usuario:

## Campos
Nombre | Tipo | Nulo | Default | Significado | Sensibilidad

## Invariantes
- ...

## Relaciones
Origen:
Destino:
Cardinalidad:
Política de eliminación:

## Acceso
Consultas principales:
Orden:
Filtros:
Volumen esperado:

## Índices
Índice:
Consulta que soporta:
Coste en escritura:

## Tiempo
Instantes:
Fechas civiles:
Zona horaria:
Retención:

## Seguridad y privacidad
Clasificación:
Cifrado:
Redacción:
Auditoría:
Exportación/eliminación:

## Evolución
Migraciones previstas:
Compatibilidad:
Backfill:
```

### Revisión

- [ ] Los nombres expresan significado
- [ ] Dinero evita floats binarios
- [ ] Tiempo distingue instante y fecha civil
- [ ] UUID no se trata como autorización
- [ ] Invariantes críticas tienen restricciones
- [ ] Foreign keys y eliminación son intencionales
- [ ] Índices responden a consultas
- [ ] Datos sensibles tienen finalidad y retención

---

## 7. Plan de migración

```text
# Migración: <nombre>

Revisión actual:
Revisión objetivo:
Responsable:

## Cambio
Esquema:
Datos:
Código relacionado:

## Compatibilidad
¿Código viejo funciona con esquema nuevo?
¿Código nuevo funciona con esquema viejo?
Ventana de coexistencia:

## Fases
1. Expandir:
2. Desplegar escritura compatible:
3. Backfill:
4. Validar:
5. Contraer:

## Impacto
Filas:
Duración estimada y evidencia:
Locks:
Espacio:
Replicación:

## Ejecución
Comando incremental:
Ambiente de prueba:
Backup:
Monitoreo:
Criterio de pausa:

## Rollback o avance
¿Puede revertirse el esquema?
¿Se prefiere corregir hacia adelante?
Datos que no pueden reconstruirse:

## Verificación
Consulta de estado:
Invariantes:
Métrica:
Prueba de aplicación:
```

### Reglas

- [ ] Nunca depende de resetear la base
- [ ] Se probó desde la revisión realmente desplegada
- [ ] La migración generada se revisó
- [ ] Backfill es acotado y reanudable
- [ ] Código viejo y nuevo tienen una ventana compatible
- [ ] Locks y espacio fueron evaluados
- [ ] Existe criterio para detener
- [ ] Estado final es verificable

---

## 8. Threat model ligero

```text
# Threat model: <sistema/flujo>

Versión:
Fecha:
Participantes:
Alcance:
Exclusiones:

## Activos
- Identidad:
- Datos:
- Dinero/inventario:
- Disponibilidad:
- Secretos:
- Evidencia:

## Actores
- Usuario:
- Operador:
- Servicio:
- Tercero:
- Atacante:

## Fronteras de confianza
1.
2.

## Flujos
Origen → destino → datos → protocolo → credencial

## Historias de abuso

### Abuso 1
Actor:
Precondición:
Acción:
Impacto:
Prevención:
Detección:
Respuesta:
Riesgo residual:
Responsable:

## Dependencias y supply chain
Paquetes:
Build:
Artefactos:
Proveedores:

## Verificación
Requisito:
Prueba:
Evidencia:

## Revisión
Cambios que obligan a actualizar:
Fecha:
```

No empieces por una lista genérica de vulnerabilidades. Empieza por activos,
fronteras y abusos del producto.

---

## 9. Diseño de tarea asíncrona

```text
# Trabajo asíncrono: <nombre>

Productor:
Consumidor:
Efecto:

## Mensaje
Tipo:
Versión:
Identificador:
Clave de idempotencia:
Payload:
Datos sensibles:

## Entrega
Semántica:
Orden:
Duplicados:
Retención:

## Publicación
Frontera transaccional:
Outbox:
Confirmación:

## Consumo
Timeout:
Reintentos:
Backoff/jitter:
Errores reintentables:
Errores terminales:
Idempotencia:

## Fallo
Dead-letter/estado terminal:
Reprocesamiento:
Compensación:
Intervención humana:

## Operación
Backlog:
Edad del mensaje:
Throughput:
Alertas:
Runbook:
```

### Casos de prueba

- [ ] Mensaje duplicado
- [ ] Proceso cae antes del efecto
- [ ] Proceso cae después del efecto y antes del ack
- [ ] Dependencia responde 429 con `Retry-After`
- [ ] Payload incompatible
- [ ] Mensaje fuera de orden
- [ ] Poison message
- [ ] Reprocesamiento manual

---

## 10. Plan de pruebas

```text
# Plan de pruebas: <capacidad>

Riesgo:
Contrato:
Ambientes:
Datos:

## Unidad
Reglas:
Límites:
Propiedades:

## Integración
Base:
Servicios:
Transacciones:
Fallos:

## Contrato
Esquema:
Compatibilidad:
Consumidores:

## E2E
Recorridos:
Navegadores/dispositivos:
Identidades:

## No funcional
Accesibilidad:
Rendimiento:
Seguridad:
Resiliencia:

## Oráculos
¿Cómo se determina éxito?
¿Qué datos se inspeccionan?

## CI
Etapa:
Paralelismo:
Flakiness:
Artefactos de fallo:

## Fuera de alcance
- ...
```

### Matriz de riesgo

| Riesgo | Probabilidad | Impacto | Prueba | Ambiente | Responsable |
|--------|--------------|---------|--------|----------|-------------|
| | | | | | |

No persigas cobertura numérica sin contexto. Relaciona pruebas con
comportamientos y riesgos.

---

## 11. Revisión de accesibilidad

### Contenido y estructura

- [ ] `lang` correcto
- [ ] Título de página útil
- [ ] Un propósito claro por encabezado
- [ ] Jerarquía sin depender del tamaño visual
- [ ] Texto alternativo comunica función
- [ ] Links describen destino
- [ ] Tablas tienen encabezados

### Operación

- [ ] Todo funciona con teclado
- [ ] Foco visible
- [ ] Orden de foco lógico
- [ ] No existe keyboard trap
- [ ] Diálogos gestionan foco y nombre
- [ ] Errores se asocian a campos
- [ ] Estados dinámicos se anuncian cuando corresponde

### Presentación

- [ ] Contraste suficiente
- [ ] Información no depende solo de color
- [ ] Zoom y reflow conservan operación
- [ ] Movimiento tiene alternativa
- [ ] Targets son utilizables
- [ ] Orientación no se restringe sin necesidad

### Verificación

- [ ] Scanner automático
- [ ] Teclado manual
- [ ] VoiceOver o NVDA
- [ ] Dispositivo/viewport realista
- [ ] Recorrido crítico con persona o revisión especializada cuando el riesgo lo
      exige

---

## 12. Plan de despliegue

```text
# Despliegue: <release>

Commit:
Artefacto/digest:
Responsable:
Ventana:

## Cambios
Código:
Configuración:
Datos:
Infraestructura:
Dependencias:

## Precondiciones
CI:
Backup:
Capacidad:
Feature flags:
Compatibilidad:

## Secuencia
1.
2.

## Migraciones
Job:
Duración:
Compatibilidad:
Verificación:

## Exposición
Estrategia: rolling / canary / blue-green / otra
Población inicial:
Incrementos:

## Verificación
Health:
Smoke:
Métrica de producto:
Errores:
Latencia:
Saturación:

## Criterios
Continuar:
Pausar:
Rollback:

## Rollback
Artefacto anterior:
Configuración:
Datos:
Feature flag:

## Comunicación
Stakeholders:
Estado:
Incidente:
```

### Lista de verificación

- [ ] Artefacto es inmutable y trazable
- [ ] Secretos no están en artefacto ni logs
- [ ] Migración se ejecuta una vez
- [ ] Instancias antiguas y nuevas pueden coexistir
- [ ] Readiness evita tráfico prematuro
- [ ] Requests en vuelo pueden drenar
- [ ] La decisión usa señales, no solo “deployment succeeded”
- [ ] Rollback se ensayó o sus límites están documentados

---

## 13. SLO y alerta

```text
# SLO: <capacidad>

Usuario/población:
Operación:
Ventana:

## SLI
Eventos buenos:
Eventos válidos:
Fuente:
Punto de medición:
Exclusiones:

## Objetivo
Porcentaje/umbral:
Justificación:
Error budget:

## Alertas
Síntoma:
Ventanas:
Severidad:
Destino:
Runbook:

## Dependencias
Qué puede distinguirse:
Qué no:

## Revisión
Datos insuficientes:
Fecha:
Responsable:
```

Una alerta útil requiere acción. Si nadie sabe qué hacer, crea primero un
diagnóstico o runbook.

---

## 14. Runbook

```text
# Runbook: <alerta/síntoma>

Servicio:
Owner:
Última prueba:

## Significado
Qué detecta:
Impacto probable:
Falsos positivos conocidos:

## Seguridad
Permisos requeridos:
Datos sensibles:
Acciones prohibidas:

## Diagnóstico
1. Confirmar síntoma:
2. Identificar versión/cambio:
3. Revisar saturación:
4. Revisar dependencias:

## Mitigación
Opción segura 1:
Opción segura 2:
Rollback:
Degradación:

## Escalamiento
Cuándo:
A quién:
Canal:

## Verificación de recuperación
Métrica:
Recorrido:
Backlog:

## Seguimiento
Datos a conservar:
Issue/postmortem:
```

No incluyas secretos ni comandos destructivos. Un runbook debe indicar
precondiciones y alcance antes de cualquier mutación.

---

## 15. Informe de incidente

```text
# Incidente: <título>

Fecha:
Severidad:
Estado:
Coordinación:

## Resumen
Impacto:
Usuarios:
Duración:

## Línea de tiempo
Hora | Evento | Evidencia/decisión

## Detección
Cómo:
Qué habría detectado antes:

## Respuesta
Mitigaciones:
Recuperación:
Comunicación:

## Análisis
Condición iniciadora:
Factores contribuyentes:
Por qué controles no evitaron o detectaron:

## Lo que funcionó
- ...

## Lo que dificultó
- ...

## Acciones
Acción | Tipo | Responsable | Fecha | Evidencia de cierre

## Aprendizaje
Cambios a diseño:
Cambios a operación:
Riesgo residual:
```

Evita buscar una persona culpable. Analiza condiciones y decisiones del sistema.
Las acciones deben ser específicas y verificables; “tener más cuidado” no lo es.

---

## 16. Brief para una tarea de IA

```text
# Tarea para agente

Objetivo:
Por qué:

## Alcance
Archivos/componentes:
Fuera de alcance:
Cambios permitidos:
Acciones prohibidas:

## Contexto
Arquitectura:
Convenciones:
Decisión relevante:
Datos ficticios:

## Contrato
Comportamiento actual:
Comportamiento esperado:
Compatibilidad:

## Seguridad
Datos que no deben leerse:
Permisos:
Red:
Secretos:
Producción:

## Entregable
Código:
Pruebas:
Documentación:
Resumen:

## Verificación
Comandos:
Casos:
Typecheck/lint:
Build:

## Criterio de aceptación
- ...

## Cuándo detenerse
Ambigüedad material:
Acción destructiva:
Fallo repetido:
Necesidad de nueva autorización:
```

### Revisión del resultado de IA

- [ ] El diff corresponde al objetivo
- [ ] No hay cambios no solicitados
- [ ] APIs existen en la versión instalada
- [ ] No aparecen secretos ni datos reales
- [ ] Autorización y tenant siguen presentes
- [ ] Errores y límites están definidos
- [ ] Pruebas fallan antes y pasan después cuando aplica
- [ ] Typecheck, lint, tests y build pasaron
- [ ] Se inspeccionó código generado, no solo resumen
- [ ] La documentación se actualizó
- [ ] Existe rollback

---

## 17. Evaluación de un agente

```text
# Eval: <capacidad>

Versión del sistema:
Modelo/configuración:
Herramientas:
Permisos:
Dataset:

## Casos
ID:
Entrada:
Estado inicial:
Resultado permitido:
Resultado prohibido:
Evidencia:

## Métricas
Corrección:
Acciones innecesarias:
Violaciones de permiso:
Coste:
Latencia:
Necesidad de intervención:

## Jueces
Automático:
Humano:
Reglas:

## Repeticiones
Cantidad:
Variación:

## Resultado
Pasa/no pasa:
Fallos:
Riesgo residual:
```

Incluye casos adversariales:

- prompt intenta ampliar alcance;
- herramienta devuelve datos maliciosos;
- recurso pertenece a otro tenant;
- acción se repite;
- dependencia falla a mitad;
- aprobación se niega;
- contexto contiene una instrucción no confiable.

---

## 18. Definition of Done

Adapta por riesgo:

### Producto

- [ ] Resultado y criterio de aceptación cumplidos
- [ ] Estados vacío, carga, error y éxito diseñados
- [ ] Analytics o métrica responde una pregunta

### Código

- [ ] Responsabilidades y nombres son claros
- [ ] No existe duplicación de regla crítica
- [ ] Dependencias nuevas están justificadas
- [ ] Configuración tiene defaults seguros

### Datos

- [ ] Esquema e invariantes revisados
- [ ] Migración incremental probada
- [ ] Compatibilidad y backfill definidos
- [ ] Privacidad y retención consideradas

### Seguridad

- [ ] Entrada validada
- [ ] Autorización por operación y objeto
- [ ] Secretos fuera del código
- [ ] Abusos relevantes probados
- [ ] Logs no contienen datos sensibles

### Calidad

- [ ] Pruebas proporcionales al riesgo
- [ ] Accesibilidad manual y automática
- [ ] Rendimiento comparado con objetivo
- [ ] Errores y fallos parciales cubiertos

### Operación

- [ ] Build reproducible
- [ ] Señales y dashboards disponibles
- [ ] Alertas tienen runbook
- [ ] Despliegue y rollback definidos
- [ ] Ownership documentado

### Documentación

- [ ] Contrato actualizado
- [ ] ADR cuando hubo decisión significativa
- [ ] Changelog/release notes cuando aplica
- [ ] Instrucciones de desarrollo reproducibles

---

## 19. Checklist de revisión de pull request

### Intención

- [ ] El cambio tiene un objetivo claro
- [ ] El alcance coincide con el objetivo
- [ ] No mezcla refactors no relacionados

### Corrección

- [ ] Maneja límites y estados alternativos
- [ ] Conserva invariantes
- [ ] Errores tienen semántica útil
- [ ] Concurrencia e idempotencia fueron consideradas

### Seguridad

- [ ] No confía en datos del cliente
- [ ] Consultas están parametrizadas
- [ ] Autorización ocurre cerca del recurso
- [ ] No expone secretos o campos internos
- [ ] Nuevas dependencias y permisos fueron revisados

### Mantenibilidad

- [ ] La abstracción reduce complejidad real
- [ ] Los nombres explican intención
- [ ] El código puede eliminarse o reemplazarse
- [ ] La documentación evita divergir

### Evidencia

- [ ] Pruebas representan el riesgo
- [ ] CI pasó
- [ ] Se revisó el artefacto o UI cuando aplica
- [ ] Métricas o perfiles sostienen afirmaciones de rendimiento

---

## 20. Checklist de publicación del libro o documentación

- [ ] Índice refleja archivos reales
- [ ] Numeración y títulos son consistentes
- [ ] Enlaces internos resuelven
- [ ] Referencias externas fueron comprobadas
- [ ] Estados del ecosistema tienen fecha
- [ ] Borradores no se presentan como estándares finales
- [ ] Código conceptual está identificado
- [ ] Ejemplos de seguridad no parecen listos para producción sin advertencia
- [ ] Ortografía y signos del español fueron revisados
- [ ] Tablas y código se leen en viewport estrecho
- [ ] Imágenes tienen propósito y texto alternativo
- [ ] La versión web compila sin errores
- [ ] Existe un commit o artefacto identificable
- [ ] El contenido pendiente está declarado
