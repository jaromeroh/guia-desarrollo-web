# 15. Persistencia y Bases de Datos

> "Los datos sobreviven al código. El schema que diseñes hoy seguirá ahí cuando hayas reescrito la aplicación tres veces."

---

## Objetivos de Aprendizaje

Al finalizar este capítulo, serás capaz de:

- Aplicar patrones de acceso a datos (Repository, Unit of Work) apropiadamente
- Elegir entre ORM, Query Builder o SQL puro según el contexto
- Diseñar transacciones con el nivel de aislamiento correcto
- Implementar estrategias de caching efectivas
- Optimizar queries mediante índices y entender cuándo usar búsqueda especializada

---

## Por Qué Este Capítulo Importa

En el capítulo 9 modelamos los datos. En el capítulo 12 estructuramos el backend en capas. Ahora conectamos ambos: **¿cómo accede tu aplicación a la base de datos de forma eficiente, segura y mantenible?**

```
┌─────────────────────────────────────────────────────────────────┐
│                    LA CAPA DE PERSISTENCIA                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Tu aplicación                                                 │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              ¿Cómo accedes a los datos?                 │   │
│   │                                                         │   │
│   │   • ¿SQL directo? ¿ORM? ¿Query Builder?                 │   │
│   │   • ¿Cómo manejas transacciones?                        │   │
│   │   • ¿Qué pasa si dos usuarios editan lo mismo?          │   │
│   │   • ¿Cómo evitas queries lentas?                        │   │
│   │   • ¿Cuándo cachear y cuándo ir a la DB?                │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼                                                        │
│   Base de datos                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Este capítulo responde esas preguntas con patrones probados y decisiones informadas.

---

## Patrones de Acceso a Datos

### El problema del acceso directo

Considera este código común en aplicaciones pequeñas:

```typescript
// ❌ Acceso directo desde el servicio
class OrderService {
  async createOrder(userId: string, items: CartItem[]) {
    // SQL directo mezclado con lógica de negocio
    const user = await db.query(
      'SELECT * FROM users WHERE id = $1',
      [userId]
    );

    if (!user) throw new Error('Usuario no encontrado');

    const order = await db.query(
      'INSERT INTO orders (user_id, total) VALUES ($1, $2) RETURNING *',
      [userId, calculateTotal(items)]
    );

    for (const item of items) {
      await db.query(
        'INSERT INTO order_items (order_id, product_id, qty) VALUES ($1, $2, $3)',
        [order.id, item.productId, item.quantity]
      );
    }

    return order;
  }
}
```

Este código tiene varios problemas:

- **Difícil de testear** — necesitas una base de datos real
- **Lógica de negocio mezclada con SQL** — difícil de mantener
- **Sin transacción** — si falla a mitad, quedan datos inconsistentes
- **Imposible cambiar de DB** — SQL específico disperso por todo el código

### El patrón Repository

El **Repository** abstrae el acceso a datos detrás de una interfaz que parece una colección en memoria:

```typescript
// ✅ Acceso a datos abstraído
interface OrderRepository {
  findById(id: string): Promise<Order | null>;
  findByUserId(userId: string): Promise<Order[]>;
  save(order: Order): Promise<Order>;
  delete(id: string): Promise<void>;
}

class PostgresOrderRepository implements OrderRepository {
  async findById(id: string): Promise<Order | null> {
    const result = await db.query(
      'SELECT * FROM orders WHERE id = $1',
      [id]
    );
    return result.rows[0] ? this.toOrder(result.rows[0]) : null;
  }

  async save(order: Order): Promise<Order> {
    // Lógica de INSERT o UPDATE según si existe
    // ...
  }

  private toOrder(row: any): Order {
    // Mapea de row de DB a objeto de dominio
    return new Order(row.id, row.user_id, row.total, row.status);
  }
}
```

**Beneficios:**

| Sin Repository | Con Repository |
|----------------|----------------|
| SQL disperso en servicios | SQL centralizado en un lugar |
| Tests requieren DB real | Puedes usar un mock/fake |
| Cambiar DB = reescribir todo | Cambiar DB = nueva implementación |
| Lógica de mapeo repetida | Mapeo en un solo lugar |

📖 **Concepto**: El Repository actúa como una "colección de objetos de dominio". El resto de la aplicación no sabe ni le importa si los datos vienen de PostgreSQL, MongoDB, o un archivo JSON.

### El patrón Unit of Work

El **Unit of Work** agrupa múltiples operaciones en una sola transacción:

```typescript
// ✅ Múltiples operaciones en una transacción
class UnitOfWork {
  private connection: PoolClient;

