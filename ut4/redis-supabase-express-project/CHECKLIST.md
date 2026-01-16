# 📋 Checklist de Verificación del Boilerplate

Usa esta lista para verificar que todo está correctamente configurado.

## ✅ Instalación Básica

- [ ] Node.js v18+ instalado (`node --version`)
- [ ] npm funciona (`npm --version`)
- [ ] Proyecto clonado/copiado
- [ ] `npm install` ejecutado sin errores
- [ ] Archivo `.env` creado (copiar de `.env.example`)

## ✅ Configuración de Supabase

- [ ] Cuenta de Supabase creada
- [ ] Proyecto creado en Supabase
- [ ] `PROJECT_URL` copiada al `.env`
- [ ] `API_KEY` (anon/public key) copiada al `.env`
- [ ] Script `setup_database.sql` ejecutado en SQL Editor
- [ ] Tabla `api_keys` visible en Table Editor

## ✅ Configuración de Redis

- [ ] Redis instalado O Docker disponible
- [ ] Redis corriendo (`redis-cli ping` → responde PONG)
- [ ] Puerto 6379 disponible

## ✅ Verificación del Servidor

- [ ] `npm start` inicia el servidor
- [ ] Mensaje "Servidor corriendo en http://localhost:3000" visible
- [ ] No hay errores en consola

## ✅ Pruebas Básicas

- [ ] `curl http://localhost:3000/api` responde con JSON
- [ ] Registro de API Key funciona:
  ```bash
  curl -X POST http://localhost:3000/api/register \
    -H "Content-Type: application/json" \
    -d '{"client_name":"Test","email":"test@test.com"}'
  ```
- [ ] Se recibe una API Key en la respuesta
- [ ] La API Key aparece en Supabase (Table Editor → api_keys)

## ✅ Estructura de Archivos

- [ ] Carpeta `src/` existe
- [ ] Subcarpetas creadas:
  - [ ] `src/config/`
  - [ ] `src/models/`
  - [ ] `src/repositories/`
  - [ ] `src/services/`
  - [ ] `src/controllers/`
  - [ ] `src/routes/`
  - [ ] `src/middlewares/`
  - [ ] `src/utils/`
- [ ] Cada carpeta tiene su README.md

## ✅ Archivos de Configuración

- [ ] `index.mjs` existe en raíz
- [ ] `src/app.mjs` existe
- [ ] `src/config/database.mjs` existe
- [ ] `src/config/redis.mjs` existe
- [ ] `.gitignore` existe
- [ ] `.env.example` existe

## ✅ Documentación

- [ ] `README.md` existe
- [ ] `BOILERPLATE_README.md` existe
- [ ] `GUIA_ESTUDIANTES.md` existe
- [ ] READMEs en cada carpeta de `src/`

## 🧪 Pruebas Avanzadas

- [ ] Endpoint protegido sin API Key devuelve 401
- [ ] Endpoint protegido con API Key funciona:
  ```bash
  curl -X GET http://localhost:3000/api/protected/data \
    -H "X-API-Key: TU_API_KEY_AQUI"
  ```
- [ ] Rate limiting funciona (>10 peticiones/min = 429)
- [ ] Desactivar API Key funciona:
  ```bash
  curl -X PUT http://localhost:3000/api/admin/keys/API_KEY/deactivate
  ```
- [ ] API Key desactivada no funciona

## 🎯 Para Estudiantes

Antes de empezar tu proyecto, verifica:

- [ ] Entiendo la estructura de carpetas
- [ ] He leído los README.md de cada carpeta
- [ ] He probado crear un endpoint de ejemplo
- [ ] Entiendo el flujo: Route → Controller → Service → Repository
- [ ] Sé dónde poner cada tipo de código

## 🚨 Problemas Comunes

### El servidor no inicia:
- [ ] Redis está corriendo
- [ ] Puerto 3000 no está ocupado
- [ ] `.env` tiene las credenciales correctas
- [ ] `npm install` se ejecutó completamente

### Error de Supabase:
- [ ] URLs en `.env` no tienen espacios
- [ ] API Key es la "anon" key, no la "service_role"
- [ ] Tabla `api_keys` existe en Supabase
- [ ] RLS (Row Level Security) está deshabilitado en la tabla

### Redis no conecta:
- [ ] `redis-server` está corriendo
- [ ] Firewall no bloquea puerto 6379
- [ ] Intentar: `docker run -d -p 6379:6379 redis`

### 404 en endpoints:
- [ ] URL correcta: `/api/register` no `/register`
- [ ] Método HTTP correcto (POST/GET/PUT)
- [ ] Servidor está corriendo

## ✨ Todo Listo

Si todos los checks están marcados, ¡estás listo para empezar a desarrollar tu proyecto!

**Siguiente paso:** Lee `GUIA_ESTUDIANTES.md` para empezar a crear tu API.
