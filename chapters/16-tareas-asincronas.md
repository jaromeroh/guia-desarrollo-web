# 16. Manejo de Tareas Asíncronas

> "No hagas esperar al usuario por algo que puede pasar después."

---

## Objetivos de Aprendizaje

Al finalizar este capítulo, serás capaz de:

- Identificar qué tareas deben ejecutarse fuera del ciclo request-response
- Implementar colas de trabajo con BullMQ y Redis
- Aplicar patrones de resiliencia: retry con backoff y circuit breaker
- Diseñar sistemas event-driven con message brokers
- Entender cuándo CQRS y Event Sourcing aportan valor

---

## El Problema: El Request Que Tarda Demasiado

```
┌─────────────────────────────────────────────────────────────────┐
│                    EL REQUEST SÍNCRONO                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Usuario                        Servidor                       │
│      │                              │                           │
│      │── POST /register ───────────>│                           │
│      │                              │── Validar datos           │
│      │                              │── Crear usuario en DB     │
│      │                              │── Enviar email bienvenida │
│      │         ⏳ 3 seg             │── Generar avatar          │
│      │                              │── Notificar a Slack       │
│      │                              │── Actualizar analytics    │
│      │<── 201 Created ──────────────│                           │
│      │                                                          │
│   "¿Por qué tarda tanto en registrarme?" 😤                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

El problema: **todo sucede dentro del request HTTP**. El usuario espera mientras el servidor hace tareas que no necesitan respuesta inmediata.

### La solución: Procesar en background

```
┌─────────────────────────────────────────────────────────────────┐
│                    CON PROCESAMIENTO ASYNC                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Usuario                        Servidor        Workers        │
│      │                              │               │           │
│      │── POST /register ───────────>│               │           │
│      │                              │── Validar     │           │
│      │                              │── Crear user  │           │
│      │                              │── Encolar ────>│           │
│      │<── 201 Created ──────────────│   tareas      │           │
│      │                              │               │           │
│      │   ✅ 200ms                   │               │── Email   │
│      │                              │               │── Avatar  │
│      │                              │               │── Slack   │
│      │                              │               │── Stats   │
│                                                                 │
│   Usuario feliz, tareas se procesan después 😊                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ¿Qué Mover a Background?

No todo debe procesarse en background. Aquí hay una guía:

```
┌─────────────────────────────────────────────────────────────────┐
│              ¿DEBERÍA SER UNA TAREA EN BACKGROUND?              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ SÍ, mover a background:                                     │
│  ──────────────────────────                                     │
│  • Envío de emails/SMS/notificaciones push                      │
│  • Procesamiento de imágenes/videos/PDFs                        │
│  • Llamadas a APIs externas lentas o rate-limited               │
│  • Sincronización con servicios de terceros                     │
│  • Generación de reportes pesados                               │
│  • Limpieza de datos / tareas de mantenimiento                  │
│  • Webhooks salientes                                           │
│  • Indexación en motores de búsqueda                            │
│                                                                 │
│  ❌ NO, mantener síncrono:                                      │
│  ─────────────────────────                                      │
│  • El usuario NECESITA el resultado para continuar              │
│  • Validaciones que determinan si la acción es válida           │
│  • Operaciones críticas que deben confirmarse inmediatamente    │
│  • Lecturas simples de base de datos                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

📖 **Concepto**: La regla general es: si el usuario no necesita ver el resultado inmediatamente, probablemente puede procesarse después.

---

## Colas de Trabajo con BullMQ

### ¿Por qué BullMQ?

BullMQ es la librería más popular para colas de trabajo en Node.js (2025). Es una reescritura moderna de Bull, escrita en TypeScript con mejor performance y más features.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA BULLMQ                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   App (Producer)              Redis              Workers        │
│   ─────────────               ─────              ───────        │
│                                                                 │
│   queue.add('email', {   ──>  ┌─────────┐                       │
│     to: 'user@...',           │ waiting │  ──>  Worker 1        │
│     subject: '...'            │  queue  │  ──>  Worker 2        │
│   })                          └─────────┘  ──>  Worker 3        │
│                                    │                            │
│                               ┌─────────┐                       │
│                               │completed│  Jobs exitosos        │
│                               └─────────┘                       │
│                               ┌─────────┐                       │
│                               │ failed  │  Jobs fallidos        │
│                               └─────────┘                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Implementación básica

```typescript
// 1. Definir la cola
import { Queue, Worker } from 'bullmq';
import Redis from 'ioredis';

