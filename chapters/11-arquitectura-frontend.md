# 11. Arquitectura Frontend

> "La complejidad del frontend no está en el código, está en el estado."

## Objetivos de Aprendizaje

Al finalizar este capítulo, serás capaz de:
- Elegir el framework adecuado para tu proyecto (o decidir no usar ninguno)
- Estructurar proyectos frontend de manera escalable
- Manejar estado de forma predecible y mantenible
- Implementar patrones de renderizado según las necesidades (CSR, SSR, SSG)
- Optimizar el rendimiento percibido y real de tu aplicación

---

## El Estado del Arte (2024-2025)

El ecosistema frontend ha madurado considerablemente. Ya no es el "Wild West" de hace unos años, pero sigue evolucionando rápidamente.

### El panorama actual

```
┌─────────────────────────────────────────────────────────────────┐
│                    ECOSISTEMA FRONTEND 2024                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Meta-frameworks (Full-stack)                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐       │
│  │ Next.js  │  │  Nuxt    │  │ SvelteKit│  │  Astro     │       │
│  │ (React)  │  │  (Vue)   │  │(Svelte)  │  │ (Agnóstico)│       │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘       │
│                                                                 │
│  Librerías UI (Componentes)                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  React   │  │   Vue    │  │  Svelte  │  │  Solid   │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
│                                                                 │
│  Build Tools                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │   Vite   │  │  Turbo   │  │  esbuild │                       │
│  └──────────┘  └──────────┘  └──────────┘                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Lo que NO muestra este diagrama

El ecosistema JavaScript es ruidoso y acapara la atención, pero **la mayoría de la web no está construida con React**.

Millones de aplicaciones en producción usan:
- **PHP**: Laravel, Symfony, CodeIgniter, WordPress
- **Python**: Django, Flask
- **Ruby**: Ruby on Rails
- **Java/.NET**: Spring, ASP.NET

Estas tecnologías no son "legacy" — muchas están innovando activamente.

---

## El Renacimiento del Server-Rendered

### Un poco de historia

Antes de 2013 (cuando apareció React), casi todo era **server-rendered**:

```
2005-2013: La era dorada del server-rendered
────────────────────────────────────────────
PHP + jQuery         → WordPress, Drupal, sitios corporativos
Ruby on Rails        → Twitter, GitHub, Shopify (inicialmente)
Django               → Instagram, Pinterest (inicialmente)
ASP.NET              → Stack empresarial Microsoft
```

Luego llegaron los SPAs (Single Page Applications) y prometieron:
- Experiencias más fluidas "como apps nativas"
- Separación frontend/backend
- Reutilización de APIs

**Pero trajeron complejidad:**
- Bundles de JavaScript enormes
- SEO complicado
- Estado duplicado (servidor + cliente)
- Tiempos de carga iniciales lentos
- Accesibilidad más difícil

### El péndulo regresa

Alrededor de 2020, la industria empezó a cuestionar: **¿realmente necesitamos todo este JavaScript?**

Surgió el movimiento **"HTML-over-the-wire"**:

```
┌─────────────────────────────────────────────────────────────┐
│              HTML-OVER-THE-WIRE (2020+)                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  En lugar de:                                               │
│  Servidor ──JSON──▶ JavaScript ──render──▶ HTML             │
│                                                             │
│  Hacer:                                                     │
│  Servidor ──HTML──▶ DOM (directamente)                      │
│                                                             │
│  Herramientas:                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │  HTMX    │  │ Livewire │  │ Hotwire  │                   │
│  │(Agnóstico)│ │ (Laravel)│  │ (Rails)  │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Frameworks Server-Rendered: Estado actual

#### Laravel + Livewire (PHP) — ↗️ En auge

Laravel es el framework PHP más popular. Livewire permite crear UIs reactivas sin escribir JavaScript.

```php
// Livewire: Componente reactivo en PHP puro
class SearchUsers extends Component
{
    public $search = '';

    public function render()
    {
        return view('livewire.search-users', [
            'users' => User::where('name', 'like', "%{$this->search}%")->get()
        ]);
    }
}
```

```html
<!-- La vista se actualiza automáticamente al escribir -->
<div>
    <input wire:model.live="search" placeholder="Buscar usuarios...">

    @foreach($users as $user)
        <div>{{ $user->name }}</div>
    @endforeach
</div>
```

**¿Por qué está en auge?**
- Productividad extrema para CRUD y dashboards
- Un solo lenguaje (PHP) para todo
- Comunidad muy activa
- Laravel Forge/Vapor simplifican deployment

**Ideal para:** Apps empresariales, CRMs, dashboards admin, MVPs rápidos

#### Django + HTMX (Python) — → Estable

Django sigue siendo sólido para aplicaciones data-heavy. HTMX le da interactividad moderna.

```html
<!-- HTMX: Interactividad declarativa en HTML -->
<button hx-post="/like/{{ post.id }}"
        hx-target="#like-count"
        hx-swap="innerHTML">
    👍 Me gusta
</button>

<span id="like-count">{{ post.likes }}</span>
```

```python
# Vista Django normal
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes += 1
    post.save()
    return HttpResponse(str(post.likes))  # Solo el número
```

**¿Por qué sigue relevante?**
- Excelente para data science / ML (Python)
- Admin automático muy poderoso
- ORM maduro y bien documentado
- HTMX lo moderniza sin reescribir

**Ideal para:** Aplicaciones de datos, admin panels, startups Python-first

#### Ruby on Rails + Hotwire — ↗️ Resurgiendo

Rails inventó muchas de las convenciones que otros copiaron. Hotwire (Turbo + Stimulus) es su respuesta moderna a los SPAs.

```erb
<!-- Turbo Frame: Actualiza solo una parte de la página -->
<%= turbo_frame_tag "cart" do %>
  <div>Items: <%= @cart.items.count %></div>
  <%= button_to "Agregar", add_to_cart_path, method: :post %>
<% end %>
```

**¿Por qué está resurgiendo?**
- 37signals (Basecamp, Hey) demostró que funciona a escala
- Hotwire ofrece SPA-like UX sin JavaScript frameworks
- Comunidad rejuvenecida
- Rails 7+ es significativamente más rápido

**Ideal para:** Startups, productos SaaS, equipos pequeños que quieren moverse rápido

#### CodeIgniter (PHP) — ↘️ En declive

```
Situación: La comunidad migró mayoritariamente a Laravel.
Recomendación: Para proyectos nuevos, usar Laravel.
Para proyectos existentes: Mantener o planificar migración.
```

