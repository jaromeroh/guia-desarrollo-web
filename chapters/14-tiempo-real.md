# Capítulo 14: Comunicación y Datos en Tiempo Real

> "La web nació como un sistema de documentos estáticos. Hoy esperamos que las aplicaciones reaccionen instantáneamente. Entender cómo lograrlo es fundamental."

---

## 📖 El Problema: HTTP es Request-Response

HTTP fue diseñado para un modelo simple: el cliente pide, el servidor responde, conexión cerrada. Pero las aplicaciones modernas necesitan algo diferente:

```
Modelo HTTP Tradicional (1991):
──────────────────────────────

Cliente                          Servidor
   │                                │
   │──── GET /noticias ────────────>│
   │                                │
   │<─── HTML con noticias ─────────│
   │                                │
   │         (conexión cerrada)     │
   │                                │
   │    ... 5 minutos después ...   │
   │                                │
   │    📰 Nueva noticia publicada  │
   │                                │
   │    ¿Cómo se entera el cliente? │
   │    No hay forma automática 😕   │
```

**El problema**: El servidor no puede "llamar" al cliente. Solo puede responder cuando el cliente pregunta.

### Lo Que Queremos vs Lo Que HTTP Ofrece

```
┌─────────────────────────────────────────────────────────────────┐
│                    Aplicaciones Modernas                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  💬 Chat            "Necesito ver mensajes al instante"         │
│  📈 Trading         "Precios actualizados cada milisegundo"     │
│  🎮 Gaming          "Posiciones de otros jugadores en tiempo    │
│                      real"                                      │
│  📊 Dashboard       "Métricas que se actualizan solas"          │
│  🔔 Notificaciones  "Alertas push sin recargar"                 │
│  📝 Colaboración    "Ver qué escribe mi compañero"              │
│                                                                 │
│  Todas necesitan: SERVIDOR → CLIENTE (sin que el cliente pida) │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Las Soluciones: Del Más Simple al Más Sofisticado

```
┌─────────────────────────────────────────────────────────────────┐
│                    Espectro de Soluciones                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Simple                                              Complejo   │
│  ──────                                              ────────   │
│                                                                 │
│  Polling ──> Long Polling ──> SSE ──> WebSockets ──> WebTransport
│                                                                 │
│  "Pregunto     "Espero        "El servidor   "Conversación  "El futuro:
│   cada X        hasta que      me envía       bidireccional   UDP sobre
│   segundos"     haya algo"     updates"       continua"       HTTP/3"
│                                                                 │
│  Latencia:     Latencia:      Latencia:      Latencia:       Latencia:
│  Alta          Media          Baja           Muy baja        Mínima
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Polling: La Solución Ingenua

La idea más simple: preguntar repetidamente si hay algo nuevo.

```
┌─────────────────────────────────────────────────────────────────┐
│                         POLLING                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cliente                               Servidor                 │
│     │                                     │                     │
│     │── "¿Hay mensajes nuevos?" ─────────>│                     │
│     │<── "No" ────────────────────────────│                     │
│     │                                     │                     │
│     │    ⏰ Espera 5 segundos             │                     │
│     │                                     │                     │
│     │── "¿Hay mensajes nuevos?" ─────────>│                     │
│     │<── "No" ────────────────────────────│                     │
│     │                                     │                     │
│     │    ⏰ Espera 5 segundos             │                     │
│     │                                     │   📨 Llega mensaje  │
│     │── "¿Hay mensajes nuevos?" ─────────>│                     │
│     │<── "Sí: [mensaje]" ─────────────────│                     │
│     │                                     │                     │
│     │    ⏰ Espera 5 segundos             │                     │
│     │    ...                              │                     │
│                                                                 │
│  ❌ Problema: Hasta 5 segundos de latencia                      │
│  ❌ Problema: Muchos requests "vacíos" desperdiciados           │
│  ✅ Ventaja: Funciona en cualquier servidor HTTP                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ Implementación de Polling

```typescript
// Cliente: Polling simple
class PollingClient {
  private intervalId: number | null = null;

