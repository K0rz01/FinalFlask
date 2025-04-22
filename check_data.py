import mysql.connector
from config import DB_CONFIG
import json

def check_database():
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        # Verificar tabla ordenes_servicio
        print("\nVerificando tabla ordenes_servicio:")
        cursor.execute("SELECT COUNT(*) as count FROM ordenes_servicio")
        count = cursor.fetchone()
        print(f"Total de registros: {count['count']}")
        
        # Mostrar algunos registros de ejemplo
        print("\nPrimeros 3 registros de ordenes_servicio:")
        cursor.execute("""
            SELECT 
                idordenes_servicio,
                marca,
                modelo,
                serial,
                estado,
                fecha_entrada,
                fecha_salida,
                id_cliente
            FROM ordenes_servicio 
            LIMIT 3
        """)
        records = cursor.fetchall()
        print(json.dumps(records, indent=2, default=str))
        
        # Verificar estados únicos
        print("\nEstados únicos en ordenes_servicio:")
        cursor.execute("SELECT DISTINCT estado FROM ordenes_servicio")
        estados = cursor.fetchall()
        print(json.dumps([r['estado'] for r in estados], indent=2))
        
        # Verificar tabla clientes
        print("\nVerificando tabla clientes:")
        cursor.execute("SELECT COUNT(*) as count FROM clientes")
        count = cursor.fetchone()
        print(f"Total de registros: {count['count']}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error al verificar la base de datos: {str(e)}")

if __name__ == "__main__":
    check_database()
