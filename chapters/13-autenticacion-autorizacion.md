# Capítulo 13: Autenticación y Autorización

> "La autenticación responde '¿quién eres?', la autorización responde '¿qué puedes hacer?'. Confundirlas es el origen de innumerables vulnerabilidades."

---

## 📖 La Diferencia Fundamental

Antes de profundizar en implementaciones, debemos tener absolutamente clara la distinción entre estos dos conceptos:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   AUTENTICACIÓN (AuthN)           AUTORIZACIÓN (AuthZ)          │
│   ─────────────────────           ──────────────────────        │
│                                                                 │
│   "¿Quién eres?"                  "¿Qué puedes hacer?"          │
│                                                                 │
│   • Verificar identidad           • Verificar permisos          │
│   • Login, contraseña             • Roles, políticas            │
│   • Tokens de acceso              • Control de acceso           │
│   • Biometría, passkeys           • Recursos permitidos         │
│                                                                 │
│   Ejemplo:                        Ejemplo:                      │
│   "Soy Juan, aquí está            "Juan puede editar            │
│    mi credencial"                  documentos pero no           │
│                                    eliminar usuarios"           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### La Analogía del Hotel

Imagina un hotel:

1. **Autenticación**: En recepción verifican tu identidad con tu documento y te dan una tarjeta-llave. Han confirmado *quién eres*.

2. **Autorización**: Tu tarjeta-llave solo abre *tu* habitación, el gimnasio (si pagaste ese servicio), y el estacionamiento (si tienes auto registrado). No abre otras habitaciones ni áreas de servicio. Han definido *qué puedes acceder*.

Un error común es pensar que "si está autenticado, puede hacer todo". Un usuario autenticado solo ha probado su identidad; sus permisos son una capa completamente separada.

---

## 📖 Estrategias de Autenticación

### Sessions vs Tokens: Dos Filosofías

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESIONES (Stateful)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cliente              Servidor                  Base de Datos   │
│     │                    │                           │          │
│     │── Login ──────────>│                           │          │
│     │                    │── Crear sesión ──────────>│          │
│     │                    │<─ session_id ─────────────│          │
│     │<── Cookie ─────────│                           │          │
│     │   (session_id)     │                           │          │
│     │                    │                           │          │
│     │── Request ────────>│                           │          │
│     │   + Cookie         │── Buscar sesión ─────────>│          │
│     │                    │<─ Datos usuario ──────────│          │
│     │<── Response ───────│                           │          │
│                                                                 │
│  ✅ Revocación inmediata    ❌ Requiere storage centralizado    │
│  ✅ Datos sensibles en      ❌ Difícil escalar horizontalmente  │
│     servidor                ❌ Latencia por lookup              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     TOKENS (Stateless)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cliente              Servidor                                  │
│     │                    │                                      │
│     │── Login ──────────>│                                      │
│     │                    │── Generar JWT ─┐                     │
│     │                    │<───────────────┘                     │
│     │<── Token ──────────│                                      │
│     │   (JWT firmado)    │                                      │
│     │                    │                                      │
│     │── Request ────────>│                                      │
│     │   + Bearer Token   │── Verificar firma ─┐                 │
│     │                    │<───────────────────┘                 │
│     │<── Response ───────│   (sin DB lookup)                    │
│                                                                 │
│  ✅ Escala horizontalmente  ❌ No se puede revocar fácilmente   │
│  ✅ Sin estado en servidor  ❌ Payload visible (aunque firmado) │
│  ✅ Ideal para APIs/móvil   ❌ Tamaño mayor que session_id      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 💡 Desde el Punto de Vista del Usuario

Para entender mejor la diferencia, veamos qué experimenta el usuario en cada caso:

#### Escenario 1: Login en una Aplicación Web Tradicional (Sessions)

```
📱 María usa una app bancaria basada en sesiones

1. LUNES 9:00 AM - María hace login desde su laptop
   ├── Ingresa usuario y contraseña
   ├── El servidor crea una sesión y guarda: "María está conectada"
   └── María recibe una cookie con session_id=abc123

2. LUNES 9:05 AM - María revisa su saldo
   ├── El navegador envía automáticamente la cookie
   ├── El servidor busca "abc123" → "Ah, es María"
   └── María ve su saldo

3. LUNES 9:10 AM - María sospecha que alguien accedió a su cuenta
   ├── Hace clic en "Cerrar todas las sesiones"
   ├── El servidor BORRA todas las sesiones de María
   └── ✅ INMEDIATAMENTE cualquier otro dispositivo queda desconectado

4. LUNES 9:15 AM - El "intruso" intenta ver el saldo
   ├── Su navegador envía la cookie session_id=xyz789
   ├── El servidor busca "xyz789" → "No existe, fue eliminada"
   └── ❌ Acceso denegado, redirigido al login
```

**Lo que María experimenta:** Control inmediato. Cuando cierra sesiones, el efecto es instantáneo en todos los dispositivos.

#### Escenario 2: Login en una App Móvil Moderna (Tokens)

