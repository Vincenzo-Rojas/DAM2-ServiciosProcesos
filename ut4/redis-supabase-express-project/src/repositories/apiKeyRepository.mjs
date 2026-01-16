import { supabase } from '../config/database.mjs';
import { ApiKey } from '../models/ApiKey.mjs';

/**
 * Repositorio para manejar operaciones de base de datos de API Keys
 */
export class ApiKeyRepository {
  /**
   * Crea una nueva API Key en la base de datos
   */
  async create(apiKeyData) {
    const { data, error } = await supabase
      .from('api_keys')
      .insert([apiKeyData])
      .select()
      .single();

    if (error) throw error;
    return new ApiKey(data);
  }

  /**
   * Busca una API Key por su valor
   */
  async findByKey(apiKey) {
    const { data, error } = await supabase
      .from('api_keys')
      .select('*')
      .eq('api_key', apiKey)
      .single();

    if (error) return null;
    return data ? new ApiKey(data) : null;
  }

  /**
   * Busca una API Key activa por su valor
   */
  async findActiveByKey(apiKey) {
    const { data, error } = await supabase
      .from('api_keys')
      .select('*')
      .eq('api_key', apiKey)
      .eq('is_active', true)
      .single();

    if (error) return null;
    return data ? new ApiKey(data) : null;
  }

  /**
   * Obtiene todas las API Keys
   */
  async findAll() {
    const { data, error } = await supabase
      .from('api_keys')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data.map(item => new ApiKey(item));
  }

  /**
   * Actualiza el estado de una API Key
   */
  async updateStatus(apiKey, isActive) {
    const { data, error } = await supabase
      .from('api_keys')
      .update({ is_active: isActive })
      .eq('api_key', apiKey)
      .select()
      .single();

    if (error) throw error;
    return data ? new ApiKey(data) : null;
  }

  /**
   * Elimina una API Key (soft delete - la desactiva)
   */
  async delete(apiKey) {
    return this.updateStatus(apiKey, false);
  }

  /**
   * Busca API Keys por email
   */
  async findByEmail(email) {
    const { data, error } = await supabase
      .from('api_keys')
      .select('*')
      .eq('email', email)
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data.map(item => new ApiKey(item));
  }
}