#### Symfony (PHP) — → Estable (Enterprise)

Usado en proyectos enterprise donde se necesita máxima flexibilidad. Más complejo que Laravel pero más configurable.

### Tecnologías en declive

Es importante reconocer qué está quedando obsoleto para no invertir en tecnología moribunda:

| Tecnología | Estado | Recomendación |
|------------|--------|---------------|
| **jQuery como framework** | ↘️ Obsoleto | Migrar a vanilla JS o framework moderno |
| **AngularJS (1.x)** | ☠️ End of Life | Migrar a Angular moderno, React o Vue |
| **Backbone.js** | ↘️ Abandonado | Migrar a framework moderno |
| **CodeIgniter** | ↘️ En declive | Considerar Laravel para nuevos proyectos |
| **Ember Classic** | ↘️ Reducido | Ember Octane o migrar |
| **PHP sin framework** | ↘️ Arriesgado | Usar Laravel o Symfony |

⚠️ **Nota**: "En declive" no significa "no funciona". Si tienes una app estable en CodeIgniter, no necesitas reescribirla. Pero para proyectos nuevos, elige tecnología con comunidad activa.

---

## ¿Necesitas un framework JavaScript?

Antes de elegir React, Vue o Svelte, pregúntate: **¿realmente lo necesitas?**

**NO necesitas un framework JS si:**
- Es un sitio mayormente estático (blog, landing, documentación)
- La interactividad es mínima (formularios simples, menús)
- El SEO es crítico y el contenido no cambia frecuentemente
- Ya usas Laravel/Django/Rails y Livewire/HTMX/Hotwire resuelven tu caso
- Tu equipo es más fuerte en PHP/Python/Ruby que en JavaScript
- Es un proyecto pequeño con vida útil corta

**Alternativas al JavaScript moderno:**
- **Laravel + Livewire** — Full-stack PHP, muy productivo
- **Rails + Hotwire** — Full-stack Ruby, convenciones sólidas
- **Django + HTMX** — Full-stack Python, ideal para data apps
- **Astro** — Genera HTML estático, agrega JS solo donde necesitas
- **HTML + Alpine.js** — Reactividad ligera, directamente en HTML

**SÍ necesitas un framework JS si:**
- La UI es altamente interactiva (editores de texto/imagen, drag & drop complejo)
- Necesitas funcionalidad offline (PWA)
- Es una aplicación tipo "app" más que tipo "sitio web"
- El equipo ya domina React/Vue y quiere reutilizar ese conocimiento
- Necesitas React Native para móvil

💡 **Insight**: GitHub, Basecamp, Shopify Admin, Hey.com — todas son aplicaciones complejas construidas principalmente con server-rendered + sprinkles de JavaScript. No todo necesita ser un SPA.

---

## Comparativa de Stacks: La vista completa

| Stack | Mejor para | Tendencia | Curva aprendizaje |
|-------|-----------|-----------|-------------------|
| **Next.js (React)** | Apps interactivas complejas, e-commerce | ↗️ En auge | Media |
| **Laravel + Livewire** | CRUD, dashboards, MVPs | ↗️ En auge | Baja |
| **Rails + Hotwire** | Startups, SaaS, productos | ↗️ Resurgiendo | Baja |
| **Nuxt (Vue)** | Apps donde Vue es preferido | → Estable | Baja |
| **Django + HTMX** | Data apps, ML, admin | → Estable | Media |
| **SvelteKit** | Performance crítico, innovadores | ↗️ Creciendo | Baja |
| **Astro** | Sitios de contenido, blogs, docs | ↗️ En auge | Baja |
| **Remix** | Apps con mucho data loading | → Estable | Media |

---

## Eligiendo tu Stack JavaScript

Si decidiste que necesitas un framework JavaScript, estas son las opciones principales:

### React: El estándar de la industria

**Fortalezas:**
- Ecosistema más grande (librerías para todo)
- Más fácil encontrar desarrolladores
- Meta-frameworks maduros (Next.js, Remix)
- React Native para móvil

**Debilidades:**
- Verboso comparado con alternativas
- Muchas formas de hacer lo mismo (confusión)
- Rendimiento no es el mejor out-of-the-box
- "JavaScript fatigue" — demasiadas decisiones

**Úsalo cuando:**
- Necesitas el ecosistema más grande
- El equipo ya lo conoce
- Quieres contratar fácilmente

```jsx
// React: Componente típico
function ProductCard({ product, onAddToCart }) {
  const [quantity, setQuantity] = useState(1);

  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <input
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
      />
      <button onClick={() => onAddToCart(product, quantity)}>
        Agregar al carrito
      </button>
    </div>
  );
}
```

### Vue: El balance pragmático

**Fortalezas:**
- Curva de aprendizaje más suave
- Documentación excelente
- Single File Components (HTML, CSS, JS juntos)
- Menos decisiones que tomar

**Debilidades:**
- Ecosistema más pequeño que React
- Menos ofertas laborales (depende de la región)
- Vue 2 vs Vue 3 fragmentó la comunidad

**Úsalo cuando:**
- Quieres productividad rápida
- El equipo tiene experiencia variada
- Prefieres convenciones sobre configuración

```vue
<!-- Vue: Single File Component -->
<template>
  <div class="product-card">
    <img :src="product.image" :alt="product.name" />
    <h3>{{ product.name }}</h3>
    <p>${{ product.price }}</p>
    <input type="number" v-model="quantity" />
    <button @click="addToCart">Agregar al carrito</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps(['product']);
const emit = defineEmits(['add-to-cart']);

const quantity = ref(1);

function addToCart() {
  emit('add-to-cart', props.product, quantity.value);
}
</script>

<style scoped>
.product-card {
  /* Estilos encapsulados automáticamente */
}
</style>
```

### Svelte: El compilador inteligente

**Fortalezas:**
- Sin Virtual DOM — compila a JavaScript vanilla
- Sintaxis más limpia y menos boilerplate
- Bundles más pequeños
- Rendimiento excelente

**Debilidades:**
- Ecosistema más pequeño
- Menos recursos de aprendizaje
- Menos desarrolladores disponibles
- SvelteKit aún madurando

**Úsalo cuando:**
- El rendimiento es crítico
- Prefieres escribir menos código
- Estás dispuesto a ser early adopter

