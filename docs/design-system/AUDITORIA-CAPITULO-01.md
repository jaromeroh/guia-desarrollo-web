# Auditoría visual del capítulo 1

> Capítulo: *Anatomía de una Aplicación Web Moderna*. Corte: 31 de julio de
> 2026. Esta auditoría aplica el [sistema visual aprobado](./SISTEMA-VISUAL.md).

## Resultado

El capítulo dispone de 15 SVG heredados:

- 12 se publican en el capítulo.
- 3 son copias visuales de antiguos bloques ASCII y no tienen referencias.
- Los 15 son XML válido.
- Ninguno contiene `role="img"`, `<title>` ni `<desc>`.
- Los 12 publicados tienen texto alternativo en Markdown, pero varios textos
  alternativos solo repiten el título visible.
- El gris `#9CA3AF` utilizado en varios recursos ofrece aproximadamente 2,54:1
  sobre blanco; no alcanza 3:1 para componentes gráficos ni 4,5:1 para texto
  normal.
- La variedad de proporciones —desde 538×216 hasta 710×1880— hace que el texto
  se reduzca de forma desigual en GitBook y sea ilegible en móvil.

El problema no es únicamente estético. Algunos SVG convierten una configuración
frecuente en una definición:

- Un monolito no exige un único repositorio ni una única base de datos.
- Separar servicios no garantiza aislamiento de fallos.
- FaaS no equivale siempre a «nada corriendo» ni a coste cero.
- «Tradicional» y «serverless» no forman un binario suficiente para describir
  procesos, contenedores administrados, funciones e isolates.
- El DOM no se pinta directamente: el navegador también construye el CSSOM,
  calcula estilos, realiza layout y pinta. Esta secuencia coincide con la
  descripción del [camino crítico de renderizado de MDN](https://developer.mozilla.org/docs/Web/Performance/Critical_rendering_path).

## Decisión por recurso

| Recurso heredado | Estado | Tratamiento |
|---|---|---|
| `02-anatomia-aplicacion_diagram_1.svg` | Sin referencia | Conservar como historial; no publicar |
| `02-anatomia-aplicacion_diagram_2.svg` | Sin referencia | Conservar como historial; devolver la comparación a texto semántico |
| `02-anatomia-aplicacion_diagram_3.svg` | Sin referencia | Conservar como historial; reemplazado por el nuevo flujo de renderizado |
| `02-arquitectura-internet.svg` | Publicado | Reemplazar por un mapa de responsabilidades y fronteras |
| `02-html-a-dom.svg` | Publicado | Reemplazar por HTML + CSS → DOM + CSSOM → layout → pintura |
| `02-http-comunicacion.svg` | Publicado | Reemplazar con mensajes HTTP mínimos y semántica explícita |
| `02-capas-aplicacion.svg` | Publicado | Simplificar; retirar nombres de frameworks y productos |
| `02-decisiones-arquitectura.svg` | Publicado | Consolidar con matriz y modelos de ejecución |
| `02-monolito.svg` | Publicado | Retirar; la definición incrustada es demasiado rígida |
| `02-microservicios.svg` | Publicado | Retirar; muestra una variante como si fuera obligatoria |
| `02-servidor-tradicional.svg` | Publicado | Retirar; sustituir el eje por procesos y contenedores de larga duración |
| `02-serverless.svg` | Publicado | Retirar; contiene afirmaciones absolutas de coste y ciclo de vida |
| `02-matriz-arquitectura.svg` | Publicado | Rediseñar sin marcas ni asociaciones dependientes de una plataforma |
| `02-guia-decision.svg` | Publicado | Retirar; conservar criterios como texto evaluable, no como receta |
| `02-viaje-peticion.svg` | Publicado | Reemplazar por una secuencia breve con caminos opcionales explícitos |

## Conjunto final

Los 12 SVG publicados se consolidaron en seis funciones pedagógicas:

1. Mapa de una aplicación web y sus fronteras.
2. De HTML y CSS a píxeles.
3. Intercambio HTTP entre cliente y servidor.
4. Capas y dirección de dependencias.
5. Dos decisiones arquitectónicas independientes.
6. Viaje de una petición y su respuesta.

El mapa, la matriz arquitectónica y el viaje de la petición tienen composición
de escritorio y móvil. Los nueve SVG finales incluyen `role="img"`, `<title>` y
`<desc>`. El texto cercano conserva la explicación completa para que ninguna
relación dependa exclusivamente de la imagen.

Los recursos heredados permanecen en `.gitbook/assets` como historial, pero el
capítulo ya no los referencia.

## Validación local

- Los nueve SVG son XML válido.
- HonKit compila las 37 páginas sin errores.
- En 1280 px se cargan las tres composiciones de escritorio.
- En 759 px el mapa conserva su composición horizontal sin colisiones y el
  viaje de la petición cambia a la secuencia vertical.
- En 420 px se cargan las tres variantes móviles y no existe desbordamiento
  horizontal.
- Todos los recursos terminan de cargar y la consola no registra advertencias
  ni errores en la página del capítulo.

### Correcciones posteriores a la revisión visual

- La frontera de confianza del mapa ahora se lee horizontalmente.
- Las cuatro columnas del mapa comparten geometría y sus textos permanecen
  dentro de cada caja.
- La respuesta del mapa circula por un carril separado, sin cruzar etiquetas.
- El flujo de renderizado reserva margen debajo de «Pintura y composición».
- La flecha de respuesta HTTP se dibuja en dos segmentos visibles alrededor del
  bloque del mensaje.
- La secuencia horizontal del viaje se conserva para escritorio amplio; hasta
  820 px se utiliza la composición vertical para mantener el tamaño del texto.

## Fuentes de contraste conceptual

- [MDN: Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview): HTTP como intercambio de solicitudes y respuestas entre cliente, intermediarios y servidor.
- [MDN: Critical rendering path](https://developer.mozilla.org/docs/Web/Performance/Critical_rendering_path): DOM, CSSOM, árbol de renderizado, layout y pintura.
- [AWS: Fargate or Lambda?](https://docs.aws.amazon.com/pdfs/decision-guides/latest/fargate-or-lambda/fargate-or-lambda.pdf): ejecución continua y ejecución activada por eventos tienen límites y modelos de coste distintos; no se reducen a «encendido» frente a «apagado».