  async begin(): Promise<void> {
    this.connection = await pool.connect();
    await this.connection.query('BEGIN');
  }

  async commit(): Promise<void> {
    await this.connection.query('COMMIT');
    this.connection.release();
  }

  async rollback(): Promise<void> {
    await this.connection.query('ROLLBACK');
    this.connection.release();
  }

  // Los repositorios usan esta conexión
  get orders(): OrderRepository {
    return new PostgresOrderRepository(this.connection);
  }

  get orderItems(): OrderItemRepository {
    return new PostgresOrderItemRepository(this.connection);
  }
}
```

Uso en el servicio:

```typescript
class OrderService {
  async createOrder(userId: string, items: CartItem[]) {
    const uow = new UnitOfWork();

    try {
      await uow.begin();

      const order = new Order(userId, calculateTotal(items));
      await uow.orders.save(order);

      for (const item of items) {
        await uow.orderItems.save(new OrderItem(order.id, item));
      }

      await uow.commit();
      return order;

    } catch (error) {
      await uow.rollback();
      throw error;
    }
  }
}
```

💡 **Insight**: Si usas un ORM como Prisma o TypeORM, el "Unit of Work" ya está implementado. En Prisma es `prisma.$transaction()`. En TypeORM, el `EntityManager` actúa como Unit of Work.

### ¿Cuándo usar estos patrones?

```
┌─────────────────────────────────────────────────────────────────┐
│                  ¿NECESITAS REPOSITORY + UOW?                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SÍ, probablemente:                                             │
│  ─────────────────                                              │
│  • Dominio complejo con muchas entidades relacionadas           │
│  • Necesitas tests unitarios sin base de datos                  │
│  • Podrías cambiar de base de datos en el futuro                │
│  • Múltiples desarrolladores trabajan en el proyecto            │
│  • La aplicación vivirá años                                    │
│                                                                 │
│  NO necesariamente:                                             │
│  ──────────────────                                             │
│  • CRUD simple (pocas entidades, operaciones básicas)           │
│  • Prototipo o MVP que validará la idea                         │
│  • Microservicio pequeño y enfocado                             │
│  • Usas un ORM que ya abstrae suficiente                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

⚠️ **Advertencia**: Agregar Repository + Unit of Work a una app CRUD simple es over-engineering. Pero en dominios complejos, no tenerlos lleva a código espagueti y tests frágiles.

---

## ORMs vs Query Builders vs SQL Puro

Esta es una de las decisiones más debatidas en desarrollo backend. No hay respuesta universal — depende del contexto.

### El espectro de abstracción

```
┌─────────────────────────────────────────────────────────────────┐
│             NIVELES DE ABSTRACCIÓN PARA ACCESO A DATOS          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Más abstracción                              Menos abstracción │
│  ───────────────                              ───────────────── │
│                                                                 │
│       ORM ─────────► Query Builder ─────────► SQL Puro          │
│                                                                 │
│   "Trabajo con       "Construyo queries      "Escribo SQL       │
│    objetos"           programáticamente"      directamente"     │
│                                                                 │
│   Prisma, TypeORM,   Knex.js, Kysely         pg, mysql2         │
│   Drizzle, Sequelize                         + herramientas     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### SQL Puro

```typescript
// SQL directo con el driver de PostgreSQL
const result = await pool.query(`
  SELECT u.name, COUNT(o.id) as order_count
  FROM users u
  LEFT JOIN orders o ON o.user_id = u.id
  WHERE u.created_at > $1
  GROUP BY u.id
  HAVING COUNT(o.id) > 5
  ORDER BY order_count DESC
  LIMIT 10
`, [lastMonth]);
```

**Ventajas:**
- Máximo control y performance
- Acceso a todas las features del motor de DB
- Sin "magia" — sabes exactamente qué ejecuta
- Ideal para queries complejas y optimizadas

**Desventajas:**
- Sin type-safety (aunque herramientas como PgTyped ayudan)
- Mapeo manual de resultados a objetos
- Más código repetitivo
- Vulnerable a SQL injection si no usas parámetros

### Query Builder (Knex.js, Kysely)

```typescript
// Misma query con Knex.js
const result = await knex('users as u')
  .select('u.name')
  .count('o.id as order_count')
  .leftJoin('orders as o', 'o.user_id', 'u.id')
  .where('u.created_at', '>', lastMonth)
  .groupBy('u.id')
  .having(knex.raw('COUNT(o.id) > 5'))
  .orderBy('order_count', 'desc')
  .limit(10);
