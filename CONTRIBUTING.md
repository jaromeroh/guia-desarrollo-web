# Guía de Contribución

## Estructura de Capítulos

Cada capítulo debe seguir esta estructura:

```markdown
# [Número]. Título del Capítulo

> Frase o pregunta que capture la esencia del capítulo

## Objetivos de Aprendizaje

Al finalizar este capítulo, serás capaz de:
- Objetivo 1
- Objetivo 2
- Objetivo 3

---

## Contenido del capítulo

[Desarrollo del contenido]

### Secciones con ejemplos

📖 **Concepto**: Para explicaciones teóricas agnósticas a tecnología

🛠️ **Práctica**: Para implementaciones concretas
```[lenguaje]
// código de ejemplo
```

⚠️ **Advertencia**: Para errores comunes
> Texto de advertencia

💡 **Insight**: Para tips avanzados
> Texto del insight

---

## Resumen

- Punto clave 1
- Punto clave 2
- Punto clave 3

## Ejercicios

1. Ejercicio básico
2. Ejercicio intermedio
3. Desafío avanzado

## Referencias

- [Enlace 1](url)
- [Enlace 2](url)

---

**Siguiente**: [Capítulo X](enlace) | **Anterior**: [Capítulo Y](enlace)
```

## Convenciones de Escritura

### Idioma
- Texto en **español**
- Código y variables en **inglés**
- Comentarios en código pueden ser en español

### Tono
- Segunda persona plural (tú/ustedes)
- Didáctico pero no condescendiente
- Práctico: siempre conectar teoría con aplicación

### Código
- Ejemplos completos y funcionales cuando sea posible
- Indicar el lenguaje en cada bloque de código
- Evitar código demasiado largo (máximo ~50 líneas por bloque)
- Usar comentarios para explicar partes no obvias

### Diagramas
- Usar Mermaid para diagramas simples (se renderizan en GitHub)
- Imágenes en `/assets/images/` con nombres descriptivos
- Diagramas en `/assets/diagrams/` (fuentes editables)

## Commits

Formato: `tipo(alcance): descripción`

Tipos:
- `feat`: Nuevo contenido
- `fix`: Corrección de errores
- `docs`: Mejoras de documentación
- `refactor`: Reorganización sin cambio de contenido
- `style`: Formato, typos

Ejemplos:
- `feat(cap-07): añadir sección sobre versionado de APIs`
- `fix(cap-12): corregir ejemplo de JWT`
- `docs(readme): actualizar índice`
