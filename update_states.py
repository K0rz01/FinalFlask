import mysql.connector
from config import DB_CONFIG

def update_states():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Estandarizar los estados
        updates = [
            "UPDATE ordenes_servicio SET estado = 'REPARADO' WHERE estado = 'REPARADADO'",
            "UPDATE ordenes_servicio SET estado = 'PENDIENTE' WHERE estado = 'Pendiente por revision' OR estado IS NULL",
            "UPDATE ordenes_servicio SET estado = 'NO REPARADO' WHERE estado = 'INDETERMINADO'",
            "UPDATE ordenes_servicio SET estado = 'EN REVISION' WHERE estado = 'FALTA PRUEBA DE CARGA'"
        ]

        for query in updates:
            cursor.execute(query)
            print(f"Ejecutado: {query}")
            print(f"Filas afectadas: {cursor.rowcount}")

        # Confirmar los cambios
        connection.commit()
        print("\nCambios guardados exitosamente")

        # Verificar estados únicos después de la actualización
        cursor.execute("SELECT DISTINCT estado FROM ordenes_servicio")
        estados = cursor.fetchall()
        print("\nEstados únicos después de la actualización:")
        print([estado[0] for estado in estados])

    except mysql.connector.Error as error:
        print(f"Error al actualizar estados: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    update_states()