```

**Ventajas:**
- Previene SQL injection por diseño
- Composición programática de queries
- Más portable entre bases de datos
- Buen balance entre control y conveniencia

**Desventajas:**
- API a aprender (aunque se parece a SQL)
- A veces queries complejas son más claras en SQL
- Menos ecosistema que ORMs populares

### ORM (Prisma, TypeORM, Drizzle)

```typescript
// Con Prisma
const result = await prisma.user.findMany({
  where: {
    createdAt: { gt: lastMonth },
    orders: { some: {} }  // tiene al menos una orden
  },
  include: {
    _count: { select: { orders: true } }
  },
  orderBy: { orders: { _count: 'desc' } },
  take: 10
});

// Filtrar en código los que tienen > 5 órdenes
// (Prisma no soporta HAVING directamente)
```

**Ventajas:**
- Type-safety completo (especialmente Prisma y Drizzle)
- Desarrollo más rápido para CRUD
- Migraciones y schema management incluidos
- Relaciones manejadas automáticamente

**Desventajas:**
- Queries generadas pueden ser subóptimas
- Algunas queries complejas son difíciles o imposibles
- Abstracción que puede ocultar problemas de performance
- Curva de aprendizaje del API específico

### Comparativa práctica

| Criterio | SQL Puro | Query Builder | ORM |
|----------|----------|---------------|-----|
| **Velocidad de desarrollo** | Lenta | Media | Rápida |
| **Performance máxima** | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **Type-safety** | Requiere herramientas | Parcial | Excelente |
| **Queries complejas** | Fácil | Posible | Difícil/Imposible |
| **Curva de aprendizaje** | Requiere SQL | Media | Alta (API específico) |
| **Cambiar de DB** | Reescribir | Ajustes menores | Casi automático |

### El enfoque híbrido (recomendado)

En la práctica, los equipos exitosos usan un **enfoque híbrido**:

```typescript
// ORM para operaciones CRUD comunes
const user = await prisma.user.create({
  data: { email, name, passwordHash }
});

// SQL puro para queries de reporting/analytics complejas
const salesReport = await prisma.$queryRaw`
  SELECT
    DATE_TRUNC('month', o.created_at) as month,
    SUM(o.total) as revenue,
    COUNT(DISTINCT o.user_id) as unique_customers
  FROM orders o
  WHERE o.created_at BETWEEN ${startDate} AND ${endDate}
  GROUP BY DATE_TRUNC('month', o.created_at)
  ORDER BY month
`;
```

💡 **Insight**: "Si conoces SQL, conoces Drizzle" es el lema de Drizzle ORM. En 2025, Drizzle ha ganado popularidad porque combina la familiaridad del SQL con type-safety de TypeScript, siendo una opción intermedia atractiva.

### ORMs populares en 2025

| ORM | Filosofía | Ideal para |
|-----|-----------|------------|
| **Prisma** | Schema-first, DX excelente | Proyectos nuevos, equipos que priorizan productividad |
| **Drizzle** | SQL-like, ligero, zero dependencies | Serverless, equipos que conocen bien SQL |
| **TypeORM** | Decoradores, similar a Hibernate | Equipos con experiencia en Java/.NET |
| **MikroORM** | Data Mapper, Unit of Work built-in | Domain-Driven Design |

---

## Transacciones y Consistencia

### El problema de la concurrencia

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROBLEMA DE CONCURRENCIA                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Usuario A                           Usuario B                 │
│      │                                   │                      │
│      │── Lee saldo: $100 ───────────────>│                      │
│      │                                   │── Lee saldo: $100    │
│      │                                   │                      │
│      │── Retira $80 ────────────────────>│                      │
│      │   Nuevo saldo: $20                │                      │
│      │                                   │── Retira $50         │
│      │                                   │   Nuevo saldo: $50   │
│      │                                   │   (¡INCORRECTO!)     │
│                                                                 │
│   Resultado: El banco perdió $30 porque ambos leyeron $100      │
│   antes de que el otro escribiera.                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Las **transacciones** y los **niveles de aislamiento** existen para prevenir estos problemas.

### ACID: Las garantías fundamentales

📖 **Concepto**: ACID son las cuatro propiedades que garantizan transacciones confiables:

| Propiedad | Significado | Ejemplo |
|-----------|-------------|---------|
| **Atomicity** | Todo o nada | Si falla el paso 3 de 5, se revierten todos |
| **Consistency** | De estado válido a estado válido | No puedes tener saldo negativo si hay constraint |
| **Isolation** | Transacciones no interfieren entre sí | Usuario A no ve cambios no commiteados de B |
| **Durability** | Una vez commiteado, persiste | Aunque se caiga el servidor, los datos están |

### Niveles de aislamiento

PostgreSQL (y la mayoría de DBs relacionales) ofrece diferentes niveles de aislamiento. Cada nivel previene diferentes tipos de anomalías:

```
┌─────────────────────────────────────────────────────────────────┐
│                    NIVELES DE AISLAMIENTO                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Nivel              Dirty   Non-Repeatable   Phantom   Perf.   │
│                     Read    Read             Read              │
│  ─────────────────  ─────   ──────────────   ───────   ─────   │
│  Read Uncommitted   ✗*      Posible          Posible   ⭐⭐⭐   │
│  Read Committed     ✗       Posible          Posible   ⭐⭐    │
│  Repeatable Read    ✗       ✗                ✗**       ⭐      │
│  Serializable       ✗       ✗                ✗         ½⭐     │
│                                                                 │
│  * PostgreSQL trata Read Uncommitted como Read Committed        │
│  ** PostgreSQL previene phantoms en Repeatable Read (MVCC)      │
│                                                                 │
│  Default en PostgreSQL: Read Committed                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Las anomalías explicadas:**

