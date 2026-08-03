# Apéndice B. Herramientas Recomendadas

> Una herramienta es recomendable cuando reduce un riesgo o un coste concreto y
> el equipo puede entenderla, actualizarla y reemplazarla.

Este apéndice no es un ranking. Presenta categorías, opciones mantenidas y
criterios para elegir. Los nombres cambian más rápido que los fundamentos.

> **Estado del ecosistema — verificado el 31 de julio de 2026.**
> Los enlaces y proyectos se comprobaron en este corte editorial. Antes de
> adoptar una herramienta revisa versiones soportadas, licencia, changelog,
> modelo de seguridad y actividad de mantenimiento.

---

## Antes de agregar una herramienta

Responde:

1. ¿Qué problema medible resuelve?
2. ¿Ya existe una capacidad equivalente en el runtime, navegador o plataforma?
3. ¿Qué permisos, datos y credenciales necesita?
4. ¿Qué entra al build o al runtime de producción?
5. ¿Cómo se actualiza y elimina?
6. ¿Qué formato abierto o exportable produce?
7. ¿Cómo se comporta sin red o sin el proveedor?
8. ¿Quién será responsable de mantenerla?

Prefiere una herramienta que:

- funciona en CI sin interfaz gráfica;
- tiene configuración versionable;
- produce resultados legibles por personas y máquinas;
- permite fijar versiones;
- documenta cambios incompatibles;
- respeta salida y códigos de error;
- puede probarse en un repositorio pequeño;
- no requiere más privilegios de los necesarios.

---

## Navegador y plataforma web

### Herramientas de desarrollo del navegador

Chrome, Firefox y Safari incluyen DevTools. Son la primera opción para:

- inspeccionar DOM y árbol de accesibilidad;
- entender cascada y layout;
- observar requests, caché y cookies;
- perfilar JavaScript, rendering y memoria;
- simular condiciones de red y dispositivo;
- depurar service workers y almacenamiento.

Aprende primero las capacidades comunes. Los nombres de paneles pueden cambiar.

### Línea de comandos para HTTP

**curl** permite reproducir requests sin depender de una UI:

```bash
curl --fail-with-body \
  --request GET \
  --header "Accept: application/json" \
  https://example.test/api/health
```

Ventajas:

- disponible en muchos ambientes;
- automatizable;
- muestra headers y TLS;
- útil en runbooks.

Riesgo: el historial del shell puede conservar tokens. Usa variables seguras,
archivos temporales protegidos o mecanismos del entorno; no pegues credenciales
reales en documentación.

### Clientes de API

Una UI puede ayudar a explorar contratos. Evalúa:

- colecciones versionables en texto;
- variables por ambiente;
- importación y exportación OpenAPI;
- ejecución en CI;
- gestión de secretos;
- colaboración sin depender de una cuenta personal.

Opciones conocidas incluyen Bruno, Insomnia y Postman. El libro no requiere una:
un archivo HTTP, curl y pruebas automatizadas pueden ser suficientes.

---

## Editor, IDE y lenguaje

### Lenguaje y protocolo antes que plugin

Prefiere herramientas que integren:

- Language Server Protocol;
- formatter;
- linter;
- type checker;
- depurador;
- búsqueda y navegación;
- tareas reproducibles del proyecto.

El editor debe ejecutar los mismos comandos que CI. Una corrección exclusiva del
IDE crea dos sistemas de verdad.

### Opciones

| Entorno | Fortaleza | Consideración |
|---------|-----------|---------------|
| Visual Studio Code | Ecosistema amplio y LSP | Revisar permisos de extensiones |
| IDEs de JetBrains | Análisis e integración profunda | Licencia y consumo de recursos |
| Neovim | Composición y automatización | Mayor inversión de configuración |
| Editores ligeros | Arranque y foco | Algunas capacidades requieren integración |

No sincronices automáticamente secretos, historiales sensibles ni archivos de
producción mediante extensiones no evaluadas.

### Formato y lint

Elige una configuración por repositorio y ejecútala en CI:

- JavaScript/TypeScript: formatter y linter compatibles con el stack;
- Python: Ruff u otras herramientas mantenidas, más un type checker cuando
  aporte valor;
- Go: `gofmt`, `go vet` y analizadores del ecosistema.

