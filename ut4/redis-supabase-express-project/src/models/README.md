# Modelos (Models)

Esta carpeta contiene las definiciones de los modelos de datos de la aplicación.

## ¿Qué va aquí?

Los modelos representan las entidades de tu aplicación y definen su estructura de datos.

## Ejemplo de uso:

```javascript
// models/Usuario.mjs
export class Usuario {
  constructor(data) {
    this.id = data.id;
    this.nombre = data.nombre;
    this.email = data.email;
    this.created_at = data.created_at;
  }

  toJSON() {
    return {
      id: this.id,
      nombre: this.nombre,
      email: this.email,
      created_at: this.created_at
    };
  }

  // Validaciones
  isValid() {
    return this.nombre && this.email;
  }
}
```

## Responsabilidades:

- ✅ Definir la estructura de datos
- ✅ Validaciones básicas
- ✅ Transformaciones de datos (toJSON, toPublic, etc.)
- ❌ **NO** debe contener lógica de base de datos
- ❌ **NO** debe contener lógica de negocio compleja