- **Dirty Read**: Leer datos que otra transacción aún no ha commiteado (y podría revertir)
- **Non-Repeatable Read**: Leer el mismo row dos veces y obtener valores diferentes porque otra transacción lo modificó
- **Phantom Read**: Ejecutar la misma query dos veces y obtener diferentes filas porque otra transacción insertó/eliminó

### MVCC: Cómo PostgreSQL maneja la concurrencia

PostgreSQL usa **Multi-Version Concurrency Control (MVCC)**:

```
┌─────────────────────────────────────────────────────────────────┐
│                          MVCC                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   En lugar de bloquear filas al leer, PostgreSQL mantiene       │
│   múltiples versiones de cada fila.                             │
│                                                                 │
│   Transacción A (snapshot t=100)     Transacción B (t=105)      │
│   ─────────────────────────────      ────────────────────       │
│   Ve: precio = $100                  UPDATE precio = $120       │
│   Ve: precio = $100 (no cambia)      COMMIT                     │
│   Ve: precio = $100 (aún)            (B terminó)                │
│   COMMIT                                                        │
│   Nueva transacción vería: $120                                 │
│                                                                 │
│   Resultado:                                                    │
│   • Lectores no bloquean escritores                             │
│   • Escritores no bloquean lectores                             │
│   • Solo escritores bloquean otros escritores en la misma fila  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Eligiendo el nivel correcto

```
┌─────────────────────────────────────────────────────────────────┐
│                  ¿QUÉ NIVEL USAR?                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Read Committed (default):                                      │
│  ─────────────────────────                                      │
│  • La mayoría de aplicaciones web                               │
│  • CRUD estándar                                                │
│  • Cuando cada statement puede ver datos actualizados           │
│                                                                 │
│  Repeatable Read:                                               │
│  ────────────────                                               │
│  • Reportes que leen múltiples tablas consistentemente          │
│  • Operaciones que no deben ver cambios a mitad de transacción  │
│  • Balance recomendado para la mayoría de casos complejos       │
│                                                                 │
│  Serializable:                                                  │
│  ─────────────                                                  │
│  • Sistemas financieros críticos                                │
│  • Auditoría y compliance                                       │
│  • Cuando necesitas garantía absoluta de consistencia           │
│  • ⚠️ Prepárate para manejar errores de serialización (40001)  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ejemplo práctico: Transferencia bancaria

```typescript
// ✅ Transferencia con nivel de aislamiento apropiado
async function transfer(fromId: string, toId: string, amount: number) {
  await prisma.$transaction(async (tx) => {
    // Leer saldos con lock
    const from = await tx.account.findUnique({
      where: { id: fromId },
    });

    if (!from || from.balance < amount) {
      throw new Error('Saldo insuficiente');
    }

    // Actualizar ambas cuentas
    await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } }
    });

    await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } }
    });

  }, {
    isolationLevel: 'Serializable'  // Máxima garantía para dinero
  });
}
```

⚠️ **Advertencia**: Con `Serializable`, tu aplicación debe estar preparada para reintentar transacciones que fallen con error de serialización. No es un error fatal — es la DB diciéndote "inténtalo de nuevo".

---

## Caching: Estrategias y Patrones

