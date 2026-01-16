import { ApiKeyService } from '../services/apiKeyService.mjs';

/**
 * Controlador para manejar las peticiones relacionadas con API Keys
 */
export class ApiKeyController {
  constructor() {
    this.service = new ApiKeyService();
  }

  /**
   * POST /api/register
   * Registra un nuevo cliente y genera una API Key
   */
  register = async (req, res) => {
    try {
      const { client_name, email, role } = req.body;

      // Solo permitir crear admins si el que lo solicita es admin
      if (role === 'admin') {
        if (!req.client || req.client.role !== 'admin') {
          return res.status(403).json({
            error: 'Solo un administrador puede crear otros administradores'
          });
        }
      }

      const apiKey = await this.service.registerClient(client_name, email, role);

      res.status(201).json({
        message: 'API Key generada exitosamente',
        api_key: apiKey.api_key,
        client_name: apiKey.client_name,
        email: apiKey.email,
        role: apiKey.role,
        info: 'Usa esta API Key en el header X-API-Key para autenticar tus peticiones'
      });
    } catch (error) {
      console.error('Error en register:', error);
      res.status(400).json({ 
        error: error.message || 'Error al crear API Key'
      });
    }
  };

  /**
   * GET /api/admin/keys
   * Lista todas las API Keys registradas
   */
  getAllKeys = async (req, res) => {
    try {
      const keys = await this.service.getAllKeys();

      res.json({
        total: keys.length,
        keys: keys.map(k => k.toJSON())
      });
    } catch (error) {
      console.error('Error en getAllKeys:', error);
      res.status(500).json({ error: 'Error al obtener las API Keys' });
    }
  };

  /**
   * PUT /api/admin/keys/:apiKey/deactivate
   * Desactiva una API Key
   */
  deactivateKey = async (req, res) => {
    try {
      const { apiKey } = req.params;

      const updatedKey = await this.service.deactivateKey(apiKey);

      res.json({
        message: 'API Key desactivada exitosamente',
        key: updatedKey.toJSON()
      });
    } catch (error) {
      console.error('Error en deactivateKey:', error);
      const status = error.message === 'API Key no encontrada' ? 404 : 500;
      res.status(status).json({ error: error.message });
    }
  };

  /**
   * PUT /api/admin/keys/:apiKey/activate
   * Activa una API Key
   */
  activateKey = async (req, res) => {
    try {
      const { apiKey } = req.params;

      const updatedKey = await this.service.activateKey(apiKey);

      res.json({
        message: 'API Key activada exitosamente',
        key: updatedKey.toJSON()
      });
    } catch (error) {
      console.error('Error en activateKey:', error);
      const status = error.message === 'API Key no encontrada' ? 404 : 500;
      res.status(status).json({ error: error.message });
    }
  };

  /**
   * GET /api/protected/me
   * Obtiene información del cliente autenticado
   */
  getMe = async (req, res) => {
    try {
      // El middleware ya validó y agregó req.client
      const client = req.client;

      res.json({
        client_name: client.client_name,
        email: client.email,
        role: client.role,
        api_key: client.api_key,
        created_at: client.created_at,
        is_active: client.is_active
      });
    } catch (error) {
      console.error('Error en getMe:', error);
      res.status(500).json({ error: 'Error al obtener información' });
    }
  };

  /**
   * GET /api/protected/data
   * Endpoint de ejemplo para datos protegidos
   */
  getProtectedData = async (req, res) => {
    try {
      res.json({
        message: 'Acceso autorizado',
        client: req.client.client_name,
        data: {
          ejemplo: 'Estos son tus datos protegidos',
          timestamp: new Date().toISOString()
        }
      });
    } catch (error) {
      console.error('Error en getProtectedData:', error);
      res.status(500).json({ error: 'Error al obtener datos' });
    }
  };
}
