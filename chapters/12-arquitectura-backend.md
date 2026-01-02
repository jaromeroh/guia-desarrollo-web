# 12. Arquitectura Backend

> "El backend es donde la magia sucede y donde los problemas se esconden."

---

## Objetivos de Aprendizaje

Al finalizar este capítulo, serás capaz de:

- Diseñar una arquitectura backend en capas clara y mantenible
- Implementar el patrón Controller-Service-Repository
- Aplicar inyección de dependencias para código testeable
- Manejar errores de forma consistente y útil
- Implementar logging estructurado para observabilidad

---

## La Arquitectura en Capas

El backend de una aplicación web moderna se organiza en **capas**, donde cada una tiene una responsabilidad específica y solo conoce a las capas adyacentes.

### El problema del código mezclado

Considera este endpoint típico de un desarrollador principiante:

```javascript
// ❌ Todo mezclado: HTTP, lógica de negocio, base de datos
app.post('/users', async (req, res) => {
  try {
    const { email, password, name } = req.body;

    // Validación mezclada con la ruta
    if (!email || !email.includes('@')) {
      return res.status(400).json({ error: 'Email inválido' });
    }

    // Lógica de negocio mezclada
    const existingUser = await db.query(
      'SELECT id FROM users WHERE email = $1',
      [email]
    );
    if (existingUser.rows.length > 0) {
      return res.status(409).json({ error: 'Email ya registrado' });
    }

    // Hash del password mezclado con todo lo demás
    const hashedPassword = await bcrypt.hash(password, 10);

    // SQL directo en el controller
    const result = await db.query(
      'INSERT INTO users (email, password, name) VALUES ($1, $2, $3) RETURNING *',
      [email, hashedPassword, name]
    );

    // Envío de email mezclado
    await sendWelcomeEmail(email, name);

    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.log(error); // Logging pobre
    res.status(500).json({ error: 'Error interno' });
  }
});
```

Este código funciona, pero tiene problemas graves:

- **Imposible de testear** sin levantar un servidor HTTP
- **Difícil de modificar** — cambiar la base de datos requiere tocar las rutas
- **Sin reutilización** — la lógica de negocio no se puede usar desde otro lugar
- **Errores inconsistentes** — cada endpoint maneja errores diferente

### La solución: separación en capas

```
┌─────────────────────────────────────────────────────────┐
│                   CAPA DE PRESENTACIÓN                  │
│         Controllers / Rutas / Middleware HTTP           │
│    Responsabilidad: Recibir requests, enviar responses  │
├─────────────────────────────────────────────────────────┤
│                   CAPA DE APLICACIÓN                    │
│                       Services                          │
│     Responsabilidad: Orquestar lógica de negocio        │
├─────────────────────────────────────────────────────────┤
│                    CAPA DE DOMINIO                      │
│              Entidades / Reglas de negocio              │
│    Responsabilidad: Modelar el problema del negocio     │
├─────────────────────────────────────────────────────────┤
│                 CAPA DE INFRAESTRUCTURA                 │
│           Repositories / APIs externas / DB             │
│    Responsabilidad: Comunicación con sistemas externos  │
└─────────────────────────────────────────────────────────┘
```

**Regla de oro**: Las dependencias van hacia abajo. La capa de presentación conoce a la de aplicación, pero la de aplicación NO conoce a la de presentación.

---

## Controllers, Services, Repositories

Este es el patrón más común para organizar código backend. Veamos cada componente:

### Controllers (Capa de Presentación)

El controller es el **punto de entrada HTTP**. Su única responsabilidad es:

1. Recibir el request
2. Extraer y validar datos de entrada
3. Llamar al service correspondiente
4. Transformar el resultado en un response HTTP

```typescript
// controllers/UserController.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/UserService';
import { CreateUserDto } from '../dtos/CreateUserDto';

export class UserController {
  constructor(private userService: UserService) {}

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      // 1. Extraer datos del request
      const dto: CreateUserDto = req.body;

      // 2. Delegar al service
      const user = await this.userService.createUser(dto);

      // 3. Responder con formato HTTP apropiado
      res.status(201).json({
        data: user,
        message: 'Usuario creado exitosamente'
      });
    } catch (error) {
      // 4. Pasar errores al middleware de manejo de errores
      next(error);
    }
  }

  async findById(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const user = await this.userService.findById(id);

      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  }
}
```