const connection = new Redis({
  host: process.env.REDIS_HOST,
  port: 6379,
  maxRetriesPerRequest: null  // Requerido por BullMQ
});

// Cola para emails
const emailQueue = new Queue('emails', { connection });

// 2. Agregar jobs desde tu aplicación
async function registerUser(userData: UserData) {
  // Operación síncrona: crear usuario
  const user = await prisma.user.create({ data: userData });

  // Operación async: encolar email de bienvenida
  await emailQueue.add('welcome', {
    userId: user.id,
    email: user.email,
    name: user.name
  }, {
    attempts: 3,           // Reintentar hasta 3 veces
    backoff: {
      type: 'exponential',
      delay: 1000          // 1s, 2s, 4s
    }
  });

  return user;  // Responder inmediatamente
}

// 3. Procesar jobs con un worker (archivo separado)
const emailWorker = new Worker('emails', async (job) => {
  const { userId, email, name } = job.data;

  switch (job.name) {
    case 'welcome':
      await sendWelcomeEmail(email, name);
      break;
    case 'password-reset':
      await sendPasswordResetEmail(email, job.data.token);
      break;
    default:
      throw new Error(`Unknown job type: ${job.name}`);
  }
}, {
  connection,
  concurrency: 5  // Procesar hasta 5 jobs en paralelo
});

// 4. Manejar eventos
emailWorker.on('completed', (job) => {
  console.log(`Job ${job.id} completed`);
});

emailWorker.on('failed', (job, err) => {
  console.error(`Job ${job?.id} failed:`, err.message);
  // Aquí podrías alertar a tu sistema de monitoreo
});
```

### Features avanzados de BullMQ

| Feature | Uso | Ejemplo |
|---------|-----|---------|
| **Delayed jobs** | Ejecutar en el futuro | `{ delay: 60000 }` (1 min) |
| **Repeatable jobs** | Cron jobs | `{ repeat: { cron: '0 9 * * *' } }` |
| **Priority** | Jobs urgentes primero | `{ priority: 1 }` (menor = más urgente) |
| **Rate limiting** | No saturar APIs externas | `{ limiter: { max: 100, duration: 60000 } }` |
| **Job dependencies** | Ejecutar después de otro | `{ parent: { queue: '...', id: '...' } }` |

### Ejemplo: Job con dependencias (Flows)

```typescript
import { FlowProducer } from 'bullmq';

const flowProducer = new FlowProducer({ connection });

// Crear un flujo: procesar imagen → generar thumbnail → notificar
await flowProducer.add({
  name: 'notify-user',
  queueName: 'notifications',
  data: { userId: '123', message: 'Tu imagen está lista' },
  children: [
    {
      name: 'generate-thumbnail',
      queueName: 'images',
      data: { imageId: 'abc', size: '200x200' },
      children: [
        {
          name: 'process-upload',
          queueName: 'images',
          data: { imageId: 'abc', url: 's3://...' }
        }
      ]
    }
  ]
});

// Se ejecuta: process-upload → generate-thumbnail → notify-user
```

### Monitoreo con Bull Board

```typescript
import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { ExpressAdapter } from '@bull-board/express';

const serverAdapter = new ExpressAdapter();
serverAdapter.setBasePath('/admin/queues');

createBullBoard({
  queues: [
    new BullMQAdapter(emailQueue),
    new BullMQAdapter(imageQueue),
  ],
  serverAdapter
});