```
📱 Carlos usa una app de delivery basada en tokens

1. LUNES 9:00 AM - Carlos hace login desde su celular
   ├── Ingresa usuario y contraseña
   ├── El servidor genera un JWT con: {user: "carlos", exp: "9:15 AM"}
   └── Carlos guarda el token en su app

2. LUNES 9:05 AM - Carlos hace un pedido
   ├── La app envía el JWT en cada request
   ├── El servidor SOLO verifica la firma (no consulta DB)
   └── ✅ Pedido procesado (muy rápido, sin consultar DB)

3. LUNES 9:10 AM - Carlos pierde su celular
   ├── Llama a soporte: "Bloqueen mi cuenta"
   ├── El servidor marca la cuenta como "bloqueada"
   └── ⚠️ PERO el token sigue siendo técnicamente válido...

4. LUNES 9:12 AM - El ladrón intenta hacer un pedido
   ├── La app envía el JWT (aún no expiró)
   ├── El servidor verifica firma ✅, pero...
   ├── ...también verifica si la cuenta está bloqueada ❌
   └── ❌ Acceso denegado (gracias a verificación extra)

5. LUNES 9:16 AM - El ladrón intenta de nuevo
   ├── El token expiró (era válido hasta 9:15)
   └── ❌ Acceso denegado (token expirado)
```

**Lo que Carlos experimenta:** La app es muy rápida (no espera consultas a DB), pero el bloqueo no es 100% instantáneo - depende de verificaciones adicionales o de que expire el token.

#### Escenario 3: Comparación Directa - Múltiples Dispositivos

```
👤 Laura usa un servicio de streaming

CON SESIONES (como Netflix):
─────────────────────────────
Laura tiene 4 dispositivos conectados.
El plan solo permite 2 simultáneos.

TV:      [Sesión activa] ──┐
Laptop:  [Sesión activa] ──┼── Servidor consulta DB
Tablet:  [Sesión activa] ──┤   "¿Cuántas sesiones tiene Laura?"
Celular: [Intenta ver]  ───┘   → "Ya tiene 3, denegar"

✅ Control preciso en tiempo real
❌ Cada request consulta la base de datos


CON TOKENS (hipotético):
────────────────────────
Cada dispositivo tiene un token válido por 1 hora.

TV:      [Token válido] ────┐
Laptop:  [Token válido] ────┼── Servidor solo verifica firma
Tablet:  [Token válido] ────┤   No sabe cuántos hay conectados
Celular: [Token válido] ────┘

❌ Difícil limitar dispositivos simultáneos
✅ Muy escalable, sin consultas a DB
```

#### Escenario 4: ¿Qué pasa si el servidor se reinicia?

```
🔄 El servidor de la aplicación se reinicia a las 3 AM

CON SESIONES (en memoria):
──────────────────────────
Antes:  Servidor tiene 10,000 sesiones activas en RAM
        [Usuario1: abc] [Usuario2: def] [Usuario3: ghi]...

3:00 AM: Servidor se reinicia
        RAM se borra 💨

Después: 0 sesiones
        😱 TODOS los usuarios deben hacer login de nuevo


CON SESIONES (en Redis/DB):
───────────────────────────
Antes:  Sesiones guardadas en Redis (externo al servidor)

3:00 AM: Servidor se reinicia
        Redis sigue funcionando ✅

Después: Todas las sesiones intactas
        👍 Usuarios ni se enteran


CON TOKENS:
───────────
Antes:  Usuarios tienen tokens en sus dispositivos
        El servidor no guarda nada

3:00 AM: Servidor se reinicia

Después: Tokens siguen siendo válidos
        👍 Usuarios ni se enteran
        (El servidor solo necesita la clave para verificar firmas)
```

#### Escenario 5: La App Funciona Offline

```
✈️ Pedro usa una app de notas en un vuelo sin WiFi

CON SESIONES:
─────────────
Pedro abre la app → Intenta validar sesión con servidor
                  → Sin conexión ❌
                  → "No se puede verificar tu sesión"
                  → 😤 No puede acceder a sus notas


CON TOKENS:
───────────
Pedro abre la app → Token guardado localmente
                  → App verifica el token offline ✅
                  → Exp: mañana, firma válida
                  → 😊 Pedro edita sus notas
                  → Se sincronizan cuando aterriza
```

### ⚠️ ¿Cuándo Usar Cada Uno?

| Escenario | Recomendación | Por qué |
|-----------|---------------|---------|
| App bancaria | **Sesiones** | Necesitas revocar acceso instantáneamente |
| Blog personal | **Sesiones** | Simple, no necesitas escalar |
| API pública | **Tokens** | Stateless, fácil de escalar |
| App móvil | **Tokens** | Funciona offline, menos requests |
| Microservicios | **Tokens** | Cada servicio puede verificar sin compartir estado |
| Netflix/Spotify | **Híbrido** | Tokens + verificación de sesiones activas en DB |

### 🛠️ JWT (JSON Web Tokens) en Profundidad

Un JWT consta de tres partes separadas por puntos:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.    <- Header (algoritmo)
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6...  <- Payload (datos)
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV...    <- Signature (firma)
```

```typescript
// Estructura decodificada
{
  // Header
  "alg": "ES256",      // Algoritmo de firma
  "typ": "JWT"
}

{
  // Payload (Claims)
  "sub": "user_123",           // Subject: ID del usuario
  "iat": 1704067200,           // Issued At: cuándo se emitió
  "exp": 1704068100,           // Expiration: cuándo expira
  "iss": "https://auth.app",   // Issuer: quién lo emitió
  "aud": "https://api.app",    // Audience: para quién es

  // Claims personalizados
  "role": "editor",
  "permissions": ["read", "write"]
}
```

#### ⚠️ Mejores Prácticas de JWT

Basado en [RFC 8725](https://datatracker.ietf.org/doc/html/rfc8725) y recomendaciones actuales:

```typescript
import jwt from 'jsonwebtoken';
import { createPrivateKey, createPublicKey } from 'crypto';