No debatas estilo manualmente si una regla automática puede resolverlo. No
conviertas el linter en un sustituto de diseño.

---

## Control de versiones y colaboración

### Git

Git es la base para historial, ramas y colaboración distribuida. Conoce:

- commit y parent;
- branch y merge;
- diff;
- rebase;
- tags;
- remotes;
- recuperación con reflog.

Una interfaz gráfica ayuda, pero el modelo mental evita pérdida de trabajo.

### Hosting

GitHub, GitLab y otros proveedores añaden:

- pull/merge requests;
- permisos;
- revisiones;
- CI/CD;
- releases;
- registro de paquetes;
- políticas de rama.

Evalúa identidad empresarial, exportación, runners, auditoría, residencia y
coste. El repositorio local debe seguir siendo clonable y construible.

### Convenciones mínimas

- commits pequeños y explicables;
- branches breves;
- revisión basada en riesgos;
- checks requeridos;
- CODEOWNERS donde exista ownership real;
- tags o releases trazables a artefactos;
- secretos fuera del repositorio.

---

## Dependencias y runtimes

### JavaScript y Node.js

- **npm** acompaña Node.js y usa `package-lock.json`.
- **pnpm** optimiza almacenamiento y ofrece workspaces.
- **Yarn** mantiene su propio modelo y versiones.

Elige uno por repositorio y conserva su lockfile. No alternes package managers
durante un build.

Comprueba:

```text
runtime soportado
package manager fijado
lockfile sin cambios inesperados
scripts revisados
dependencias directas justificadas
actualizaciones automatizadas con pruebas
```

### Python

Un proyecto moderno necesita:

- versión de Python declarada;
- ambiente aislado;
- metadata en `pyproject.toml`;
- lock reproducible;
- separación entre dependencias de runtime y desarrollo.

`uv` integra resolución, lock, ambientes y ejecución; pip sigue siendo una
interfaz fundamental del ecosistema. Elige según compatibilidad del equipo y del
despliegue.

### Go

El toolchain incluye módulos, formatter, tests, benchmarks, fuzzing y análisis
básico:

```text
go mod tidy
go test ./...
go test -race ./...
go vet ./...
```

`go.sum` verifica contenido de módulos; no implica que una dependencia sea
segura o adecuada.

### Actualización automatizada

Dependabot y Renovate pueden proponer cambios. Configura:

- frecuencia;
- agrupación prudente;
- límites de PRs;
- changelog visible;
- pruebas completas;
- revisión especial para majors y cadena de suministro.

Automatizar la apertura no autoriza el merge.

---

## Bases de datos

### Cliente nativo primero

Aprende al menos un cliente oficial:

- PostgreSQL: `psql`;
- SQLite: `sqlite3`;
- Redis: `redis-cli` o equivalente mantenido.

Permiten ejecutar diagnósticos desde ambientes mínimos y seguir documentación
primaria.

### Interfaces gráficas

pgAdmin, DBeaver y DataGrip facilitan:

- explorar esquemas;
- revisar planes;
- editar datos;
- comparar ambientes.

Configura conexiones de solo lectura para diagnóstico cuando sea posible. Una
tabla editable en una UI no convierte una mutación de producción en una acción
segura.

### Migraciones

Usa la herramienta nativa del stack o una solución compatible:

- Prisma Migrate, Drizzle Kit u otra para su ORM;
- Alembic con SQLAlchemy;
- Flyway, Liquibase o migradores basados en SQL;
- herramientas específicas del proyecto Go.

Requisitos:

- revisiones ordenadas;
- SQL inspeccionable;
- estado actual consultable;
- ejecución no interactiva;
- migración incremental;
- prueba desde la versión anterior.

Nunca uses “reset” como solución ordinaria de una migración fallida.

---

## Pruebas

### Matriz por riesgo

| Riesgo | Herramienta o nivel |
|--------|---------------------|
| Regla pura | Runner del lenguaje |
| Integración de módulo | Test framework + dependencias controladas |
| Semántica de base | Base real aislada |
| Contrato HTTP | Cliente HTTP y esquema |
| Recorrido de usuario | Navegador real |
| Rendimiento | Generador de carga y telemetría |
| Accesibilidad | Automatización + revisión manual |
| Seguridad | Análisis + pruebas autorizadas |