### Por qué cachear

```
┌─────────────────────────────────────────────────────────────────┐
│                    EL IMPACTO DEL CACHING                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Sin cache:                                                    │
│   ──────────                                                    │
│   Request → App → DB Query (50ms) → Response                    │
│   Request → App → DB Query (50ms) → Response                    │
│   Request → App → DB Query (50ms) → Response                    │
│   ...                                                           │
│   1000 requests = 1000 queries = 50 segundos de DB time         │
│                                                                 │
│   Con cache:                                                    │
│   ──────────                                                    │
│   Request → App → Cache HIT (1ms) → Response                    │
│   Request → App → Cache HIT (1ms) → Response                    │
│   Request → App → Cache MISS → DB (50ms) → Cache → Response     │
│   ...                                                           │
│   1000 requests = ~50 queries = ~3 segundos de DB time          │
│                                                                 │
│   Resultado: 95% menos carga en la DB, respuestas más rápidas   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Estrategias de caching

#### 1. Cache-Aside (Lazy Loading)

La aplicación maneja el cache explícitamente:

```typescript
async function getProduct(id: string): Promise<Product> {
  // 1. Intentar obtener del cache
  const cached = await redis.get(`product:${id}`);
  if (cached) {
    return JSON.parse(cached);
  }

  // 2. Cache miss: ir a la DB
  const product = await prisma.product.findUnique({ where: { id } });

  if (product) {
    // 3. Guardar en cache para próximas peticiones
    await redis.set(
      `product:${id}`,
      JSON.stringify(product),
      'EX', 3600  // Expira en 1 hora
    );
  }

  return product;
}
```

**Pros**: Simple, solo cachea lo que realmente se usa
**Contras**: Primera petición siempre lenta (cache miss)

#### 2. Write-Through

Escribe en cache y DB simultáneamente:

```typescript
async function updateProduct(id: string, data: ProductUpdate) {
  // 1. Actualizar en DB
  const product = await prisma.product.update({
    where: { id },
    data
  });

  // 2. Actualizar en cache inmediatamente
  await redis.set(
    `product:${id}`,
    JSON.stringify(product),
    'EX', 3600
  );

  return product;
}
```

**Pros**: Cache siempre actualizado
**Contras**: Escrituras más lentas (doble operación)

#### 3. Write-Behind (Write-Back)

Escribe en cache primero, DB después (asíncrono):

```typescript
async function updateProduct(id: string, data: ProductUpdate) {
  // 1. Actualizar en cache (rápido)
  await redis.set(`product:${id}`, JSON.stringify({...existingData, ...data}));

  // 2. Encolar actualización a DB (asíncrono)
  await queue.add('sync-to-db', { entity: 'product', id, data });

  return {...existingData, ...data};
}

// Worker procesa la cola
async function syncToDb(job) {
  await prisma.product.update({
    where: { id: job.data.id },
    data: job.data.data
  });
}
```

**Pros**: Escrituras muy rápidas
**Contras**: Riesgo de pérdida de datos si el cache falla antes de sincronizar

### Invalidación de cache

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

```
┌─────────────────────────────────────────────────────────────────┐
│                 ESTRATEGIAS DE INVALIDACIÓN                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TTL (Time-To-Live):                                            │
│  ───────────────────                                            │
│  El dato expira automáticamente después de X tiempo.            │
│  Simple pero puede servir datos stale hasta que expire.         │
│                                                                 │
│  Invalidación explícita:                                        │
│  ───────────────────────                                        │
│  Cuando actualizas la DB, borras el cache correspondiente.      │
│  Preciso pero requiere disciplina en todo el código.            │
│                                                                 │
│  Event-driven (Pub/Sub):                                        │
│  ───────────────────────                                        │
│  Publicas eventos cuando hay cambios, suscriptores invalidan.   │
│  Escalable pero más infraestructura.                            │
│                                                                 │
│  Versionado de keys:                                            │
│  ───────────────────                                            │
│  product:v3:123 → cuando cambias, incrementas versión.          │
│  El viejo key expira solo, no necesitas borrarlo.               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ejemplo: Invalidación explícita con patrón

