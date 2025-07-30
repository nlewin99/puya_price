# 📱 Puya Price Scanner

Aplicación Streamlit para consultar precios y stock de productos escaneando códigos de barras desde la cámara del teléfono.

## 🚀 Características

- **Escáner de códigos de barras** usando la cámara del dispositivo
- **Consulta en tiempo real** de información de productos en Odoo
- **Interfaz moderna y responsive** optimizada para móviles
- **Información completa** del producto: precio, stock, SKU

## 📋 Requisitos

- Acceso a la API de Odoo v16
- Cámara web o cámara de teléfono
- Aplicación desplegada en Streamlit Cloud

## 🛠️ Configuración en Streamlit Cloud

1. **Subir el código** a un repositorio de GitHub

2. **Configurar credenciales** en Streamlit Cloud:
   - Ve a tu aplicación en Streamlit Cloud
   - En la sección "Settings" → "Secrets"
   - Agrega las siguientes variables:
   ```toml
   ODOO_URL = "https://tu-servidor-odoo.com"
   ODOO_DB = "nombre_base_datos"
   ODOO_USERNAME = "usuario_odoo"
   ODOO_PASSWORD = "contraseña_odoo"
   ```

3. **Desplegar la aplicación** en Streamlit Cloud

## 📱 Uso

1. **Abrir la aplicación** en tu navegador o dispositivo móvil
2. **Hacer clic en "INICIAR ESCANEO"** en la página principal
3. **Apunta la cámara** hacia el código de barras del producto
4. **Espera la detección** automática del código
5. **Revisa la información** del producto que se muestra

## 🔧 Configuración

### Credenciales de Odoo

Las credenciales se configuran en Streamlit Cloud:

- `ODOO_URL`: URL base de tu servidor Odoo
- `ODOO_DB`: Nombre de la base de datos
- `ODOO_USERNAME`: Usuario con permisos de lectura
- `ODOO_PASSWORD`: Contraseña del usuario

### Permisos de Cámara

La aplicación requiere acceso a la cámara del dispositivo. Asegúrate de:

- Permitir el acceso a la cámara cuando el navegador lo solicite
- Usar HTTPS (automático en Streamlit Cloud)

## 📊 Información del Producto

La aplicación muestra la siguiente información para cada producto:

- **Nombre del producto**
- **Precio de venta** (list_price)
- **Stock disponible** (immediately_usable_qty)
- **SKU/Código interno**
- **Código de barras**

## 🐛 Solución de Problemas

### Error de cámara
- Verifica que el dispositivo tenga cámara
- Asegúrate de permitir el acceso a la cámara
- En móviles, usa HTTPS (automático en Streamlit Cloud)

### Error de conexión con Odoo
- Verifica las credenciales en Streamlit Cloud
- Confirma que el servidor Odoo esté accesible
- Verifica que el usuario tenga permisos de lectura

### Producto no encontrado
- Confirma que el código de barras existe en Odoo
- Verifica que el producto esté activo
- Revisa que el campo `barcode` esté configurado

## 📁 Estructura del Proyecto

```
puya_price/
├── app.py              # Aplicación principal
├── odoo_client.py      # Cliente para API de Odoo
├── barcode_scanner.py  # Módulo de escaneo
├── requirements.txt     # Dependencias
└── README.md          # Este archivo
```

## 🔒 Seguridad

- Las credenciales se almacenan en Streamlit Cloud (no en el código)
- Solo se realizan operaciones de lectura en Odoo
- No se almacenan datos sensibles en la aplicación

## 📞 Soporte

Para problemas o preguntas, contacta al equipo de desarrollo.
