from flask import Flask, request, jsonify, make_response, send_from_directory, session, render_template, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename
import logging
from datetime import datetime, timedelta
from database import execute_query, get_db_connection
from config import FLASK_CONFIG, UPLOAD_CONFIG, API_CONFIG, DB_CONFIG, ERROR_MESSAGES
import hashlib
from api_integration import TicketAPI
import mysql.connector
from mysql.connector import Error
from werkzeug.security import check_password_hash, generate_password_hash
import traceback

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurar logging para mysql.connector
logging.getLogger('mysql.connector').setLevel(logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'tecnocomputer_secret_key')

# Configuración de la sesión
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_COOKIE_SECURE'] = False  # Para desarrollo local
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_DOMAIN'] = None  # Para permitir cookies en localhost
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['SESSION_COOKIE_NAME'] = 'tecnocomputer_session'
app.config['REMEMBER_COOKIE_NAME'] = 'tecnocomputer_remember'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)
app.config['REMEMBER_COOKIE_SECURE'] = False  # Cambiar a True en producción
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

class User(UserMixin):
    def __init__(self, id, email, name, rol):
        self.id = id
        self.email = email
        self.name = name
        self.rol = rol

@login_manager.user_loader
def load_user(user_id):
    try:
        query = "SELECT * FROM usuarios WHERE usuario_id = %s"
        result = execute_query(query, (user_id,))
        if result:
            user_data = result[0]
            return User(
                id=user_data['usuario_id'],
                email=user_data['email'],
                name=user_data['nombre'],
                rol=user_data['rol']
            )
        return None
    except Exception as e:
        logger.error(f"Error al cargar usuario: {str(e)}")
        return None

# Configuración de CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True,
        "expose_headers": ["Set-Cookie"]
    }
})

# Configuración de la ruta para las imágenes
IMAGE_FOLDER = os.path.join(os.getcwd(), 'static/images')
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['MAX_CONTENT_LENGTH'] = UPLOAD_CONFIG['MAX_CONTENT_LENGTH']
app.config['ALLOWED_EXTENSIONS'] = UPLOAD_CONFIG['ALLOWED_EXTENSIONS']

# Configuración de la API de tickets
TICKET_API_URL = os.getenv('TICKET_API_URL', 'http://localhost:8000/api')
TICKET_API_KEY = os.getenv('TICKET_API_KEY', 'your-api-key-here')