```typescript
class ProductCache {
  private redis: Redis;
  private keyPrefix = 'product';

  private key(id: string): string {
    return `${this.keyPrefix}:${id}`;
  }

  private listKey(category?: string): string {
    return category
      ? `${this.keyPrefix}:list:${category}`
      : `${this.keyPrefix}:list:all`;
  }

  async get(id: string): Promise<Product | null> {
    const cached = await this.redis.get(this.key(id));
    return cached ? JSON.parse(cached) : null;
  }

  async set(product: Product): Promise<void> {
    await this.redis.set(
      this.key(product.id),
      JSON.stringify(product),
      'EX', 3600
    );
  }

  async invalidate(id: string, categoryId?: string): Promise<void> {
    // Invalida el producto específico
    await this.redis.del(this.key(id));

    // Invalida listas que podrían contenerlo
    await this.redis.del(this.listKey());
    if (categoryId) {
      await this.redis.del(this.listKey(categoryId));
    }
  }
}
```

💡 **Insight**: Redis no es la única opción. Para caching en proceso (misma instancia), soluciones como `node-cache` o `lru-cache` evitan el round-trip de red. Usa Redis cuando necesites cache compartido entre múltiples instancias.

---

## Índices: Optimizando Queries

### El problema de las búsquedas sin índice

```
┌─────────────────────────────────────────────────────────────────┐
│                    SIN ÍNDICE vs CON ÍNDICE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Tabla: users (1,000,000 filas)                                │
│   Query: SELECT * FROM users WHERE email = 'juan@email.com'     │
│                                                                 │
│   Sin índice (Full Table Scan):                                 │
│   ─────────────────────────────                                 │
│   Revisa fila 1... no                                           │
│   Revisa fila 2... no                                           │
│   ...                                                           │
│   Revisa fila 847,293... ¡SÍ!                                   │
│   ...sigue revisando por si hay más                             │
│   Revisa fila 1,000,000... terminó                              │
│                                                                 │
│   Tiempo: ~500ms (revisa todas las filas)                       │
│                                                                 │
│   Con índice B-tree en email:                                   │
│   ────────────────────────────                                  │
│   Árbol balanceado: log₂(1,000,000) ≈ 20 comparaciones          │
│                                                                 │
│   Tiempo: ~1ms                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Tipos de índices

| Tipo | Uso | Ejemplo en PostgreSQL |
|------|-----|----------------------|
| **B-tree** | Default. Igualdad, rangos, ORDER BY | `CREATE INDEX idx ON users(email)` |
| **Hash** | Solo igualdad exacta, muy rápido | `CREATE INDEX idx ON users USING hash(email)` |
| **GIN** | Arrays, JSONB, full-text search | `CREATE INDEX idx ON products USING gin(tags)` |
| **GiST** | Datos geométricos, rangos | `CREATE INDEX idx ON locations USING gist(coordinates)` |
| **BRIN** | Datos ordenados naturalmente (timestamps) | `CREATE INDEX idx ON logs USING brin(created_at)` |

### Índices compuestos: La regla del prefijo izquierdo

```sql
-- Índice compuesto en (user_id, status, created_at)
CREATE INDEX idx_orders_user_status_date
ON orders(user_id, status, created_at);
```

```
┌─────────────────────────────────────────────────────────────────┐
│              REGLA DEL PREFIJO IZQUIERDO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Índice: (user_id, status, created_at)                         │
│                                                                 │
│   ✅ Usa el índice:                                             │
│   WHERE user_id = 123                                           │
│   WHERE user_id = 123 AND status = 'pending'                    │
│   WHERE user_id = 123 AND status = 'pending' AND created_at > X │
│                                                                 │
│   ❌ NO usa el índice (o solo parcialmente):                    │
│   WHERE status = 'pending'                    ← falta user_id   │
│   WHERE created_at > X                        ← faltan ambos    │
│   WHERE status = 'pending' AND created_at > X ← falta user_id   │
│                                                                 │
│   El índice está ordenado: primero por user_id, luego por       │
│   status dentro de cada user_id, luego por fecha.               │
│   No puedes "saltar" columnas.                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Diseñando índices efectivos

```
┌─────────────────────────────────────────────────────────────────┐
│                   GUÍA PARA CREAR ÍNDICES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Identifica tus queries más frecuentes y lentas              │
│     └─ Usa EXPLAIN ANALYZE para ver qué hace la DB              │
│                                                                 │
│  2. Ordena columnas en el índice:                               │
│     └─ Primero: columnas de igualdad (=)                        │
│     └─ Luego: columnas de rango (<, >, BETWEEN)                 │
│     └─ Finalmente: columnas de ORDER BY                         │
│                                                                 │
│  3. Considera índices parciales para subconjuntos comunes:      │
│     CREATE INDEX idx_active_users ON users(email)               │
│     WHERE active = true;  ← Solo indexa usuarios activos        │
│                                                                 │
│  4. Considera covering indexes si evitan ir a la tabla:         │
│     CREATE INDEX idx_user_summary ON users(id)                  │
│     INCLUDE (name, email);  ← Incluye datos extra               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

⚠️ **Advertencia**: Cada índice ralentiza los INSERTs y UPDATEs porque debe mantenerse actualizado. No indexes "por si acaso" — indexa basado en queries reales.

### EXPLAIN ANALYZE: Tu mejor amigo

```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 123
  AND status = 'pending'