  start(intervalMs: number = 5000) {
    this.intervalId = setInterval(async () => {
      try {
        const response = await fetch('/api/messages/new');
        const data = await response.json();

        if (data.messages.length > 0) {
          this.onNewMessages(data.messages);
        }
      } catch (error) {
        console.error('Error polling:', error);
      }
    }, intervalMs);
  }

  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  onNewMessages(messages: Message[]) {
    // Procesar mensajes nuevos
    messages.forEach(msg => displayMessage(msg));
  }
}

// Uso
const poller = new PollingClient();
poller.start(3000); // Cada 3 segundos
```

```typescript
// Servidor: Endpoint para polling
app.get('/api/messages/new', async (req, res) => {
  const lastSeenId = req.query.since || 0;

  const newMessages = await db.message.findMany({
    where: {
      id: { gt: Number(lastSeenId) },
      recipientId: req.user.id,
    },
    orderBy: { createdAt: 'asc' },
  });

  res.json({
    messages: newMessages,
    lastId: newMessages.at(-1)?.id || lastSeenId,
  });
});
```

### ⚠️ Cuándo Usar Polling

| Escenario | ¿Polling? | Por qué |
|-----------|-----------|---------|
| Dashboard que actualiza cada minuto | ✅ Sí | Latencia aceptable, simple |
| Feed de noticias | ✅ Sí | No es crítico el tiempo real |
| Chat en vivo | ❌ No | Latencia inaceptable |
| Trading financiero | ❌ No | Milisegundos importan |
| Sistema legacy sin WebSockets | ✅ Sí | Única opción disponible |

---

## 📖 Long Polling: Polling Mejorado

La idea: el servidor **no responde hasta que tenga algo que decir**.

```
┌─────────────────────────────────────────────────────────────────┐
│                       LONG POLLING                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cliente                               Servidor                 │
│     │                                     │                     │
│     │── "¿Hay mensajes nuevos?" ─────────>│                     │
│     │                                     │                     │
│     │         (conexión abierta,          │                     │
│     │          servidor espera...)        │                     │
│     │                                     │                     │
│     │              ... 30 segundos ...    │   📨 Llega mensaje  │
│     │                                     │                     │
│     │<── "Sí: [mensaje]" ─────────────────│  (responde ahora)   │
│     │                                     │                     │
│     │── "¿Hay más?" ─────────────────────>│  (nueva conexión    │
│     │                                     │   inmediata)        │
│     │         (servidor espera...)        │                     │
│     │                                     │                     │
│                                                                 │
│  ✅ Ventaja: Latencia casi cero cuando hay datos                │
│  ✅ Ventaja: Menos requests que polling normal                  │
│  ❌ Problema: Conexiones abiertas consumen recursos             │
│  ❌ Problema: Timeout si no hay datos en X tiempo               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ Implementación de Long Polling

```typescript
// Cliente: Long Polling
async function longPoll(lastEventId: string = '0'): Promise<void> {
  try {
    const response = await fetch(`/api/events?since=${lastEventId}`, {
      // Timeout largo para esperar eventos
      signal: AbortSignal.timeout(30000),
    });

    if (response.ok) {
      const data = await response.json();

      if (data.events.length > 0) {
        data.events.forEach(handleEvent);
        lastEventId = data.lastEventId;
      }
    }
  } catch (error) {
    if (error.name === 'TimeoutError') {
      // Timeout normal, reconectar
      console.log('Timeout, reconnecting...');
    } else {
      // Error real, esperar antes de reintentar
      console.error('Error:', error);
      await sleep(5000);
    }
  }

  // Siempre reconectar
  longPoll(lastEventId);
}

// Iniciar
longPoll();
```