**Lo que NO debe hacer un controller:**
- Contener lógica de negocio
- Acceder directamente a la base de datos
- Conocer detalles de implementación de otras capas

### Services (Capa de Aplicación)

El service contiene la **lógica de negocio**. Orquesta operaciones y aplica reglas:

```typescript
// services/UserService.ts
import { UserRepository } from '../repositories/UserRepository';
import { EmailService } from './EmailService';
import { CreateUserDto } from '../dtos/CreateUserDto';
import { User } from '../entities/User';
import {
  UserAlreadyExistsError,
  InvalidPasswordError
} from '../errors/UserErrors';

export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(dto: CreateUserDto): Promise<User> {
    // Regla de negocio: email debe ser único
    const existingUser = await this.userRepository.findByEmail(dto.email);
    if (existingUser) {
      throw new UserAlreadyExistsError(dto.email);
    }

    // Regla de negocio: password debe tener mínimo 8 caracteres
    if (dto.password.length < 8) {
      throw new InvalidPasswordError('Password debe tener mínimo 8 caracteres');
    }

    // Crear usuario (el hash del password es responsabilidad del repository o de una utilidad)
    const user = await this.userRepository.create({
      email: dto.email,
      password: dto.password,
      name: dto.name
    });

    // Efecto secundario: enviar email de bienvenida
    await this.emailService.sendWelcomeEmail(user.email, user.name);

    return user;
  }

  async findById(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new UserNotFoundError(id);
    }
    return user;
  }

  async updateEmail(userId: string, newEmail: string): Promise<User> {
    // Regla de negocio: no puede cambiar a un email que ya existe
    const existingUser = await this.userRepository.findByEmail(newEmail);
    if (existingUser && existingUser.id !== userId) {
      throw new UserAlreadyExistsError(newEmail);
    }

    return this.userRepository.updateEmail(userId, newEmail);
  }
}
```

**Lo que hace un service:**
- Implementa reglas de negocio
- Orquesta múltiples repositories
- Maneja transacciones
- Dispara efectos secundarios (emails, notificaciones)

**Lo que NO debe hacer un service:**
- Conocer detalles de HTTP (status codes, headers)
- Escribir SQL directamente
- Tener lógica de presentación

### Repositories (Capa de Infraestructura)

El repository es una **abstracción sobre el almacenamiento de datos**:

```typescript
// repositories/UserRepository.ts
import { Pool } from 'pg';
import { User } from '../entities/User';
import bcrypt from 'bcrypt';

export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserData): Promise<User>;
  updateEmail(id: string, email: string): Promise<User>;
}

export class PostgresUserRepository implements IUserRepository {
  constructor(private db: Pool) {}

  async findById(id: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT id, email, name, created_at FROM users WHERE id = $1',
      [id]
    );

    if (result.rows.length === 0) return null;

    return this.mapToUser(result.rows[0]);
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT id, email, name, created_at FROM users WHERE email = $1',
      [email]
    );

    if (result.rows.length === 0) return null;

    return this.mapToUser(result.rows[0]);
  }

  async create(data: CreateUserData): Promise<User> {
    const hashedPassword = await bcrypt.hash(data.password, 10);

    const result = await this.db.query(
      `INSERT INTO users (email, password, name)
       VALUES ($1, $2, $3)
       RETURNING id, email, name, created_at`,
      [data.email, hashedPassword, data.name]
    );

    return this.mapToUser(result.rows[0]);
  }

  private mapToUser(row: any): User {
    return {
      id: row.id,
      email: row.email,
      name: row.name,
      createdAt: row.created_at
    };
  }
}
```

**Por qué usar interfaces:**