ORDER BY created_at DESC
LIMIT 10;
```

```
-- Output (simplificado):
Limit  (cost=0.43..12.35 rows=10) (actual time=0.045..0.089 rows=10)
  -> Index Scan using idx_orders_user_status_date on orders
       Index Cond: (user_id = 123 AND status = 'pending')

-- ✅ "Index Scan" = está usando el índice
-- ❌ "Seq Scan" = está revisando toda la tabla
```

---

## Búsqueda: Más Allá de LIKE

### El espectro de soluciones de búsqueda

```
┌─────────────────────────────────────────────────────────────────┐
│                SOLUCIONES DE BÚSQUEDA DE TEXTO                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Complejidad                                         Features   │
│  ──────────                                         ─────────   │
│                                                                 │
│  LIKE/ILIKE ────► PostgreSQL FTS ────► Meilisearch ────► Elastic│
│                                                                 │
│  "Busca         "Stemming,           "Typo tolerance, "Escala   │
│   substring"     ranking,             facets,          masiva,  │
│                  ts_vector"           instant"         analytics"│
│                                                                 │
│  Sin infra       Sin infra            +1 servicio      +cluster │
│  extra           extra                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### LIKE: Simple pero limitado

```sql
-- Funciona, pero tiene problemas
SELECT * FROM products WHERE name ILIKE '%laptop%';

-- ❌ No usa índices con wildcard al inicio (%)
-- ❌ No maneja typos ("laptp" no encuentra "laptop")
-- ❌ No entiende sinónimos ("computadora" vs "ordenador")
-- ❌ No rankea por relevancia
```

### PostgreSQL Full-Text Search

```sql
-- 1. Crear columna de búsqueda
ALTER TABLE products ADD COLUMN search_vector tsvector;

-- 2. Llenarla con datos tokenizados
UPDATE products SET search_vector =
  to_tsvector('spanish', name || ' ' || description);

-- 3. Crear índice GIN
CREATE INDEX idx_products_search ON products USING gin(search_vector);

-- 4. Buscar
SELECT name, ts_rank(search_vector, query) as rank
FROM products, to_tsquery('spanish', 'laptop & gaming') query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

**Ventajas:**
- Sin infraestructura adicional
- Stemming (buscar "corriendo" encuentra "correr")
- Ranking por relevancia
- Integrado con transacciones

**Limitaciones:**
- No tolera typos por defecto (necesita pg_trgm)
- Faceted search es complejo de implementar
- Performance limitada en datasets muy grandes

### Cuándo escalar a búsqueda dedicada

```
┌─────────────────────────────────────────────────────────────────┐
│              ¿NECESITAS BÚSQUEDA DEDICADA?                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PostgreSQL FTS es suficiente si:                               │
│  ─────────────────────────────────                              │
│  • < 1 millón de documentos                                     │
│  • Búsqueda es feature secundaria                               │
│  • No necesitas typo tolerance avanzada                         │
│  • No necesitas faceted search compleja                         │
│  • Latencia de 50-100ms es aceptable                            │
│                                                                 │
│  Considera Meilisearch/Typesense si:                            │
│  ────────────────────────────────────                           │
│  • Search-as-you-type es importante                             │
│  • Usuarios esperan tolerancia a typos                          │
│  • Necesitas facets y filtros combinados                        │
│  • Latencia < 50ms es requerida                                 │
│                                                                 │
│  Considera Elasticsearch si:                                    │
│  ────────────────────────────                                   │
│  • Millones de documentos                                       │
│  • Queries analíticas complejas                                 │
│  • Necesitas scoring/boosting avanzado                          │
│  • Tienes equipo para operarlo                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

💡 **Insight**: La ruta de migración típica es: PostgreSQL FTS → Meilisearch → Elasticsearch. No saltes directamente a Elasticsearch a menos que sepas que lo necesitas. Es como "comprar un motor jet para impulsar una bicicleta".

---

## 🤖 Usando IA para Persistencia

### Generación de queries

La IA es excelente para generar queries SQL complejas:

