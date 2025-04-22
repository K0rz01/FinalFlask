import mysql.connector
from mysql.connector import Error
import logging
from config import DB_CONFIG, ERROR_MESSAGES
import traceback

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Establece una conexión con la base de datos MySQL.
    Retorna la conexión o None si hay un error.
    """
    try:
        logger.info(f"Intentando conectar a la base de datos: {DB_CONFIG['database']}")
        logger.debug(f"Configuración de conexión: {DB_CONFIG}")
        
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            logger.info(f"Conexión exitosa a MySQL (versión {db_info})")
            return connection
        else:
            logger.error("No se pudo establecer la conexión")
            return None
            
    except mysql.connector.Error as err:
        logger.error(f"Error de MySQL: {err}")
        logger.error(f"Error code: {err.errno}")
        logger.error(f"SQLSTATE: {err.sqlstate}")
        logger.error(f"Error message: {err.msg}")
        if err.errno == 2003:
            logger.error("No se puede conectar al servidor MySQL. Verifique que el servidor esté en ejecución.")
        elif err.errno == 1045:
            logger.error("Error de autenticación. Verifique las credenciales.")
        elif err.errno == 1049:
            logger.error("Base de datos no existe.")
        return None
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None

def execute_query(query, params=None, fetch=True):
    """
    Ejecuta una consulta SQL y retorna los resultados.
    """
    connection = None
    cursor = None
    try:
        logger.info("Intentando establecer conexión a la base de datos...")
        connection = get_db_connection()
        if not connection:
            logger.error("No se pudo establecer conexión con la base de datos")
            return None
            
        logger.info("Conexión establecida, creando cursor...")
        cursor = connection.cursor(dictionary=True)
        
        # Log de la consulta y parámetros
        logger.info(f"Ejecutando query: {query}")
        logger.info(f"Parámetros: {params}")
        
        cursor.execute(query, params or ())
        logger.info("Query ejecutada exitosamente")
        
        if fetch:
            logger.info("Obteniendo resultados...")
            result = cursor.fetchall()
            logger.info(f"Resultados obtenidos: {len(result)} registros")
            return result
        else:
            logger.info("Committing cambios...")
            connection.commit()
            logger.info(f"Query ejecutado exitosamente. Rows affected: {cursor.rowcount}")
            return True
            
    except mysql.connector.Error as e:
        logger.error(f"Error de MySQL al ejecutar query: {str(e)}")
        logger.error(f"Query: {query}")
        logger.error(f"Parámetros: {params}")
        logger.error(f"Código de error: {e.errno}")
        logger.error(f"SQL State: {e.sqlstate}")
        if connection:
            logger.error(f"Estado de la conexión: {'Conectado' if connection.is_connected() else 'Desconectado'}")
        return None
        
    except Exception as e:
        logger.error(f"Error inesperado al ejecutar query: {str(e)}")
        logger.error(f"Query: {query}")
        logger.error(f"Parámetros: {params}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None
        
    finally:
        if cursor:
            cursor.close()
            logger.info("Cursor cerrado")
        if connection and connection.is_connected():
            connection.close()
            logger.info("Conexión cerrada")
