import express from 'express';
import { ApiKeyController } from '../controllers/apiKeyController.mjs';
import { apiKeyMiddleware } from '../middlewares/apiKeyMiddleware.mjs';
import { adminMiddleware } from '../middlewares/adminMiddleware.mjs';

const router = express.Router();
const controller = new ApiKeyController();

// ============================================
// RUTAS PÚBLICAS
// ============================================

/**
 * POST /api/register
 * Registra un nuevo cliente y genera una API Key
 */
router.post('/register', controller.register);

// ============================================
// RUTAS PROTEGIDAS (requieren API Key)
// ============================================

/**
 * GET /api/protected/data
 * Obtiene datos protegidos de ejemplo
 */
router.get('/protected/data', apiKeyMiddleware, controller.getProtectedData);

/**
 * GET /api/protected/me
 * Obtiene información del cliente autenticado
 */
router.get('/protected/me', apiKeyMiddleware, controller.getMe);

// ============================================
// RUTAS ADMINISTRATIVAS (requieren rol admin)
// ============================================

/**
 * GET /api/admin/keys
 * Lista todas las API Keys registradas
 * Requiere: API Key válida con rol 'admin'
 */
router.get('/admin/keys', adminMiddleware, controller.getAllKeys);

/**
 * PUT /api/admin/keys/:apiKey/deactivate
 * Desactiva una API Key específica
 * Requiere: API Key válida con rol 'admin'
 */
router.put('/admin/keys/:apiKey/deactivate', adminMiddleware, controller.deactivateKey);

/**
 * PUT /api/admin/keys/:apiKey/activate
 * Activa una API Key específica
 * Requiere: API Key válida con rol 'admin'
 */
router.put('/admin/keys/:apiKey/activate', adminMiddleware, controller.activateKey);

export default router;