```typescript
// En tests, puedes usar un repository fake
class InMemoryUserRepository implements IUserRepository {
  private users: User[] = [];

  async findById(id: string): Promise<User | null> {
    return this.users.find(u => u.id === id) || null;
  }

  async create(data: CreateUserData): Promise<User> {
    const user = { id: uuid(), ...data, createdAt: new Date() };
    this.users.push(user);
    return user;
  }

  // ... otros métodos
}
```

Con la interfaz `IUserRepository`, el service no sabe si está hablando con PostgreSQL, MongoDB, o un array en memoria. Esto hace el código **testeable** y **flexible**.

---

## Inyección de Dependencias

La inyección de dependencias (DI) es el patrón que hace que todo esto funcione junto. Es un concepto simple pero transformador.

### ¿Qué es una dependencia?

Una **dependencia** es cualquier objeto que tu código necesita para funcionar. Si tu `UserService` necesita acceder a la base de datos, entonces el `UserRepository` es una dependencia del `UserService`.

```typescript
class UserService {
  // UserRepository es una DEPENDENCIA de UserService
  // UserService no puede funcionar sin él
}
```

### ¿Qué significa "inyectar"?

**Inyectar** significa pasar algo desde afuera en lugar de crearlo adentro.

Piensa en un auto: el auto necesita combustible para funcionar (el combustible es una dependencia). Hay dos formas de obtenerlo:

1. **Sin inyección**: El auto tiene una refinería de petróleo adentro y fabrica su propio combustible
2. **Con inyección**: Alguien llena el tanque desde afuera

Obviamente la segunda opción es mejor. El auto no necesita saber cómo se fabrica el combustible, solo lo recibe y lo usa.

### La analogía en código

```typescript
// ❌ SIN inyección: la clase crea sus propias dependencias
class UserService {
  private repository = new PostgresRepository();  // Crea su dependencia internamente

  // Problemas:
  // - Si quiero usar MongoDB, tengo que modificar UserService
  // - Si quiero testear, necesito una base de datos PostgreSQL real
  // - UserService "sabe demasiado" sobre cómo se crea el repository
}

// ✅ CON inyección: la clase recibe sus dependencias
class UserService {
  constructor(private repository: IRepository) {}  // Recibe su dependencia

  // Ventajas:
  // - Puedo pasar PostgresRepository, MongoRepository, o un mock
  // - Para testear, paso un fake que no necesita base de datos
  // - UserService solo sabe que necesita "algo que cumpla IRepository"
}
```

### El principio detrás: Inversión de Control

La inyección de dependencias implementa el principio de **Inversión de Control (IoC)**:

> "No llames, te llamaremos" — Hollywood Principle

Sin IoC:
```
UserService → crea → PostgresRepository
(UserService controla qué repository usar)
```

Con IoC:
```
Main/Container → crea → PostgresRepository
                      ↓ inyecta en
                  UserService
(Algo externo controla qué repository usar)
```

El control se **invierte**: ya no es `UserService` quien decide qué repository usar, sino algo externo (el "contenedor" o el código de inicialización).

### ¿Por qué esto importa?

| Sin DI | Con DI |
|--------|--------|
| Difícil de testear | Fácil de testear con mocks |
| Acoplamiento fuerte | Acoplamiento débil |
| Cambiar implementación = modificar código | Cambiar implementación = cambiar configuración |
| Las clases saben demasiado | Las clases solo conocen interfaces |

### El problema sin DI (ejemplo concreto)

```typescript
// ❌ Sin inyección de dependencias
class UserService {
  private userRepository = new PostgresUserRepository(getDbConnection());
  private emailService = new SendGridEmailService(process.env.SENDGRID_KEY);

  // El service crea sus propias dependencias
  // Imposible testear sin una base de datos real
  // Imposible cambiar implementaciones
}
```

### La solución con DI

```typescript
// ✅ Con inyección de dependencias
class UserService {
  constructor(
    private userRepository: IUserRepository,
    private emailService: IEmailService
  ) {}

  // Las dependencias se reciben desde afuera
  // Fácil de testear con mocks
  // Fácil de cambiar implementaciones
}
```

