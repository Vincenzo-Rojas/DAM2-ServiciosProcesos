# Middlewares

Esta carpeta contiene los middlewares de Express.

## ¿Qué va aquí?

Los middlewares son funciones que se ejecutan antes de llegar a los controladores.

## Ejemplo de uso:

```javascript
// middlewares/authMiddleware.mjs
import jwt from 'jsonwebtoken';

export const authMiddleware = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({ error: 'No autorizado' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;

    next();
  } catch (error) {
    res.status(401).json({ error: 'Token inválido' });
  }
};
```

```javascript
// middlewares/validarCampos.mjs
import { validationResult } from 'express-validator';

export const validarCampos = (req, res, next) => {
  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    return res.status(400).json({
      errors: errors.array()
    });
  }

  next();
};
```

```javascript
// middlewares/logger.mjs
export const logger = (req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(
      `[${new Date().toISOString()}] ${req.method} ${req.path} - ${res.statusCode} (${duration}ms)`
    );
  });

  next();
};
```

```javascript
// middlewares/errorHandler.mjs
export const errorHandler = (err, req, res, next) => {
  console.error('Error:', err);

  // Error de validación
  if (err.name === 'ValidationError') {
    return res.status(400).json({
      error: 'Error de validación',
      details: err.message
    });
  }

  // Error 404
  if (err.status === 404) {
    return res.status(404).json({
      error: 'Recurso no encontrado'
    });
  }

  // Error genérico
  res.status(500).json({
    error: 'Error interno del servidor',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
};
```

## Tipos comunes de middlewares:

- **Autenticación**: Verificar tokens, sesiones, API keys
- **Autorización**: Verificar permisos y roles
- **Validación**: Validar datos de entrada
- **Logging**: Registrar peticiones
- **Rate Limiting**: Limitar peticiones
- **CORS**: Configurar acceso entre dominios
- **Error Handling**: Manejar errores globalmente
