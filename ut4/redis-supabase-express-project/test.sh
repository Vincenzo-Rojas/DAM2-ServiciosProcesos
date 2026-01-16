#!/bin/bash

# Script de pruebas para el sistema de API Keys

BASE_URL="http://localhost:3000"

echo "🧪 PRUEBAS DEL SISTEMA DE API KEYS"
echo "=================================="
echo ""

# 1. Probar endpoint raíz
echo "1️⃣  Probando endpoint raíz..."
curl -s $BASE_URL | jq '.'
echo ""
echo ""

# 2. Registrar un nuevo cliente
echo "2️⃣  Registrando nuevo cliente..."
RESPONSE=$(curl -s -X POST $BASE_URL/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "App de Prueba",
    "email": "prueba@example.com"
  }')

echo $RESPONSE | jq '.'
API_KEY=$(echo $RESPONSE | jq -r '.api_key')
echo ""
echo "✅ API Key generada: $API_KEY"
echo ""
echo ""

# 3. Probar acceso sin API Key
echo "3️⃣  Probando acceso SIN API Key (debería fallar)..."
curl -s $BASE_URL/api/protected/data | jq '.'
echo ""
echo ""

# 4. Probar acceso con API Key válida
echo "4️⃣  Probando acceso CON API Key válida..."
curl -s -X GET $BASE_URL/api/protected/data \
  -H "X-API-Key: $API_KEY" | jq '.'
echo ""
echo ""

# 5. Obtener información del cliente
echo "5️⃣  Obteniendo información del cliente autenticado..."
curl -s -X GET $BASE_URL/api/protected/me \
  -H "X-API-Key: $API_KEY" | jq '.'
echo ""
echo ""

# 6. Listar todas las API Keys
echo "6️⃣  Listando todas las API Keys registradas..."
curl -s $BASE_URL/api/admin/keys | jq '.keys[] | {client_name, email, api_key, is_active}'
echo ""
echo ""

# 7. Probar rate limiting
echo "7️⃣  Probando rate limiting (12 peticiones rápidas)..."
for i in {1..12}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET $BASE_URL/api/protected/data \
    -H "X-API-Key: $API_KEY")
  if [ $STATUS -eq 429 ]; then
    echo "   Request $i: ⛔ Rate limit excedido (HTTP $STATUS)"
  else
    echo "   Request $i: ✅ OK (HTTP $STATUS)"
  fi
done
echo ""
echo ""

# 8. Desactivar API Key
echo "8️⃣  Desactivando API Key..."
curl -s -X PUT $BASE_URL/api/admin/keys/$API_KEY/deactivate | jq '.'
echo ""
echo ""

# 9. Probar acceso con API Key desactivada
echo "9️⃣  Probando acceso con API Key DESACTIVADA (debería fallar)..."
curl -s -X GET $BASE_URL/api/protected/data \
  -H "X-API-Key: $API_KEY" | jq '.'
echo ""
echo ""

echo "✨ Pruebas completadas!"