# Inicialización de la API de tickets
ticket_api = TicketAPI(TICKET_API_URL, TICKET_API_KEY)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/images/<path:filename>')
def serve_image(filename):
    try:
        return send_from_directory(app.config['IMAGE_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({"error": "Imagen no encontrada"}), 404

# Endpoints para Órdenes de Servicio
@app.route('/api/ordenes_servicio', methods=['GET'])
@login_required
def obtener_ordenes_servicio():
    try:
        logger.info("Obteniendo órdenes de servicio...")
        query = '''
            SELECT 
                os.idordenes_servicio,
                os.marca,
                os.modelo,
                os.serial,
                os.diag_inicial,
                os.diag_final,
                os.serial_ram_1,
                os.serial_ram_2,
                os.serial_disco_1,
                os.serial_disco_2,
                os.serial_cargador,
                os.serial_bateria,
                os.fecha_entrada,
                os.fecha_salida,
                os.id_cliente,
                os.inicio_trabajo,
                os.fin_trabajo,
                os.estado,
                os.id_tecnico,
                CONCAT(COALESCE(c.first_name, ''), ' ', COALESCE(c.last_name, '')) as nombre_cliente,
                CASE 
                    WHEN os.inicio_trabajo IS NOT NULL AND os.fin_trabajo IS NOT NULL
                    THEN TIMESTAMPDIFF(MINUTE, os.inicio_trabajo, os.fin_trabajo)
                    ELSE 0
                END as tiempo_trabajo
            FROM ordenes_servicio os
            LEFT JOIN clientes c ON os.id_cliente = c.cliente_id
            ORDER BY os.fecha_entrada DESC
        '''
        result = execute_query(query)
        
        if result is None:
            logger.error("Error al ejecutar la consulta")
            return jsonify({"error": "Error al obtener las órdenes de servicio"}), 500
            
        # Convertir fechas a string para JSON
        for orden in result:
            for key, value in orden.items():
                if isinstance(value, datetime):
                    orden[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"Se encontraron {len(result)} órdenes")
        return jsonify(result)
            
    except Exception as e:
        logger.error(f"Error al obtener órdenes de servicio: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/ordenes/agregar')
@login_required
def agregar_orden():
    if current_user.rol != 'tecnico':
        return redirect(url_for('login'))
    return render_template('agregar_orden.html')

@app.route('/api/ordenes_servicio', methods=['POST'])
@login_required
def crear_orden_servicio():
    conn = None
    cursor = None
    try:
        # Verificar rol del usuario
        if not hasattr(current_user, 'rol') or current_user.rol != 'tecnico':
            return jsonify({"error": "No autorizado. Se requiere rol de técnico"}), 401

        data = request.json
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        # Validar campos requeridos
        required_fields = ['cliente_id', 'marca', 'modelo', 'serial', 'diag_inicial', 'tipo', 'prioridad', 'fecha_estimada']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Obtener conexión a la base de datos
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Error al conectar con la base de datos"}), 500

        cursor = conn.cursor()

        # Verificar que el cliente existe
        cursor.execute("SELECT cliente_id FROM clientes WHERE cliente_id = %s", (data['cliente_id'],))
        if not cursor.fetchone():
            return jsonify({"error": "Cliente no encontrado"}), 404

        # Insertar la orden de servicio
        query = """
            INSERT INTO ordenes_servicio 
            (id_cliente, marca, modelo, serial, tipo, diag_inicial, observaciones, 
             prioridad, fecha_estimada, estado, id_tecnico, fecha_entrada)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        params = (
            data['cliente_id'],
            data['marca'],
            data['modelo'],
            data['serial'],
            data['tipo'],
            data['diag_inicial'],
            data.get('observaciones', ''),
            data['prioridad'],
            data['fecha_estimada'],
            'Pendiente',  # Estado inicial
            current_user.id  # ID del técnico actual
        )

        cursor.execute(query, params)
        conn.commit()

        # Obtener el ID de la orden creada
        orden_id = cursor.lastrowid

        return jsonify({
            "success": True,
            "message": "Orden creada exitosamente",
            "orden_id": orden_id
        }), 201

    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Error de MySQL al crear orden: {str(e)}")
        return jsonify({"error": "Error al crear la orden en la base de datos"}), 500

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error inesperado al crear orden: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Endpoints para Clientes
@app.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html')

@app.route('/api/clientes', methods=['GET'])
@login_required
def get_clientes():
    conn = None
    cursor = None
    try:
        logger.info("Intentando obtener lista de clientes")
        
        # Obtener conexión a la base de datos
        conn = get_db_connection()
        if not conn:
            logger.error("No se pudo establecer conexión con la base de datos")
            return jsonify({
                'success': False,
                'message': 'Error al conectar con la base de datos'
            }), 500

        cursor = conn.cursor(dictionary=True)
        
        # Consulta para obtener todos los clientes
        query = "SELECT * FROM clientes ORDER BY first_name, last_name"
        logger.info(f"Ejecutando query: {query}")
        cursor.execute(query)
        clientes = cursor.fetchall()
        
        logger.info(f"Se encontraron {len(clientes)} clientes")
        return jsonify({
            'success': True,
            'clientes': clientes
        })

    except mysql.connector.Error as e:
        logger.error(f"Error de MySQL al obtener clientes: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener la lista de clientes'
        }), 500

    except Exception as e:
        logger.error(f"Error inesperado al obtener clientes: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/clientes/<cliente_id>', methods=['GET'])
@login_required
def get_cliente(cliente_id):
    conn = None
    cursor = None
    try:
        logger.info(f"Intentando obtener cliente con ID: {cliente_id}")
        
        # Obtener conexión a la base de datos
        conn = get_db_connection()
        if not conn:
            logger.error("No se pudo establecer conexión con la base de datos")
            return jsonify({"error": "Error al conectar con la base de datos"}), 500

        cursor = conn.cursor(dictionary=True)
        
        # Verificar que el cliente existe
        query = "SELECT * FROM clientes WHERE cliente_id = %s"
        cursor.execute(query, (cliente_id,))
        cliente = cursor.fetchone()
        
        if not cliente:
            logger.warning(f"Cliente no encontrado con ID: {cliente_id}")
            return jsonify({
                'success': False,
                'message': 'Cliente no encontrado'
            }), 404
            
        logger.info(f"Cliente encontrado: {cliente}")
        return jsonify({
            'success': True,
            'cliente': cliente
        })

    except mysql.connector.Error as e:
        logger.error(f"Error de MySQL al obtener cliente: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener la información del cliente'
        }), 500

    except Exception as e:
        logger.error(f"Error inesperado al obtener cliente: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/clientes', methods=['POST'])
@login_required
def crear_cliente():
    try:
        data = request.json
        logger.info(f"Datos recibidos para crear cliente: {data}")
        
        if not data:
            logger.error("No se recibieron datos en la solicitud")
            return jsonify({"error": "No se recibieron datos"}), 400

        # Validar campos requeridos
        required_fields = ['cliente_id', 'first_name', 'last_name', 'email']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.error(f"Faltan campos requeridos: {missing_fields}")
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Validar formato de email
        if not '@' in data['email']:
            logger.error(f"Email inválido: {data['email']}")
            return jsonify({"error": "El email no tiene un formato válido"}), 400

        # Validar longitud de campos
        if len(data['cliente_id']) > 50:
            return jsonify({"error": "El ID del cliente no puede tener más de 50 caracteres"}), 400
        if len(data['first_name']) > 50:
            return jsonify({"error": "El nombre no puede tener más de 50 caracteres"}), 400
        if len(data['last_name']) > 50:
            return jsonify({"error": "El apellido no puede tener más de 50 caracteres"}), 400
        if len(data['email']) > 100:
            return jsonify({"error": "El email no puede tener más de 100 caracteres"}), 400
        if 'phone_number' in data and len(data['phone_number']) > 20:
            return jsonify({"error": "El número de teléfono no puede tener más de 20 caracteres"}), 400

        # Verificar si el cliente_id o email ya existen
        check_query = "SELECT cliente_id, email FROM clientes WHERE cliente_id = %s OR email = %s"
        existing = execute_query(check_query, (data['cliente_id'], data['email']))
        
        if existing:
            if existing[0]['cliente_id'] == data['cliente_id']:
                logger.error(f"ID de cliente duplicado: {data['cliente_id']}")
                return jsonify({"error": "El ID del cliente ya existe"}), 400
            if existing[0]['email'] == data['email']:
                logger.error(f"Email duplicado: {data['email']}")
                return jsonify({"error": "El email ya está registrado"}), 400

        # Insertar el nuevo cliente
        insert_query = '''
            INSERT INTO clientes 
            (cliente_id, first_name, last_name, email, phone_number, 
            street_address, city, state, postal_code, country, 
            gender, account_status, notes, contact_preferences, 
            referred_by, customer_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        params = (
            data['cliente_id'],
            data['first_name'],
            data['last_name'],
            data['email'],
            data.get('phone_number', None),
            data.get('street_address', None),
            data.get('city', None),
            data.get('state', None),
            data.get('postal_code', None),
            data.get('country', None),
            data.get('gender', None),
            data.get('account_status', 'active'),
            data.get('notes', None),
            data.get('contact_preferences', None),
            data.get('referred_by', None),
            data.get('customer_type', None)
        )

        logger.info(f"Ejecutando query de inserción para cliente: {data['cliente_id']}")
        result = execute_query(insert_query, params, fetch=False)
        
        if result:
            logger.info(f"Cliente creado exitosamente con ID: {data['cliente_id']}")
            return jsonify({
                "success": True,
                "message": "Cliente creado exitosamente",
                "cliente_id": data['cliente_id']
            }), 201
        else:
            logger.error("Error al ejecutar la inserción del cliente")
            return jsonify({"error": "Error al crear el cliente en la base de datos"}), 500

    except Exception as e:
        logger.error(f"Error inesperado al crear cliente: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Endpoints de Autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        logger.info(f"Intento de login con datos: {data}")
        
        if not data or 'email' not in data or 'password' not in data:
            logger.warning("Faltan email o contraseña en la solicitud de login")
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        logger.info(f"Conectando a la base de datos para usuario: {data['email']}")
        conn = get_db_connection()
        if not conn:
            logger.error("Error al conectar con la base de datos")
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            logger.info("Buscando usuario en la base de datos")
            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (data['email'],))
            user = cursor.fetchone()
            
            if not user:
                logger.warning(f"Usuario no encontrado: {data['email']}")
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            logger.info(f"Usuario encontrado: {user['email']}")
            
            if user['estado'] != 'activo':
                logger.warning(f"Cuenta inactiva: {data['email']}")
                return jsonify({'error': 'Cuenta inactiva'}), 403
            
            logger.info("Verificando contraseña")
            # Hash la contraseña proporcionada con SHA-256
            hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
            if user['password'] != hashed_password:
                logger.warning(f"Contraseña incorrecta para usuario: {data['email']}")
                return jsonify({'error': 'Contraseña incorrecta'}), 401
            
            logger.info("Actualizando último login")
            cursor.execute('UPDATE usuarios SET ultimo_login = NOW() WHERE usuario_id = %s', (user['usuario_id'],))
            conn.commit()
            
            # Crear objeto User para Flask-Login
            user_obj = User(
                id=user['usuario_id'],
                email=user['email'],
                name=user['nombre'],
                rol=user['rol']
            )
            
            # Iniciar sesión con Flask-Login
            login_user(user_obj, remember=True)
            
            # Configurar la sesión
            session.permanent = True
            session['user_id'] = user['usuario_id']
            session['email'] = user['email']
            session['name'] = user['nombre']
            session['rol'] = user['rol']
            
            logger.info(f"Login exitoso para usuario: {data['email']}")
            return jsonify({
                'message': 'Login exitoso',
                'user': {
                    'id': user['usuario_id'],
                    'email': user['email'],
                    'name': user['nombre'],
                    'rol': user['rol']
                }
            })
            
        except mysql.connector.Error as e:
            logger.error(f"Error de MySQL durante el login: {str(e)}")
            logger.error(f"Código de error: {e.errno}")
            logger.error(f"SQL State: {e.sqlstate}")
            return jsonify({'error': 'Error de base de datos'}), 500
            
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                logger.info("Conexión cerrada")
    
    except Exception as e:
        logger.error(f"Error inesperado durante el login: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Error inesperado'}), 500

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        # Obtener el email del usuario antes de cerrar sesión para logging
        user_email = current_user.email if current_user.is_authenticated else 'Desconocido'
        
        # Cerrar sesión con Flask-Login
        logout_user()
        
        # Limpiar la sesión de Flask
        session.clear()
        
        # Eliminar las cookies de sesión
        response = make_response(redirect(url_for('login')))
        response.delete_cookie('session')
        response.delete_cookie('remember_token')
        response.delete_cookie('tecnocomputer_session')
        response.delete_cookie('tecnocomputer_remember')
        
        logger.info(f"Usuario {user_email} ha cerrado sesión exitosamente")
        return response
        
    except Exception as e:
        logger.error(f"Error al cerrar sesión: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return redirect(url_for('login'))

@app.route('/api/check-session', methods=['GET'])
def check_session():
    if current_user.is_authenticated:
        return jsonify({
            "authenticated": True,
            "user": {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name,
                "rol": current_user.rol
            }
        })
    return jsonify({"authenticated": False})

# Rutas para las vistas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/ordenes')
@login_required
def ordenes():
    return render_template('ordenes.html')

# Middleware para verificar autenticación
@app.before_request
def check_auth():
    # Rutas que no requieren autenticación
    public_routes = ['/', '/login', '/nosotros', '/productos', '/api/login', '/static/', '/images/']
    
    logger.info(f"Ruta solicitada: {request.path}")
    logger.info(f"Método: {request.method}")
    logger.info(f"Usuario autenticado: {current_user.is_authenticated}")
    
    # Permitir acceso a rutas públicas y recursos estáticos
    if any(request.path.startswith(route) for route in public_routes):
        logger.info(f"Acceso permitido a ruta pública: {request.path}")
        return None
        
    # Verificar autenticación para rutas API
    if request.path.startswith('/api/'):
        if not current_user.is_authenticated and request.path != '/api/login':
            logger.warning(f"Intento de acceso no autorizado a API: {request.path}")
            return jsonify({"error": "No autorizado"}), 401
        logger.info(f"Acceso permitido a API: {request.path}")
        return None
    
    # Verificar autenticación para otras rutas
    if not current_user.is_authenticated:
        logger.warning(f"Intento de acceso no autorizado a ruta: {request.path}")
        return redirect(url_for('login', next=request.path))
    
    logger.info(f"Acceso permitido a ruta: {request.path}")
    return None

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    try:
        query = '''
            SELECT 
                t.ticket_id,
                t.orden_id,
                t.titulo,
                t.descripcion,
                t.departamento_id,
                d.nombre as departamento_nombre,
                t.estado,
                t.prioridad,
                t.fecha_creacion,
                t.fecha_actualizacion,
                t.creado_por,
                t.asignado_a,
                CONCAT(cu.first_name, ' ', cu.last_name) as creado_por_nombre,
                CONCAT(au.first_name, ' ', au.last_name) as asignado_a_nombre,
                os.idordenes_servicio,
                os.marca,
                os.modelo,
                os.serial,
                os.estado as orden_estado
            FROM tickets t
            LEFT JOIN departamentos d ON t.departamento_id = d.departamento_id
            LEFT JOIN usuarios cu ON t.creado_por = cu.usuario_id
            LEFT JOIN usuarios au ON t.asignado_a = au.usuario_id
            LEFT JOIN ordenes_servicio os ON t.orden_id = os.idordenes_servicio
            ORDER BY t.fecha_creacion DESC
        '''
        success, result = execute_query(query)
        
        if not success:
            logger.error(f"Error en la consulta: {result}")
            return jsonify({"error": str(result)}), 500
            
        return jsonify({"success": True, "tickets": result})
    except Exception as e:
        logger.error(f"Error al obtener tickets: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    try:
        data = request.get_json()
        required_fields = ['titulo', 'descripcion', 'departamento_id']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
        
        # Obtener el ID del usuario actual
        usuario_id = session.get('user_id')
        if not usuario_id:
            return jsonify({"error": "Usuario no autenticado"}), 401
        
        # Insertar el ticket
        query = '''
            INSERT INTO tickets (
                titulo, descripcion, departamento_id, estado, prioridad,
                creado_por, asignado_a, orden_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (
            data['titulo'],
            data['descripcion'],
            data['departamento_id'],
            data.get('estado', 'abierto'),
            data.get('prioridad', 'normal'),
            usuario_id,
            data.get('asignado_a'),
            data.get('orden_id')
        )
        
        success, result = execute_query(query, values)
        
        if not success:
            logger.error(f"Error al crear ticket: {result}")
            return jsonify({"error": str(result)}), 500
            
        # Si se especificó una orden, actualizar la referencia
        if data.get('orden_id'):
            update_query = '''
                UPDATE ordenes_servicio 
                SET ticket_id = %s 
                WHERE idordenes_servicio = %s
            '''
            execute_query(update_query, (result, data['orden_id']))
        
        return jsonify({
            "success": True,
            "message": "Ticket creado exitosamente",
            "ticket_id": result
        })
    except Exception as e:
        logger.error(f"Error al crear ticket: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ordenes/<int:orden_id>/tickets', methods=['GET'])
def get_orden_tickets(orden_id):
    try:
        query = '''
            SELECT 
                t.ticket_id,
                t.titulo,
                t.descripcion,
                t.departamento_id,
                d.nombre as departamento_nombre,
                t.estado,
                t.prioridad,
                t.fecha_creacion,
                t.fecha_actualizacion,
                CONCAT(u.first_name, ' ', u.last_name) as creado_por_nombre
            FROM tickets t
            LEFT JOIN departamentos d ON t.departamento_id = d.departamento_id
            LEFT JOIN usuarios u ON t.creado_por = u.usuario_id
            WHERE t.orden_id = %s
            ORDER BY t.fecha_creacion DESC
        '''
        success, result = execute_query(query, (orden_id,))
        
        if not success:
            logger.error(f"Error en la consulta: {result}")
            return jsonify({"error": str(result)}), 500
            
        return jsonify({"success": True, "tickets": result})
    except Exception as e:
        logger.error(f"Error al obtener tickets de la orden: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ordenes/<int:orden_id>/tickets', methods=['POST'])
def create_orden_ticket(orden_id):
    try:
        data = request.get_json()
        required_fields = ['titulo', 'descripcion', 'departamento_id']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
        
        # Obtener el ID del usuario actual
        usuario_id = session.get('user_id')
        if not usuario_id:
            return jsonify({"error": "Usuario no autenticado"}), 401
        
        # Insertar el ticket
        query = '''
            INSERT INTO tickets (
                titulo, descripcion, departamento_id, estado, prioridad,
                creado_por, asignado_a, orden_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (
            data['titulo'],
            data['descripcion'],
            data['departamento_id'],
            data.get('estado', 'abierto'),
            data.get('prioridad', 'normal'),
            usuario_id,
            data.get('asignado_a'),
            orden_id
        )
        
        success, result = execute_query(query, values)
        
        if not success:
            logger.error(f"Error al crear ticket: {result}")
            return jsonify({"error": str(result)}), 500
            
        # Actualizar la referencia en la orden
        update_query = '''
            UPDATE ordenes_servicio 
            SET ticket_id = %s 
            WHERE idordenes_servicio = %s
        '''
        execute_query(update_query, (result, orden_id))
        
        return jsonify({
            "success": True,
            "message": "Ticket creado exitosamente",
            "ticket_id": result
        })
    except Exception as e:
        logger.error(f"Error al crear ticket para la orden: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/departamentos', methods=['GET'])
def get_departamentos():
    try:
        query = '''
            SELECT 
                departamento_id,
                nombre,
                descripcion,
                estado
            FROM departamentos
            WHERE estado = 'activo'
            ORDER BY nombre
        '''
        success, result = execute_query(query)
        
        if not success:
            logger.error(f"Error en la consulta: {result}")
            return jsonify({"error": str(result)}), 500
            
        return jsonify({"success": True, "departamentos": result})
    except Exception as e:
        logger.error(f"Error al obtener departamentos: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Nuevos endpoints para tickets y órdenes
@app.route('/api/tickets/orden/<int:orden_id>', methods=['GET'])
@login_required
def get_tickets_by_order(orden_id):
    try:
        cursor = mysql.connection.cursor()
        query = """
            SELECT t.*, d.nombre as departamento_nombre, 
                   u.nombre as usuario_nombre, u.apellido as usuario_apellido
            FROM tickets t
            LEFT JOIN departamentos d ON t.departamento_id = d.departamento_id
            LEFT JOIN usuarios u ON t.usuario_id = u.usuario_id
            WHERE t.orden_id = %s
            ORDER BY t.fecha_creacion DESC
        """
        cursor.execute(query, (orden_id,))
        tickets = cursor.fetchall()
        return jsonify([dict(ticket) for ticket in tickets])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tickets/historial/<int:ticket_id>', methods=['GET'])
@login_required
def get_ticket_history(ticket_id):
    try:
        cursor = mysql.connection.cursor()
        query = """
            SELECT h.*, u.nombre, u.apellido
            FROM ticket_historial h
            JOIN usuarios u ON h.usuario_id = u.usuario_id
            WHERE h.ticket_id = %s
            ORDER BY h.fecha_cambio DESC
        """
        cursor.execute(query, (ticket_id,))
        historial = cursor.fetchall()
        return jsonify([dict(registro) for registro in historial])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ordenes/estadisticas', methods=['GET'])
@login_required
def get_order_statistics():
    try:
        cursor = mysql.connection.cursor()
        query = """
            SELECT 
                COUNT(*) as total_ordenes,
                SUM(CASE WHEN estado = 'Pendiente' THEN 1 ELSE 0 END) as pendientes,
                SUM(CASE WHEN estado = 'En Proceso' THEN 1 ELSE 0 END) as en_proceso,
                SUM(CASE WHEN estado = 'Completado' THEN 1 ELSE 0 END) as completados,
                AVG(tiempo_estimado) as tiempo_promedio,
                AVG(costo_estimado) as costo_promedio
            FROM ordenes_servicio
            WHERE fecha_entrada >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """
        cursor.execute(query)
        estadisticas = cursor.fetchone()
        return jsonify(dict(estadisticas))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Optimizar consulta existente de órdenes
@app.route('/api/ordenes_servicio', methods=['GET'])
@login_required
def get_ordenes_servicio():
    try:
        cursor = mysql.connection.cursor()
        query = """
            SELECT 
                os.*,
                c.nombre as cliente_nombre,
                c.apellido as cliente_apellido,
                c.telefono as cliente_telefono,
                t.ticket_id,
                t.estado as ticket_estado,
                t.prioridad as ticket_prioridad
            FROM ordenes_servicio os
            LEFT JOIN clientes c ON os.cliente_id = c.cliente_id
            LEFT JOIN tickets t ON os.ticket_id = t.ticket_id
            ORDER BY os.fecha_entrada DESC
        """
        cursor.execute(query)
        ordenes = cursor.fetchall()
        return jsonify([dict(orden) for orden in ordenes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Configuración para servir archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)
    app.run(
        host=FLASK_CONFIG['HOST'],
        port=FLASK_CONFIG['PORT'],
        debug=FLASK_CONFIG['DEBUG']
    )
