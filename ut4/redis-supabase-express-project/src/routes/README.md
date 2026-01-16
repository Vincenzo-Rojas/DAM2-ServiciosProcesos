# Rutas (Routes)

Esta carpeta contiene las definiciones de rutas y endpoints de la API.

## ¿Qué va aquí?

Las rutas conectan los endpoints HTTP con los controladores.

## Ejemplo de uso:

```javascript
// routes/usuarioRoutes.mjs
import express from 'express';
import { UsuarioController } from '../controllers/usuarioController.mjs';
import { authMiddleware } from '../middlewares/authMiddleware.mjs';

const router = express.Router();
const controller = new UsuarioController();

// Rutas públicas
router.post('/register', controller.crear);
router.post('/login', controller.login);

// Rutas protegidas
router.get('/', authMiddleware, controller.listar);
router.get('/:id', authMiddleware, controller.obtener);
router.put('/:id', authMiddleware, controller.actualizar);
router.delete('/:id', authMiddleware, controller.eliminar);

export default router;
```

```javascript
// routes/index.mjs
import express from 'express';
import usuarioRoutes from './usuarioRoutes.mjs';
import productoRoutes from './productoRoutes.mjs';

const router = express.Router();

// Montar rutas
router.use('/usuarios', usuarioRoutes);
router.use('/productos', productoRoutes);

// Ruta de bienvenida
router.get('/', (req, res) => {
  res.json({
    message: 'Bienvenido a la API',
    version: '1.0.0'
  });
});

export default router;
```

## Mejores prácticas:

- ✅ Agrupar rutas relacionadas en un archivo
- ✅ Usar nombres descriptivos
- ✅ Aplicar middlewares específicos por ruta
- ✅ Documentar cada endpoint con comentarios
- ✅ Seguir convenciones REST:
  - `GET /recursos` - Listar
  - `GET /recursos/:id` - Obtener uno
  - `POST /recursos` - Crear
  - `PUT /recursos/:id` - Actualizar
  - `DELETE /recursos/:id` - Eliminar