```
Prompt: "Escribe una query PostgreSQL que obtenga los 10 productos
más vendidos del último mes, incluyendo el nombre del producto,
cantidad total vendida, y revenue generado. Ordena por revenue."

-- La IA genera:
SELECT
  p.name,
  SUM(oi.quantity) as total_sold,
  SUM(oi.quantity * oi.unit_price) as revenue
FROM order_items oi
JOIN products p ON p.id = oi.product_id
JOIN orders o ON o.id = oi.order_id
WHERE o.created_at >= NOW() - INTERVAL '1 month'
  AND o.status = 'completed'
GROUP BY p.id, p.name
ORDER BY revenue DESC
LIMIT 10;
```

### Optimización de queries

```
Prompt: "Esta query tarda 5 segundos. Tengo un índice en
orders(user_id). ¿Cómo puedo optimizarla?

SELECT * FROM orders
WHERE user_id = 123
  AND status IN ('pending', 'processing')
ORDER BY created_at DESC;"

-- La IA sugiere:
-- 1. Crear índice compuesto: (user_id, status, created_at DESC)
-- 2. Evitar SELECT * si no necesitas todas las columnas
-- 3. Usar LIMIT si solo necesitas los primeros N
```

### Limitaciones a tener en cuenta

⚠️ **La IA no conoce:**
- Tu schema específico (a menos que se lo des)
- El volumen de datos que manejas
- Los índices que ya existen
- Las queries que corren en paralelo
- Las características específicas de tu versión de PostgreSQL

Siempre valida con `EXPLAIN ANALYZE` antes de implementar sugerencias.

---

## Resumen

- **Patrones de acceso**: Repository abstrae la persistencia, Unit of Work agrupa operaciones en transacciones. Úsalos en dominios complejos, no en CRUD simple.

- **ORM vs Query Builder vs SQL**: No hay ganador universal. ORMs para productividad, SQL para control, híbrido para lo mejor de ambos mundos.

- **Transacciones**: ACID garantiza consistencia. PostgreSQL usa MVCC. Read Committed es el default, Repeatable Read para la mayoría de casos complejos, Serializable para financiero.

- **Caching**: Cache-Aside es el patrón más común. La invalidación es difícil — usa TTL + invalidación explícita. Redis para cache distribuido.

- **Índices**: B-tree por default. Índices compuestos siguen la regla del prefijo izquierdo. Usa EXPLAIN ANALYZE para validar.

- **Búsqueda**: PostgreSQL FTS para empezar, Meilisearch como paso intermedio, Elasticsearch para escala masiva.

---

## Ejercicios

1. **Repository pattern**: Tienes un servicio que hace queries SQL directamente. Refactoriza para usar el patrón Repository. ¿Qué métodos expondrías? ¿Cómo lo testearías sin base de datos?

2. **Diseño de índices**: Tu tabla `orders` tiene 10 millones de filas. Las queries más comunes son:
   - Órdenes de un usuario ordenadas por fecha
   - Órdenes pendientes de los últimos 7 días
   - Buscar orden por número de referencia

   Diseña los índices necesarios. ¿Crearías un índice para cada query o combinarías alguno?

3. **Estrategia de cache**: Tu e-commerce muestra productos con sus precios. Los precios cambian una vez al día a medianoche. ¿Qué estrategia de cache usarías? ¿Cómo invalidarías?

4. **Niveles de aislamiento**: Un sistema de reservas de cine permite reservar asientos. Dos usuarios intentan reservar el mismo asiento simultáneamente. ¿Qué nivel de aislamiento usarías? ¿Cómo manejarías el conflicto?

---

## Referencias

- PostgreSQL Documentation. *Transaction Isolation*. https://www.postgresql.org/docs/current/transaction-iso.html
- Fowler, M. *Patterns of Enterprise Application Architecture*. Addison-Wesley. (Repository, Unit of Work)
- AWS. *Database Caching Strategies Using Redis*. https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/
- Prisma. *Comparing SQL, Query Builders and ORMs*. https://www.prisma.io/dataguide/types/relational/comparing-sql-query-builders-and-orms
- AppSignal. *How to Choose Between SQL, Query Builders, and ORMs in Node.js*. https://blog.appsignal.com/2025/03/26/how-to-choose-between-sql-query-builders-and-orms-in-nodejs.html

---

**Anterior**: [Comunicación y Datos en Tiempo Real](./14-tiempo-real.md) | **Siguiente**: [Manejo de Tareas Asíncronas](./16-tareas-asincronas.md)
