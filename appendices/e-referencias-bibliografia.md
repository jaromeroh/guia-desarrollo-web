# Apéndice E. Referencias y Bibliografía

Este apéndice reúne las fuentes centrales del libro. Cada capítulo conserva sus
referencias específicas cerca de las afirmaciones que sostienen. La
[auditoría fuente por fuente](../docs/AUDITORIA-REFERENCIAS.md) registra todos
los enlaces, su clasificación y la fecha de comprobación.

> **Corte editorial: 31 de julio de 2026.**
> Un enlace disponible no demuestra que toda interpretación sea correcta.
> Estándares vivos, borradores y documentación de herramientas deben revisarse
> en la versión correspondiente al proyecto.

---

## Cómo se priorizaron las fuentes

Orden general:

1. especificación normativa o estándar;
2. documentación mantenida por el proyecto;
3. publicación original de un concepto;
4. libro técnico con contexto y edición identificada;
5. artículo secundario para perspectiva, no como única base normativa.

Los blogs y benchmarks de proveedores pueden ser útiles para comprender una
implementación. No deben convertir una característica del proveedor en una ley
universal.

---

## Formato recomendado de cita

### Estándar o RFC

```text
Entidad. (Año). Título, versión o número.
URL. Consultado el <fecha>.
```

### Documentación versionada

```text
Proyecto. Título de la página. Documentación de <versión>.
URL. Consultado el <fecha>.
```

### Libro

```text
Apellido, Inicial. (Año). Título (edición). Editorial.
```

### Página cambiante

Registra además:

- versión;
- fecha de acceso;
- commit o snapshot si es crítico;
- fragmento interpretado;
- decisión que dependió de la fuente.

---

## Plataforma web