app.use('/admin/queues', serverAdapter.getRouter());
```

💡 **Insight**: En producción, protege el dashboard de Bull Board con autenticación. No quieres que cualquiera vea y manipule tus colas.

---

## Patrones de Resiliencia

### El problema de las fallas

En sistemas distribuidos, las fallas son inevitables:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TIPOS DE FALLAS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Transitorias (temporales):                                    │
│   ─────────────────────────                                     │
│   • Timeout de red                                              │
│   • API externa sobrecargada                                    │
│   • Rate limit alcanzado                                        │
│   • Connection reset                                            │
│   → Solución: REINTENTAR                                        │
│                                                                 │
│   Persistentes (el servicio está caído):                        │
│   ───────────────────────────────────────                       │
│   • Servicio externo fuera de línea                             │
│   • Certificado expirado                                        │
│   • Credenciales inválidas                                      │
│   → Solución: CIRCUIT BREAKER                                   │
│                                                                 │
│   Permanentes (error en el código/datos):                       │
│   ────────────────────────────────────────                      │
│   • Payload inválido                                            │
│   • Bug en el procesamiento                                     │
│   • Recurso no existe                                           │
│   → Solución: DEAD LETTER QUEUE + alertas                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Retry con Exponential Backoff

Reintentar inmediatamente después de una falla puede empeorar las cosas (si el servicio está sobrecargado, más requests lo saturan más). La solución: **exponential backoff con jitter**.

```typescript
interface RetryConfig {
  maxAttempts: number;
  baseDelay: number;
  maxDelay: number;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  config: RetryConfig = { maxAttempts: 3, baseDelay: 1000, maxDelay: 30000 }
): Promise<T> {
  let lastError: Error;

  for (let attempt = 1; attempt <= config.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (attempt === config.maxAttempts) {
        break;  // No más reintentos
      }

      // Exponential backoff: 1s, 2s, 4s, 8s...
      const exponentialDelay = config.baseDelay * Math.pow(2, attempt - 1);

      // Jitter: añade aleatoriedad (±25%) para evitar "thundering herd"
      const jitter = exponentialDelay * 0.25 * (Math.random() * 2 - 1);

      const delay = Math.min(exponentialDelay + jitter, config.maxDelay);

      console.log(`Attempt ${attempt} failed, retrying in ${delay}ms...`);
      await sleep(delay);
    }
  }

  throw lastError!;
}

// Uso
const result = await withRetry(
  () => callExternalAPI(payload),
  { maxAttempts: 5, baseDelay: 1000, maxDelay: 60000 }
);
```

```
┌─────────────────────────────────────────────────────────────────┐
│              EXPONENTIAL BACKOFF CON JITTER                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Intento 1: Falla → espera ~1s                                  │
│  Intento 2: Falla → espera ~2s                                  │
│  Intento 3: Falla → espera ~4s                                  │
│  Intento 4: Falla → espera ~8s                                  │
│  Intento 5: Éxito ✓                                             │
│                                                                 │
│  Sin jitter:        Con jitter:                                 │
│  ────────────       ───────────                                 │
│  Todos reintentan   Cada cliente                                │
│  al mismo tiempo    reintenta en momentos                       │
│       ↓             diferentes                                  │
│  Thundering herd!        ↓                                      │
│                     Carga distribuida ✓                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Circuit Breaker

El Circuit Breaker previene llamadas a servicios que están fallando, dando tiempo para que se recuperen.

```typescript
import CircuitBreaker from 'opossum';

// Crear circuit breaker para API externa
const breaker = new CircuitBreaker(callPaymentAPI, {
  timeout: 5000,           // Timeout por request
  errorThresholdPercentage: 50,  // Abre si 50% falla
  resetTimeout: 30000,     // Intenta cerrar después de 30s
  volumeThreshold: 10,     // Mínimo 10 requests para evaluar
});

// Estados del circuit breaker
breaker.on('open', () => {
  console.warn('Circuit OPEN: Payment API is down');
  alertOps('Payment API circuit breaker opened');
});

breaker.on('halfOpen', () => {
  console.info('Circuit HALF-OPEN: Testing if Payment API recovered');
});

breaker.on('close', () => {
  console.info('Circuit CLOSED: Payment API is healthy again');
});

// Usar el breaker
async function processPayment(amount: number) {
  try {
    return await breaker.fire(amount);
  } catch (error) {
    if (error.message === 'Breaker is open') {
      // Fallback: encolar para procesar después
      await paymentQueue.add('retry-payment', { amount });
      return { status: 'pending', message: 'Payment queued for processing' };
    }
    throw error;
  }
}
```