```svelte
<!-- Svelte: Sintaxis minimalista -->
<script>
  export let product;
  let quantity = 1;

  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function addToCart() {
    dispatch('add-to-cart', { product, quantity });
  }
</script>

<div class="product-card">
  <img src={product.image} alt={product.name} />
  <h3>{product.name}</h3>
  <p>${product.price}</p>
  <input type="number" bind:value={quantity} />
  <button on:click={addToCart}>Agregar al carrito</button>
</div>

<style>
  .product-card {
    /* Estilos automáticamente scoped */
  }
</style>
```

### Comparación rápida

| Aspecto | React | Vue | Svelte |
|---------|-------|-----|--------|
| Curva de aprendizaje | Media | Baja | Baja |
| Tamaño del bundle | ~40KB | ~30KB | ~2KB |
| Ecosistema | Enorme | Grande | Pequeño |
| Ofertas laborales | Muchas | Moderadas | Pocas |
| Rendimiento | Bueno | Bueno | Excelente |
| DX (Developer Experience) | Buena | Muy buena | Excelente |

---

## Estructura de Proyecto

Una buena estructura te salva cuando el proyecto crece.

### Estructura por tipo (la clásica)

```
src/
├── components/        # Todos los componentes
│   ├── Button.jsx
│   ├── Card.jsx
│   ├── Modal.jsx
│   └── ...
├── pages/            # Páginas/rutas
│   ├── Home.jsx
│   ├── Product.jsx
│   └── Checkout.jsx
├── hooks/            # Custom hooks
├── utils/            # Funciones utilitarias
├── services/         # Llamadas a APIs
├── styles/           # CSS global
└── assets/           # Imágenes, fuentes
```

**Pros:** Simple, familiar
**Cons:** Escala mal, archivos no relacionados juntos

### Estructura por feature (recomendada)

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   ├── services/
│   │   │   └── authApi.js
│   │   └── index.js          # Exporta la API pública
│   │
│   ├── products/
│   │   ├── components/
│   │   │   ├── ProductCard.jsx
│   │   │   ├── ProductList.jsx
│   │   │   └── ProductFilters.jsx
│   │   ├── hooks/
│   │   │   └── useProducts.js
│   │   ├── services/
│   │   │   └── productsApi.js
│   │   └── index.js
│   │
│   └── cart/
│       ├── components/
│       ├── hooks/
│       └── ...
│
├── shared/               # Componentes compartidos
│   ├── components/
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   └── Modal.jsx
│   ├── hooks/
│   │   └── useLocalStorage.js
│   └── utils/
│       └── formatCurrency.js
│
├── pages/               # Solo routing, importa de features
│   ├── index.jsx
│   ├── products/[id].jsx
│   └── checkout.jsx
│
└── app/                 # Configuración global
    ├── providers.jsx
    ├── routes.jsx
    └── store.js
```

**Pros:**
- Código relacionado junto
- Fácil de navegar
- Escala bien
- Fácil de extraer a paquetes

**Cons:**
- Más setup inicial
- Puede ser overkill para proyectos pequeños

### Reglas de importación

```
┌─────────────────────────────────────────────────────────────┐
│                    REGLAS DE DEPENDENCIA                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   pages  ────────────▶  features  ────────────▶  shared     │
│                              │                               │
│                              │                               │
│                              ▼                               │
│                           app/store                          │
│                                                              │
│   ✓ pages importa de features                                │
│   ✓ features importa de shared                               │
│   ✓ shared NO importa de features                            │
│   ✗ features NO importan entre sí (usar shared o store)      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

💡 **Insight**: Si un componente se usa en múltiples features, pertenece a `shared/`. Si solo se usa en una feature, quédate ahí.

---

## Manejo de Estado

El estado es la fuente de la mayoría de bugs en frontend. Manejarlo bien es crítico.

### Tipos de estado

```
┌─────────────────────────────────────────────────────────────┐
│                     TIPOS DE ESTADO                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  LOCAL              │  COMPARTIDO          │  SERVER         │
│  ──────────────     │  ─────────────────   │  ──────────     │
│  • Form inputs      │  • Usuario actual    │  • Productos    │
│  • UI toggles       │  • Carrito           │  • Pedidos      │
│  • Animaciones      │  • Tema/idioma       │  • Usuarios     │
│  • Modals abiertos  │  • Notificaciones    │  • Comentarios  │
│                     │                      │                  │
│  useState/          │  Context/Zustand/    │  React Query/   │
│  useReducer         │  Redux               │  SWR/TanStack   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Estado Local: useState y useReducer

**useState** — Para estado simple:

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicks: {count}
    </button>
  );
}
```

**useReducer** — Para estado con lógica compleja:

```jsx
const initialState = {
  items: [],
  loading: false,
  error: null
};

function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM':
      return {
        ...state,
        items: [...state.items, action.payload]
      };
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload)
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
}

function Cart() {
  const [state, dispatch] = useReducer(cartReducer, initialState);

  const addItem = (item) => dispatch({ type: 'ADD_ITEM', payload: item });
  const removeItem = (id) => dispatch({ type: 'REMOVE_ITEM', payload: id });

  // ...
}
```

### Estado Compartido: Las opciones

#### 1. Context API (built-in)

Bueno para estado que cambia poco (tema, usuario, idioma).

```jsx
// AuthContext.jsx
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = async (credentials) => {
    const user = await authApi.login(credentials);
    setUser(user);
  };

  const logout = () => {
    authApi.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

// Uso
function Header() {
  const { user, logout } = useAuth();

  return user ? (
    <button onClick={logout}>Cerrar sesión</button>
  ) : (
    <Link to="/login">Iniciar sesión</Link>
  );
}
```

⚠️ **Problema**: Context re-renderiza TODOS los consumidores cuando cambia cualquier valor. Para estado que cambia frecuentemente, considera alternativas.

#### 2. Zustand (ligero, moderno)

Mi recomendación para la mayoría de proyectos:

```jsx
// stores/cartStore.js
import { create } from 'zustand';

const useCartStore = create((set, get) => ({
  items: [],

  addItem: (product) => set((state) => ({
    items: [...state.items, { ...product, quantity: 1 }]
  })),

  removeItem: (productId) => set((state) => ({
    items: state.items.filter(item => item.id !== productId)
  })),

  updateQuantity: (productId, quantity) => set((state) => ({
    items: state.items.map(item =>
      item.id === productId ? { ...item, quantity } : item
    )
  })),

  // Computed values
  get totalItems() {
    return get().items.reduce((sum, item) => sum + item.quantity, 0);
  },

  get totalPrice() {
    return get().items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );
  },

  clearCart: () => set({ items: [] })
}));

// Uso - solo re-renderiza si cambia lo que usas
function CartIcon() {
  const totalItems = useCartStore((state) => state.totalItems);
  return <span>🛒 {totalItems}</span>;
}

function CartTotal() {
  const totalPrice = useCartStore((state) => state.totalPrice);
  return <span>Total: ${totalPrice}</span>;
}
```

