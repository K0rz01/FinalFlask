# 🖥️ FlaskTecnoComputer API

Sistema de gestión integral para empresa de servicios técnicos y ventas de equipos de computación.

## 📋 Descripción

API desarrollada en Flask que permite administrar:
- 👥 **Clientes** - Gestión completa de información de clientes
- 🔧 **Órdenes de servicio** - Creación y seguimiento de órdenes
- 📦 **Inventario** - Control de productos y categorías
- 🎫 **Tickets de soporte** - Sistema de tickets con asignación por departamentos
- 👤 **Usuarios** - Sistema de autenticación y roles
- 🏢 **Departamentos** - Organización interna

## 🚀 Tecnologías

- **Backend:** Python 3.13, Flask, Flask-Login, Flask-CORS
- **Base de datos:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript
- **Seguridad:** Hash de contraseñas, manejo de sesiones

## 📦 Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/K0rz01/FinalFlask.git
   cd FinalFlask
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar base de datos:**
   - Crear base de datos MySQL
   - Ejecutar scripts SQL en la carpeta `bd/`
   - Configurar `config.py` con credenciales

4. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

## 🔧 Configuración

Editar `config.py` con tus credenciales de base de datos:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'tecnocomputer'
}
```

## 📚 Documentación

- `DOCUMENTACION_PROYECTO.txt` - Documentación completa del sistema
- `DOCUMENTACION_BD.txt` - Estructura de base de datos
- `bd/` - Scripts SQL y modelos de base de datos

## 👥 Colaboradores

- **K0rz01** (oe.martinez05@ciaf.edu.co) - Desarrollador principal
- **Olavio Loaiza** (ol.loaiza17@ciaf.edu.co) - Desarrollador colaborador

## 🚀 Características Principales

- **API RESTful** completa para gestión de servicios técnicos
- **Sistema de autenticación** robusto con roles de usuario
- **Base de datos MySQL** optimizada con triggers y procedimientos
- **Interfaz web** responsive y moderna
- **Documentación completa** del sistema y API

## 📝 Licencia

Este proyecto es parte de un taller académico de Git y desarrollo colaborativo.
