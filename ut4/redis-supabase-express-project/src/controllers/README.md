# Controladores (Controllers)

Esta carpeta contiene los controladores que manejan las peticiones HTTP.

## ¿Qué va aquí?

Los controladores son responsables de recibir las peticiones, llamar a los servicios y enviar respuestas.

## Ejemplo de uso:

```javascript
// controllers/usuarioController.mjs
import { UsuarioService } from '../services/usuarioService.mjs';

export class UsuarioController {
  constructor() {
    this.service = new UsuarioService();
  }

  // POST /usuarios
  crear = async (req, res) => {
    try {
      const { nombre, email, password } = req.body;

      // Validar entrada
      if (!nombre || !email || !password) {
        return res.status(400).json({
          error: 'Faltan campos requeridos'
        });
      }

      // Llamar al servicio
      const usuario = await this.service.registrarUsuario(
        nombre,
        email,
        password
      );

      // Responder
      res.status(201).json({
        message: 'Usuario creado exitosamente',
        usuario: usuario.toPublic()
      });
    } catch (error) {
      console.error('Error en crear:', error);
      res.status(400).json({ error: error.message });
    }
  };

  // GET /usuarios/:id
  obtener = async (req, res) => {
    try {
      const { id } = req.params;
      const usuario = await this.service.obtenerPerfil(id);

      res.json(usuario.toPublic());
    } catch (error) {
      console.error('Error en obtener:', error);
      const status = error.message === 'Usuario no encontrado' ? 404 : 500;
      res.status(status).json({ error: error.message });
    }
  };

  // GET /usuarios
  listar = async (req, res) => {
    try {
      const usuarios = await this.service.listarUsuarios();

      res.json({
        total: usuarios.length,
        usuarios: usuarios.map(u => u.toPublic())
      });
    } catch (error) {
      console.error('Error en listar:', error);
      res.status(500).json({ error: 'Error al obtener usuarios' });
    }
  };

  // PUT /usuarios/:id
  actualizar = async (req, res) => {
    try {
      const { id } = req.params;
      const cambios = req.body;

      const usuario = await this.service.actualizarPerfil(id, cambios);

      res.json({
        message: 'Usuario actualizado',
        usuario: usuario.toPublic()
      });
    } catch (error) {
      console.error('Error en actualizar:', error);
      res.status(400).json({ error: error.message });
    }
  };

  // DELETE /usuarios/:id
  eliminar = async (req, res) => {
    try {
      const { id } = req.params;

      await this.service.eliminarUsuario(id);

      res.json({ message: 'Usuario eliminado' });
    } catch (error) {
      console.error('Error en eliminar:', error);
      res.status(400).json({ error: error.message });
    }
  };
}
```

## Responsabilidades:

- ✅ Recibir peticiones HTTP
- ✅ Validar datos de entrada básicos
- ✅ Llamar a servicios
- ✅ Formatear respuestas
- ✅ Manejar errores HTTP
- ❌ **NO** debe contener lógica de negocio
- ❌ **NO** debe acceder directamente a repositorios
