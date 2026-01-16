import express from 'express';
import apiKeyRoutes from './apiKeyRoutes.mjs';

const router = express.Router();

// Montar las rutas de API Keys
router.use('/', apiKeyRoutes);

// Ruta raíz con información de la API
router.get('/', (req, res) => {
  res.json({
    name: 'API con autenticación por API Key',
    version: '1.0.0',
    endpoints: {
      public: [
        'POST /api/register - Registrar y obtener nueva API Key'
      ],
      protected: [
        'GET /api/protected/data - Datos protegidos (requiere API Key)',
        'GET /api/protected/me - Info del cliente (requiere API Key)'
      ],
      admin: [
        'GET /api/admin/keys - Listar todas las API Keys',
        'PUT /api/admin/keys/:apiKey/deactivate - Desactivar API Key',
        'PUT /api/admin/keys/:apiKey/activate - Activar API Key'
      ]
    },
    usage: {
      header: 'X-API-Key',
      example: 'X-API-Key: tu-uuid-aqui'
    }
  });
});

export default router;
