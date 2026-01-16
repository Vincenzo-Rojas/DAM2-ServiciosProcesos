import { ApiKeyRepository } from '../repositories/apiKeyRepository.mjs';
import { generateApiKey } from '../utils/apiKey.mjs';

/**
 * Servicio que contiene la lógica de negocio para API Keys
 */
export class ApiKeyService {
  constructor() {
    this.repository = new ApiKeyRepository();
  }

  /**
   * Registra un nuevo cliente y genera su API Key
   */
  async registerClient(clientName, email, role = 'user') {
    if (!clientName || !email) {
      throw new Error('Se requiere client_name y email');
    }

    // Validar formato de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      throw new Error('Formato de email inválido');
    }

    // Validar rol
    if (role && !['user', 'admin'].includes(role)) {
      throw new Error('Rol inválido. Debe ser "user" o "admin"');
    }

    // Generar API Key única
    const apiKey = generateApiKey();

    // Crear registro en la base de datos
    const apiKeyData = {
      api_key: apiKey,
      client_name: clientName,
      email: email,
      role: role || 'user',
      is_active: true,
      created_at: new Date().toISOString()
    };

    const newApiKey = await this.repository.create(apiKeyData);
    return newApiKey;
  }

  /**
   * Obtiene todas las API Keys registradas
   */
  async getAllKeys() {
    return await this.repository.findAll();
  }

  /**
   * Valida una API Key
   */
  async validateKey(apiKey) {
    return await this.repository.findActiveByKey(apiKey);
  }

  /**
   * Desactiva una API Key
   */
  async deactivateKey(apiKey) {
    const key = await this.repository.findByKey(apiKey);
    if (!key) {
      throw new Error('API Key no encontrada');
    }

    return await this.repository.updateStatus(apiKey, false);
  }

  /**
   * Activa una API Key
   */
  async activateKey(apiKey) {
    const key = await this.repository.findByKey(apiKey);
    if (!key) {
      throw new Error('API Key no encontrada');
    }

    return await this.repository.updateStatus(apiKey, true);
  }

  /**
   * Obtiene las API Keys de un cliente por email
   */
  async getKeysByEmail(email) {
    return await this.repository.findByEmail(email);
  }
}