// ✅ CORRECTO: Configuración segura de JWT
const jwtConfig = {
  // 1. Usar algoritmos asimétricos modernos
  algorithm: 'ES256',  // EdDSA es aún mejor si está disponible

  // 2. Tiempo de expiración corto (15 min máximo para access tokens)
  expiresIn: '15m',

  // 3. Especificar issuer y audience
  issuer: 'https://auth.myapp.com',
  audience: 'https://api.myapp.com',
};

// Generar token
function generateAccessToken(user: User): string {
  const payload = {
    sub: user.id,
    email: user.email,
    role: user.role,
    // ❌ NUNCA incluir datos sensibles
    // password: user.password  <- NUNCA
    // ssn: user.ssn            <- NUNCA
  };

  return jwt.sign(payload, privateKey, jwtConfig);
}

// Verificar token
function verifyToken(token: string): JwtPayload {
  return jwt.verify(token, publicKey, {
    // ✅ Whitelist de algoritmos permitidos
    algorithms: ['ES256'],  // NUNCA usar 'none' o permitir todos

    // ✅ Validar issuer y audience
    issuer: 'https://auth.myapp.com',
    audience: 'https://api.myapp.com',

    // ✅ Requerir expiración
    maxAge: '15m',
  });
}
```

#### Almacenamiento Seguro de Tokens

```typescript
// ✅ MEJOR: HttpOnly Cookies (para aplicaciones web)
// El token nunca es accesible desde JavaScript
res.cookie('access_token', token, {
  httpOnly: true,      // No accesible desde JS (previene XSS)
  secure: true,        // Solo HTTPS
  sameSite: 'strict',  // Previene CSRF
  maxAge: 15 * 60 * 1000,  // 15 minutos
  path: '/api',        // Solo se envía a rutas /api
});

// ⚠️ ACEPTABLE: Memoria (para SPAs)
// Se pierde al refrescar la página
class TokenStore {
  private accessToken: string | null = null;

  setToken(token: string) {
    this.accessToken = token;
  }

  getToken(): string | null {
    return this.accessToken;
  }
}

// ❌ EVITAR: localStorage
// Vulnerable a XSS - cualquier script puede leerlo
localStorage.setItem('token', token);  // NO RECOMENDADO
```

#### Patrón de Refresh Tokens

```typescript
// Access Token: corta duración, lleva la información
// Refresh Token: larga duración, solo sirve para obtener nuevos access tokens

interface TokenPair {
  accessToken: string;   // Expira en 15 minutos
  refreshToken: string;  // Expira en 7 días
}

async function login(credentials: Credentials): Promise<TokenPair> {
  const user = await validateCredentials(credentials);

  const accessToken = generateAccessToken(user);  // 15 min
  const refreshToken = generateRefreshToken(user); // 7 días

  // Guardar refresh token en DB para poder revocarlo
  await saveRefreshToken(user.id, refreshToken);

  return { accessToken, refreshToken };
}

async function refresh(refreshToken: string): Promise<TokenPair> {
  // Verificar que el refresh token es válido
  const payload = verifyRefreshToken(refreshToken);

  // Verificar que no ha sido revocado
  const isValid = await isRefreshTokenValid(payload.sub, refreshToken);
  if (!isValid) {
    throw new UnauthorizedError('Refresh token revocado');
  }

  // Rotación de refresh token (buena práctica de seguridad)
  await revokeRefreshToken(refreshToken);

  const user = await getUserById(payload.sub);
  return login({ userId: user.id }); // Genera nuevo par
}

async function logout(userId: string, refreshToken: string): Promise<void> {
  // Revocar el refresh token
  await revokeRefreshToken(refreshToken);

  // Opcionalmente, revocar todos los refresh tokens del usuario
  // await revokeAllRefreshTokens(userId);
}
```

---

## 📖 Hashing de Contraseñas

Si tu aplicación permite autenticación con contraseñas, **nunca** almacenes contraseñas en texto plano. Usa algoritmos de hashing diseñados específicamente para contraseñas.

### Jerarquía de Algoritmos (2025)

| Algoritmo | Recomendación | Cuándo usar |
|-----------|---------------|-------------|
| **Argon2id** | ✅ Preferido | Nuevos sistemas |
| **scrypt** | ✅ Bueno | Si Argon2 no está disponible |
| **bcrypt** | ⚠️ Aceptable | Sistemas legacy |
| **PBKDF2** | ⚠️ Solo FIPS | Requisitos de compliance |
| SHA-256/MD5 | ❌ Nunca | No usar para contraseñas |

### 🛠️ Implementación con Argon2id

```typescript
import argon2 from 'argon2';

// Configuración recomendada por OWASP
const hashConfig = {
  type: argon2.argon2id,  // Variante híbrida (resistente a GPU y side-channel)
  memoryCost: 65536,      // 64 MB de memoria
  timeCost: 3,            // 3 iteraciones
  parallelism: 1,         // 1 hilo
  hashLength: 32,         // 32 bytes de salida
};

// Crear hash de contraseña
async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, hashConfig);
  // Resultado: $argon2id$v=19$m=65536,t=3,p=1$salt$hash
  // El salt se genera automáticamente y se incluye en el resultado
}

// Verificar contraseña
async function verifyPassword(password: string, hash: string): Promise<boolean> {
  try {
    return await argon2.verify(hash, password);
  } catch {
    return false;  // Hash inválido o error
  }
}

// Ejemplo de uso
async function register(email: string, password: string) {
  // Validar fortaleza de contraseña primero
  if (!isStrongPassword(password)) {
    throw new Error('Contraseña muy débil');
  }

  const passwordHash = await hashPassword(password);

  await db.user.create({
    data: {
      email,
      passwordHash,  // NUNCA almacenar password, solo el hash
    },
  });
}

