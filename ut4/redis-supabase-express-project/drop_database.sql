-- Script SQL para ELIMINAR completamente la tabla api_keys y sus componentes
-- ⚠️ ADVERTENCIA: Este script eliminará TODOS los datos de la tabla api_keys
-- Ejecuta este script en el SQL Editor de tu proyecto Supabase

-- Eliminar la tabla (esto también elimina los índices automáticamente)
DROP TABLE IF EXISTS api_keys CASCADE;

-- Eliminar la función del trigger si existe
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Confirmar que todo fue eliminado
DO $$
BEGIN
    RAISE NOTICE '✅ Tabla api_keys eliminada';
    RAISE NOTICE '✅ Función update_updated_at_column() eliminada';
    RAISE NOTICE '✅ Todos los triggers e índices asociados eliminados';
    RAISE NOTICE '⚠️  La base de datos ha sido limpiada completamente';
END $$;