```
┌─────────────────────────────────────────────────────────────────┐
│                  ESTADOS DEL CIRCUIT BREAKER                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │    ┌──────────┐    Fallas > umbral    ┌──────────┐      │   │
│   │    │  CLOSED  │ ─────────────────────>│   OPEN   │      │   │
│   │    │          │                       │          │      │   │
│   │    │ (normal) │<───────────────────── │ (falla   │      │   │
│   │    └──────────┘    Éxito en           │  rápido) │      │   │
│   │         ^          half-open          └──────────┘      │   │
│   │         │                                   │           │   │
│   │         │          ┌───────────┐            │           │   │
│   │         └──────────│ HALF-OPEN │<───────────┘           │   │
│   │         Éxito      │           │    Timeout expiró      │   │
│   │                    │ (prueba)  │                        │   │
│   │                    └───────────┘                        │   │
│   │                          │                              │   │
│   │                          │ Falla                        │   │
│   │                          └─────────> Vuelve a OPEN      │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Combinando patrones

En producción, estos patrones trabajan juntos:

```typescript
// Pipeline de resiliencia completo
async function resilientExternalCall(payload: any) {
  // 1. Rate limiter: no exceder límites de la API
  await rateLimiter.acquire();

  // 2. Circuit breaker: no llamar si el servicio está caído
  return circuitBreaker.fire(async () => {
    // 3. Retry: manejar fallas transitorias
    return withRetry(
      () => externalAPI.call(payload),
      { maxAttempts: 3, baseDelay: 1000, maxDelay: 10000 }
    );
  });
}
```

⚠️ **Advertencia**: Solo reintenta operaciones **idempotentes**. Si una operación puede tener efectos secundarios duplicados (como cobrar dos veces), necesitas lógica adicional para evitarlo.

---

## Arquitectura Event-Driven

### De llamadas directas a eventos

En una arquitectura tradicional, los servicios se llaman directamente:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA ACOPLADA                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Order Service                                                 │
│        │                                                        │
│        ├──────> Inventory Service.reserveStock()                │
│        │             (si falla, order falla)                    │
│        │                                                        │
│        ├──────> Payment Service.charge()                        │
│        │             (si falla, order falla)                    │
│        │                                                        │
│        ├──────> Email Service.sendConfirmation()                │
│        │             (si falla, order falla)                    │
│        │                                                        │
│        └──────> Analytics Service.trackOrder()                  │
│                     (si falla, order falla)                     │
│                                                                 │
│   Problemas:                                                    │
│   • Order Service conoce todos los otros servicios              │
│   • Si uno falla, todo falla                                    │
│   • Agregar un servicio = modificar Order Service               │
│   • Latencia acumulativa de todas las llamadas                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Con eventos, los servicios se desacoplan:

```
┌─────────────────────────────────────────────────────────────────┐
│                  ARQUITECTURA EVENT-DRIVEN                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Order Service                                                 │
│        │                                                        │
│        └──> Publica: "OrderCreated" ─────────────────────>      │
│                            │                                    │
│                       Message Broker                            │
│                       (RabbitMQ/Kafka)                          │
│                            │                                    │
│             ┌──────────────┼──────────────┐                     │
│             │              │              │                     │
│             v              v              v                     │
│        Inventory      Payment        Email                      │
│        Service        Service        Service                    │
│        (suscrito)     (suscrito)     (suscrito)                 │
│                                                                 │
│   Beneficios:                                                   │
│   • Order Service no conoce a los consumidores                  │
│   • Cada servicio puede fallar independientemente               │
│   • Agregar servicio = suscribirse al evento                    │
│   • Order Service responde inmediatamente                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Message Brokers: Kafka vs RabbitMQ