**¿Por qué Zustand sobre Redux?**
- Menos boilerplate (mucho menos)
- No necesita Provider
- TypeScript friendly
- Selectores automáticos para evitar re-renders

#### 3. Redux Toolkit (cuando necesitas el cañón)

Para apps enterprise con estado muy complejo:

```jsx
// features/cart/cartSlice.js
import { createSlice } from '@reduxjs/toolkit';

const cartSlice = createSlice({
  name: 'cart',
  initialState: { items: [] },
  reducers: {
    addItem: (state, action) => {
      state.items.push(action.payload); // Immer permite "mutación"
    },
    removeItem: (state, action) => {
      state.items = state.items.filter(item => item.id !== action.payload);
    }
  }
});

export const { addItem, removeItem } = cartSlice.actions;
export default cartSlice.reducer;
```

### Estado del Servidor: React Query / TanStack Query

El estado del servidor (datos de APIs) es diferente al estado de UI. Necesita:
- Caché
- Revalidación
- Estados de carga/error
- Sincronización

**React Query maneja todo esto:**

```jsx
// hooks/useProducts.js
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useProducts(filters) {
  return useQuery({
    queryKey: ['products', filters],
    queryFn: () => api.getProducts(filters),
    staleTime: 5 * 60 * 1000, // 5 minutos antes de refetch
  });
}

export function useProduct(id) {
  return useQuery({
    queryKey: ['product', id],
    queryFn: () => api.getProduct(id),
  });
}

export function useCreateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.createProduct,
    onSuccess: () => {
      // Invalida el caché para que se refetche
      queryClient.invalidateQueries({ queryKey: ['products'] });
    }
  });
}

// Uso en componente
function ProductList() {
  const { data: products, isLoading, error } = useProducts({ category: 'electronics' });

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return (
    <ul>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </ul>
  );
}
```

**Beneficios:**
- Caché automático
- Deduplicación de requests
- Background refetching
- Optimistic updates
- Retry automático
- DevTools excelentes

💡 **Insight**: Para la mayoría de apps, React Query + Zustand es todo lo que necesitas. Context para auth/theme, Zustand para UI compartida, React Query para datos del servidor.

---

## Patrones de Renderizado

### CSR: Client-Side Rendering

El navegador recibe HTML vacío, JavaScript construye la UI.

```
Servidor                    Navegador
────────                    ─────────
   │                            │
   │ ──── HTML vacío ────────▶ │
   │                            │ (pantalla blanca)
   │ ──── bundle.js ─────────▶ │
   │                            │ (descargando...)
   │                            │ (parseando...)
   │                            │ (ejecutando...)
   │ ◀──── fetch /api/data ─── │
   │                            │
   │ ──── JSON ───────────────▶│
   │                            │ ¡UI lista!
   │                            │
```

**Pros:**
- Simple de implementar
- Hosting barato (CDN)
- Buena experiencia después de carga inicial

**Cons:**
- Mala primera carga (pantalla blanca)
- Malo para SEO (robots ven HTML vacío)
- Requiere JavaScript

**Úsalo para:** Dashboards, apps internas, SPAs detrás de login

### SSR: Server-Side Rendering

El servidor genera HTML completo en cada request.

```
Servidor                    Navegador
────────                    ─────────
   │ (genera HTML)              │
   │                            │
   │ ──── HTML completo ─────▶ │ ¡Contenido visible!
   │                            │ (pero no interactivo)
   │ ──── bundle.js ─────────▶ │
   │                            │ (hydration)
   │                            │ ¡Interactivo!
   │                            │
```

**Pros:**
- Buena primera carga (contenido inmediato)
- Bueno para SEO
- Funciona sin JavaScript (parcialmente)

**Cons:**
- Servidor más cargado
- TTFB más lento (Time To First Byte)
- Complejidad de hydration

**Úsalo para:** E-commerce, blogs, contenido público que necesita SEO

### SSG: Static Site Generation

HTML generado en build time, servido desde CDN.

```
Build time                  Runtime
──────────                  ───────
   │                            │
   │ (genera HTML              │
   │  para cada página)        │
   │                            │
   │ ──── archivos .html ────▶ CDN
   │                            │
                           Navegador
                           ─────────
   CDN ──── HTML completo ──▶ │ ¡Instantáneo!
       ──── bundle.js ──────▶ │ (hydration)
                               │ ¡Interactivo!
```

**Pros:**
- Más rápido posible (CDN)
- SEO excelente
- Muy barato de hostear
- Seguro (no hay servidor que hackear)

**Cons:**
- No sirve para contenido dinámico
- Rebuild necesario para cambios
- Build times largos con muchas páginas

**Úsalo para:** Blogs, documentación, landing pages, sitios de marketing

### ISR: Incremental Static Regeneration

Lo mejor de SSG + SSR: páginas estáticas que se regeneran.

```jsx
// Next.js
export async function getStaticProps() {
  const products = await getProducts();

  return {
    props: { products },
    revalidate: 60, // Regenerar cada 60 segundos
  };
}
```

**Cómo funciona:**
1. Primera visita: sirve página estática del build
2. Si tiene más de 60 segundos, sirve la vieja Y regenera en background
3. Siguiente visita: sirve la nueva versión

**Úsalo para:** E-commerce, noticias, contenido que cambia pero no en tiempo real

### Comparación

| Patrón | Primera carga | SEO | Servidor | Caso de uso |
|--------|--------------|-----|----------|-------------|
| CSR | Lenta | Malo | No necesita | Dashboards, SPAs |
| SSR | Rápida | Bueno | Necesita | Apps dinámicas |
| SSG | Muy rápida | Excelente | No necesita | Blogs, docs |
| ISR | Muy rápida | Excelente | Necesita | E-commerce |

### React Server Components (RSC)

El futuro: componentes que SOLO corren en el servidor.

```jsx
// Este componente NUNCA llega al navegador
async function ProductList() {
  // Puedes hacer fetch directamente, sin useEffect
  const products = await db.query('SELECT * FROM products');

  return (
    <ul>
      {products.map(product => (
        // Este es un Client Component (interactivo)
        <ProductCard key={product.id} product={product} />
      ))}
    </ul>
  );
}
```

**Beneficios:**
- Bundle más pequeño (código del servidor no se envía)
- Acceso directo a base de datos
- Sin waterfalls de fetch