### JavaScript y TypeScript

- Vitest o Jest para unidades e integración;
- Testing Library para comportamiento de UI;
- Playwright para navegador y recorridos;
- el runner propio del runtime cuando cubra la necesidad.

### Python

- pytest para unidades, fixtures e integración;
- HTTPX/TestClient para ASGI;
- Hypothesis para pruebas basadas en propiedades.

### Go

- paquete `testing`;
- `httptest`;
- fuzzing;
- race detector;
- benchmarks.

No elijas por popularidad. Verifica soporte del framework, ESM, async,
paralelismo, reportes y depuración.

---

## Accesibilidad

Automatización útil:

- axe-core;
- reglas de accesibilidad de Lighthouse;
- Accessibility Insights;
- linters de templates o JSX.

Pruebas manuales:

- teclado;
- zoom y reflow;
- contraste y estados;
- VoiceOver en plataformas Apple;
- NVDA en Windows;
- lectores y controles que use tu población.

Una herramienta automática encuentra solo parte de los problemas. No puede
decidir si un texto alternativo comunica el propósito ni si el recorrido es
comprensible.

---

## Rendimiento

### Navegador

- panel Performance y Network de DevTools;
- Lighthouse para auditoría de laboratorio;
- WebPageTest para condiciones y ubicaciones controladas;
- APIs de Performance y Web Vitals para datos reales.

### Backend y carga

- perfiles del runtime;
- OpenTelemetry para recorridos;
- k6, Locust u otra herramienta de carga automatizable;
- métricas de base y pools;
- pruebas con datos y mix representativos.

Una puntuación de laboratorio no es un SLO. Conserva:

- escenario;
- versión;
- ambiente;
- distribución de latencia;
- errores;
- saturación;
- comparación con baseline.

---

## Seguridad y cadena de suministro

### Dependencias

- `npm audit`, `pip-audit` y `govulncheck` aportan señales específicas del
  ecosistema;
- OSV-Scanner consulta vulnerabilidades abiertas;
- Dependabot o Renovate mantienen propuestas de actualización.

Un CVE no determina prioridad por sí solo. Comprueba alcanzabilidad, exposición,
impacto y mitigaciones.

### Código y aplicación

- Semgrep u otros analizadores estáticos;
- OWASP ZAP para pruebas dinámicas autorizadas;
- linters de secretos;
- threat modeling y revisión manual.

Nunca apuntes un scanner a un sistema fuera del alcance acordado. Las pruebas
activas pueden alterar datos o disponibilidad.

### Artefactos

- Trivy para imágenes, filesystem y configuraciones;
- Syft para generar SBOM;
- cosign para firmas y atestaciones;
- políticas del registry y del pipeline.

La firma demuestra una relación criptográfica con una identidad o clave; no
demuestra que el software sea correcto.

---

## Observabilidad

### Estándar de instrumentación

OpenTelemetry ofrece APIs, SDKs y protocolo para trazas, métricas y logs según
madurez por lenguaje. Un Collector puede recibir, procesar y exportar señales.

### Almacenamiento y visualización

Prometheus, Grafana, Loki, Tempo y Jaeger son componentes abiertos comunes.
También existen plataformas administradas.

Evalúa:

- volumen y retención;
- cardinalidad;
- residencia y privacidad;
- lenguaje de consulta;
- alertas;
- correlación;
- exportación;
- coste predecible;
- operación del propio sistema de observabilidad.

Empieza por preguntas y SLOs, no por instalar todos los componentes.

---

## Contenedores, infraestructura y CI/CD

### Entorno local

- Docker Engine/Desktop o Podman para contenedores;
- Compose para varias dependencias locales;
- dev containers cuando mejoren reproducibilidad sin ocultar el runtime.

No necesitas Kubernetes para simular producción. Necesitas reproducir las
dependencias y contratos relevantes.

### Infraestructura como código

Terraform/OpenTofu, Pulumi y herramientas del proveedor describen recursos.
Elige considerando:

- estado y locking;
- revisión del plan;
- módulos;
- importación de recursos existentes;
- política;
- secretos;
- estrategia de actualización;
- capacidad de recuperación.

### Pipelines

