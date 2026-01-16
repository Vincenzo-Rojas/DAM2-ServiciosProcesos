# 🎓 GUÍA RÁPIDA PARA ESTUDIANTES

## ¿Qué es este proyecto?

Es un **boilerplate** (plantilla base) para crear APIs REST con Node.js siguiendo las mejores prácticas de arquitectura en capas.

## ✅ ¿Está listo para usar?

**SÍ**, solo necesitas:
1. Configurar tu `.env` con credenciales de Supabase
2. Ejecutar el script SQL en Supabase
3. Iniciar Redis
4. `npm start`

## 🎯 ¿Qué puedo hacer con esto?

Puedes crear cualquier tipo de API:
- 🛒 E-commerce
- 📝 Blog/CMS
- 👥 Red social
- 📊 Sistema de gestión
- 🎮 Backend de juego
- 💬 Chat/Mensajería
- Y mucho más...

## 📚 Pasos para tu proyecto

### 1️⃣ Diseña tu base de datos

Piensa qué tablas necesitas. Ejemplo para un e-commerce:

```sql
-- productos
CREATE TABLE productos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255),
  precio DECIMAL(10,2),
  stock INTEGER,
  categoria VARCHAR(100)
);

-- pedidos
CREATE TABLE pedidos (
  id SERIAL PRIMARY KEY,
  cliente_id INTEGER,
  total DECIMAL(10,2),
  estado VARCHAR(50),
  fecha TIMESTAMP DEFAULT NOW()
);
```

### 2️⃣ Crea tus modelos

En `src/models/` crea archivos para cada entidad:

```javascript
// src/models/Producto.mjs
export class Producto {
  constructor(data) {
    this.id = data.id;
    this.nombre = data.nombre;
    this.precio = data.precio;
    this.stock = data.stock;
  }
}
```

### 3️⃣ Crea repositorios

En `src/repositories/` para acceder a la base de datos:

```javascript
// src/repositories/productoRepository.mjs
import { supabase } from '../config/database.mjs';

export class ProductoRepository {
  async buscarTodos() {
    const { data } = await supabase
      .from('productos')
      .select('*');
    return data;
  }
}
```

### 4️⃣ Crea servicios

En `src/services/` para la lógica de negocio:

```javascript
// src/services/productoService.mjs
export class ProductoService {
  async listarProductos() {
    return await this.repository.buscarTodos();
  }

  async calcularDescuento(producto, porcentaje) {
    // Lógica de negocio aquí
  }
}
```

### 5️⃣ Crea controladores

En `src/controllers/` para manejar HTTP:

```javascript
// src/controllers/productoController.mjs
export class ProductoController {
  listar = async (req, res) => {
    const productos = await this.service.listarProductos();
    res.json({ productos });
  };
}
```

### 6️⃣ Define rutas

En `src/routes/`:

```javascript
// src/routes/productoRoutes.mjs
import express from 'express';
const router = express.Router();

router.get('/', controller.listar);
router.post('/', controller.crear);

export default router;
```

### 7️⃣ Registra en index

En `src/routes/index.mjs`:

```javascript
import productoRoutes from './productoRoutes.mjs';
router.use('/productos', productoRoutes);
```

## 🔍 Estructura Simplificada

```
TU PROYECTO
│
├── index.mjs                    ← Punto de entrada
├── package.json                 ← Dependencias
├── .env                         ← Tus credenciales
│
└── src/
    ├── models/                  ← Tus entidades
    │   └── Producto.mjs
    │
    ├── repositories/            ← Acceso a BD
    │   └── productoRepository.mjs
    │
    ├── services/                ← Lógica de negocio
    │   └── productoService.mjs
    │
    ├── controllers/             ← Manejo de HTTP
    │   └── productoController.mjs
    │
    └── routes/                  ← URLs de tu API
        └── productoRoutes.mjs
```

## 🚦 Reglas de Oro

### ✅ HAZ:
- Sigue la estructura de carpetas
- Usa async/await
- Maneja errores con try/catch
- Valida los datos de entrada
- Lee los README.md de cada carpeta

### ❌ NO HAGAS:
- Poner lógica de BD en controladores
- Poner lógica HTTP en servicios
- Mezclar responsabilidades
- Hardcodear credenciales
- Ignorar los errores

## 💡 Ejemplos Prácticos

### Crear un nuevo endpoint:

**Quieres:** `GET /api/productos/destacados`

**Pasos:**
1. Service: `obtenerDestacados()` → lógica para filtrar
2. Controller: `getDestacados()` → llamar al service
3. Route: `router.get('/destacados', controller.getDestacados)`

### Proteger un endpoint:

Simplemente añade el middleware:

```javascript
router.post('/productos', apiKeyMiddleware, controller.crear);
//                       ↑ Requiere API Key
```

### Validar datos:

En el servicio:

```javascript
async crearProducto(data) {
  if (!data.nombre) {
    throw new Error('Nombre requerido');
  }
  if (data.precio < 0) {
    throw new Error('Precio inválido');
  }
  // ... crear producto
}
```

## 🆘 Ayuda Rápida

### ¿Dónde pongo...?

- **Consulta a BD** → Repository
- **Validación de negocio** → Service  
- **Manejo de HTTP** → Controller
- **Definir URL** → Routes
- **Entidad de datos** → Model
- **Función auxiliar** → Utils
- **Autenticación** → Middleware
- **Configuración** → Config

### ¿Cómo...?

**Agregar una nueva tabla:**
1. Crear SQL en Supabase
2. Crear modelo en `src/models/`
3. Crear repository en `src/repositories/`
4. Seguir el patrón ↑

**Proteger todos mis endpoints:**
```javascript
// En src/routes/tuRuta.mjs
import { apiKeyMiddleware } from '../middlewares/apiKeyMiddleware.mjs';

// Aplicar a todas las rutas
router.use(apiKeyMiddleware);

router.get('/ruta1', ...);
router.post('/ruta2', ...);
```

**Hacer una relación entre tablas:**
```javascript
// En el repository
async obtenerProductoConCategoria(id) {
  const { data } = await supabase
    .from('productos')
    .select(`
      *,
      categorias (
        id,
        nombre
      )
    `)
    .eq('id', id)
    .single();
  
  return data;
}
```

## 📖 Recursos

- **Supabase Docs**: https://supabase.com/docs
- **Express Docs**: https://expressjs.com/
- **README de cada carpeta**: Ejemplos específicos

## 🎯 Checklist Antes de Empezar

- [ ] Tengo Node.js instalado
- [ ] Tengo una cuenta en Supabase
- [ ] He ejecutado `npm install`
- [ ] He configurado mi `.env`
- [ ] He ejecutado el script SQL
- [ ] Redis está corriendo
- [ ] El servidor inicia con `npm start`
- [ ] He probado el endpoint de ejemplo

## 💪 ¡Éxito!

Ahora tienes una base sólida para construir cualquier API. Empieza pequeño, prueba cada parte, y ve construyendo paso a paso.

**¿Dudas?** Lee los README.md en cada carpeta de `src/` - tienen ejemplos detallados.
