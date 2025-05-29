from database import get_db_connection

def test_connection():
    connection = get_db_connection()
    if connection:
        print("Conexión a la base de datos exitosa.")
        connection.close()
    else:
        print("Error al conectar a la base de datos.")

if __name__ == "__main__":
    test_connection()
