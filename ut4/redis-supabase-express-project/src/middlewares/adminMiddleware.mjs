import { apiKeyMiddleware } from './apiKeyMiddleware.mjs';

/**
 * Middleware para verificar que el usuario tiene rol de administrador
 * Debe usarse después de apiKeyMiddleware
 */
export const adminMiddleware = async (req, res, next) => {
  // Primero validar que tiene API Key válida
  await new Promise((resolve, reject) => {
    apiKeyMiddleware(req, res, (err) => {
      if (err) reject(err);
      else resolve();
    });
  }).catch(() => {
    // Si apiKeyMiddleware ya envió respuesta, salir
    return;
  });

  // Si ya se envió respuesta (no autorizado o API key inválida), salir
  if (res.headersSent) {
    return;
  }

  // Verificar que el usuario tenga rol de admin
  if (!req.client || req.client.role !== 'admin') {
    return res.status(403).json({ 
      error: 'Acceso denegado',
      message: 'Se requiere rol de administrador para acceder a este recurso'
    });
  }

  next();
};