### Implementación manual (Composition Root)

En la raíz de tu aplicación, conectas todo:

```typescript
// src/main.ts (Composition Root)
import { Pool } from 'pg';
import { UserController } from './controllers/UserController';
import { UserService } from './services/UserService';
import { PostgresUserRepository } from './repositories/UserRepository';
import { SendGridEmailService } from './services/SendGridEmailService';

// Crear conexión a la base de datos
const db = new Pool({
  connectionString: process.env.DATABASE_URL
});

// Crear el grafo de dependencias
const userRepository = new PostgresUserRepository(db);
const emailService = new SendGridEmailService(process.env.SENDGRID_KEY);
const userService = new UserService(userRepository, emailService);
const userController = new UserController(userService);

// Conectar rutas
app.post('/users', (req, res, next) => userController.create(req, res, next));
app.get('/users/:id', (req, res, next) => userController.findById(req, res, next));
```

### Contenedores de DI

Para aplicaciones más grandes, un contenedor de DI automatiza este proceso:

**Con NestJS** (el más popular para Node.js + TypeScript):

```typescript
// users/users.module.ts
@Module({
  imports: [DatabaseModule],
  controllers: [UsersController],
  providers: [
    UsersService,
    {
      provide: 'IUserRepository',
      useClass: PostgresUserRepository
    }
  ]
})
export class UsersModule {}

// users/users.service.ts
@Injectable()
export class UsersService {
  constructor(
    @Inject('IUserRepository')
    private userRepository: IUserRepository
  ) {}
}
```

**Con Awilix** (ligero, sin decoradores):

```typescript
// container.ts
import { createContainer, asClass, asValue } from 'awilix';

const container = createContainer();

container.register({
  // Infraestructura
  db: asValue(new Pool({ connectionString: process.env.DATABASE_URL })),

  // Repositories
  userRepository: asClass(PostgresUserRepository).singleton(),

  // Services
  userService: asClass(UserService).scoped(),
  emailService: asClass(SendGridEmailService).singleton(),

  // Controllers
  userController: asClass(UserController).scoped()
});

export { container };
```

### Cuándo usar DI manual vs contenedor

| Escenario | Recomendación |
|-----------|---------------|
| Proyecto pequeño (<20 clases) | DI manual |
| Proyecto mediano (20-100 clases) | Awilix o TypeDI |
| Proyecto grande o equipo grande | NestJS |
| Aplicación serverless | DI manual (simplicidad) |

📖 **Concepto**: La inyección de dependencias no es sobre frameworks. Es sobre **invertir el control**: en lugar de que una clase cree sus dependencias, las recibe desde afuera. Esto hace el código más testeable, flexible y mantenible.

---

## Manejo de Errores

Un buen sistema de errores distingue entre diferentes tipos de problemas y comunica información útil.

### Tipos de errores

```typescript
// errors/AppError.ts
export abstract class AppError extends Error {
  abstract readonly statusCode: number;
  abstract readonly isOperational: boolean;

  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Errores de cliente (4xx) - errores operacionales esperados
export class ValidationError extends AppError {
  readonly statusCode = 400;
  readonly isOperational = true;

  constructor(message: string, public readonly field?: string) {
    super(message);
  }
}

export class NotFoundError extends AppError {
  readonly statusCode = 404;
  readonly isOperational = true;

  constructor(resource: string, id: string) {
    super(`${resource} con id ${id} no encontrado`);
  }
}

export class UnauthorizedError extends AppError {
  readonly statusCode = 401;
  readonly isOperational = true;

  constructor(message = 'No autorizado') {
    super(message);
  }
}

export class ConflictError extends AppError {
  readonly statusCode = 409;
  readonly isOperational = true;

  constructor(message: string) {
    super(message);
  }
}

// Errores específicos del dominio
export class UserAlreadyExistsError extends ConflictError {
  constructor(email: string) {
    super(`El email ${email} ya está registrado`);
  }
}
```

### Middleware de manejo de errores

