# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'tecnocomputer',
    'user': 'root',
    'password': '11111111',
    'charset': 'utf8mb4',
    'port': 3306,
    'auth_plugin': 'mysql_native_password',
    'use_pure': True,
    'raise_on_warnings': True,
    'pool_size': 5,
    'pool_name': 'tecnocomputer_pool',
    'connect_timeout': 20
}

# Flask Configuration
FLASK_CONFIG = {
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'DEBUG': True,
    'SECRET_KEY': 'tecnocomputer_secret_key',
    'SESSION_TYPE': 'filesystem',
    'PERMANENT_SESSION_LIFETIME': 86400,  # 24 horas en segundos
    'SESSION_COOKIE_SECURE': False,  # Cambiar a True en producción
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'SESSION_COOKIE_DOMAIN': None,  # Para desarrollo local
    'SESSION_COOKIE_PATH': '/',
    'SESSION_COOKIE_NAME': 'tecnocomputer_session',
    'REMEMBER_COOKIE_NAME': 'tecnocomputer_remember',
    'REMEMBER_COOKIE_DURATION': 86400,  # 24 horas en segundos
    'REMEMBER_COOKIE_SECURE': False,  # Cambiar a True en producción
    'REMEMBER_COOKIE_HTTPONLY': True,
    'REMEMBER_COOKIE_SAMESITE': 'Lax'
}

# Upload Configuration
UPLOAD_CONFIG = {
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max file size
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'gif'}
}

# API Configuration
API_CONFIG = {
    'CORS_ORIGINS': ['http://localhost:5000', 'http://127.0.0.1:5000'],
    'TICKET_API_URL': 'http://localhost:8000/api',
    'TICKET_API_KEY': 'your-api-key-here',
    'DEPARTMENTS': {
        1: 'Soporte Técnico',
        2: 'Ventas',
        3: 'Administración'
    },
    'PRIORITIES': {
        'low': 'Baja',
        'normal': 'Normal',
        'high': 'Alta'
    },
    'STATUSES': {
        'open': 'Abierto',
        'closed': 'Cerrado',
        'pending': 'Pendiente'
    }
}

# Estados de Órdenes de Servicio
ESTADOS_ORDEN = [
    'Pendiente',
    'En Revisión',
    'En Reparación',
    'Completado',
    'Entregado',
    'Cancelado'
]

# Mensajes de error
ERROR_MESSAGES = {
    'db_auth': 'Error de autenticación en la base de datos. Verifique las credenciales.',
    'db_not_found': 'La base de datos no existe. Verifique el nombre de la base de datos.',
    'db_connection': 'No se puede conectar al servidor MySQL. Verifique que el servidor esté en ejecución.',
    'db_query': 'Error al ejecutar la consulta en la base de datos.',
    'db_duplicate': 'Error: El registro ya existe en la base de datos.',
    'db_foreign_key': 'Error: Violación de llave foránea en la base de datos.',
    'db_general': 'Error general de la base de datos.'
}

# Configuración de la aplicación
SECRET_KEY = 'tu_clave_secreta_aqui'
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