async function login(email: string, password: string) {
  const user = await db.user.findUnique({ where: { email } });

  // Timing-safe: siempre verificar aunque el usuario no exista
  const dummyHash = '$argon2id$v=19$m=65536,t=3,p=1$dummy$dummyhash';
  const hashToVerify = user?.passwordHash ?? dummyHash;

  const isValid = await verifyPassword(password, hashToVerify);

  if (!user || !isValid) {
    throw new Error('Credenciales inválidas');  // Mensaje genérico
  }

  return user;
}
```

### bcrypt para Sistemas Legacy

```typescript
import bcrypt from 'bcrypt';

// Cost factor: cada incremento duplica el tiempo
// Factor 12 ≈ 250ms en hardware moderno (2025)
const BCRYPT_ROUNDS = 12;

async function hashPasswordBcrypt(password: string): Promise<string> {
  // ⚠️ bcrypt tiene límite de 72 bytes
  if (Buffer.byteLength(password, 'utf8') > 72) {
    throw new Error('Contraseña muy larga para bcrypt');
  }

  return bcrypt.hash(password, BCRYPT_ROUNDS);
}

async function verifyPasswordBcrypt(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

### 💡 Pepper: Capa Adicional de Seguridad

```typescript
// El pepper es un secreto que se añade antes del hashing
// Se almacena en variables de entorno, NO en la base de datos

const PEPPER = process.env.PASSWORD_PEPPER;  // Secreto de 32+ bytes

async function hashWithPepper(password: string): Promise<string> {
  // Combinar password con pepper antes de hashear
  const pepperedPassword = `${password}${PEPPER}`;
  return argon2.hash(pepperedPassword, hashConfig);
}

// Beneficio: si roban solo la DB, no pueden crackear los hashes
// porque no tienen el pepper
```

---

## 📖 Autenticación Moderna: Passkeys y WebAuthn

En 2025, los **passkeys** han alcanzado adopción masiva: el 69% de usuarios tiene al menos un passkey, y el 48% de los 100 sitios más grandes ya los soportan. Son más seguros y tienen una tasa de éxito del 93% vs 63% de métodos tradicionales.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ¿Qué es un Passkey?                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Un passkey es una credencial criptográfica que reemplaza       │
│  las contraseñas. Usa criptografía de clave pública:            │
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │   Dispositivo │         │   Servidor   │                      │
│  │              │         │              │                      │
│  │  🔐 Clave    │         │  🔓 Clave    │                      │
│  │    Privada   │         │    Pública   │                      │
│  │  (nunca sale)│         │  (registrada)│                      │
│  └──────────────┘         └──────────────┘                      │
│         │                        │                              │
│         │    Challenge ──────────│                              │
│         │<───────────────────────│                              │
│         │                        │                              │
│         │    Firma ──────────────│                              │
│         │───────────────────────>│ Verifica con                 │
│         │                        │ clave pública                │
│                                                                 │
│  ✅ Resistente a phishing (vinculado al dominio)                │
│  ✅ No hay contraseña que robar                                 │
│  ✅ Autenticación biométrica (Face ID, huella)                  │
│  ✅ Sincronizable entre dispositivos (iCloud, Google)           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ Implementando WebAuthn

```typescript
// Registro de passkey (simplificado)
// En el frontend
async function registerPasskey() {
  // 1. Obtener challenge del servidor
  const options = await fetch('/api/auth/webauthn/register-options', {
    method: 'POST',
  }).then(r => r.json());

  // 2. Crear credencial con el navegador
  const credential = await navigator.credentials.create({
    publicKey: {
      challenge: base64ToBuffer(options.challenge),
      rp: {
        name: 'Mi Aplicación',
        id: 'miapp.com',  // Vinculado al dominio
      },
      user: {
        id: base64ToBuffer(options.userId),
        name: options.userEmail,
        displayName: options.userName,
      },
      pubKeyCredParams: [
        { alg: -7, type: 'public-key' },   // ES256
        { alg: -257, type: 'public-key' }, // RS256
      ],
      authenticatorSelection: {
        authenticatorAttachment: 'platform',  // Dispositivo actual
        residentKey: 'required',
        userVerification: 'required',
      },
    },
  });

  // 3. Enviar credencial al servidor
  await fetch('/api/auth/webauthn/register', {
    method: 'POST',
    body: JSON.stringify({
      id: credential.id,
      rawId: bufferToBase64(credential.rawId),
      response: {
        clientDataJSON: bufferToBase64(credential.response.clientDataJSON),
        attestationObject: bufferToBase64(credential.response.attestationObject),
      },
    }),
  });
}

// Login con passkey
async function loginWithPasskey() {
  // 1. Obtener challenge
  const options = await fetch('/api/auth/webauthn/login-options').then(r => r.json());

  // 2. Obtener credencial (activa biometría)
  const credential = await navigator.credentials.get({
    publicKey: {
      challenge: base64ToBuffer(options.challenge),
      rpId: 'miapp.com',
      userVerification: 'required',
    },
  });

  // 3. Verificar en servidor
  const result = await fetch('/api/auth/webauthn/login', {
    method: 'POST',
    body: JSON.stringify({
      id: credential.id,
      rawId: bufferToBase64(credential.rawId),
      response: {
        clientDataJSON: bufferToBase64(credential.response.clientDataJSON),
        authenticatorData: bufferToBase64(credential.response.authenticatorData),
        signature: bufferToBase64(credential.response.signature),
      },
    }),
  }).then(r => r.json());

  return result;  // { accessToken, refreshToken }
}
```

---

## 📖 OAuth 2.1 y OpenID Connect

OAuth permite que una aplicación acceda a recursos de un usuario en otro servicio, **sin que el usuario comparta su contraseña**.

### La Evolución: OAuth 2.0 → OAuth 2.1

OAuth 2.1 (actualmente en borrador final) consolida las mejores prácticas y elimina flujos inseguros:

| Cambio | OAuth 2.0 | OAuth 2.1 |
|--------|-----------|-----------|
| PKCE | Opcional | **Obligatorio** |
| Implicit Grant | Permitido | **Eliminado** |
| Password Grant | Permitido | **Eliminado** |
| Redirect URI | Matching flexible | **Exacto** |
| Tokens en URL | Permitido | **Prohibido** |
| Refresh Tokens | Sin restricción | **Rotación o binding** |

### El Flujo Authorization Code con PKCE

```
┌─────────────────────────────────────────────────────────────────┐
│                    OAuth 2.1 + PKCE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Usuario        App Cliente       Auth Server      Resource API │
│     │               │                  │                │       │
│     │──Click Login─>│                  │                │       │
│     │               │                  │                │       │
│     │               │──1. Generar──┐   │                │       │
│     │               │   code_verifier  │                │       │
│     │               │   code_challenge │                │       │
│     │               │<─────────────┘   │                │       │
│     │               │                  │                │       │
│     │               │──2. Redirect────>│                │       │
│     │               │   + code_challenge                │       │
│     │               │   + state        │                │       │
│     │               │                  │                │       │
│     │<──────────────────3. Login Form──│                │       │
│     │                                  │                │       │
│     │────4. Credenciales──────────────>│                │       │
│     │                                  │                │       │
│     │<──5. Redirect + code─────────────│                │       │
│     │               │                  │                │       │
│     │──6. Code─────>│                  │                │       │
│     │               │                  │                │       │
│     │               │──7. Code + ──────>                │       │
│     │               │   code_verifier  │                │       │
│     │               │                  │                │       │
│     │               │<─8. Tokens───────│                │       │
│     │               │   (access+refresh)                │       │
│     │               │                  │                │       │
│     │               │──9. API Request──────────────────>│       │
│     │               │   + Access Token │                │       │
│     │               │                  │                │       │
│     │               │<─10. Data────────────────────────│       │
│     │               │                  │                │       │
│     │<──11. Result──│                  │                │       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ Implementación con PKCE

```typescript
import crypto from 'crypto';

// Generar PKCE (en el cliente)
function generatePKCE(): { verifier: string; challenge: string } {
  // Code Verifier: string aleatorio de alta entropía
  const verifier = crypto.randomBytes(32).toString('base64url');

  // Code Challenge: hash SHA256 del verifier
  const challenge = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');

  return { verifier, challenge };
}

// Paso 1: Iniciar flujo OAuth
async function startOAuthFlow(): Promise<void> {
  const { verifier, challenge } = generatePKCE();
  const state = crypto.randomBytes(16).toString('hex');

  // Guardar para validar después
  sessionStorage.setItem('oauth_verifier', verifier);
  sessionStorage.setItem('oauth_state', state);

  const params = new URLSearchParams({
    client_id: 'my_client_id',
    redirect_uri: 'https://myapp.com/callback',
    response_type: 'code',
    scope: 'openid profile email',
    state: state,
    code_challenge: challenge,
    code_challenge_method: 'S256',
  });

  window.location.href = `https://auth.provider.com/authorize?${params}`;
}

// Paso 2: Manejar callback
async function handleOAuthCallback(): Promise<TokenPair> {
  const params = new URLSearchParams(window.location.search);
  const code = params.get('code');
  const state = params.get('state');

  // Validar state para prevenir CSRF
  const savedState = sessionStorage.getItem('oauth_state');
  if (state !== savedState) {
    throw new Error('Invalid state - possible CSRF attack');
  }

  const verifier = sessionStorage.getItem('oauth_verifier');

  // Intercambiar code por tokens
  const response = await fetch('https://auth.provider.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      client_id: 'my_client_id',
      code: code,
      redirect_uri: 'https://myapp.com/callback',
      code_verifier: verifier,  // PKCE: el servidor verifica el hash
    }),
  });

  // Limpiar datos temporales
  sessionStorage.removeItem('oauth_verifier');
  sessionStorage.removeItem('oauth_state');

  return response.json();
}
```

### OpenID Connect: Identidad sobre OAuth

OAuth fue diseñado para **autorización** (acceder a recursos), no para **autenticación** (verificar identidad). OpenID Connect (OIDC) añade una capa de identidad:

```typescript
// OAuth solo te da un access_token para acceder a recursos
// OIDC además te da un id_token con información del usuario

