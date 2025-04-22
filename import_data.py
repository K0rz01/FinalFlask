import mysql.connector
from config import DB_CONFIG
import os
import logging

logging.basicConfig(level=logging.INFO)

def execute_sql_file(connection, file_path):
    try:
        cursor = connection.cursor()
        
        # Leer el archivo SQL
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_commands = file.read()
            
        # Ejecutar los comandos SQL
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        for command in sql_commands.split(';'):
            if command.strip():
                cursor.execute(command + ';')
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        
        connection.commit()
        logging.info(f"Archivo SQL importado exitosamente: {file_path}")
        
    except Exception as e:
        logging.error(f"Error al importar archivo SQL {file_path}: {str(e)}")
        connection.rollback()
    finally:
        cursor.close()

def import_all_data():
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        
        # Lista de archivos SQL a importar
        sql_files = [
            'bd/tecnocomputer_clientes.sql',
            'bd/tecnocomputer_ordenes_servicio.sql'
        ]
        
        # Importar cada archivo
        for sql_file in sql_files:
            if os.path.exists(sql_file):
                execute_sql_file(connection, sql_file)
            else:
                logging.error(f"Archivo no encontrado: {sql_file}")
        
    except Exception as e:
        logging.error(f"Error de conexión: {str(e)}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    import_all_data()