- [WHATWG — HTML Living Standard](https://html.spec.whatwg.org/)
- [WHATWG — DOM Standard](https://dom.spec.whatwg.org/)
- [WHATWG — URL Standard](https://url.spec.whatwg.org/)
- [WHATWG — Fetch Standard](https://fetch.spec.whatwg.org/)
- [W3C — CSS Snapshot](https://www.w3.org/TR/css/)
- [ECMA International — ECMAScript Language Specification](https://tc39.es/ecma262/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [IETF RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [IETF RFC 9111 — HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111)
- [IETF RFC 9112 — HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112)
- [IETF RFC 9113 — HTTP/2](https://www.rfc-editor.org/rfc/rfc9113)
- [IETF RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114)
- [IETF RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [W3C TAG — Web Platform Design Principles](https://www.w3.org/TR/design-principles/)

### Lecturas

- Flanagan, D. (2020). *JavaScript: The Definitive Guide* (7.ª ed.). O'Reilly.
- Simpson, K. (2015–2020). *You Don't Know JS Yet*. Independently published.

---

## Accesibilidad y experiencia

- [W3C — Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/)
- [W3C — WAI-ARIA](https://www.w3.org/TR/wai-aria/)
- [WAI — ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WAI — Tutorials](https://www.w3.org/WAI/tutorials/)
- [W3C — Accessible Name and Description Computation](https://www.w3.org/TR/accname-1.2/)
- [W3C — Accessibility Guidelines 3.0, Working Draft](https://www.w3.org/TR/wcag-3.0/)
- [Nielsen Norman Group — Ten Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [WebAIM — Screen Reader User Survey](https://webaim.org/projects/screenreadersurvey/)

### Lecturas

- Krug, S. (2014). *Don't Make Me Think, Revisited* (3.ª ed.). New Riders.
- Holmes, K. (2018). *Mismatch: How Inclusion Shapes Design*. MIT Press.

---

## Producto, diseño y arquitectura

- [C4 Model](https://c4model.com/)
- [Architecture Decision Records](https://adr.github.io/)
- [Martin Fowler — Patterns of Enterprise Application Architecture](https://martinfowler.com/books/eaa.html)
- [Martin Fowler — Monolith First](https://martinfowler.com/bliki/MonolithFirst.html)
- [Alistair Cockburn — Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [12-Factor App](https://12factor.net/)

### Lecturas

- Evans, E. (2003). *Domain-Driven Design*. Addison-Wesley.
- Vernon, V. (2013). *Implementing Domain-Driven Design*. Addison-Wesley.
- Ford, N., Richards, M., Sadalage, P. y Dehghani, Z. (2021).
  *Software Architecture: The Hard Parts*. O'Reilly.
- Skelton, M. y Pais, M. (2019). *Team Topologies*. IT Revolution.
- Forsgren, N., Humble, J. y Kim, G. (2018). *Accelerate*. IT Revolution.

---

## APIs y contratos

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [GraphQL Specification](https://spec.graphql.org/)
- [JSON Schema](https://json-schema.org/specification)
- [IETF RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)
- [IETF RFC 9745 — Deprecation HTTP Response Header](https://www.rfc-editor.org/rfc/rfc9745)
- [IETF RFC 8594 — Sunset HTTP Header](https://www.rfc-editor.org/rfc/rfc8594)
- [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/latest)

### Lecturas

- Richardson, L. y Ruby, S. (2007). *RESTful Web Services*. O'Reilly.
- Masse, M. (2011). *REST API Design Rulebook*. O'Reilly.

---

## Datos, persistencia y sistemas distribuidos

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Redis Documentation](https://redis.io/docs/latest/)
- [IETF RFC 3339 — Date and Time on the Internet](https://www.rfc-editor.org/rfc/rfc3339)
- [Unicode CLDR](https://cldr.unicode.org/)
- [IANA Time Zone Database](https://www.iana.org/time-zones)

### Publicaciones y libros

- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly.
- Gray, J. y Reuter, A. (1992). *Transaction Processing*. Morgan Kaufmann.
- Garcia-Molina, H., Ullman, J. y Widom, J. (2008).
  *Database Systems: The Complete Book* (2.ª ed.). Pearson.
- Bernstein, P. y Newcomer, E. (2009).
  *Principles of Transaction Processing* (2.ª ed.). Morgan Kaufmann.

---

## Identidad y seguridad

- [OWASP Top 10:2025](https://owasp.org/Top10/2025/)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [IETF RFC 9700 — Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700)
- [OAuth 2.1 Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [W3C — Web Authentication Level 3](https://www.w3.org/TR/webauthn-3/)
- [FIDO Alliance — Passkey Central](https://www.fidoalliance.org/passkeys/)
- [IETF RFC 7519 — JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519)
- [IETF RFC 9106 — Argon2](https://www.rfc-editor.org/rfc/rfc9106)
- [CWE](https://cwe.mitre.org/)
- [MITRE ATT&CK](https://attack.mitre.org/)

### Lecturas

- Ross Anderson. (2020). *Security Engineering* (3.ª ed.). Wiley.
- Shostack, A. (2014). *Threat Modeling: Designing for Security*. Wiley.

---

## Testing y entrega

- [Testing Library — Guiding Principles](https://testing-library.com/docs/guiding-principles/)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [pytest Documentation](https://docs.pytest.org/)
- [Go — Testing](https://go.dev/doc/tutorial/add-a-test)
- [Trunk Based Development](https://trunkbaseddevelopment.com/)
- [OpenSSF Scorecard](https://securityscorecards.dev/)
- [SLSA](https://slsa.dev/)
- [OCI Image Specification](https://github.com/opencontainers/image-spec)

### Lecturas

- Meszaros, G. (2007). *xUnit Test Patterns*. Addison-Wesley.
- Humble, J. y Farley, D. (2010). *Continuous Delivery*. Addison-Wesley.
- Crispin, L. y Gregory, J. (2009). *Agile Testing*. Addison-Wesley.

---

## Fiabilidad, rendimiento y observabilidad

- [Google SRE Books](https://sre.google/books/)
- [OpenTelemetry Specification](https://opentelemetry.io/docs/specs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [W3C — Resource Timing](https://www.w3.org/TR/resource-timing/)
- [W3C — Server Timing](https://www.w3.org/TR/server-timing/)
- [web.dev — Web Vitals](https://web.dev/articles/vitals)
- [IETF RFC 9211 — The Cache-Status HTTP Response Header](https://www.rfc-editor.org/rfc/rfc9211)

### Lecturas

- Beyer, B., Jones, C., Petoff, J. y Murphy, N. R. (eds.). (2016).
  *Site Reliability Engineering*. O'Reilly.
- Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K. y Thorne, S. (eds.).
  (2018). *The Site Reliability Workbook*. O'Reilly.
- Majors, C., Fong-Jones, L. y Miranda, G. (2022).
  *Observability Engineering*. O'Reilly.
- Gregg, B. (2020). *Systems Performance* (2.ª ed.). Pearson.

---

## Stacks usados en el libro

### JavaScript y Next.js

- [Node.js Documentation](https://nodejs.org/docs/latest/api/)
- [Node.js Release Schedule](https://nodejs.org/en/about/previous-releases)
- [React Documentation](https://react.dev/)
- [Next.js App Router](https://nextjs.org/docs/app)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

### Python y FastAPI

- [Python 3 Documentation](https://docs.python.org/3/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)

### Go

- [Go Documentation](https://go.dev/doc/)
- [Go Packages](https://pkg.go.dev/)
- [Go — Accessing Relational Databases](https://go.dev/doc/database/)
- [Go — Race Detector](https://go.dev/doc/articles/race_detector)
- [Go — Vulnerability Management](https://go.dev/security/vuln/)

La documentación de una versión “latest” debe contrastarse con la versión
bloqueada en el proyecto.

---

## IA, agentes y protocolos

- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [OpenAI — Harness Engineering](https://openai.com/index/harness-engineering/)
- [Anthropic — Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [Linux Foundation — Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation?hs_amp=true)

### Publicaciones

- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS.
- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for
  Knowledge-Intensive NLP Tasks*. NeurIPS.

Las capacidades de modelos y productos cambian rápidamente. Conserva fecha,
modelo, configuración, herramientas y dataset al reportar una evaluación.

---

## Horizontes de la plataforma

- [W3C — WebAssembly Core Specification](https://www.w3.org/TR/wasm-core/)
- [W3C — WebGPU](https://www.w3.org/TR/webgpu/)
- [WASI — Releases](https://wasi.dev/releases)
- [WebAssembly Component Model](https://component-model.bytecodealliance.org/)
- [Ecma International — TC55: Web-interoperable server runtimes](https://ecma-international.org/technical-committees/tc55/)
- [W3C Standards and Drafts](https://www.w3.org/TR/)
- [IETF Datatracker](https://datatracker.ietf.org/)

Consulta el estado del documento. Candidate Recommendation, Working Draft,
Internet-Draft y propuesta estable de un proyecto no significan lo mismo.

---

## Mantenimiento de esta bibliografía

En cada edición:

1. ejecutar la auditoría automática de enlaces;
2. revisar manualmente respuestas bloqueadas o redirigidas;
3. comprobar versión y estado normativo;
4. sustituir documentación archivada;
5. retirar estadísticas sin metodología;
6. actualizar libros solo cuando una nueva edición cambie el contenido relevante;
7. conservar fecha de corte;
8. registrar fuentes añadidas o retiradas en el historial editorial.

La bibliografía no debe crecer por prestigio. Cada fuente debe sostener una idea
del libro o ayudar al lector a profundizar. El resultado de la comprobación
automática se conserva en la
[auditoría de referencias del manuscrito](../docs/AUDITORIA-REFERENCIAS.md).