| Aspecto | RabbitMQ | Kafka |
|---------|----------|-------|
| **Modelo** | Message Queue | Event Log |
| **Mensajes** | Se eliminan tras consumir | Se retienen (configurable) |
| **Casos de uso** | Task queues, RPC | Event streaming, analytics |
| **Orden** | Por cola | Por partición |
| **Throughput** | Medio-alto | Muy alto |
| **Complejidad** | Menor | Mayor |
| **Cuándo elegir** | La mayoría de aplicaciones | Alto volumen, replay de eventos |

💡 **Insight**: Para la mayoría de aplicaciones web, RabbitMQ (o incluso BullMQ con Redis) es suficiente. Kafka brilla cuando necesitas procesar millones de eventos por segundo o mantener un log inmutable de eventos.

### Implementación con RabbitMQ

```typescript
import amqp from 'amqplib';

// Publisher (Order Service)
class OrderEventPublisher {
  private channel: amqp.Channel;

  async connect() {
    const connection = await amqp.connect(process.env.RABBITMQ_URL!);
    this.channel = await connection.createChannel();

    // Declarar exchange de tipo "topic"
    await this.channel.assertExchange('orders', 'topic', { durable: true });
  }

  async publishOrderCreated(order: Order) {
    const event = {
      type: 'order.created',
      timestamp: new Date().toISOString(),
      data: {
        orderId: order.id,
        userId: order.userId,
        items: order.items,
        total: order.total
      }
    };

    this.channel.publish(
      'orders',
      'order.created',
      Buffer.from(JSON.stringify(event)),
      { persistent: true }
    );
  }
}

// Consumer (Email Service)
class EmailEventConsumer {
  async start() {
    const connection = await amqp.connect(process.env.RABBITMQ_URL!);
    const channel = await connection.createChannel();

    // Crear cola para este servicio
    const queue = await channel.assertQueue('email-service-orders', {
      durable: true
    });

    // Suscribirse a eventos de órdenes
    await channel.bindQueue(queue.queue, 'orders', 'order.*');

    // Procesar mensajes
    channel.consume(queue.queue, async (msg) => {
      if (!msg) return;

      try {
        const event = JSON.parse(msg.content.toString());

        if (event.type === 'order.created') {
          await this.handleOrderCreated(event.data);
        }

        channel.ack(msg);  // Confirmar procesamiento
      } catch (error) {
        // Rechazar y reencolar (o enviar a dead letter)
        channel.nack(msg, false, false);
      }
    });
  }

  private async handleOrderCreated(data: any) {
    await sendOrderConfirmationEmail(data.userId, data.orderId);
  }
}
```

### Dead Letter Queues

Cuando un mensaje falla repetidamente, va a una "cola de mensajes muertos" para análisis:

```typescript
// Configurar dead letter exchange
await channel.assertExchange('orders-dlx', 'direct', { durable: true });
await channel.assertQueue('orders-dead-letter', { durable: true });
await channel.bindQueue('orders-dead-letter', 'orders-dlx', '');

// Cola principal con dead letter configurado
await channel.assertQueue('email-service-orders', {
  durable: true,
  deadLetterExchange: 'orders-dlx',
  messageTtl: 86400000  // 24h antes de ir a DLQ
});
```

---

## CQRS y Event Sourcing (Introducción)

Estos son patrones avanzados. No los necesitas para la mayoría de aplicaciones, pero es importante saber cuándo considerarlos.

### CQRS: Command Query Responsibility Segregation

📖 **Concepto**: Separar el modelo de escritura (commands) del modelo de lectura (queries).

