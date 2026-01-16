# 🏗️ Arquitectura del Boilerplate

## Diagrama de Arquitectura en Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE HTTP                             │
│                    (curl, Postman, Browser)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CAPA DE RUTAS                             │
│                      (src/routes/*.mjs)                          │
│                                                                   │
│  • Define endpoints (URLs)                                       │
│  • Mapea URLs a controladores                                   │
│  • Aplica middlewares específicos                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CAPA DE MIDDLEWARES                          │
│                   (src/middlewares/*.mjs)                        │
│                                                                   │
│  • Autenticación (API Keys)                                     │
│  • Rate Limiting (Redis)                                        │
│  • Validación de entrada                                        │
│  • Logging                                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE CONTROLADORES                         │
│                   (src/controllers/*.mjs)                        │
│                                                                   │
│  • Recibe peticiones HTTP                                       │
│  • Valida datos básicos                                         │
│  • Llama a servicios                                            │
│  • Formatea respuestas HTTP                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CAPA DE SERVICIOS                            │
│                    (src/services/*.mjs)                          │
│                                                                   │
│  • Lógica de negocio                                            │
│  • Validaciones complejas                                       │
│  • Orquestación de repositorios                                │
│  • Transacciones                                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CAPA DE REPOSITORIOS                           │
│                  (src/repositories/*.mjs)                        │
│                                                                   │
│  • Operaciones CRUD                                             │
│  • Consultas a base de datos                                    │
│  • Conversión a modelos                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA DE MODELOS                             │
│                     (src/models/*.mjs)                           │
│                                                                   │
│  • Definición de entidades                                      │
│  • Validaciones básicas                                         │
│  • Transformaciones (toJSON)                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS (Supabase)                      │
│                                                                   │
│  • PostgreSQL                                                    │
│  • Almacenamiento persistente                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de una Petición HTTP

```
1. Cliente hace petición
   POST /api/register
   
   ↓

2. Express Router
   src/routes/apiKeyRoutes.mjs
   router.post('/register', controller.register)
   
   ↓

3. Controller recibe
   src/controllers/apiKeyController.mjs
   register = async (req, res) => {
     const { client_name, email } = req.body;
     const apiKey = await this.service.registerClient(...)
   
   ↓

4. Service ejecuta lógica
   src/services/apiKeyService.mjs
   async registerClient(clientName, email) {
     // Validaciones de negocio
     if (!emailRegex.test(email)) throw Error(...)
     // Genera API Key
     const apiKey = generateApiKey()
     // Llama al repository
     return await this.repository.create(...)
   
   ↓

5. Repository accede a BD
   src/repositories/apiKeyRepository.mjs
   async create(apiKeyData) {
     const { data, error } = await supabase
       .from('api_keys')
       .insert([apiKeyData])
   
   ↓

6. Supabase (PostgreSQL)
   INSERT INTO api_keys ...
   
   ↓

7. Respuesta regresa
   Repository → Service → Controller → Cliente
```

## Separación de Responsabilidades

### ❌ MAL - Todo en un archivo

```javascript
// app.js (antipatrón - no hagas esto)
app.post('/api/register', async (req, res) => {
  const { client_name, email } = req.body;
  
  // Validación
  if (!email.includes('@')) {
    return res.status(400).json({ error: 'Email inválido' });
  }
  
  // Generar UUID
  const apiKey = randomUUID();
  
  // Guardar en BD
  const { data, error } = await supabase
    .from('api_keys')
    .insert([{ api_key: apiKey, client_name, email }]);
  
  // Enviar email (servicio externo)
  await sendEmail(email, 'Bienvenido', '...');
  
  res.json({ api_key: apiKey });
});
```

### ✅ BIEN - Separado en capas

```javascript
// src/routes/apiKeyRoutes.mjs
router.post('/register', controller.register);

// src/controllers/apiKeyController.mjs
register = async (req, res) => {
  try {
    const { client_name, email } = req.body;
    const apiKey = await this.service.registerClient(client_name, email);
    res.status(201).json({ api_key: apiKey });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

// src/services/apiKeyService.mjs
async registerClient(clientName, email) {
  if (!emailRegex.test(email)) {
    throw new Error('Email inválido');
  }
  
  const apiKey = generateApiKey();
  const newKey = await this.repository.create({ apiKey, clientName, email });
  
  await this.emailService.sendWelcome(email, clientName);
  
  return newKey;
}

// src/repositories/apiKeyRepository.mjs
async create(apiKeyData) {
  const { data, error } = await supabase
    .from('api_keys')
    .insert([apiKeyData])
    .select()
    .single();
  
  if (error) throw error;
  return new ApiKey(data);
}
```

## Componentes Auxiliares

```
┌─────────────────────────────────────────────────────────────────┐
│                     COMPONENTES AUXILIARES                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   src/config/    │  │    src/utils/    │  │ src/middlewares/ │
│                  │  │                  │  │                  │
│  • database.mjs  │  │  • validators    │  │  • auth          │
│  • redis.mjs     │  │  • formatters    │  │  • validation    │
│  • constants.mjs │  │  • encryption    │  │  • rate-limiting │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

## Ventajas de esta Arquitectura

### 🎯 Separación de Responsabilidades
- Cada capa tiene una única responsabilidad
- Fácil de entender y mantener
- Cambios aislados (cambiar BD no afecta controllers)

### 🔄 Reutilización
- Servicios reutilizables en diferentes controllers
- Repositorios reutilizables en diferentes services
- Middlewares aplicables a múltiples rutas

### 🧪 Testeable
- Cada capa se puede testear independientemente
- Fácil crear mocks de repositories o services

### 📈 Escalable
- Fácil agregar nuevas funcionalidades
- Patrón claro para todos los desarrolladores
- Crecimiento organizado

### 🔧 Mantenible
- Bugs fáciles de localizar
- Cambios predecibles
- Código autodocumentado por estructura

## Ejemplo Completo: Agregar "Productos"

```
1. Crear tabla en Supabase:
   CREATE TABLE productos (...)

2. Crear modelo:
   src/models/Producto.mjs

3. Crear repository:
   src/repositories/productoRepository.mjs

4. Crear service:
   src/services/productoService.mjs

5. Crear controller:
   src/controllers/productoController.mjs

6. Crear routes:
   src/routes/productoRoutes.mjs

7. Registrar en index:
   src/routes/index.mjs
   router.use('/productos', productoRoutes)

8. ¡Listo! Tu API de productos funciona
```

## Patrones de Diseño Implementados

- **Repository Pattern**: Abstrae acceso a datos
- **Service Layer**: Encapsula lógica de negocio
- **MVC Pattern**: Model-View-Controller (sin View, es API)
- **Dependency Injection**: Services inyectan repositories
- **Middleware Pattern**: Chain of responsibility

## Conclusión

Esta arquitectura te permite:
- ✅ Desarrollar rápido y ordenado
- ✅ Trabajar en equipo sin conflictos
- ✅ Escalar tu aplicación fácilmente
- ✅ Mantener código limpio y profesional