```typescript
// Servidor: Long Polling con Express
const waitingClients = new Map<string, Response>();

app.get('/api/events', async (req, res) => {
  const userId = req.user.id;
  const since = req.query.since || '0';

  // Verificar si hay eventos pendientes
  const pendingEvents = await getEventsSince(userId, since);

  if (pendingEvents.length > 0) {
    // Hay eventos, responder inmediatamente
    return res.json({
      events: pendingEvents,
      lastEventId: pendingEvents.at(-1).id,
    });
  }

  // No hay eventos, guardar conexión para responder después
  waitingClients.set(userId, res);

  // Timeout después de 30 segundos
  const timeout = setTimeout(() => {
    waitingClients.delete(userId);
    res.json({ events: [], lastEventId: since });
  }, 30000);

  // Limpiar si el cliente se desconecta
  req.on('close', () => {
    clearTimeout(timeout);
    waitingClients.delete(userId);
  });
});

// Cuando hay un nuevo evento, notificar al cliente esperando
async function notifyUser(userId: string, event: Event) {
  const waitingResponse = waitingClients.get(userId);

  if (waitingResponse) {
    waitingClients.delete(userId);
    waitingResponse.json({
      events: [event],
      lastEventId: event.id,
    });
  }
}
```

---

## 📖 Server-Sent Events (SSE): El Servidor Empuja

SSE es un estándar del navegador para recibir un **stream de eventos del servidor**. Simple, eficiente, y usa HTTP normal.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SERVER-SENT EVENTS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cliente                               Servidor                 │
│     │                                     │                     │
│     │── GET /events ─────────────────────>│                     │
│     │   Accept: text/event-stream         │                     │
│     │                                     │                     │
│     │<── HTTP 200 ────────────────────────│                     │
│     │    Content-Type: text/event-stream  │                     │
│     │                                     │                     │
│     │<── data: {"price": 100} ────────────│  (evento 1)         │
│     │                                     │                     │
│     │<── data: {"price": 101} ────────────│  (evento 2)         │
│     │                                     │                     │
│     │<── data: {"price": 99} ─────────────│  (evento 3)         │
│     │                                     │                     │
│     │    ... conexión permanece abierta   │                     │
│     │    ... servidor envía cuando quiera │                     │
│                                                                 │
│  ✅ Reconexión automática del navegador                         │
│  ✅ Usa HTTP estándar (funciona con proxies, CDNs)              │
│  ✅ Simple de implementar                                       │
│  ❌ Solo servidor → cliente (unidireccional)                    │
│  ❌ Solo texto (no binario)                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ Implementación de SSE

```typescript
// Cliente: EventSource API nativa del navegador
const eventSource = new EventSource('/api/events/stream');

// Evento por defecto (sin nombre)
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Mensaje:', data);
};

// Eventos con nombre específico
eventSource.addEventListener('price-update', (event) => {
  const { symbol, price } = JSON.parse(event.data);
  updatePriceDisplay(symbol, price);
});

eventSource.addEventListener('notification', (event) => {
  const notification = JSON.parse(event.data);
  showNotification(notification);
});

// Manejo de errores y reconexión
eventSource.onerror = (error) => {
  console.error('SSE error:', error);
  // El navegador reconecta automáticamente
};

// Cerrar conexión cuando no se necesite
function disconnect() {
  eventSource.close();
}
```

```typescript
// Servidor: SSE con Express
app.get('/api/events/stream', (req, res) => {
  // Headers para SSE
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Deshabilitar buffering (importante para nginx)
  res.setHeader('X-Accel-Buffering', 'no');

  // Enviar comentario inicial para establecer conexión
  res.write(':ok\n\n');

  const userId = req.user.id;

  // Función para enviar eventos
  const sendEvent = (eventName: string, data: unknown) => {
    res.write(`event: ${eventName}\n`);
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  };

  // Registrar este cliente
  const clientId = addSSEClient(userId, sendEvent);

  // Enviar heartbeat cada 30 segundos (mantiene conexión viva)
  const heartbeat = setInterval(() => {
    res.write(':heartbeat\n\n');
  }, 30000);

  // Limpiar cuando el cliente se desconecta
  req.on('close', () => {
    clearInterval(heartbeat);
    removeSSEClient(clientId);
  });
});

// Gestión de clientes SSE conectados
const sseClients = new Map<string, { userId: string; send: Function }>();

function addSSEClient(userId: string, send: Function): string {
  const clientId = crypto.randomUUID();
  sseClients.set(clientId, { userId, send });
  return clientId;
}

function removeSSEClient(clientId: string) {
  sseClients.delete(clientId);
}

// Enviar evento a un usuario específico
function sendToUser(userId: string, eventName: string, data: unknown) {
  for (const [, client] of sseClients) {
    if (client.userId === userId) {
      client.send(eventName, data);
    }
  }
}

// Enviar a todos los clientes (broadcast)
function broadcast(eventName: string, data: unknown) {
  for (const [, client] of sseClients) {
    client.send(eventName, data);
  }
}

// Uso: cuando hay una actualización de precio
priceService.onPriceChange((symbol, price) => {
  broadcast('price-update', { symbol, price, timestamp: Date.now() });
});
```