```
┌─────────────────────────────────────────────────────────────────┐
│                         CQRS                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TRADICIONAL (un modelo para todo):                            │
│   ──────────────────────────────────                            │
│                                                                 │
│   ┌─────────┐     ┌─────────────┐     ┌──────────┐              │
│   │ API     │────>│   Service   │────>│ Database │              │
│   │ (R + W) │<────│ (R + W)     │<────│ (1 tabla)│              │
│   └─────────┘     └─────────────┘     └──────────┘              │
│                                                                 │
│   CON CQRS (modelos separados):                                 │
│   ─────────────────────────────                                 │
│                                                                 │
│   Commands (escritura):                                         │
│   ┌─────────┐     ┌─────────────┐     ┌──────────┐              │
│   │ Command │────>│   Write     │────>│  Write   │              │
│   │ API     │     │   Model     │     │    DB    │              │
│   └─────────┘     └─────────────┘     └──────────┘              │
│                          │                                      │
│                          │ (eventos/sync)                       │
│                          ▼                                      │
│   Queries (lectura):                                            │
│   ┌─────────┐     ┌─────────────┐     ┌──────────┐              │
│   │ Query   │────>│   Read      │────>│   Read   │              │
│   │ API     │<────│   Model     │<────│    DB    │              │
│   └─────────┘     └─────────────┘     └──────────┘              │
│                                                                 │
│   El Read DB puede ser:                                         │
│   • Tabla desnormalizada optimizada para queries                │
│   • Elasticsearch para búsquedas                                │
│   • Cache en memoria                                            │
│   • Vista materializada                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Event Sourcing

📖 **Concepto**: En lugar de guardar el estado actual, guardas todos los eventos que llevaron a ese estado.

```
┌─────────────────────────────────────────────────────────────────┐
│                      EVENT SOURCING                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TRADICIONAL (guardar estado):                                 │
│   ─────────────────────────────                                 │
│                                                                 │
│   accounts table:                                               │
│   ┌────────┬─────────┐                                          │
│   │ id     │ balance │    Solo ves el estado actual             │
│   ├────────┼─────────┤    No sabes cómo llegó ahí               │
│   │ ACC-1  │ $150.00 │                                          │
│   └────────┴─────────┘                                          │
│                                                                 │
│   EVENT SOURCING (guardar eventos):                             │
│   ─────────────────────────────────                             │
│                                                                 │
│   events table:                                                 │
│   ┌────────┬──────────────────┬────────┬────────────────────┐   │
│   │ seq    │ type             │ data   │ timestamp          │   │
│   ├────────┼──────────────────┼────────┼────────────────────┤   │
│   │ 1      │ AccountCreated   │ ACC-1  │ 2025-01-01 10:00   │   │
│   │ 2      │ MoneyDeposited   │ $200   │ 2025-01-01 10:05   │   │
│   │ 3      │ MoneyWithdrawn   │ $50    │ 2025-01-02 14:30   │   │
│   └────────┴──────────────────┴────────┴────────────────────┘   │
│                                                                 │
│   Estado actual = replay de todos los eventos                   │
│   $0 + $200 - $50 = $150                                        │
│                                                                 │
│   Ventajas:                                                     │
│   • Auditoría completa (historial inmutable)                    │
│   • Debugging: "¿cómo llegamos a este estado?"                  │
│   • Replay: reconstruir estado en cualquier punto del tiempo    │
│   • Nuevas vistas: crear read models retroactivamente           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### ¿Cuándo usar CQRS / Event Sourcing?

```
┌─────────────────────────────────────────────────────────────────┐
│              ¿NECESITAS CQRS / EVENT SOURCING?                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ Considera CQRS si:                                          │
│  ─────────────────────                                          │
│  • Queries y commands tienen requisitos MUY diferentes          │
│  • Necesitas escalar lectura y escritura independientemente     │
│  • Tienes queries complejas que no encajan en tu modelo         │
│                                                                 │
│  ✅ Considera Event Sourcing si:                                │
│  ────────────────────────────────                               │
│  • Auditoría completa es requisito legal (finanzas, salud)      │
│  • Necesitas reconstruir estado histórico                       │
│  • El dominio es naturalmente basado en eventos                 │
│  • Necesitas derivar nuevas vistas de datos históricos          │
│                                                                 │
│  ❌ Probablemente NO necesitas si:                              │
│  ─────────────────────────────────                              │
│  • CRUD simple es suficiente                                    │
│  • No tienes requisitos especiales de auditoría                 │
│  • El equipo no tiene experiencia con el patrón                 │
│  • "Por si algún día lo necesitamos"                            │
│                                                                 │
│  ⚠️ Riesgos:                                                    │
│  ───────────                                                    │
│  • Curva de aprendizaje alta                                    │
│  • Event versioning es complejo                                 │
│  • Consistencia eventual puede ser difícil de manejar           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

💡 **Insight**: "CQRS y Event Sourcing resuelven problemas que quizás nunca tengas; CRUD con columnas de auditoría es suficiente la mayoría de las veces." Empieza simple y evoluciona solo cuando tengas evidencia de que lo necesitas.

---

## 🤖 Usando IA para Tareas Asíncronas

### Diseño de workers

```
Prompt: "Tengo un sistema de e-commerce que necesita:
- Enviar email de confirmación al crear orden
- Actualizar inventario
- Notificar al warehouse
- Generar factura PDF