```typescript
// middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../errors/AppError';
import { logger } from '../utils/logger';

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Si es un error conocido (operacional)
  if (error instanceof AppError) {
    // Loggear con nivel apropiado
    if (error.statusCode >= 500) {
      logger.error('Error del servidor', {
        error: error.message,
        stack: error.stack,
        requestId: req.id
      });
    } else {
      logger.warn('Error de cliente', {
        error: error.message,
        statusCode: error.statusCode,
        requestId: req.id
      });
    }

    return res.status(error.statusCode).json({
      error: {
        code: error.name,
        message: error.message,
        ...(error instanceof ValidationError && error.field && { field: error.field })
      }
    });
  }

  // Error no esperado (bug, error de programación)
  logger.error('Error no manejado', {
    error: error.message,
    stack: error.stack,
    requestId: req.id
  });

  // En producción, no exponer detalles internos
  const message = process.env.NODE_ENV === 'production'
    ? 'Error interno del servidor'
    : error.message;

  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message
    }
  });
}
```

### Errores asíncronos

Express no captura automáticamente errores en funciones async. Solución:

```typescript
// utils/asyncHandler.ts
import { Request, Response, NextFunction } from 'express';

type AsyncHandler = (
  req: Request,
  res: Response,
  next: NextFunction
) => Promise<any>;

export function asyncHandler(fn: AsyncHandler) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Uso
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.findById(req.params.id);
  res.json(user);
}));
```

### Formato consistente de respuestas de error

```typescript
// Respuestas exitosas
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}

// Respuestas de error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "El email no es válido",
    "field": "email",
    "details": [
      { "field": "email", "message": "Debe ser un email válido" },
      { "field": "password", "message": "Debe tener mínimo 8 caracteres" }
    ]
  }
}
```

---

## Logging Estructurado

El logging es fundamental para entender qué pasa en producción. Pero no cualquier logging — necesitas **logging estructurado**.

### El problema del logging tradicional

```javascript
// ❌ Logs como strings — difíciles de procesar
console.log('Usuario creado: ' + userId + ' por IP ' + ip);
console.log('Error al procesar pedido ' + orderId + ': ' + error.message);

// En producción, esto se vuelve imposible de analizar:
// "Usuario creado: 123 por IP 192.168.1.1"
// "Error al procesar pedido 456: Connection refused"
```

### Logging estructurado con JSON

```typescript
// ✅ Logs estructurados — fáciles de procesar, filtrar, analizar
logger.info('Usuario creado', {
  userId: '123',
  ip: '192.168.1.1',
  duration: 45
});

// Output:
// {"level":"info","message":"Usuario creado","userId":"123","ip":"192.168.1.1","duration":45,"timestamp":"2025-01-02T12:00:00Z"}
```

### Configuración con Winston o Pino (Node.js)

En Node.js hay dos opciones principales:
- **Winston**: Más flexible, múltiples transportes, ideal para aplicaciones complejas
- **Pino**: Hasta 5x más rápido, ideal para APIs de alto tráfico y microservicios

**Con Winston** (flexibilidad):

```typescript
// utils/logger.ts
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'user-service',
    version: process.env.APP_VERSION
  },
  transports: [
    new winston.transports.Console({
      format: process.env.NODE_ENV === 'development'
        ? winston.format.combine(
            winston.format.colorize(),
            winston.format.simple()
          )
        : winston.format.json()
    })
  ]
});

export { logger };
```

**Con Pino** (performance):

```typescript
// utils/logger.ts
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  base: {
    service: 'user-service',
    version: process.env.APP_VERSION
  },
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined
});

export { logger };
```

> 💡 **Tip**: Si tu aplicación maneja alto tráfico (>1000 req/s), considera Pino. Para aplicaciones típicas con necesidades de logging complejas (múltiples destinos, formatos), Winston es suficiente.

### Configuración con structlog (Python)

```python
# utils/logger.py
import structlog
import logging

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
```

### Niveles de log apropiados

