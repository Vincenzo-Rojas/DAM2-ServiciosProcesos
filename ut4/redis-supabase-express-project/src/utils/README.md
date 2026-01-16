# Utilidades (Utils)

Esta carpeta contiene funciones auxiliares y utilidades reutilizables.

## ¿Qué va aquí?

Funciones helper, validadores, formateadores y otras utilidades.

## Ejemplo de uso:

```javascript
// utils/validators.mjs
export const validarEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

export const validarPassword = (password) => {
  return password.length >= 8;
};

export const validarTelefono = (telefono) => {
  const regex = /^\+?[1-9]\d{1,14}$/;
  return regex.test(telefono);
};
```

```javascript
// utils/formatters.mjs
export const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES');
};

export const formatearMoneda = (cantidad) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'EUR'
  }).format(cantidad);
};

export const capitalizarTexto = (texto) => {
  return texto.charAt(0).toUpperCase() + texto.slice(1).toLowerCase();
};
```

```javascript
// utils/encryption.mjs
import bcrypt from 'bcrypt';

export const hashPassword = async (password) => {
  const salt = await bcrypt.genSalt(10);
  return await bcrypt.hash(password, salt);
};

export const compararPassword = async (password, hash) => {
  return await bcrypt.compare(password, hash);
};
```

```javascript
// utils/email.mjs
import { emailTransporter } from '../config/email.mjs';

export const enviarEmail = async (destinatario, asunto, contenido) => {
  const mailOptions = {
    from: process.env.EMAIL_FROM,
    to: destinatario,
    subject: asunto,
    html: contenido
  };

  return await emailTransporter.sendMail(mailOptions);
};

export const enviarEmailBienvenida = async (email, nombre) => {
  const html = `
    <h1>¡Bienvenido ${nombre}!</h1>
    <p>Gracias por registrarte en nuestra plataforma.</p>
  `;

  return await enviarEmail(email, 'Bienvenido!', html);
};
```

```javascript
// utils/apiResponse.mjs
export const successResponse = (data, message = 'Success') => {
  return {
    success: true,
    message,
    data
  };
};

export const errorResponse = (message, errors = null) => {
  return {
    success: false,
    message,
    errors
  };
};
```

```javascript
// utils/pagination.mjs
export const paginar = (array, page = 1, limit = 10) => {
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;

  return {
    data: array.slice(startIndex, endIndex),
    pagination: {
      page,
      limit,
      total: array.length,
      totalPages: Math.ceil(array.length / limit)
    }
  };
};
```

## Tipos comunes de utilidades:

- **Validadores**: Validar formatos de datos
- **Formateadores**: Formatear fechas, números, texto
- **Encriptación**: Hash de passwords, encriptación de datos
- **Email**: Envío de correos
- **Logging**: Funciones de registro
- **API Response**: Estandarizar respuestas
- **Paginación**: Helper para paginar resultados
