# Exploración visual 03: diagramas ancla

## Objetivo

Probar el sistema visual aprobado en tres diagramas de distinta naturaleza y
con contenido real del manuscrito:

1. Flujo y pensamiento en sistemas.
2. Comparación de patrones arquitectónicos.
3. Modelo lógico de datos.

Los tres utilizan el e-commerce como caso transversal.

## Pensamiento en sistemas

![El sistema vive en las conexiones](../../assets/diagrams/explorations/cap03-sistema-conexiones-v2.png)

### Función editorial

La lámina no presenta únicamente componentes. Muestra el flujo de «agregar al
carrito», los riesgos que aparecen entre componentes y el feedback que confirma
o revierte la actualización optimista de la interfaz.

Se propone para la sección «Pensando en flujos, no en cajas» del capítulo 7.

## Arquitectura de software

![Capas, Clean Architecture y Arquitectura Hexagonal](../../assets/diagrams/explorations/cap07-arquitecturas-comparadas-v3.png)

### Función editorial

La comparación conserva la notación propia de cada patrón:

- Capas como separación horizontal.
- Clean Architecture como dependencias hacia el núcleo.
- Arquitectura Hexagonal como puertos y adaptadores intercambiables.

La lámina enfatiza que no son tres arquitecturas rivales. Son distintas maneras
de razonar sobre separación, dependencias y protección del negocio.

## Modelado de datos

![Modelo lógico del e-commerce](../../assets/diagrams/explorations/cap09-erd-ecommerce-v2.png)

### Función editorial

El ERD conecta usuarios, direcciones, pedidos, pagos, líneas de pedido,
productos y categorías. Incluye claves principales, claves foráneas,
cardinalidades y la tabla puente de la relación entre productos y categorías.

La revisión visual también detectó una discrepancia útil en el manuscrito: la
relación Pedido–Pago se describe como `1:1`, pero el SQL actual no declara
`pagos.pedido_id` como `UNIQUE`. La lámina mantiene la intención conceptual y
señala el detalle físico que debería verificarse.

## Evaluación

| Criterio | Sistemas | Arquitectura | Datos |
|---|---|---|---|
| Tipo dominante | Flujo + feedback | Comparación estructural | ERD |
| Orientación | Horizontal | Vertical | Horizontal |
| Color principal | Azul petróleo | Paleta completa | Color por familia |
| Color de excepción | Terracota | Terracota | Terracota |
| Uso de ocre | Persistencia | Dominio y puertos | Producto y categoría |
| Densidad | Media | Media | Alta |

## Próximos ajustes

Antes de publicarlos en los capítulos:

1. Confirmar que la densidad y el nivel de detalle son adecuados.
2. Decidir si los títulos deben vivir dentro de la imagen o como encabezados de
   GitBook.
3. Probar cada PNG al ancho real de lectura y conservar el SVG como fuente.
4. Corregir, si corresponde, la restricción `UNIQUE` del ejemplo de pagos.