| Nivel | Cuándo usarlo | Ejemplo |
|-------|---------------|---------|
| **ERROR** | Algo falló y requiere atención | Error de conexión a DB, excepción no manejada |
| **WARN** | Algo inesperado pero no crítico | Rate limit casi alcanzado, retry exitoso |
| **INFO** | Eventos importantes de negocio | Usuario creado, pedido completado |
| **DEBUG** | Detalles para desarrollo | Query SQL ejecutada, valores de variables |

### Context y Request ID

Para correlacionar logs de un mismo request:

```typescript
// middleware/requestId.ts
import { v4 as uuid } from 'uuid';
import { AsyncLocalStorage } from 'async_hooks';

export const asyncLocalStorage = new AsyncLocalStorage<{ requestId: string }>();

export function requestIdMiddleware(req: Request, res: Response, next: NextFunction) {
  const requestId = req.headers['x-request-id'] as string || uuid();
  req.id = requestId;
  res.setHeader('x-request-id', requestId);

  asyncLocalStorage.run({ requestId }, () => {
    next();
  });
}

// logger con contexto automático
export function getLogger() {
  const store = asyncLocalStorage.getStore();
  return logger.child({ requestId: store?.requestId });
}
```

### Qué loggear y qué no

**✅ Loggear:**
- Inicio y fin de operaciones importantes
- Errores con contexto suficiente para debuggear
- Métricas de performance (duración de queries, latencia de APIs)
- Eventos de seguridad (login, cambio de password, acceso denegado)

**❌ NO loggear:**
- Passwords (ni hasheados)
- Tokens de sesión o API keys
- Datos personales sensibles (PII) sin enmascarar
- Información de tarjetas de crédito
- Datos de salud

```typescript
// Enmascarar datos sensibles
logger.info('Pago procesado', {
  userId: user.id,
  amount: payment.amount,
  cardLast4: payment.card.slice(-4),  // Solo últimos 4 dígitos
  email: maskEmail(user.email)         // j***@example.com
});
```

---

## Middleware y Pipelines

Los middlewares permiten procesar requests de forma modular:

```typescript
// Orden de middlewares (importa!)
app.use(requestIdMiddleware);        // 1. Asignar ID a cada request
app.use(express.json());             // 2. Parsear body JSON
app.use(rateLimitMiddleware);        // 3. Rate limiting
app.use(authMiddleware);             // 4. Autenticación
app.use(loggerMiddleware);           // 5. Logging de requests

// Rutas
app.use('/api/users', userRoutes);
app.use('/api/orders', orderRoutes);

// Middleware de errores (siempre al final)
app.use(notFoundHandler);            // 6. 404 para rutas no encontradas
app.use(errorHandler);               // 7. Manejo centralizado de errores
```

### Middleware de logging

```typescript
// middleware/requestLogger.ts
export function requestLogger(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;

    logger.info('Request completado', {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration,
      userAgent: req.get('user-agent'),
      ip: req.ip
    });
  });

  next();
}
```

---

## 🤖 Usando IA para Desarrollo Backend

La IA puede acelerar significativamente el desarrollo backend, especialmente en tareas repetitivas y boilerplate.

### Generación de código estructurado

```
Prompt efectivo:
"Genera un módulo completo para gestión de productos:

- Entity: Product con id, name, price, categoryId, stock
- DTO: CreateProductDto, UpdateProductDto
- Repository interface y implementación PostgreSQL
- Service con validaciones de negocio
- Controller con endpoints REST

Usa TypeScript, el patrón que te mostré arriba,
y manejo de errores con clases personalizadas."
```

La IA genera todo el boilerplate manteniendo consistencia.

### Casos de uso principales

**1. Generar repositories**

```
Prompt:
"Dado este schema de Prisma:
model Order {
  id        String   @id @default(uuid())
  userId    String
  status    OrderStatus
  total     Decimal
  items     OrderItem[]
  createdAt DateTime @default(now())
}

Genera el repository con:
- Métodos CRUD básicos
- findByUserId con paginación
- updateStatus con validación de transiciones
- Cálculo de totales"
```

**2. Diseñar manejo de errores**

