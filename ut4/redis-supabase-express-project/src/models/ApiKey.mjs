/**
 * Modelo de datos para API Key
 * Representa la estructura de una API Key en la base de datos
 */
export class ApiKey {
  constructor(data) {
    this.id = data.id;
    this.api_key = data.api_key;
    this.client_name = data.client_name;
    this.email = data.email;
    this.role = data.role || 'user';
    this.is_active = data.is_active ?? true;
    this.created_at = data.created_at;
    this.updated_at = data.updated_at;
  }

  /**
   * Convierte el modelo a un objeto plano para la respuesta
   */
  toJSON() {
    return {
      id: this.id,
      api_key: this.api_key,
      client_name: this.client_name,
      email: this.email,
      role: this.role,
      is_active: this.is_active,
      created_at: this.created_at,
      updated_at: this.updated_at
    };
  }

  /**
   * Convierte el modelo a un objeto seguro (sin datos sensibles)
   */
  toPublic() {
    return {
      client_name: this.client_name,
      role: this.role,
      is_active: this.is_active,
      created_at: this.created_at
    };
  }

  /**
   * Verifica si el usuario tiene rol de administrador
   */
  isAdmin() {
    return this.role === 'admin'
    };
}
