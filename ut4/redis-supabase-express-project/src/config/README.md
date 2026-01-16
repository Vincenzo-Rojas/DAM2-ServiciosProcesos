# Configuración (Config)

Esta carpeta contiene archivos de configuración de la aplicación.

## ¿Qué va aquí?

Configuraciones de bases de datos, servicios externos, y constantes.

## Ejemplo de uso:

```javascript
// config/database.mjs
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();

export const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);
```

```javascript
// config/redis.mjs
import { createClient } from 'redis';

const redis = await createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
}).connect();

export default redis;
```

```javascript
// config/constants.mjs
export const CONSTANTS = {
  JWT_EXPIRATION: '7d',
  MAX_FILE_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_ORIGINS: [
    'http://localhost:3000',
    'https://mi-app.com'
  ],
  PAGINATION: {
    DEFAULT_PAGE: 1,
    DEFAULT_LIMIT: 10,
    MAX_LIMIT: 100
  }
};
```

```javascript
// config/email.mjs
import nodemailer from 'nodemailer';

export const emailTransporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: process.env.SMTP_PORT,
  secure: true,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASSWORD
  }
});
```

## Mejores prácticas:

- ✅ Usar variables de entorno para datos sensibles
- ✅ Agrupar configuraciones relacionadas
- ✅ Exportar instancias configuradas listas para usar
- ❌ **NO** hardcodear credenciales
- ❌ **NO** commitear archivos .env al repositorio