interface OIDCTokenResponse {
  access_token: string;   // Para acceder a APIs
  refresh_token: string;  // Para renovar
  id_token: string;       // JWT con identidad del usuario
  token_type: 'Bearer';
  expires_in: number;
}

// El id_token contiene claims estándar
interface IDTokenPayload {
  iss: string;        // Issuer
  sub: string;        // Subject (user ID único)
  aud: string;        // Audience (client ID)
  exp: number;        // Expiration
  iat: number;        // Issued at

  // Claims de identidad (con scope 'profile')
  name?: string;
  given_name?: string;
  family_name?: string;
  picture?: string;

  // Con scope 'email'
  email?: string;
  email_verified?: boolean;
}
```

---

## 📖 Modelos de Autorización

Una vez autenticado el usuario, ¿cómo determinamos qué puede hacer?

### RBAC: Role-Based Access Control

El modelo más común. Los permisos se asignan a roles, y los roles se asignan a usuarios.

```
┌─────────────────────────────────────────────────────────────────┐
│                         RBAC                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Usuarios           Roles              Permisos                 │
│  ─────────          ─────              ────────                 │
│                                                                 │
│  Ana ─────────────> Admin ──────────> crear_usuario             │
│                        │               eliminar_usuario         │
│                        │               ver_reportes             │
│                        │               editar_config            │
│                        │                                        │
│  Bob ─────────────> Editor ─────────> crear_articulo            │
│  Carlos ──────────>    │               editar_articulo          │
│                        │               ver_reportes             │
│                                                                 │
│  Diana ───────────> Viewer ─────────> ver_articulo              │
│                                        ver_reportes             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```typescript
// Definición de roles y permisos
const ROLES = {
  ADMIN: 'admin',
  EDITOR: 'editor',
  VIEWER: 'viewer',
} as const;

const PERMISSIONS = {
  CREATE_USER: 'create_user',
  DELETE_USER: 'delete_user',
  VIEW_REPORTS: 'view_reports',
  EDIT_CONFIG: 'edit_config',
  CREATE_ARTICLE: 'create_article',
  EDIT_ARTICLE: 'edit_article',
  VIEW_ARTICLE: 'view_article',
} as const;

const ROLE_PERMISSIONS: Record<string, string[]> = {
  [ROLES.ADMIN]: Object.values(PERMISSIONS),
  [ROLES.EDITOR]: [
    PERMISSIONS.CREATE_ARTICLE,
    PERMISSIONS.EDIT_ARTICLE,
    PERMISSIONS.VIEW_ARTICLE,
    PERMISSIONS.VIEW_REPORTS,
  ],
  [ROLES.VIEWER]: [
    PERMISSIONS.VIEW_ARTICLE,
    PERMISSIONS.VIEW_REPORTS,
  ],
};

// Middleware de autorización
function requirePermission(permission: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userRole = req.user?.role;

    if (!userRole) {
      return res.status(401).json({ error: 'No autenticado' });
    }

    const permissions = ROLE_PERMISSIONS[userRole] || [];

    if (!permissions.includes(permission)) {
      return res.status(403).json({
        error: 'No autorizado',
        required: permission,
        userRole: userRole,
      });
    }

    next();
  };
}

// Uso
router.delete(
  '/users/:id',
  authenticate,
  requirePermission(PERMISSIONS.DELETE_USER),
  deleteUserHandler
);
```