### Formato del Protocolo SSE

```
// Formato del stream SSE

// Evento sin nombre (usa onmessage)
data: {"mensaje": "Hola mundo"}

// Evento con nombre (usa addEventListener)
event: notification
data: {"tipo": "info", "texto": "Nuevo usuario"}

// Evento con ID (para reconexión)
id: 12345
event: message
data: {"texto": "Hola"}

// Datos multilínea
data: {"linea1": "valor1",
data:  "linea2": "valor2"}

// Comentario (ignorado, útil para heartbeat)
:esto es un comentario

// Cada mensaje termina con doble newline
```

### 💡 SSE con HTTP/2: Sin Límite de Conexiones

```
HTTP/1.1: Límite de ~6 conexiones por dominio
          Si tienes 6 tabs abiertas con SSE, bloqueas TODO

HTTP/2:   Multiplexado - todas las conexiones SSE comparten
          una sola conexión TCP
          ✅ Ya no hay límite práctico
```

---

## 📖 WebSockets: Comunicación Bidireccional

WebSockets establecen una conexión **persistente y bidireccional**. Ambos lados pueden enviar mensajes en cualquier momento.

```
┌─────────────────────────────────────────────────────────────────┐
│                       WEBSOCKETS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cliente                               Servidor                 │
│     │                                     │                     │
│     │── GET /chat (Upgrade: websocket) ──>│                     │
│     │<── 101 Switching Protocols ─────────│                     │
│     │                                     │                     │
│     │═══════════════════════════════════════  (WebSocket abierto)
│     │                                     │                     │
│     │──> "Hola, soy Ana" ─────────────────│                     │
│     │                                     │                     │
│     │<── "Ana se ha conectado" ───────────│  (a todos)          │
│     │                                     │                     │
│     │<── "Hola Ana!" ─────────────────────│  (de otro usuario)  │
│     │                                     │                     │
│     │──> "¿Cómo están?" ──────────────────│                     │
│     │                                     │                     │
│     │<── "Usuario X está escribiendo..." ─│                     │
│     │                                     │                     │
│     │══════════════════════════════════════                     │
│                                                                 │
│  ✅ Bidireccional: cliente ↔ servidor                           │
│  ✅ Baja latencia (conexión persistente)                        │
│  ✅ Soporta binario y texto                                     │
│  ❌ Más complejo de escalar (estado en servidor)                │
│  ❌ No reconecta automáticamente                                │
│  ❌ Algunos proxies/firewalls lo bloquean                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ Implementación con WebSocket Nativo

```typescript
// Cliente: WebSocket API nativa
class ChatClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect() {
    this.ws = new WebSocket('wss://api.myapp.com/chat');

    this.ws.onopen = () => {
      console.log('Conectado');
      this.reconnectAttempts = 0;

      // Autenticarse
      this.send({
        type: 'auth',
        token: getAuthToken(),
      });
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = (event) => {
      console.log('Desconectado:', event.code, event.reason);
      this.attemptReconnect();
    };
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

      console.log(`Reconectando en ${delay}ms...`);
      setTimeout(() => this.connect(), delay);
    } else {
      console.error('Máximo de reconexiones alcanzado');
    }
  }

  send(data: object) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  private handleMessage(message: any) {
    switch (message.type) {
      case 'chat':
        displayChatMessage(message);
        break;
      case 'typing':
        showTypingIndicator(message.userId);
        break;
      case 'presence':
        updateUserPresence(message.userId, message.status);
        break;
    }
  }

  disconnect() {
    this.maxReconnectAttempts = 0; // Prevenir reconexión
    this.ws?.close();
  }
}
```

```typescript
// Servidor: WebSocket con ws (Node.js)
import { WebSocketServer, WebSocket } from 'ws';
import { createServer } from 'http';

