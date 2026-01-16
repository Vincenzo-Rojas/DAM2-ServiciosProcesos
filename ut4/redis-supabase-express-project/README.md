# Sistema de Autenticación con API Keys usando Supabase

Este proyecto implementa un sistema de autenticación basado en API Keys (UUIDs) utilizando Supabase como base de datos y Redis para rate limiting.

## 📋 Requisitos

- Node.js (v16 o superior)
- Redis (para rate limiting)
- Cuenta en Supabase

## 🚀 Instalación

1. **Instalar dependencias:**
```bash
npm install
```

2. **Configurar variables de entorno:**

Edita el archivo `.env` con tus credenciales de Supabase:
```env
PROJECT_URL=https://tu-proyecto.supabase.co
API_KEY=tu_api_key_de_supabase
```

3. **Configurar la base de datos en Supabase:**

- Ve a tu proyecto en Supabase
- Abre el SQL Editor
- Ejecuta el script `setup_database.sql`

4. **Iniciar Redis:**
```bash
# En Linux/Mac
redis-server

# O usando Docker
docker run -d -p 6379:6379 redis
```

5. **Iniciar el servidor:**
```bash
npm start
```

## 📡 Endpoints

### Públicos

#### `POST /api/register`
Registra un nuevo cliente y genera una API Key única.

**Request:**
```bash
curl -X POST http://localhost:3000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Mi Aplicación",
    "email": "app@example.com"
  }'
```

**Response:**
```json
{
  "message": "API Key generada exitosamente",
  "api_key": "550e8400-e29b-41d4-a716-446655440000",
  "client_name": "Mi Aplicación",
  "email": "app@example.com",
  "info": "Usa esta API Key en el header X-API-Key para autenticar tus peticiones"
}
```

### Protegidos (requieren API Key)

#### `GET /api/protected/data`
Obtiene datos protegidos.

**Request:**
```bash
curl -X GET http://localhost:3000/api/protected/data \
  -H "X-API-Key: tu-api-key-aqui"
```

**Response:**
```json
{
  "message": "Acceso autorizado",
  "client": "Mi Aplicación",
  "data": {
    "ejemplo": "Estos son tus datos protegidos",
    "timestamp": "2026-01-15T10:30:00.000Z"
  }
}
```

#### `GET /api/protected/me`
Obtiene información del cliente autenticado.

**Request:**
```bash
curl -X GET http://localhost:3000/api/protected/me \
  -H "X-API-Key: tu-api-key-aqui"
```

### Administrativos

#### `GET /api/admin/keys`
Lista todas las API Keys registradas.

```bash
curl http://localhost:3000/api/admin/keys
```

#### `PUT /api/admin/keys/:apiKey/deactivate`
Desactiva una API Key específica.

```bash
curl -X PUT http://localhost:3000/api/admin/keys/550e8400-e29b-41d4-a716-446655440000/deactivate
```

## 🔒 Características de Seguridad

### 1. **API Keys únicas (UUID v4)**
- Cada cliente recibe un UUID único e irrepetible
- Generación criptográficamente segura

### 2. **Validación en base de datos**
- Todas las API Keys se validan contra Supabase
- Solo las keys activas (`is_active: true`) son aceptadas

### 3. **Rate Limiting con Redis**
- Límite de 10 peticiones por minuto por API Key
- Ventana deslizante de 60 segundos
- Respuesta HTTP 429 cuando se excede el límite

### 4. **Gestión de estados**
- Las API Keys pueden desactivarse sin eliminarlas
- Mantiene historial de todas las keys generadas

## 🗄️ Estructura de la Base de Datos

La tabla `api_keys` tiene la siguiente estructura:

```sql
CREATE TABLE api_keys (
  id SERIAL PRIMARY KEY,
  api_key UUID UNIQUE NOT NULL,
  client_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 📁 Estructura del Proyecto

```
auth_supabase/
├── app.mjs                    # Servidor Express principal
├── auth.mjs                   # Generación de API Keys (UUID)
├── apiKeyMiddleware.mjs       # Middleware de autenticación
├── supabaseClient.mjs         # Cliente de Supabase
├── redisClient.mjs            # Cliente de Redis
├── setup_database.sql         # Script SQL para crear la tabla
├── .env                       # Variables de entorno
├── package.json               # Dependencias del proyecto
└── README.md                  # Esta documentación
```

## 🧪 Pruebas

### Probar el registro de un cliente:
```bash
curl -X POST http://localhost:3000/api/register \
  -H "Content-Type: application/json" \
  -d '{"client_name":"Test App","email":"test@test.com"}'
```

### Probar acceso con API Key:
```bash
# Reemplaza YOUR_API_KEY con la key obtenida
curl -X GET http://localhost:3000/api/protected/data \
  -H "X-API-Key: YOUR_API_KEY"
```

### Probar rate limiting:
```bash
# Ejecuta este comando más de 10 veces en menos de 1 minuto
for i in {1..15}; do
  curl -X GET http://localhost:3000/api/protected/data \
    -H "X-API-Key: YOUR_API_KEY"
  echo "\nRequest $i"
done
```

## ⚙️ Configuración Avanzada

### Cambiar el límite de peticiones:

Edita [apiKeyMiddleware.mjs](apiKeyMiddleware.mjs#L24-L26):
```javascript
if (count > 10) {  // Cambia este número
  return res.status(429).json({ error: 'Rate limit exceeded' })
}
```

### Cambiar la ventana de tiempo:

Edita [apiKeyMiddleware.mjs](apiKeyMiddleware.mjs#L20-L21):
```javascript
const window = Math.floor(Date.now() / 60000)  // 60000 = 1 minuto
const redisKey = `rate:${apiKey}:${window}`
```

## 🛠️ Solución de Problemas

### Redis no conecta:
```bash
# Verifica que Redis esté corriendo
redis-cli ping
# Debería responder: PONG
```

### Error de Supabase:
- Verifica que las credenciales en `.env` sean correctas
- Asegúrate de haber ejecutado `setup_database.sql`
- Verifica los permisos RLS en Supabase (desactívalos para desarrollo)

## 📝 Notas

- En producción, considera agregar HTTPS
- Implementa autenticación adicional para endpoints admin
- Considera agregar logging más robusto
- Evalúa agregar métricas de uso por cliente

## 📄 Licencia

ISC