GitHub Actions, GitLab CI, Buildkite y otros sistemas pueden ejecutar el mismo
contrato:

> checkout → dependencias → análisis → pruebas → build → escaneo → publicación
> → despliegue → verificación

Usa OIDC o identidad de workload para evitar credenciales largas cuando la
plataforma lo permita.

---

## Herramientas de IA para desarrollo

No existe una recomendación universal de modelo o cliente. Evalúa el sistema
completo:

- calidad en tu lenguaje y repositorio;
- tamaño y selección de contexto;
- permisos y aislamiento;
- herramientas disponibles;
- política de retención;
- residencia de datos;
- coste y límites;
- capacidad de revisar diffs;
- ejecución de pruebas;
- logs y aprobaciones;
- soporte para instrucciones versionadas.

### Configuración segura

1. empieza con acceso de lectura;
2. habilita escritura solo en el workspace;
3. conserva aprobación para red, secretos y producción;
4. excluye archivos sensibles;
5. entrega comandos de verificación;
6. limita tareas y criterios de aceptación;
7. revisa el diff;
8. mide defectos y retrabajo.

Una herramienta que escribe más código no necesariamente aumenta throughput del
equipo. Mide tiempo hasta cambio correcto y operable.

---

## Kit mínimo por etapa

### Aprendizaje

- navegador y DevTools;
- editor con LSP;
- Git;
- runtime y package manager;
- curl;
- base local;
- runner de tests.

### Producto pequeño

Añade:

- CI;
- migraciones;
- navegador E2E;
- escaneo de dependencias;
- logs estructurados;
- métricas básicas;
- backups probados.

### Sistema crítico

Añade según riesgo:

- SLOs y alertas;
- trazas;
- gestión de secretos;
- SBOM y firma;
- ambientes y promoción;
- pruebas de carga;
- threat model;
- runbooks e incidentes;
- controles de acceso y auditoría.

No instales la tercera etapa el primer día. Tampoco esperes al incidente para
descubrir que no puedes restaurar datos.

---

## Plantilla de evaluación

```text
Herramienta:
Problema:
Alternativa actual:
Responsable:

Evidencia de mantenimiento:
Licencia:
Datos que procesa:
Permisos:
Dependencias de runtime:
Formato de configuración y salida:
Integración con CI:
Observabilidad:
Coste inicial y recurrente:
Riesgo de lock-in:
Plan de actualización:
Plan de eliminación:

Experimento:
Métrica de éxito:
Fecha de decisión:
Fecha de revisión:
```

---

## Referencias

- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [Firefox Developer Tools](https://firefox-source-docs.mozilla.org/devtools-user/)
- [WebKit Web Inspector](https://webkit.org/web-inspector/)
- [curl Documentation](https://curl.se/docs/)
- [Git Documentation](https://git-scm.com/doc)
- [npm Documentation](https://docs.npmjs.com/)
- [pnpm Documentation](https://pnpm.io/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Go Toolchains](https://go.dev/doc/toolchain)
- [PostgreSQL — psql](https://www.postgresql.org/docs/current/app-psql.html)
- [Playwright](https://playwright.dev/docs/intro)
- [pytest](https://docs.pytest.org/)
- [Go — Testing](https://go.dev/doc/tutorial/add-a-test)
- [axe-core](https://github.com/dequelabs/axe-core)
- [Accessibility Insights for Web — repositorio oficial](https://github.com/microsoft/accessibility-insights-web)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/)
- [WebPageTest — repositorio oficial](https://github.com/catchpoint/WebPageTest)
- [k6 Documentation](https://grafana.com/docs/k6/latest/)
- [OWASP ZAP](https://www.zaproxy.org/docs/)
- [OSV-Scanner](https://google.github.io/osv-scanner/)
- [govulncheck](https://go.dev/doc/tutorial/govulncheck)
- [Trivy](https://trivy.dev/docs/)
- [Syft](https://github.com/anchore/syft)
- [Sigstore cosign](https://docs.sigstore.dev/cosign/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Docker Documentation](https://docs.docker.com/)
- [Podman Documentation](https://podman.io/docs)
- [OpenTofu Documentation](https://opentofu.org/docs/)
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [GitHub Actions](https://docs.github.com/actions)
- [GitLab CI/CD](https://docs.gitlab.com/ci/)