```
Prompt:
"Para un sistema de e-commerce, diseña la jerarquía de errores:
- Errores de validación
- Errores de autenticación/autorización
- Errores de negocio (stock insuficiente, etc.)
- Errores de integración (pasarela de pago)

Incluye códigos de error únicos y mensajes claros."
```

**3. Configurar logging**

```
Prompt:
"Configura Winston para un proyecto Node.js con:
- Diferentes formatos para dev y prod
- Rotación de archivos
- Integración con Datadog
- Enmascarado automático de campos sensibles"
```

### Herramientas

| Herramienta | Uso para backend |
|-------------|------------------|
| **GitHub Copilot** | Autocompletado de métodos, queries SQL |
| **Cursor** | Refactoring de clases completas |
| **Claude** | Diseño de arquitectura, code review |
| **Amazon Q** | Integración con AWS services |

### Limitaciones

| ❌ Cuidado con... | ✅ Usa IA para... |
|-------------------|-------------------|
| Lógica de negocio sin contexto | Boilerplate y estructura repetitiva |
| Queries SQL complejas sin verificar | Generar queries simples, luego optimizar |
| Configuración de seguridad | Generar base, luego auditar |
| Código de producción sin review | Prototipos rápidos y pruebas de concepto |

> 🤖 **Nota**: La IA es excelente para generar la estructura de capas y boilerplate, pero la **lógica de negocio crítica** y las **decisiones de arquitectura** requieren tu criterio. Siempre revisa el código generado, especialmente queries SQL y manejo de errores.

---

## Resumen

### Arquitectura en capas
- **Controller**: Punto de entrada HTTP, extrae datos, delega al service
- **Service**: Lógica de negocio, orquesta repositories, aplica reglas
- **Repository**: Abstracción sobre almacenamiento, implementa acceso a datos

### Inyección de dependencias
- Las clases reciben sus dependencias, no las crean
- Permite testear con mocks y cambiar implementaciones fácilmente
- Usa DI manual para proyectos pequeños, contenedores para grandes

### Manejo de errores
- Diferencia entre errores operacionales (esperados) y de programación
- Usa clases de error personalizadas con status codes
- Centraliza el manejo en un middleware

### Logging estructurado
- Usa JSON, no strings concatenados
- Incluye contexto: requestId, userId, timestamps
- Niveles apropiados: ERROR, WARN, INFO, DEBUG
- NUNCA loggear datos sensibles

---

## Ejercicios

1. **Refactoring a capas**: Toma un endpoint que tenga todo mezclado (HTTP + lógica + SQL) y refactorízalo en Controller + Service + Repository. ¿Cuántas líneas tiene cada capa?

2. **Inyección de dependencias**: Modifica tu service para recibir el repository por constructor. Escribe un test usando un repository fake que devuelva datos hardcodeados.

3. **Sistema de errores**: Diseña 5 clases de error personalizadas para tu dominio. Implementa el middleware de manejo de errores que formatee respuestas consistentes.

4. **Logging**: Configura Winston o Pino con formato JSON. Agrega logging a un endpoint completo (inicio, operaciones intermedias, fin, errores). Verifica que los logs sean parseables.

---

## Referencias

- Goldberger, Y. (2024). *Node.js Best Practices*. https://github.com/goldbergyoni/nodebestpractices — Referencia definitiva de mejores prácticas
- Martin, R. C. (2017). *Clean Architecture*. — Principios de arquitectura por capas
- NestJS Documentation. *Dependency Injection*. https://docs.nestjs.com/providers — Implementación de DI en Node.js
- Better Stack. (2024). *Logging Best Practices*. https://betterstack.com/community/guides/logging/logging-best-practices/
- Better Stack. (2024). *Pino vs Winston*. https://betterstack.com/community/comparisons/pino-vs-winston/ — Comparativa de loggers
- OpenTelemetry. *Logging Specification*. https://opentelemetry.io/ — Estándar para observabilidad

---

**Anterior**: [Arquitectura Frontend](./11-arquitectura-frontend.md) | **Siguiente**: [Autenticación y Autorización](./13-autenticacion-autorizacion.md)