const server = createServer(app);
const wss = new WebSocketServer({ server });

// Mapa de usuarios conectados
const clients = new Map<string, WebSocket>();

wss.on('connection', (ws, req) => {
  let userId: string | null = null;

  ws.on('message', async (data) => {
    try {
      const message = JSON.parse(data.toString());

      switch (message.type) {
        case 'auth':
          // Verificar token y obtener usuario
          const user = await verifyToken(message.token);
          if (user) {
            userId = user.id;
            clients.set(userId, ws);

            // Notificar a otros que este usuario está online
            broadcast({
              type: 'presence',
              userId,
              status: 'online',
            }, userId);
          } else {
            ws.close(4001, 'Unauthorized');
          }
          break;

        case 'chat':
          if (!userId) return;

          const chatMessage = {
            type: 'chat',
            from: userId,
            text: message.text,
            timestamp: Date.now(),
          };

          // Guardar en DB
          await saveMessage(chatMessage);

          // Enviar a todos (o a un canal específico)
          broadcast(chatMessage);
          break;

        case 'typing':
          if (!userId) return;

          broadcast({
            type: 'typing',
            userId,
            channelId: message.channelId,
          }, userId);
          break;
      }
    } catch (error) {
      console.error('Error procesando mensaje:', error);
    }
  });

  ws.on('close', () => {
    if (userId) {
      clients.delete(userId);

      // Notificar que el usuario se fue
      broadcast({
        type: 'presence',
        userId,
        status: 'offline',
      });
    }
  });

  // Heartbeat para detectar conexiones muertas
  ws.on('pong', () => {
    (ws as any).isAlive = true;
  });
});

// Ping periódico para detectar clientes desconectados
setInterval(() => {
  wss.clients.forEach((ws) => {
    if ((ws as any).isAlive === false) {
      return ws.terminate();
    }
    (ws as any).isAlive = false;
    ws.ping();
  });
}, 30000);

function broadcast(message: object, excludeUserId?: string) {
  const data = JSON.stringify(message);

  for (const [id, client] of clients) {
    if (id !== excludeUserId && client.readyState === WebSocket.OPEN) {
      client.send(data);
    }
  }
}

function sendToUser(userId: string, message: object) {
  const client = clients.get(userId);
  if (client?.readyState === WebSocket.OPEN) {
    client.send(JSON.stringify(message));
  }
}
```

### 🛠️ Socket.IO: WebSockets con Superpoderes

Socket.IO añade funcionalidades útiles sobre WebSockets:

```typescript
// Servidor: Socket.IO
import { Server } from 'socket.io';

const io = new Server(server, {
  cors: {
    origin: 'https://myapp.com',
    methods: ['GET', 'POST'],
  },
});

// Middleware de autenticación
io.use(async (socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const user = await verifyToken(token);
    socket.data.user = user;
    next();
  } catch {
    next(new Error('Authentication error'));
  }
});

io.on('connection', (socket) => {
  const user = socket.data.user;
  console.log(`${user.name} conectado`);

  // Unirse a "rooms" (canales)
  socket.join(`user:${user.id}`);
  socket.join('general');

  // Escuchar eventos
  socket.on('chat:message', async (data) => {
    const message = {
      from: user.id,
      text: data.text,
      room: data.room,
      timestamp: Date.now(),
    };

    await saveMessage(message);

    // Enviar a todos en el room
    io.to(data.room).emit('chat:message', message);
  });

  socket.on('chat:typing', (data) => {
    // Enviar a todos EXCEPTO el que envía
    socket.to(data.room).emit('chat:typing', {
      userId: user.id,
      userName: user.name,
    });
  });

  socket.on('disconnect', () => {
    console.log(`${user.name} desconectado`);
    io.emit('user:offline', { userId: user.id });
  });
});