¿Debería usar una cola para todo o colas separadas?
¿Cómo manejo si el servicio de email falla?"
```

La IA puede ayudar a diseñar la estructura de colas y estrategias de error handling.

### Debugging de jobs fallidos

```
Prompt: "Este job de BullMQ falla intermitentemente con este error:
[error log]. El job procesa webhooks de Stripe. ¿Qué podría
estar causando el problema y cómo lo depuro?"
```

### Limitaciones

⚠️ **La IA no puede:**
- Ver el estado actual de tus colas en producción
- Saber qué volumen de jobs procesas
- Conocer las características de tus servicios externos
- Debuggear race conditions sin contexto completo

Siempre complementa con métricas y logs reales.

---

## Resumen

- **Background jobs**: Mueve operaciones lentas fuera del request HTTP. BullMQ + Redis es el estándar en Node.js 2025.

- **Retry + Backoff**: Usa exponential backoff con jitter para fallas transitorias. Solo reintenta operaciones idempotentes.

- **Circuit Breaker**: Previene cascadas de fallas cortando llamadas a servicios que están fallando.

- **Event-Driven Architecture**: Desacopla servicios publicando eventos en lugar de hacer llamadas directas. RabbitMQ para la mayoría, Kafka para alto volumen.

- **CQRS/Event Sourcing**: Patrones avanzados para escenarios específicos. No los uses "por si acaso" — tienen costos significativos.

---

## Ejercicios

1. **Diseño de colas**: Tu aplicación permite a usuarios subir videos que se transcodifican a múltiples resoluciones. Diseña el sistema de colas: ¿cuántas colas? ¿cómo manejas si la transcodificación falla a la mitad? ¿cómo notificas al usuario cuando termina?

2. **Circuit breaker**: Tu servicio depende de una API de pagos externa. Implementa un circuit breaker que: abra después de 5 fallas consecutivas, cierre después de 30 segundos en half-open si hay 3 éxitos, y tenga un fallback que encole el pago para reintento.

3. **Event-driven refactor**: Tienes un `OrderService.createOrder()` que llama directamente a `InventoryService`, `PaymentService`, `EmailService` y `AnalyticsService`. Refactoriza para usar eventos. ¿Qué eventos publicarías? ¿Qué pasa si uno de los consumidores falla?

4. **¿CQRS o no?**: Tu sistema tiene un dashboard que muestra métricas agregadas de ventas por región, producto y período. Las queries son lentas porque agregan sobre millones de filas. ¿Aplicarías CQRS? ¿Cómo sincronizarías el read model?

---

## Referencias

- BullMQ. *Documentation*. https://docs.bullmq.io/
- Microsoft. *Circuit Breaker Pattern*. https://docs.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
- RabbitMQ. *Tutorials*. https://www.rabbitmq.com/getstarted.html
- Opossum. *Node.js Circuit Breaker*. https://nodeshift.dev/opossum/
- Fowler, M. *CQRS*. https://martinfowler.com/bliki/CQRS.html
- Event-Driven.io. *Event Sourcing with TypeScript and Node.js*. https://event-driven.io/en/type_script_node_js_event_sourcing/

---

**Anterior**: [Persistencia y Bases de Datos](./15-persistencia.md) | **Siguiente**: [Testing](./17-testing.md)
