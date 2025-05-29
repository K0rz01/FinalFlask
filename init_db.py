import mysql.connector
from mysql.connector import Error
import os
import logging
from config import DB_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_sql_file(cursor, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sql_file = f.read()
            # Dividir el archivo en comandos individuales
            sql_commands = sql_file.split(';')
            
            for command in sql_commands:
                # Ignorar líneas vacías y comentarios
                if command.strip() and not command.strip().startswith('--'):
                    try:
                        cursor.execute(command)
                        logger.info(f"Comando ejecutado exitosamente")
                    except Error as e:
                        logger.error(f"Error ejecutando comando: {e}")
                        
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {filename}")
    except Exception as e:
        logger.error(f"Error leyendo archivo {filename}: {e}")

def init_database():
    try:
        # Conectar a MySQL sin especificar la base de datos
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        
        cursor = connection.cursor()
        
        # Crear la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
        cursor.execute(f"USE `{DB_CONFIG['database']}`")
        
        # Leer y ejecutar el archivo SQL
        with open('bd/tecnocomputer_user.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
            
        # Ejecutar cada comando SQL
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        logger.info("Base de datos inicializada correctamente")
        
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    init_database()
