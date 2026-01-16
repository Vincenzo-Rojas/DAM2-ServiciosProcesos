# Boilerplate API Node.js + Supabase + Redis

Sistema de autenticación con API Keys utilizando arquitectura en capas, Supabase como base de datos y Redis para rate limiting.

## 🏗️ Arquitectura

Este proyecto sigue una arquitectura en capas (Layered Architecture) con separación de responsabilidades:

```
src/
├── config/          # Configuraciones (BD, Redis, constantes)
├── models/          # Modelos de datos (entidades)
├── repositories/    # Acceso a datos (CRUD)
├── services/        # Lógica de negocio
├── controllers/     # Manejo de peticiones HTTP
├── routes/          # Definición de endpoints
├── middlewares/     # Middlewares de Express
└── utils/           # Funciones auxiliares
```

### Flujo de una petición:

```
Cliente HTTP
    ↓
Routes (define endpoint)
    ↓
Middlewares (autenticación, validación)
    ↓
Controller (recibe petición)
    ↓
Service (lógica de negocio)
    ↓
Repository (acceso a BD)
    ↓
Base de Datos (Supabase)
```

## 📋 Requisitos

- Node.js v18 o superior
- Redis (para rate limiting)
- Cuenta en Supabase

## 🚀 Instalación Rápida

1. **Clonar o copiar el proyecto**

2. **Instalar dependencias:**
```bash
npm install
```

3. **Configurar variables de entorno:**

Edita el archivo `.env` con tus credenciales:
```env
PROJECT_URL=https://tu-proyecto.supabase.co
API_KEY=tu_api_key_de_supabase
PORT=3000
NODE_ENV=development
```

4. **Crear tabla en Supabase:**

Ve a tu proyecto Supabase → SQL Editor → Ejecuta `setup_database.sql`

5. **Iniciar Redis:**
```bash
# Opción 1: Redis local
redis-server

# Opción 2: Docker
docker run -d -p 6379:6379 redis
```

6. **Iniciar servidor:**
```bash
npm start

# O en modo desarrollo (auto-reload):
npm run dev
```

## 📡 API Endpoints

### Públicos

#### `POST /api/register`
Registra un nuevo cliente y genera una API Key.

```bash
curl -X POST http://localhost:3000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Mi App",
    "email": "app@example.com"
  }'
```

### Protegidos (requieren header `X-API-Key`)

#### `GET /api/protected/data`
Obtiene datos protegidos.

```bash
curl -X GET http://localhost:3000/api/protected/data \
  -H "X-API-Key: tu-api-key-aqui"
```

#### `GET /api/protected/me`
Obtiene información del cliente autenticado.

```bash
curl -X GET http://localhost:3000/api/protected/me \
  -H "X-API-Key: tu-api-key-aqui"
```

### Administrativos

#### `GET /api/admin/keys`
Lista todas las API Keys.

#### `PUT /api/admin/keys/:apiKey/activate`
Activa una API Key.

#### `PUT /api/admin/keys/:apiKey/deactivate`
Desactiva una API Key.

## 🏫 Guía para Estudiantes

### Para empezar tu proyecto:

1. **Define tus modelos** en `src/models/`
   - Ejemplo: `Usuario.mjs`, `Producto.mjs`, `Pedido.mjs`

2. **Crea tus repositorios** en `src/repositories/`
   - Ejemplo: `usuarioRepository.mjs`, `productoRepository.mjs`

3. **Implementa servicios** en `src/services/`
   - Aquí va tu lógica de negocio

4. **Crea controladores** en `src/controllers/`
   - Manejan las peticiones HTTP

5. **Define rutas** en `src/routes/`
   - Conecta URLs con controladores

### Ejemplo completo de un nuevo recurso:

#### 1. Crear tabla en Supabase:
```sql
CREATE TABLE productos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  stock INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### 2. Modelo (`src/models/Producto.mjs`):
```javascript
export class Producto {
  constructor(data) {
    this.id = data.id;
    this.nombre = data.nombre;
    this.precio = data.precio;
    this.stock = data.stock;
    this.created_at = data.created_at;
  }

  toJSON() {
    return {
      id: this.id,
      nombre: this.nombre,
      precio: this.precio,
      stock: this.stock,
      created_at: this.created_at
    };
  }
}
```

#### 3. Repositorio (`src/repositories/productoRepository.mjs`):
```javascript
import { supabase } from '../config/database.mjs';
import { Producto } from '../models/Producto.mjs';

export class ProductoRepository {
  async crear(data) {
    const { data: producto, error } = await supabase
      .from('productos')
      .insert([data])
      .select()
      .single();

    if (error) throw error;
    return new Producto(producto);
  }

  async buscarTodos() {
    const { data, error } = await supabase
      .from('productos')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data.map(p => new Producto(p));
  }
}
```

#### 4. Servicio (`src/services/productoService.mjs`):
```javascript
import { ProductoRepository } from '../repositories/productoRepository.mjs';

