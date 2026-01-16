import { supabase } from '../config/database.mjs';
import redis from '../config/redis.mjs';

/**
 * Middleware para validar API Keys y aplicar rate limiting
 */
export const apiKeyMiddleware = async (req, res, next) => {
  const apiKey = req.header('X-API-Key');
  
  if (!apiKey) {
    return res.status(401).json({ error: 'Falta API Key' });
  }

  // Comprobar que la API key existe y está activa en Supabase
  const { data: key, error } = await supabase
    .from('api_keys')
    .select('*')
    .eq('api_key', apiKey)
    .eq('is_active', true)
    .single();

  if (error || !key) {
    return res.status(403).json({ error: 'API Key Inválida' });
  }

  // Rate limiting con Redis (ventana de 1 minuto)
  const window = Math.floor(Date.now() / 60000);
  const redisKey = `rate:${apiKey}:${window}`;

  try {
    const count = await redis.incr(redisKey);
    if (count === 1) {
      await redis.expire(redisKey, 60);
    }

    if (count > 10) {
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }
  } catch (redisError) {
    console.error('Redis error:', redisError);
    // Continuar sin rate limiting si Redis falla
  }

  // Adjuntar información del cliente a la request
  req.client = key;
  next();
};