### ABAC: Attribute-Based Access Control

Más flexible que RBAC. Las decisiones se basan en **atributos** del usuario, recurso, acción y contexto.

```
┌─────────────────────────────────────────────────────────────────┐
│                         ABAC                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  La decisión considera múltiples atributos:                     │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Usuario   │  │   Recurso   │  │  Contexto   │             │
│  │  ─────────  │  │  ─────────  │  │  ─────────  │             │
│  │ department  │  │ owner       │  │ time        │             │
│  │ clearance   │  │ sensitivity │  │ ip_address  │             │
│  │ location    │  │ type        │  │ device      │             │
│  │ tenure      │  │ status      │  │ risk_score  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                   ┌─────────────┐                               │
│                   │   Policy    │                               │
│                   │   Engine    │                               │
│                   └─────────────┘                               │
│                          │                                      │
│                          ▼                                      │
│                   ALLOW / DENY                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```typescript
// Ejemplo: Solo el dueño puede editar, o un admin del mismo departamento

interface PolicyContext {
  user: {
    id: string;
    role: string;
    department: string;
    clearanceLevel: number;
  };
  resource: {
    id: string;
    ownerId: string;
    department: string;
    sensitivityLevel: number;
    status: 'draft' | 'published' | 'archived';
  };
  action: 'read' | 'write' | 'delete';
  environment: {
    ipAddress: string;
    time: Date;
    riskScore: number;
  };
}

// Motor de políticas ABAC
class PolicyEngine {
  private policies: Policy[] = [];

  addPolicy(policy: Policy) {
    this.policies.push(policy);
  }

  evaluate(context: PolicyContext): 'ALLOW' | 'DENY' {
    // Evaluar todas las políticas aplicables
    for (const policy of this.policies) {
      if (policy.appliesTo(context)) {
        const result = policy.evaluate(context);
        if (result === 'DENY') {
          return 'DENY';  // Deny tiene precedencia
        }
      }
    }

    // Por defecto denegar (fail-closed)
    return 'DENY';
  }
}

