# Plan editorial

El avance de la revisión se registra en el
[checklist de auditoría editorial](./CHECKLIST-AUDITORIA-EDITORIAL.md).

## Propósito del libro

*El Arte del Desarrollo Web Moderno* enseñará a diseñar, construir, operar y
evolucionar aplicaciones web en un entorno donde la inteligencia artificial
participa activamente en la producción de software.

El libro no partirá de la premisa de que los fundamentos han perdido valor. Al
contrario: cuando producir código es más rápido, comprender la plataforma,
evaluar decisiones y verificar resultados se vuelve más importante.

## Promesa al lector

Al terminar el libro, el lector deberá poder:

1. Explicar cómo funciona una aplicación web desde el navegador hasta la base
   de datos y la infraestructura.
2. Traducir un problema real en una solución técnica proporcionada a su
   contexto.
3. Elegir tecnologías mediante trade-offs explícitos, no por popularidad.
4. Trabajar con asistentes y agentes de IA sin delegarles la responsabilidad
   sobre el resultado.
5. Verificar seguridad, accesibilidad, corrección y comportamiento en
   producción.
6. Seguir aprendiendo aunque cambien los frameworks y las herramientas.

## Arquitectura propuesta

La arquitectura y la numeración definitivas se aplicaron en julio de 2026.
El recorrido comienza en la plataforma web, antes de presentar el cambio de
paradigma provocado por la IA.

### Parte I — Fundamentos de las aplicaciones web

- Anatomía de una aplicación web.
- HTML semántico, formularios y mejora progresiva.
- CSS, layout adaptable y sistema visual.
- JavaScript, eventos y runtime del navegador.
- URL, DNS, TLS, HTTP, caché y modelo de seguridad del navegador.

### Parte II — El nuevo paradigma

- Evolución del desarrollador web.
- Pensamiento en sistemas.
- Desarrollo asistido por IA.

### Parte III — Entender y diseñar

- Entender el problema.
- Diseño de producto y experiencia de usuario.
- Arquitectura de software.
- Diseño de APIs.
- Modelado de datos.
- Planificación técnica.

### Parte IV — Construir

- Arquitectura frontend.
- Arquitectura backend.
- Autenticación y autorización.
- Comunicación en tiempo real.
- Persistencia.
- Tareas asíncronas.

### Parte V — Verificar y operar

- Testing.
- Integración y entrega continua.
- Despliegue e infraestructura.
- Observabilidad.
- Escalabilidad y rendimiento.
- Seguridad de aplicaciones web.

### Parte VI — Integrar los conocimientos

Los capítulos de stack no serán catálogos de sintaxis. Cada uno construirá un
slice vertical pequeño y completo que incluya interfaz, contrato, persistencia,
autenticación, pruebas, despliegue y observabilidad.

- Next.js y Node.js.
- Python y FastAPI.
- Go para servicios web.

Los tres capítulos implementan el mismo slice vertical de solicitudes de
soporte. Esto permite comparar fronteras de ejecución, validación, persistencia,
autorización, concurrencia, pruebas y operación sin cambiar el dominio.

### Parte VII — El futuro

La parte final separa dos escalas temporales:

- El capítulo 30 explica la capa de abstracción que ya introducen agentes,
  herramientas, contexto, memoria, permisos, evaluaciones y protocolos.
- El capítulo 31 ofrece un radar para observar tendencias sin confundir
  borradores, señales e hipótesis con hechos consolidados.

### Apéndices — Referencia operativa

Los cinco apéndices reúnen el glosario, las herramientas recomendadas, los
recursos de aprendizaje, las plantillas y listas de verificación, y la
bibliografía. Complementan el recorrido sin interrumpir la progresión de los
capítulos.

## Política de vigencia

El texto distinguirá tres clases de contenido:

### Fundamento

Principios que deberían seguir siendo útiles aunque cambien las herramientas:
HTTP, semántica, concurrencia, transacciones, acoplamiento, cohesión, pruebas,
seguridad y observabilidad.

### Práctica

Una implementación concreta que demuestra el fundamento. El lector debe poder
reemplazar la herramienta sin perder el modelo mental.

### Estado del ecosistema

Versiones, proveedores, precios, soporte de navegadores, popularidad y
capacidades de herramientas. Estas secciones indicarán una fecha de
verificación con el formato:

> **Estado del ecosistema — verificado el 31 de julio de 2026.**

Las afirmaciones volátiles deberán:

- enlazar preferentemente a documentación o especificaciones primarias;
- evitar porcentajes sin una fuente identificable y contextualizada;
- distinguir estándares publicados, borradores y propuestas;
- evitar presentar precios o límites de proveedores como propiedades
  universales;
- incluir versiones solo cuando aporten información útil.

## Contrato de los ejemplos

Todo ejemplo de código se clasificará como uno de estos dos tipos:

- **Ejemplo conceptual:** omite detalles para explicar una idea. No debe
  presentarse como código listo para producción.
- **Ejemplo ejecutable:** incluye dependencias, manejo de errores y una forma
  concreta de verificar el resultado.

Los ejemplos relacionados con autenticación, criptografía, autorización,
procesamiento de datos sensibles o despliegues destructivos deberán apoyarse en
fuentes primarias y pasar una revisión de seguridad específica.

## Estructura común de los capítulos

Cuando sea apropiado, cada capítulo tendrá:

1. Objetivos de aprendizaje.
2. Modelo mental.
3. Fundamentos.
4. Decisiones y trade-offs.
5. Ejemplo práctico.
6. Fallos y riesgos frecuentes.
7. Uso responsable de IA en ese contexto.
8. Lista de verificación.
9. Ejercicios.
10. Referencias primarias y lecturas adicionales.

## Principios para el contenido sobre IA

El libro enseñará un ciclo basado en evidencia:

> especificar → proporcionar contexto → ejecutar → observar → evaluar →
> corregir → revisar

La calidad no se atribuirá únicamente al prompt. También depende de:

- la claridad de los criterios de aceptación;
- el acceso a herramientas y documentación;
- la reproducibilidad del entorno;
- los permisos y límites de actuación;
- las pruebas y evaluaciones;
- la evidencia obtenida del sistema real;
- la revisión humana proporcional al riesgo.

El principio rector será:

> La IA puede ejecutar una parte creciente del trabajo, pero la responsabilidad
> sobre el resultado no se delega.

## Trabajo visual posterior

Los diagramas ASCII se conservarán durante la revisión textual. En una fase
posterior se inventariarán y se reemplazarán por imágenes con un sistema visual
coherente. Cada imagen deberá justificar su existencia ayudando a comprender
una relación, flujo, jerarquía o trade-off que resulte menos claro en prosa.

La revisión textual ya concluyó. El alcance, las prioridades y los recursos
existentes se registran en el
[inventario visual del manuscrito](./INVENTARIO-VISUAL.md).
