import mysql.connector
from mysql.connector import Error

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678'
}

def setup_database():
    connection = None
    try:
        # Conectar con las credenciales existentes
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS `tecno-computer`")
        
        # Usar la base de datos
        cursor.execute("USE `tecno-computer`")

        # Crear tablas si no existen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cliente_id varchar(50) NOT NULL,
                first_name varchar(50) NOT NULL,
                last_name varchar(50) NOT NULL,
                email varchar(100) NOT NULL,
                phone_number varchar(20) DEFAULT NULL,
                street_address varchar(100) DEFAULT NULL,
                city varchar(50) DEFAULT NULL,
                state varchar(50) DEFAULT NULL,
                postal_code varchar(10) DEFAULT NULL,
                country varchar(50) DEFAULT NULL,
                gender varchar(10) DEFAULT NULL,
                registration_date datetime DEFAULT CURRENT_TIMESTAMP,
                account_status varchar(20) DEFAULT 'active',
                notes text,
                contact_preferences varchar(50) DEFAULT NULL,
                referred_by varchar(50) DEFAULT NULL,
                customer_type varchar(20) DEFAULT NULL,
                PRIMARY KEY (cliente_id),
                UNIQUE KEY email (email)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ordenes_servicio (
                idordenes_servicio int NOT NULL AUTO_INCREMENT,
                marca varchar(45) DEFAULT NULL,
                modelo varchar(45) DEFAULT NULL,
                serial varchar(45) DEFAULT NULL,
                diag_inicial varchar(500) DEFAULT NULL,
                diag_final varchar(500) DEFAULT NULL,
                serial_ram_1 varchar(45) DEFAULT NULL,
                serial_ram_2 varchar(45) DEFAULT NULL,
                serial_disco_1 varchar(45) DEFAULT NULL,
                serial_disco_2 varchar(45) DEFAULT NULL,
                serial_cargador varchar(45) DEFAULT NULL,
                serial_bateria varchar(45) DEFAULT NULL,
                fecha_entrada datetime DEFAULT CURRENT_TIMESTAMP,
                fecha_salida datetime DEFAULT NULL,
                id_cliente bigint DEFAULT NULL,
                inicio_trabajo datetime DEFAULT NULL,
                fin_trabajo datetime DEFAULT NULL,
                estado varchar(45) DEFAULT NULL,
                id_tecnico varchar(45) DEFAULT NULL,
                PRIMARY KEY (idordenes_servicio)
            )
        """)

        print("Base de datos y tablas creadas exitosamente")
        connection.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_database()