Esto es el default en Next.js 13+ con App Router.

---

## Performance Frontend

### Core Web Vitals

Google mide tres métricas clave:

```
┌─────────────────────────────────────────────────────────────┐
│                    CORE WEB VITALS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  LCP (Largest Contentful Paint)                              │
│  ────────────────────────────────                            │
│  ¿Cuándo aparece el contenido principal?                     │
│  Bueno: < 2.5s  │  Mejorar: 2.5-4s  │  Malo: > 4s           │
│                                                              │
│  FID (First Input Delay) / INP (Interaction to Next Paint)  │
│  ──────────────────────────────────────────────────────────  │
│  ¿Cuánto tarda en responder a un click?                      │
│  Bueno: < 100ms  │  Mejorar: 100-300ms  │  Malo: > 300ms    │
│                                                              │
│  CLS (Cumulative Layout Shift)                               │
│  ─────────────────────────────                               │
│  ¿Cuánto "salta" el contenido mientras carga?                │
│  Bueno: < 0.1  │  Mejorar: 0.1-0.25  │  Malo: > 0.25        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Optimizaciones comunes

#### 1. Code Splitting

No cargues todo el JavaScript de una vez:

```jsx
// Antes: todo en un bundle
import HeavyChart from './HeavyChart';

// Después: carga bajo demanda
const HeavyChart = lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      <HeavyChart data={data} />
    </Suspense>
  );
}
```

#### 2. Imágenes optimizadas

```jsx
// Next.js Image - optimización automática
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // Para LCP
  placeholder="blur" // Evita CLS
/>

// HTML nativo con lazy loading
<img
  src="product.jpg"
  alt="Product"
  loading="lazy"  // Carga cuando está visible
  decoding="async"
  width="300"
  height="200"  // Evita CLS
/>
```

#### 3. Memoización

Evita re-renders innecesarios:

```jsx
// memo: evita re-render si props no cambian
const ProductCard = memo(function ProductCard({ product }) {
  return <div>{product.name}</div>;
});

// useMemo: cachea valores calculados
function ProductList({ products }) {
  const sortedProducts = useMemo(
    () => products.sort((a, b) => a.price - b.price),
    [products]
  );

  return sortedProducts.map(p => <ProductCard key={p.id} product={p} />);
}