export class ProductoService {
  constructor() {
    this.repository = new ProductoRepository();
  }

  async crearProducto(nombre, precio, stock) {
    if (precio < 0) {
      throw new Error('El precio no puede ser negativo');
    }

    return await this.repository.crear({
      nombre,
      precio,
      stock
    });
  }

  async listarProductos() {
    return await this.repository.buscarTodos();
  }
}
```

#### 5. Controlador (`src/controllers/productoController.mjs`):
```javascript
import { ProductoService } from '../services/productoService.mjs';

export class ProductoController {
  constructor() {
    this.service = new ProductoService();
  }

  crear = async (req, res) => {
    try {
      const { nombre, precio, stock } = req.body;
      const producto = await this.service.crearProducto(nombre, precio, stock);

      res.status(201).json({
        message: 'Producto creado',
        producto: producto.toJSON()
      });
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  };

  listar = async (req, res) => {
    try {
      const productos = await this.service.listarProductos();
      res.json({ productos: productos.map(p => p.toJSON()) });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  };
}
```

#### 6. Rutas (`src/routes/productoRoutes.mjs`):
```javascript
import express from 'express';
import { ProductoController } from '../controllers/productoController.mjs';
import { apiKeyMiddleware } from '../middlewares/apiKeyMiddleware.mjs';

const router = express.Router();
const controller = new ProductoController();

router.post('/', apiKeyMiddleware, controller.crear);
router.get('/', apiKeyMiddleware, controller.listar);

export default router;
```

#### 7. Registrar rutas (`src/routes/index.mjs`):
```javascript
import productoRoutes from './productoRoutes.mjs';

// Agregar después de las rutas existentes:
router.use('/productos', productoRoutes);
```

## 🧪 Pruebas

Ejecuta el script de pruebas:
```bash
./test.sh
```

O usa el cliente de ejemplo:
```bash
node client_example.mjs
```

## 📁 Estructura de Archivos

```
auth_supabase/
├── package.json               # Dependencias y scripts (start: node src/app.mjs)
├── .env                       # Variables de entorno
├── setup_database.sql         # Script de BD
├── README.md                  # Esta documentación
├── test.sh                    # Script de pruebas
├── client_example.mjs         # Cliente de ejemplo
│
└── src/
    ├── app.mjs               # Configuración de Express
    │
    ├── config/               # Configuraciones
    │   ├── database.mjs      # Supabase
    │   ├── redis.mjs         # Redis
    │   └── README.md
    │
    ├── models/               # Modelos de datos
    │   ├── ApiKey.mjs
    │   └── README.md
    │
    ├── repositories/         # Acceso a datos
    │   ├── apiKeyRepository.mjs
    │   └── README.md
    │
    ├── services/             # Lógica de negocio
    │   ├── apiKeyService.mjs
    │   └── README.md
    │
    ├── controllers/          # Controladores HTTP
    │   ├── apiKeyController.mjs
    │   └── README.md
    │
    ├── routes/               # Rutas/Endpoints
    │   ├── index.mjs
    │   ├── apiKeyRoutes.mjs
    │   └── README.md
    │
    ├── middlewares/          # Middlewares
    │   ├── apiKeyMiddleware.mjs
    │   └── README.md
    │
    └── utils/                # Utilidades
        ├── apiKey.mjs
        └── README.md
```

## 🔒 Seguridad

- ✅ API Keys UUID v4 criptográficamente seguras
- ✅ Validación en base de datos
- ✅ Rate limiting (10 req/min por API Key)
- ✅ Middleware de autenticación
- ✅ Variables de entorno para credenciales

## 🛠️ Tecnologías

- **Node.js** - Runtime de JavaScript
- **Express** - Framework web
- **Supabase** - Base de datos PostgreSQL
- **Redis** - Cache y rate limiting
- **dotenv** - Variables de entorno

## 📝 Mejores Prácticas Implementadas

1. **Separación de responsabilidades** (cada capa tiene un propósito)
2. **Inyección de dependencias** (servicios y repositorios)
3. **Manejo de errores** consistente
4. **Validación de datos** en múltiples capas
5. **Código reutilizable** (modelos, utils)
6. **Configuración centralizada**
7. **Middleware reutilizable**
8. **Respuestas HTTP estandarizadas**

## 💡 Tips para el Desarrollo

- Lee los README.md en cada carpeta de `src/`
- Cada README tiene ejemplos específicos
- Sigue el patrón establecido para consistencia
- No mezcles responsabilidades entre capas
- Usa async/await para operaciones asíncronas
- Maneja errores con try/catch
- Valida datos de entrada
- Documenta tu código

## 🤝 Contribuir (para estudiantes)

Cada grupo puede:
1. Fork este boilerplate
2. Crear sus propios modelos/servicios/controladores
3. Mantener la estructura de carpetas
4. Documentar sus cambios

## 📄 Licencia

ISC