// Enviar a un usuario específico desde cualquier parte del código
function notifyUser(userId: string, event: string, data: any) {
  io.to(`user:${userId}`).emit(event, data);
}
```

```typescript
// Cliente: Socket.IO
import { io } from 'socket.io-client';

const socket = io('https://api.myapp.com', {
  auth: {
    token: getAuthToken(),
  },
  reconnection: true,           // ✅ Reconexión automática
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
});

socket.on('connect', () => {
  console.log('Conectado con ID:', socket.id);
});

socket.on('chat:message', (message) => {
  displayMessage(message);
});

socket.on('chat:typing', (data) => {
  showTypingIndicator(data.userName);
});

// Emitir eventos
function sendMessage(room: string, text: string) {
  socket.emit('chat:message', { room, text });
}

function startTyping(room: string) {
  socket.emit('chat:typing', { room });
}

// Socket.IO tiene "acknowledgements" para confirmar recepción
socket.emit('chat:message', { room: 'general', text: 'Hola' }, (response) => {
  if (response.ok) {
    console.log('Mensaje entregado');
  }
});
```

### Alternativas a Socket.IO (2025)

| Librería | Tipo | Ideal para |
|----------|------|------------|
| **ws** | Self-hosted | Control total, Node.js puro |
| **Socket.IO** | Self-hosted | Features out-of-the-box, rooms |
| **Ably** | Managed | Escala global, sin infraestructura |
| **Pusher** | Managed | Simple, buen free tier |
| **Azure Web PubSub** | Managed | Ecosistema Microsoft |
| **SocketCluster** | Self-hosted | Multi-proceso, alta escala |

---

## 📖 WebTransport: El Futuro (HTTP/3)

WebTransport es el sucesor de WebSockets, construido sobre HTTP/3 y QUIC. Ofrece ventajas significativas pero aún tiene soporte limitado.

```
┌─────────────────────────────────────────────────────────────────┐
│                      WEBTRANSPORT                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WebSockets (TCP)              WebTransport (QUIC/UDP)          │
│  ─────────────────             ───────────────────────          │
│                                                                 │
│  • Un solo stream ordenado     • Múltiples streams paralelos    │
│  • Head-of-line blocking       • Sin head-of-line blocking      │
│  • Solo entrega confiable      • Confiable O best-effort        │
│  • Handshake TCP+TLS lento     • 0-RTT connection setup         │
│                                                                 │
│  Soporte navegadores (2025):                                    │
│  ✅ Chrome, Edge                                                │
│  ⚠️ Firefox (en desarrollo)                                     │
│  ❌ Safari (no soportado)                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ Ejemplo de WebTransport

```typescript
// Cliente: WebTransport API (experimental)
async function connectWebTransport() {
  const transport = new WebTransport('https://api.myapp.com/webtransport');

  await transport.ready;
  console.log('WebTransport conectado');

  // Stream bidireccional (como WebSocket)
  const stream = await transport.createBidirectionalStream();
  const writer = stream.writable.getWriter();
  const reader = stream.readable.getReader();

  // Enviar mensaje
  await writer.write(new TextEncoder().encode('Hola servidor'));

  // Leer respuesta
  const { value } = await reader.read();
  console.log('Respuesta:', new TextDecoder().decode(value));

  // Datagrams: envío no confiable pero ultra-rápido (ideal para gaming)
  const datagramWriter = transport.datagrams.writable.getWriter();
  await datagramWriter.write(new Uint8Array([1, 2, 3, 4]));

  transport.closed.then(() => {
    console.log('Conexión cerrada');
  });
}
```

### ⚠️ ¿Cuándo Usar WebTransport?

**Hoy (2025)**: Solo si tu audiencia es mayormente Chrome/Edge Y necesitas:
- Gaming multiplayer con baja latencia
- Streaming de video/audio custom
- IoT con muchos mensajes pequeños

