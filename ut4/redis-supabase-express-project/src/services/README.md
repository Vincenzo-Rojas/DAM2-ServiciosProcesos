# Servicios (Services)

Esta carpeta contiene la lógica de negocio de la aplicación.

## ¿Qué va aquí?

Los servicios contienen la lógica de negocio y orquestan las operaciones entre repositorios.

## Ejemplo de uso:

```javascript
// services/usuarioService.mjs
import { UsuarioRepository } from '../repositories/usuarioRepository.mjs';
import { enviarEmail } from '../utils/email.mjs';

export class UsuarioService {
  constructor() {
    this.repository = new UsuarioRepository();
  }

  async registrarUsuario(nombre, email, password) {
    // Validaciones de negocio
    if (!email.includes('@')) {
      throw new Error('Email inválido');
    }

    if (password.length < 8) {
      throw new Error('La contraseña debe tener al menos 8 caracteres');
    }

    // Verificar que no exista
    const existente = await this.repository.buscarPorEmail(email);
    if (existente) {
      throw new Error('El usuario ya existe');
    }

    // Hash de password (ejemplo)
    const passwordHash = await hashPassword(password);

    // Crear usuario
    const usuario = await this.repository.crear({
      nombre,
      email,
      password: passwordHash
    });

    // Enviar email de bienvenida
    await enviarEmail(email, 'Bienvenido!', '...');

    return usuario;
  }

  async obtenerPerfil(id) {
    const usuario = await this.repository.buscarPorId(id);
    if (!usuario) {
      throw new Error('Usuario no encontrado');
    }
    return usuario;
  }

  async actualizarPerfil(id, cambios) {
    // Validaciones
    if (cambios.email && !cambios.email.includes('@')) {
      throw new Error('Email inválido');
    }

    return await this.repository.actualizar(id, cambios);
  }
}
```

## Responsabilidades:

- ✅ Lógica de negocio
- ✅ Validaciones complejas
- ✅ Orquestación de múltiples repositorios
- ✅ Transacciones
- ✅ Integración con servicios externos
- ❌ **NO** debe contener lógica de presentación
- ❌ **NO** debe acceder directamente a la BD (usar repositorios)
