# Repositorios (Repositories)

Esta carpeta contiene los repositorios que manejan todas las operaciones de base de datos.

## ¿Qué va aquí?

Los repositorios son responsables de todas las operaciones CRUD y consultas a la base de datos.

## Ejemplo de uso:

```javascript
// repositories/usuarioRepository.mjs
import { supabase } from '../config/database.mjs';
import { Usuario } from '../models/Usuario.mjs';

export class UsuarioRepository {
  async crear(usuarioData) {
    const { data, error } = await supabase
      .from('usuarios')
      .insert([usuarioData])
      .select()
      .single();

    if (error) throw error;
    return new Usuario(data);
  }

  async buscarPorId(id) {
    const { data, error } = await supabase
      .from('usuarios')
      .select('*')
      .eq('id', id)
      .single();

    if (error) return null;
    return data ? new Usuario(data) : null;
  }

  async buscarTodos() {
    const { data, error } = await supabase
      .from('usuarios')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data.map(item => new Usuario(item));
  }

  async actualizar(id, cambios) {
    const { data, error } = await supabase
      .from('usuarios')
      .update(cambios)
      .eq('id', id)
      .select()
      .single();

    if (error) throw error;
    return new Usuario(data);
  }

  async eliminar(id) {
    const { error } = await supabase
      .from('usuarios')
      .delete()
      .eq('id', id);

    if (error) throw error;
    return true;
  }
}
```

## Responsabilidades:

- ✅ Operaciones CRUD (Create, Read, Update, Delete)
- ✅ Consultas a la base de datos
- ✅ Convertir datos de BD a modelos
- ❌ **NO** debe contener lógica de negocio
- ❌ **NO** debe manejar validaciones complejas