// Definición de políticas
const documentEditPolicy: Policy = {
  name: 'document-edit',

  appliesTo: (ctx) => ctx.action === 'write',

  evaluate: (ctx) => {
    // El dueño siempre puede editar
    if (ctx.resource.ownerId === ctx.user.id) {
      return 'ALLOW';
    }

    // Admin del mismo departamento puede editar
    if (ctx.user.role === 'admin' &&
        ctx.user.department === ctx.resource.department) {
      return 'ALLOW';
    }

    // Verificar nivel de clearance para documentos sensibles
    if (ctx.resource.sensitivityLevel > ctx.user.clearanceLevel) {
      return 'DENY';
    }

    // No editar documentos archivados
    if (ctx.resource.status === 'archived') {
      return 'DENY';
    }

    // Denegar acceso fuera de horario laboral para documentos sensibles
    const hour = ctx.environment.time.getHours();
    if (ctx.resource.sensitivityLevel > 2 && (hour < 8 || hour > 18)) {
      return 'DENY';
    }

    return 'DENY';
  },
};
```

### ReBAC: Relationship-Based Access Control

Moderno enfoque donde los permisos derivan de **relaciones** entre entidades. Popular en sistemas como Google Docs, Notion.

```
┌─────────────────────────────────────────────────────────────────┐
│                         ReBAC                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  "Ana puede editar el Documento X porque es miembro del         │
│   Equipo Y, y el Equipo Y tiene acceso de edición al            │
│   Folder Z, que contiene el Documento X"                        │
│                                                                 │
│      Ana ──member──> Team Y                                     │
│                        │                                        │
│                      editor                                     │
│                        │                                        │
│                        ▼                                        │
│                     Folder Z                                    │
│                        │                                        │
│                      parent                                     │
│                        │                                        │
│                        ▼                                        │
│                   Document X                                    │
│                                                                 │
│  Query: check(user:ana, edit, document:x) → true                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```typescript
// Usando un sistema como SpiceDB/Authzed o OpenFGA

// Definir el modelo de relaciones
const schema = `
definition user {}

definition team {
  relation member: user
  relation admin: user

  permission can_manage = admin
}

definition folder {
  relation owner: user
  relation editor: user | team#member
  relation viewer: user | team#member

  permission can_edit = owner + editor
  permission can_view = owner + editor + viewer
}

definition document {
  relation parent: folder
  relation owner: user
  relation editor: user

  // Hereda permisos del folder padre
  permission can_edit = owner + editor + parent->can_edit
  permission can_view = can_edit + parent->can_view
}
`;

// Crear relaciones
await authz.writeRelationships([
  { resource: 'team:engineering', relation: 'member', subject: 'user:ana' },
  { resource: 'folder:projects', relation: 'editor', subject: 'team:engineering#member' },
  { resource: 'document:roadmap', relation: 'parent', subject: 'folder:projects' },
]);

// Verificar permisos
const canEdit = await authz.check({
  resource: 'document:roadmap',
  permission: 'can_edit',
  subject: 'user:ana',
});
// → true (Ana es miembro de engineering, que tiene editor en projects,
//         que es parent de roadmap)
```

---

## 📖 Seguridad en la Práctica

### Checklist de Seguridad para Autenticación

```typescript
// ❌ ERRORES COMUNES

// 1. Comparación de timing insegura
if (providedToken === storedToken) { ... }  // Vulnerable a timing attacks

// ✅ Usar comparación de tiempo constante
import { timingSafeEqual } from 'crypto';
if (timingSafeEqual(Buffer.from(providedToken), Buffer.from(storedToken))) { ... }


// 2. Mensajes de error que revelan información
if (!user) {
  throw new Error('Usuario no existe');  // ❌ Revela que el email no está registrado
}
if (!validPassword) {
  throw new Error('Contraseña incorrecta');  // ❌ Confirma que el email sí existe
}

// ✅ Mensaje genérico
throw new Error('Credenciales inválidas');


// 3. Rate limiting ausente
app.post('/login', loginHandler);  // ❌ Vulnerable a fuerza bruta

// ✅ Con rate limiting
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutos
  max: 5,  // 5 intentos
  message: 'Demasiados intentos. Intenta de nuevo en 15 minutos.',
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => req.body.email || req.ip,  // Por email, no solo IP
});

app.post('/login', loginLimiter, loginHandler);


// 4. Sesiones que no se invalidan
async function logout(req, res) {
  res.clearCookie('session');  // ❌ El token sigue siendo válido
}

// ✅ Invalidar en el servidor
async function logout(req, res) {
  await invalidateSession(req.session.id);  // Marcar como inválida en DB
  await revokeRefreshToken(req.user.id, req.refreshToken);
  res.clearCookie('session');
  res.clearCookie('refresh_token');
}
```

### Protección contra Ataques Comunes

```typescript
// CSRF (Cross-Site Request Forgery)
// Atacante hace que el usuario ejecute acciones no deseadas

// ✅ Protección con tokens CSRF
import csrf from 'csurf';

const csrfProtection = csrf({ cookie: true });
app.use(csrfProtection);

// En el formulario HTML
app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

// O con SameSite cookies (protección moderna)
res.cookie('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',  // No se envía en requests cross-site
});


// Session Fixation
// Atacante fija un session ID antes del login

// ✅ Regenerar session ID después del login
async function login(req, res) {
  const user = await authenticate(req.body);

  // Regenerar ID de sesión
  req.session.regenerate((err) => {
    if (err) throw err;

    req.session.userId = user.id;
    req.session.save();
  });
}


// Brute Force en Reset de Password
// ✅ Tokens de un solo uso con expiración corta
async function requestPasswordReset(email: string) {
  const user = await findUserByEmail(email);

  // No revelar si el email existe
  if (!user) {
    return { message: 'Si el email existe, recibirás instrucciones' };
  }

  // Token seguro, un solo uso
  const token = crypto.randomBytes(32).toString('hex');
  const expiry = Date.now() + 15 * 60 * 1000; // 15 minutos

  await saveResetToken(user.id, {
    tokenHash: await hash(token),  // Guardar hash, no el token
    expiresAt: expiry,
    used: false,
  });

  await sendEmail(email, `Reset: https://app.com/reset?token=${token}`);

  return { message: 'Si el email existe, recibirás instrucciones' };
}