**Para la mayoría**: Sigue usando WebSockets o SSE.

---

## 📖 Comparativa: ¿Cuál Elegir?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GUÍA DE DECISIÓN                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ¿Necesitas comunicación servidor → cliente únicamente?                     │
│  │                                                                          │
│  ├── SÍ ──> ¿Con qué frecuencia?                                            │
│  │          │                                                               │
│  │          ├── Cada minuto o más ──────────────> POLLING                   │
│  │          │                                                               │
│  │          └── Tiempo real (segundos) ─────────> SSE                       │
│  │                                                                          │
│  └── NO (bidireccional) ──> ¿Qué tipo de datos?                             │
│                             │                                               │
│                             ├── Solo texto ──────────> WebSockets o SSE+POST│
│                             │                                               │
│                             └── Binario/Gaming ──────> WebSockets           │
│                                                        (o WebTransport)     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Tabla Comparativa

| Característica | Polling | Long Polling | SSE | WebSockets | WebTransport |
|----------------|---------|--------------|-----|------------|--------------|
| **Dirección** | Cliente→Server | Cliente→Server | Server→Cliente | Bidireccional | Bidireccional |
| **Latencia** | Alta | Media | Baja | Muy baja | Mínima |
| **Binario** | ✅ (base64) | ✅ (base64) | ❌ | ✅ | ✅ |
| **Reconexión auto** | Manual | Manual | ✅ | Manual | Manual |
| **Complejidad** | Baja | Media | Baja | Media | Alta |
| **Escala** | Fácil | Media | Fácil | Difícil | Media |
| **HTTP/2 friendly** | ✅ | ✅ | ✅✅ | ❌ | ✅✅✅ |
| **Soporte** | Universal | Universal | Universal* | Universal | Chrome/Edge |

*SSE no soportado en IE11 (irrelevante en 2025)

### Casos de Uso Reales

| Aplicación | Tecnología | Por qué |
|------------|------------|---------|
| **Slack/Discord** | WebSockets | Bidireccional, typing indicators |
| **Twitter/X feed** | SSE o Polling | Unidireccional, escala masiva |
| **Google Docs** | WebSockets + OT | Colaboración en tiempo real |
| **Crypto prices** | SSE | Unidireccional, muchos updates |
| **Uber mapa** | WebSockets | Posición GPS bidireccional |
| **YouTube Live chat** | Long Polling/SSE | Escala, mayormente unidireccional |
| **Fortnite** | UDP/WebTransport | Gaming requiere ultra-baja latencia |

---

## 📖 Escalando Conexiones en Tiempo Real

El desafío: cada conexión WebSocket/SSE consume recursos del servidor.

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROBLEMA DE ESCALA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1 servidor con WebSockets:                                     │
│                                                                 │
│  [Servidor 1]                                                   │
│      │                                                          │
│      ├── Usuario A (conectado)                                  │
│      ├── Usuario B (conectado)                                  │
│      └── Usuario C (conectado)                                  │
│                                                                 │
│  Si A envía mensaje a B: ✅ Fácil, ambos en mismo servidor      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  3 servidores con load balancer:                                │
│                                                                 │
│  [Load Balancer]                                                │
│      │                                                          │
│      ├── [Servidor 1] ── Usuario A                              │
│      ├── [Servidor 2] ── Usuario B                              │
│      └── [Servidor 3] ── Usuario C                              │
│                                                                 │
│  Si A envía mensaje a B: ❌ Están en servidores diferentes!     │
│                                                                 │
│  Solución: Sistema de mensajería entre servidores (Redis PubSub)│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ Escalando con Redis Pub/Sub

```typescript
// Adaptador de Socket.IO con Redis
import { Server } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

const io = new Server(server);

// Usar Redis como "puente" entre servidores
io.adapter(createAdapter(pubClient, subClient));

// Ahora io.emit() llegará a TODOS los clientes,
// sin importar a qué servidor estén conectados
io.on('connection', (socket) => {
  socket.on('chat:message', (data) => {
    // Esto se propaga automáticamente a todos los servidores
    io.to(data.room).emit('chat:message', data);
  });
});
```

