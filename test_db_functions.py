from database import get_db_connection, execute_query

def test_db_functions():
    print("Probando conexión a la base de datos...")
    connection = get_db_connection()
    if connection:
        print("Conexión establecida correctamente.")
        connection.close()
    else:
        print("No se pudo establecer la conexión.")
        return

    print("Probando ejecución de consulta: SHOW TABLES;")
    result = execute_query("SHOW TABLES;")
    if result is not None:
        print(f"Consulta ejecutada correctamente. Tablas encontradas: {len(result)}")
        for row in result:
            print(row)
    else:
        print("Error al ejecutar la consulta.")

if __name__ == "__main__":
    test_db_functions()