// useCallback: cachea funciones
function Parent() {
  const handleClick = useCallback((id) => {
    // ...
  }, []);

  return <Child onClick={handleClick} />;
}
```

⚠️ **Advertencia**: No memoices todo. Medir primero, optimizar después. La memoización prematura puede empeorar el rendimiento.

#### 4. Virtualización

Para listas largas (miles de items):

```jsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }) {
  const parentRef = useRef(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // altura estimada de cada item
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: virtualItem.start,
              height: virtualItem.size,
            }}
          >
            {items[virtualItem.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

Solo renderiza los items visibles, no importa si tienes 10,000.

#### 5. Prefetching

Carga recursos antes de que se necesiten:

```jsx
// Next.js - prefetch automático en links visibles
<Link href="/products" prefetch>
  Ver productos
</Link>

// React Query - prefetch en hover
function ProductLink({ id }) {
  const queryClient = useQueryClient();

  const prefetchProduct = () => {
    queryClient.prefetchQuery({
      queryKey: ['product', id],
      queryFn: () => api.getProduct(id),
    });
  };

  return (
    <Link
      href={`/products/${id}`}
      onMouseEnter={prefetchProduct}
    >
      Ver producto
    </Link>
  );
}
```

---

## Styling: Las opciones

El estilado en aplicaciones web ha evolucionado dramáticamente. Pasamos de escribir CSS global a tener docenas de soluciones, cada una intentando resolver problemas específicos. Entender el **por qué** de cada opción te ayudará a elegir la correcta.

### El problema original del CSS

CSS fue diseñado para documentos, no para aplicaciones. Esto causa problemas:

```
┌─────────────────────────────────────────────────────────────┐
│           PROBLEMAS DEL CSS GLOBAL                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. COLISIONES DE NOMBRES                                    │
│     Dos desarrolladores crean .button → conflicto           │
│                                                              │
│  2. ESPECIFICIDAD IMPREDECIBLE                               │
│     .nav .button vs #main .button → ¿cuál gana?             │
│                                                              │
│  3. CSS MUERTO                                               │
│     ¿Puedo borrar .old-header? ¿Lo usa alguien?             │
│                                                              │
│  4. DEPENDENCIAS OCULTAS                                     │
│     Un componente asume que existe .container en otro lugar │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

Las diferentes soluciones intentan resolver uno o más de estos problemas.

### Opción 1: CSS Global (el baseline)

La forma más simple: archivos `.css` que se aplican a toda la aplicación.

```css
/* styles/global.css */
.button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.button-primary {
  background-color: #3b82f6;
  color: white;
}

.button-secondary {
  background-color: #e5e7eb;
  color: #374151;
}
```

```jsx
// En tu componente
function Button({ variant, children }) {
  return (
    <button className={`button button-${variant}`}>
      {children}
    </button>
  );
}
```

**Cuándo funciona bien:**
- Proyectos pequeños (menos de 20 componentes)
- Equipos pequeños donde todos conocen el CSS existente
- Prototipos rápidos
- Sitios estáticos simples

**Problemas:**
- Las clases son globales: `.button` en un archivo afecta a todo
- Difícil de mantener cuando crece
- No sabes qué CSS está en uso
- Los nombres se vuelven largos para evitar colisiones: `.homepage-hero-button-primary`

### Opción 2: Preprocesadores (Sass/SCSS)

Sass añade características que CSS no tiene: variables, anidamiento, mixins, funciones.

```scss
/* styles/button.scss */

// Variables reutilizables
$primary-color: #3b82f6;
$secondary-color: #e5e7eb;
$border-radius: 4px;

// Mixins para patrones comunes
@mixin button-base {
  padding: 8px 16px;
  border-radius: $border-radius;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.button {
  @include button-base;

  // Anidamiento - más legible que selectores largos
  &-primary {
    background-color: $primary-color;
    color: white;

    &:hover {
      background-color: darken($primary-color, 10%);
    }
  }

  &-secondary {
    background-color: $secondary-color;
    color: #374151;

    &:hover {
      background-color: darken($secondary-color, 5%);
    }
  }

  // Estados
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
```

**¿Qué resuelve?**
- Variables evitan repetir valores (colores, tamaños)
- Anidamiento hace el código más organizado
- Mixins eliminan duplicación de patrones
- Funciones como `darken()` calculan valores

**¿Qué NO resuelve?**
- Las clases siguen siendo globales
- Aún puedes tener colisiones de nombres
- El CSS compilado puede ser enorme si no tienes cuidado

**Estado actual (2024):** Sass sigue siendo muy usado, especialmente en proyectos con Laravel, Rails, o sitios tradicionales. Sin embargo, CSS moderno ha adoptado variables nativas (`--variable`) que cubren el caso de uso más común.

### Opción 3: CSS Modules

CSS Modules resuelve el problema de las colisiones: cada clase es **automáticamente única** por archivo.

```css
/* Button.module.css */
.button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.primary {
  background-color: #3b82f6;
  color: white;
}

.secondary {
  background-color: #e5e7eb;
  color: #374151;
}
```

```jsx
// Button.jsx
import styles from './Button.module.css';

function Button({ variant, children }) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}

// En el navegador, las clases se transforman:
// <button class="Button_button_x7d3f Button_primary_k2m9s">
```

**¿Cómo funciona?**

El bundler (Webpack, Vite) transforma las clases:
- `.button` → `Button_button_x7d3f` (nombre de archivo + clase + hash)
- Esto hace imposible que dos `.button` de archivos diferentes colisionen

**Composición:**

Puedes combinar estilos entre archivos:

```css
/* shared/typography.module.css */
.heading {
  font-weight: 700;
  line-height: 1.2;
}

/* Card.module.css */
.title {
  composes: heading from '../shared/typography.module.css';
  font-size: 1.5rem;
  color: #111;
}
```

**Pros:**
- CSS puro (sin aprender sintaxis nueva)
- Sin colisiones de nombres
- Bundler elimina CSS no usado
- Sin JavaScript en runtime (performance óptima)
- Funciona con cualquier framework

**Cons:**
- Estilos dinámicos requieren múltiples clases o CSS variables
- No hay anidamiento (a menos que combines con Sass)
- Nombres de clase largos en el HTML generado

**Ideal para:** Proyectos que quieren CSS tradicional pero con scope automático.

### Opción 4: Tailwind CSS

Tailwind es un framework **utility-first**: en lugar de escribir CSS, aplicas clases pequeñas directamente en el HTML.

```jsx
// Sin Tailwind: CSS separado
// button.css: .button { padding: 8px 16px; border-radius: 4px; ... }
// <button className="button button-primary">Click</button>

// Con Tailwind: estilos en el HTML
function Button({ variant, children }) {
  const baseStyles = "px-4 py-2 rounded font-medium transition-colors";
  const variants = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300"
  };

  return (
    <button className={`${baseStyles} ${variants[variant]}`}>
      {children}
    </button>
  );
}
```

**¿Qué significa cada clase?**
- `px-4` → padding horizontal de 1rem (16px)
- `py-2` → padding vertical de 0.5rem (8px)
- `rounded` → border-radius
- `bg-blue-500` → background color (escala de azules)
- `hover:bg-blue-600` → color más oscuro al hacer hover

**Sistema de diseño incluido:**

Tailwind viene con una escala predefinida y consistente:

```
Espaciado: 0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 14, 16...
           (en múltiplos de 0.25rem)

Colores: gray-50 a gray-900, blue-50 a blue-900, red-50...
         (escala de 10 tonos por color)

Font sizes: xs, sm, base, lg, xl, 2xl, 3xl...
```

Esto fuerza consistencia: no puedes poner `padding: 13px` arbitrariamente.

**Personalización:**

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          900: '#0c4a6e',
        }
      },
      spacing: {
        '18': '4.5rem',
      }
    }
  }
}
```

**Componentes reutilizables:**

Para evitar repetir clases, extraes a componentes:

```jsx
// components/Button.jsx
export function Button({ variant = 'primary', children, ...props }) {
  const styles = {
    base: "px-4 py-2 rounded-lg font-medium transition-colors focus:ring-2",
    primary: "bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-300",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-300",
    danger: "bg-red-500 text-white hover:bg-red-600 focus:ring-red-300",
  };

  return (
    <button
      className={`${styles.base} ${styles[variant]}`}
      {...props}
    >
      {children}
    </button>
  );
}

// Uso
<Button variant="primary">Guardar</Button>
<Button variant="danger">Eliminar</Button>
```

**¿Por qué es controversial?**

Tailwind genera debates fuertes. Argumentos a favor y en contra:

| A favor | En contra |
|---------|-----------|
| Desarrollo muy rápido | HTML muy verboso |
| Consistencia forzada | Curva de aprendizaje (memorizar clases) |
| No hay CSS muerto | Difícil de leer para algunos |
| Cambios sin miedo (no afectas otros componentes) | Estilos responsivos verbosos |
| Bundle final pequeño (purga lo no usado) | Menos semántico |

**Ejemplo de HTML verboso (la crítica principal):**

```html
<!-- Tailwind puede volverse así -->
<div class="flex items-center justify-between p-4 bg-white rounded-lg shadow-md
            hover:shadow-lg transition-shadow border border-gray-100
            dark:bg-gray-800 dark:border-gray-700">
  <div class="flex items-center space-x-3">
    <img class="w-10 h-10 rounded-full object-cover" src="...">
    <div class="flex flex-col">
      <span class="font-medium text-gray-900 dark:text-white">...</span>
      <span class="text-sm text-gray-500 dark:text-gray-400">...</span>
    </div>
  </div>
</div>
```

**Solución al HTML verboso:** Extraer a componentes. El HTML largo solo existe una vez, en el componente.

**Ideal para:**
- Prototipos rápidos
- Equipos que quieren consistencia sin escribir CSS
- Proyectos con muchos componentes únicos
- Desarrolladores que prefieren "todo en un lugar"

### Opción 5: CSS-in-JS (styled-components, Emotion)

CSS-in-JS escribe los estilos **dentro de JavaScript**, junto al componente.

```jsx
import styled from 'styled-components';

// Creas un componente estilizado
const Button = styled.button`
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;

  /* Estilos dinámicos basados en props */
  background-color: ${props => props.primary ? '#3b82f6' : '#e5e7eb'};
  color: ${props => props.primary ? 'white' : '#374151'};

  &:hover {
    background-color: ${props => props.primary ? '#2563eb' : '#d1d5db'};
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Uso: es un componente normal de React
function App() {
  return (
    <div>
      <Button primary>Guardar</Button>
      <Button>Cancelar</Button>
      <Button primary disabled>Cargando...</Button>
    </div>
  );
}
```

**¿Cómo funciona?**

1. En runtime, la librería parsea el template literal (el CSS)
2. Genera clases únicas dinámicamente
3. Inyecta el CSS en un `<style>` tag en el `<head>`

**Variantes con Emotion:**

```jsx
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';

// Opción 1: css prop
function Button({ primary, children }) {
  return (
    <button
      css={css`
        padding: 8px 16px;
        background-color: ${primary ? '#3b82f6' : '#e5e7eb'};
        color: ${primary ? 'white' : '#374151'};
      `}
    >
      {children}
    </button>
  );
}

// Opción 2: styled (igual que styled-components)
import styled from '@emotion/styled';

const Button = styled.button`
  /* ... */
`;
```

**Pros:**
- Estilos junto al componente (colocation)
- Estilos completamente dinámicos (cualquier lógica JS)
- Scope automático (clases únicas generadas)
- Tematización fácil (ThemeProvider)
- TypeScript-friendly (props tipadas)

**Cons:**
- **Runtime overhead**: El CSS se genera en el navegador
- **Bundle size**: La librería añade ~10-15KB
- **Server Components**: No funcionan bien con React Server Components
- **Debugging**: El CSS generado tiene clases como `css-1a2b3c4`

**El problema con Server Components:**

React Server Components (Next.js 13+) ejecutan en el servidor, pero CSS-in-JS necesita JavaScript en el cliente para funcionar. Esto crea conflictos y peor performance.

**¿Cuándo usar CSS-in-JS?**
- Apps muy dinámicas donde los estilos dependen mucho del estado
- Si ya lo estás usando y funciona (no migres por moda)
- Proyectos pre-Server Components que funcionan bien

**Tendencia (2024):** CSS-in-JS está en declive para nuevos proyectos. La industria se mueve hacia soluciones zero-runtime como Tailwind o CSS Modules.

### Opción 6: CSS Variables (Custom Properties)

CSS moderno tiene variables nativas. Esto resuelve muchos casos sin librerías.

```css
/* variables.css */
:root {
  /* Colores */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-secondary: #e5e7eb;
  --color-text: #374151;
  --color-text-light: #6b7280;

  /* Espaciado */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;

  /* Tipografía */
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;

  /* Otros */
  --border-radius: 4px;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Dark mode con variables */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #60a5fa;
    --color-secondary: #374151;
    --color-text: #f3f4f6;
    --color-text-light: #9ca3af;
  }
}

/* Usando las variables */
.button {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  background-color: var(--color-primary);
  color: white;
  transition: background-color 0.2s;
}

.button:hover {
  background-color: var(--color-primary-hover);
}
```

**Dinámico desde JavaScript:**

```jsx
function App() {
  const changeTheme = (primaryColor) => {
    document.documentElement.style.setProperty('--color-primary', primaryColor);
  };

  return (
    <div>
      <button onClick={() => changeTheme('#ef4444')}>Tema Rojo</button>
      <button onClick={() => changeTheme('#22c55e')}>Tema Verde</button>
    </div>
  );
}
```

**Pros:**
- Nativo (sin librerías)
- Zero runtime
- Funciona con cualquier solución CSS
- Excelente para tematización (dark mode, branding)

**Cons:**
- Sin scope automático
- Necesitas disciplina para organizar las variables

**Combínalo con otras soluciones:** CSS Variables funciona bien con CSS Modules o incluso Tailwind.

### Comparativa rápida

| Solución | Scope | Runtime | Curva aprendizaje | Server Components | Ideal para |
|----------|-------|---------|-------------------|-------------------|------------|
| CSS Global | ❌ Global | Ninguno | Muy baja | ✅ Perfecto | Proyectos pequeños |
| Sass/SCSS | ❌ Global | Ninguno | Baja | ✅ Perfecto | Proyectos tradicionales |
| CSS Modules | ✅ Automático | Ninguno | Baja | ✅ Perfecto | Balance simplicidad/scope |
| Tailwind | ✅ Por clase | Ninguno | Media | ✅ Perfecto | Desarrollo rápido |
| CSS-in-JS | ✅ Automático | Alto | Media | ⚠️ Problemas | Apps muy dinámicas |
| CSS Variables | ❌ Global | Ninguno | Baja | ✅ Perfecto | Temas, design tokens |

### Mi recomendación (2024+)

```
┌─────────────────────────────────────────────────────────────┐
│              DECISIÓN DE STYLING                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ¿Proyecto nuevo con React/Vue/Svelte?                       │
│  └─▶ Tailwind CSS (más productivo, mejor DX)                │
│                                                              │
│  ¿Prefieres CSS tradicional?                                 │
│  └─▶ CSS Modules + CSS Variables (scope + temas)            │
│                                                              │
│  ¿Proyecto Laravel/Rails/Django?                             │
│  └─▶ Sass + CSS Variables (convención del ecosistema)       │
│                                                              │
│  ¿Proyecto existente con styled-components?                  │
│  └─▶ No migres solo por moda, pero evita en nuevos          │
│                                                              │
│  ¿Sitio estático simple?                                     │
│  └─▶ CSS Global + CSS Variables (no over-engineer)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**La tendencia clara:** La industria se mueve hacia soluciones **zero-runtime** (Tailwind, CSS Modules) y lejos de CSS-in-JS. React Server Components aceleraron este cambio.

---

## Testing Frontend

### Pirámide de tests

```
                 ┌─────────┐
                 │   E2E   │  Pocos, lentos, frágiles
                 │Playwright│
                └───────────┘
               ┌─────────────┐
               │ Integration │  Moderados
               │   Testing   │
               │   Library   │
              └───────────────┘
             ┌─────────────────┐
             │      Unit       │  Muchos, rápidos, estables
             │     Vitest      │
            └───────────────────┘
```

### Unit Tests con Vitest

```jsx
// utils/formatCurrency.test.js
import { describe, it, expect } from 'vitest';
import { formatCurrency } from './formatCurrency';

describe('formatCurrency', () => {
  it('formats positive numbers', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56');
  });

  it('handles zero', () => {
    expect(formatCurrency(0)).toBe('$0.00');
  });

  it('handles negative numbers', () => {
    expect(formatCurrency(-50)).toBe('-$50.00');
  });
});
```

### Integration Tests con Testing Library

```jsx
// ProductCard.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ProductCard } from './ProductCard';

describe('ProductCard', () => {
  const product = {
    id: 1,
    name: 'Laptop',
    price: 999,
    image: '/laptop.jpg'
  };

  it('renders product info', () => {
    render(<ProductCard product={product} />);

    expect(screen.getByText('Laptop')).toBeInTheDocument();
    expect(screen.getByText('$999')).toBeInTheDocument();
  });

  it('calls onAddToCart when button clicked', () => {
    const onAddToCart = vi.fn();
    render(<ProductCard product={product} onAddToCart={onAddToCart} />);

    fireEvent.click(screen.getByRole('button', { name: /agregar/i }));

    expect(onAddToCart).toHaveBeenCalledWith(product, 1);
  });
});
```

### E2E con Playwright

```javascript
// tests/checkout.spec.js
import { test, expect } from '@playwright/test';

test('user can complete checkout', async ({ page }) => {
  await page.goto('/products');

  // Agregar producto al carrito
  await page.click('[data-testid="product-1"] button');

  // Ir al carrito
  await page.click('[data-testid="cart-icon"]');
  expect(await page.locator('.cart-item').count()).toBe(1);

  // Checkout
  await page.click('text=Proceder al pago');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="card"]', '4242424242424242');
  await page.click('text=Pagar');

  // Confirmación
  await expect(page.locator('text=¡Pedido confirmado!')).toBeVisible();
});
```

---

## 🤖 Usando IA para Desarrollo Frontend

La IA ha transformado el desarrollo frontend. Según datos de 2025, el 68% de desarrolladores ahorran más de 10 horas semanales usando herramientas de IA, y Google reporta que el 30% de su código es escrito por IA.

### Generación de componentes

```
Prompt efectivo:
"Crea un componente React de ProductCard que:
- Muestre imagen, nombre, precio y rating
- Tenga botón de agregar al carrito
- Use Tailwind CSS para estilos
- Incluya estados de hover y loading
- Sea accesible (ARIA labels apropiados)"
```

Herramientas como **v0.dev** reducen el tiempo de desarrollo frontend hasta un 70%.

### Casos de uso principales

**1. De diseño a código**

```
Prompt:
"Convierte este diseño de Figma/screenshot en un componente React:
- Usa los colores y espaciados exactos
- Hazlo responsive (mobile-first)
- Usa mi sistema de diseño existente (Tailwind config adjunta)"
```

Herramientas como **Visual Copilot** o **Kombai** generan código directamente desde Figma.

**2. Refactoring de componentes**

```
Prompt:
"Este componente de 300 líneas hace demasiado.
Divídelo en componentes más pequeños siguiendo
el principio de responsabilidad única.
Mantén la misma funcionalidad."
```

**3. Optimización de rendimiento**

```
Prompt:
"Revisa este componente React y sugiere optimizaciones:
- ¿Hay re-renders innecesarios?
- ¿Debería usar useMemo/useCallback?
- ¿Se puede hacer lazy loading de algo?
- ¿Los event handlers están bien optimizados?"
```

**4. Tests automatizados**

```
Prompt:
"Para este componente LoginForm, genera:
1. Tests unitarios con Vitest
2. Tests de integración con Testing Library
3. Casos edge (validación, errores de red)
Usa el patrón AAA (Arrange, Act, Assert)"
```

**5. Accesibilidad**

```
Prompt:
"Revisa este formulario de checkout y:
- Identifica problemas de accesibilidad
- Sugiere ARIA labels faltantes
- Verifica el orden de tabulación
- Genera atributos para screen readers"
```

### Herramientas destacadas

| Herramienta | Función |
|-------------|---------|
| **v0.dev** | Componentes React + Tailwind desde prompts |
| **Cursor** | IDE con IA que entiende todo tu proyecto |
| **GitHub Copilot** | Autocompletado inteligente y code review |
| **Visual Copilot** | Figma → React con un click |
| **Kombai** | Diseños → código production-ready |
| **Lovable** | Apps completas desde descripción |

### Limitaciones importantes

| ❌ Cuidado con... | ✅ Usa IA para... |
|-------------------|-------------------|
| Código generado sin revisar | Prototipos rápidos y borradores |
| Estilos inconsistentes con tu design system | Explorar ideas de UI |
| Componentes sin tests | Generar tests para código existente |
| Accesibilidad asumida | Auditar y sugerir mejoras de a11y |
| Lógica de negocio en la UI | Separar concerns cuando refactorizas |

### Flujo recomendado

```
1. Describe el componente en lenguaje natural
              ↓
2. IA genera estructura inicial
              ↓
3. Ajustas a tu design system
              ↓
4. IA genera tests
              ↓
5. Revisas accesibilidad con IA
              ↓
6. Optimizas rendimiento si es necesario
```

### Advertencia sobre código generado

> ⚠️ **Importante**: El código generado por IA puede:
> - No seguir tus convenciones de proyecto
> - Tener dependencias que no usas
> - Incluir patrones obsoletos
> - Fallar en edge cases
>
> **Siempre revisa, prueba, y adapta** a tu contexto.

> 🤖 **Nota**: La IA acelera tremendamente el desarrollo de UI, pero la **experiencia de usuario** requiere empatía humana. Los mejores frontends combinan velocidad de IA con criterio de diseño humano.

---

## Resumen

- **Evalúa si necesitas un framework** — A veces vanilla JS o Astro es suficiente
- **Elige basándote en tu contexto** — React (ecosistema), Vue (balance), Svelte (rendimiento)
- **Estructura por feature** — Código relacionado junto, escala mejor
- **Estado**: Local (useState), Compartido (Zustand), Servidor (React Query)
- **Renderizado**: CSR (dashboards), SSR/ISR (e-commerce), SSG (blogs)
- **Performance**: Core Web Vitals, code splitting, lazy loading
- **Testing**: Unit → Integration → E2E

---

## Ejercicios

1. **Auditoría**: Toma un proyecto frontend existente y mide sus Core Web Vitals con Lighthouse. Identifica 3 mejoras.

2. **Refactor**: Convierte una estructura "por tipo" a "por feature" en un proyecto pequeño.

3. **Estado**: Implementa un carrito de compras usando Zustand con persistencia en localStorage.

4. **Testing**: Escribe tests de integración para un formulario de login con Testing Library.

---

## Referencias

- Patterns.dev (2024). *React Design Patterns*. https://patterns.dev/
- web.dev (2024). *Core Web Vitals*. https://web.dev/vitals/
- Kent C. Dodds. *Testing JavaScript*. https://testingjavascript.com/
- Documentación oficial de React, Vue, Svelte, Next.js

---

**Anterior**: [Planificación Técnica](./10-planificacion-tecnica.md) | **Siguiente**: [Arquitectura Backend](./12-arquitectura-backend.md)