```
Con Redis Adapter:

[Servidor 1] ←──┐
     │          │
     │      [Redis PubSub]
     │          │
[Servidor 2] ←──┤
     │          │
[Servidor 3] ←──┘

Usuario A (Server 1) envía mensaje:
1. Server 1 publica en Redis
2. Redis distribuye a Server 2 y 3
3. Todos los servidores emiten a sus clientes
4. Usuario B (Server 2) recibe el mensaje ✅
```

---

## 🤖 IA en Comunicación en Tiempo Real

### Streaming de Respuestas de LLM

```typescript
// SSE es perfecto para streaming de respuestas de IA

// Servidor
app.get('/api/ai/chat', async (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');

  const prompt = req.query.prompt as string;

  try {
    const stream = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
      stream: true,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content;
      if (content) {
        res.write(`data: ${JSON.stringify({ content })}\n\n`);
      }
    }

    res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
    res.end();
  } catch (error) {
    res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
    res.end();
  }
});

// Cliente
const eventSource = new EventSource(`/api/ai/chat?prompt=${encodeURIComponent(prompt)}`);

let fullResponse = '';

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.done) {
    eventSource.close();
    return;
  }

  if (data.content) {
    fullResponse += data.content;
    updateChatUI(fullResponse);  // Actualiza en tiempo real como ChatGPT
  }
};
```

### Detección de Actividad Sospechosa

```typescript
// Analizar patrones de conexión en tiempo real
class ConnectionMonitor {
  private connectionHistory = new Map<string, number[]>();

  onNewConnection(userId: string, ip: string) {
    const now = Date.now();
    const key = `${userId}:${ip}`;

    if (!this.connectionHistory.has(key)) {
      this.connectionHistory.set(key, []);
    }

    const history = this.connectionHistory.get(key)!;
    history.push(now);

    // Mantener solo últimos 5 minutos
    const fiveMinutesAgo = now - 5 * 60 * 1000;
    const recent = history.filter(t => t > fiveMinutesAgo);
    this.connectionHistory.set(key, recent);

    // Detectar patrones sospechosos
    if (recent.length > 50) {
      // Más de 50 conexiones en 5 minutos = posible ataque
      this.flagSuspiciousActivity(userId, ip, 'rapid_reconnection');
    }
  }

  private async flagSuspiciousActivity(
    userId: string,
    ip: string,
    reason: string
  ) {
    await alertSecurityTeam({
      type: 'suspicious_ws_activity',
      userId,
      ip,
      reason,
      timestamp: new Date(),
    });

    // Opcionalmente, rate limit este usuario
    await rateLimiter.penalize(userId);
  }
}
```

---

## 💡 Insights Clave

1. **SSE para el 90% de los casos** - Si solo necesitas push del servidor (notificaciones, feeds, precios), SSE es más simple y escala mejor que WebSockets.

2. **WebSockets solo cuando necesitas bidireccional** - Chat, gaming, colaboración. No uses WebSockets "porque sí".

3. **Long Polling como fallback** - Algunos entornos corporativos bloquean WebSockets. Tener fallback es buena práctica.

4. **Redis Pub/Sub para escalar** - No reinventes el wheel. Usa adaptadores probados como `@socket.io/redis-adapter`.

5. **Heartbeats son obligatorios** - Las conexiones mueren silenciosamente. Sin ping/pong, tendrás "fantasmas".

6. **WebTransport es el futuro, no el presente** - Espera mejor soporte antes de adoptarlo en producción.

---

## 📚 Referencias

- [MDN: Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [MDN: WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Socket.IO Documentation](https://socket.io/docs/v4/)
- [WebTransport Explainer](https://web.dev/webtransport/)
- [Scaling WebSockets](https://ably.com/topic/scaling-websockets)

---

## Navegación

- [← Capítulo 13: Autenticación y Autorización](./13-autenticacion-autorizacion.md)
- [→ Capítulo 15: Persistencia y Bases de Datos](./15-persistencia.md)
- [Índice](../README.md)
