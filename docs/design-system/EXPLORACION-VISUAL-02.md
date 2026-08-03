# Exploración visual 02: tipologías y paleta editorial

## Objetivo

Comprobar que el lenguaje editorial luminoso funciona en varias familias de
diagramas y sustituir los colores asociados visualmente con productos de IA por
una paleta más cercana a un libro técnico impreso.

![Muestrario de tipologías con paleta editorial](../../assets/diagrams/explorations/muestrario-tipologias-editorial-v2.png)

## Paleta propuesta

| Token | Color | Uso |
|---|---|---|
| Tinta | `#20262E` | Texto, títulos y estructura principal |
| Azul petróleo | `#31536A` | Flujo principal, selección y elementos técnicos |
| Terracota | `#B95736` | Riesgo, excepción, identidad y transición crítica |
| Ocre | `#C59132` | Datos, decisión y estados intermedios |
| Gris cálido | `#A9A49B` | Bordes, relaciones secundarias y contexto |
| Papel | `#F2EEE6` | Fondo editorial |
| Superficie | `#FFFDFA` | Láminas y tarjetas |

La paleta evita violetas, verdes menta, neones y degradados. El color no
reemplaza las etiquetas, formas o patrones de línea.

## Tipologías representadas

### Mapa de sistema

Muestra componentes, fronteras y dependencias. Se utilizaría en anatomía de una
aplicación, arquitectura, frontend, backend, tareas asíncronas, infraestructura
y sistemas con agentes.

### Proceso

Muestra etapas, entregables y bucles. Se utilizaría en diseño de producto,
desarrollo asistido por IA, planificación, testing y CI/CD.

### Secuencia

Muestra actores, mensajes y orden temporal. Se utilizaría en HTTP,
autenticación, OAuth, comunicación en tiempo real, transacciones y colas.

### Matriz de decisión

Compara alternativas mediante dos ejes explícitos. Se utilizaría para riesgos,
trade-offs arquitectónicos, estrategias de testing y selección de tecnologías.

### Modelo de datos

Representa entidades, campos, claves y cardinalidades. Se utilizaría
principalmente en modelado de datos, persistencia, autorización basada en
relaciones y event sourcing.

### Máquina de estados

Representa estados y condiciones de transición. Se utilizaría en circuit
breaker, ciclo de vida de tokens, jobs, feature flags y estrategias de
despliegue.

## Criterio de uso

Estas tipologías comparten paleta, tipografía, radios, conectores y jerarquía,
pero conservan la notación propia de cada problema. Un modelo de datos no debe
parecer un flujo y una máquina de estados no debe representarse como una lista
de pasos.