async function resetPassword(token: string, newPassword: string) {
  const tokenHash = await hash(token);
  const resetRequest = await findResetByHash(tokenHash);

  if (!resetRequest || resetRequest.used || resetRequest.expiresAt < Date.now()) {
    throw new Error('Token inválido o expirado');
  }

  // Marcar como usado ANTES de cambiar password (previene race conditions)
  await markTokenAsUsed(resetRequest.id);

  await updatePassword(resetRequest.userId, newPassword);

  // Invalidar todas las sesiones existentes
  await invalidateAllSessions(resetRequest.userId);
}
```

### Headers de Seguridad

```typescript
import helmet from 'helmet';

app.use(helmet({
  // Content Security Policy
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'strict-dynamic'"],
      styleSrc: ["'self'", "'unsafe-inline'"],  // Idealmente sin unsafe-inline
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://api.myapp.com"],
      frameSrc: ["'none'"],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: [],
    },
  },

  // Strict Transport Security
  strictTransportSecurity: {
    maxAge: 31536000,  // 1 año
    includeSubDomains: true,
    preload: true,
  },

  // Prevenir clickjacking
  frameguard: { action: 'deny' },

  // No MIME sniffing
  noSniff: true,

  // XSS filter
  xssFilter: true,
}));
```

---

## 🤖 IA en Autenticación y Autorización

### Detección de Anomalías

```typescript
// La IA puede detectar patrones sospechosos de login

interface LoginAttempt {
  userId: string;
  timestamp: Date;
  ipAddress: string;
  userAgent: string;
  location: GeoLocation;
  success: boolean;
}

async function analyzeLoginRisk(attempt: LoginAttempt): Promise<RiskScore> {
  const userHistory = await getRecentLogins(attempt.userId);

  const riskFactors = {
    // ¿Nuevo dispositivo?
    newDevice: !userHistory.some(h => h.userAgent === attempt.userAgent),

    // ¿Nueva ubicación?
    newLocation: !userHistory.some(h =>
      isNearby(h.location, attempt.location, 100) // 100km
    ),

    // ¿Viaje imposible? (login desde otra ciudad muy rápido)
    impossibleTravel: detectImpossibleTravel(userHistory, attempt),

    // ¿Hora inusual?
    unusualTime: isUnusualHour(attempt.timestamp, userHistory),

    // ¿Muchos intentos fallidos recientes?
    recentFailures: countRecentFailures(attempt.userId, attempt.ipAddress),
  };

  // Calcular score de riesgo
  return calculateRiskScore(riskFactors);
}

// Basado en el riesgo, decidir acción
async function handleLogin(credentials: Credentials, context: LoginContext) {
  const user = await validateCredentials(credentials);

  const riskScore = await analyzeLoginRisk({
    userId: user.id,
    ...context,
    success: true,
  });

  if (riskScore > 0.8) {
    // Alto riesgo: bloquear y notificar
    await notifyUser(user, 'Intento de login bloqueado desde ubicación sospechosa');
    throw new Error('Login bloqueado por seguridad');
  }

  if (riskScore > 0.5) {
    // Riesgo medio: requerir verificación adicional
    return { requiresMFA: true, mfaMethod: 'email' };
  }

  // Riesgo bajo: login normal
  return generateTokens(user);
}
```

### Generación de Políticas con IA

```typescript
// La IA puede ayudar a generar políticas ABAC basadas en patrones observados

const prompt = `
Analiza los siguientes patrones de acceso y sugiere políticas de autorización:

Patrones observados:
- Usuarios del departamento "ventas" acceden a documentos en /sales/ en horario 9-18
- Usuarios con rol "manager" acceden a reportes de su equipo
- El usuario admin@company.com accede a todo
- Usuarios externos (email no @company.com) solo acceden a /public/

Genera políticas ABAC en formato estructurado.
`;

// La IA puede generar:
const suggestedPolicies = [
  {
    name: 'sales-department-access',
    conditions: {
      user: { department: 'ventas' },
      resource: { path: { startsWith: '/sales/' } },
      environment: { hour: { between: [9, 18] } },
    },
    effect: 'ALLOW',
  },
  {
    name: 'manager-team-reports',
    conditions: {
      user: { role: 'manager' },
      resource: { type: 'report', teamId: '${user.teamId}' },
    },
    effect: 'ALLOW',
  },
  // ...
];
```

---

## 💡 Insights Clave

1. **Siempre separa autenticación de autorización** - Son preocupaciones diferentes que cambian independientemente.

2. **JWT no es una sesión** - No intentes "revocar" JWTs; usa refresh tokens y tiempos de expiración cortos.

3. **Passkeys son el futuro** - Con 69% de adopción y soporte en los principales sitios, es momento de implementarlos.

4. **OAuth 2.1 es el nuevo estándar** - PKCE obligatorio, implicit flow eliminado. Actualiza tus implementaciones.

5. **RBAC es suficiente para el 80% de los casos** - No sobre-ingenierices con ABAC o ReBAC a menos que realmente lo necesites.

6. **La seguridad es en capas** - Rate limiting + CSRF protection + secure cookies + CSP + validación = defensa en profundidad.

---

## 📚 Referencias

- [RFC 8725 - JWT Best Current Practices](https://datatracker.ietf.org/doc/html/rfc8725)
- [OAuth 2.1 Draft](https://oauth.net/2.1/)
- [WebAuthn Level 3 Specification](https://www.w3.org/TR/webauthn-3/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [FIDO Alliance - Passkeys](https://fidoalliance.org/passkeys/)

---

## Navegación

- [← Capítulo 12: Arquitectura Backend](./12-arquitectura-backend.md)
- [→ Capítulo 14: Comunicación y Datos en Tiempo Real](./14-tiempo-real.md)
- [Índice](../README.md)
