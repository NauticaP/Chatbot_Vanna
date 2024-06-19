import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name="Crimen_Car_Security", db_user="postgres", db_password="1234", db_host="localhost", db_port="5432"):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

# Reemplaza con tus credenciales
connection = create_connection(
    "Crimen_Car_Security", "postgres", "1234"
)

# Crear un cursor
#cur = connection.cursor()

# Realizar una consulta
#try:
#    cur.execute("SELECT * FROM data_car_security WHERE "YEAR" = 2020;")  # Reemplaza con tu consulta SQL
    #cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'data_car_security';")  # Reemplaza con tu consulta SQL
#    resultados = cur.fetchall()
    
    # Imprimir los resultados
#    for fila in resultados:
#        print(fila)
#except Exception as e:
#    print(f"Error al ejecutar la consulta: {e}")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        cursor.close()

connection = create_connection()
query = 'SELECT * FROM data_car_security WHERE "YEAR" = 2020;'
result = execute_query(connection, query)
print(result)

# Cerrar el cursor y la conexión
#cursor.close()
connection.close()
