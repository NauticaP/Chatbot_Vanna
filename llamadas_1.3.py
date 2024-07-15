import streamlit as st
from vanna.remote import VannaDefault
import psycopg2
from psycopg2 import OperationalError
import vanna as vn



@st.cache_resource(ttl=3600)
def create_connection(db_name="database", db_user="user", db_password="password", db_host="host", db_port="port"):
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



#La función está decorada con @st.cache_resource(ttl=3600), lo que significa que los resultados se cachearán durante una hora para mejorar el rendimiento.

@st.cache_resource(ttl=3600)
def setup_vanna():
    api_key = 'api_key'
    model = 'Vanna model'

    # Crea la conexion a la base de datos usando psycopg2
    connection = create_connection()

    if connection is not None:

        # Configuramos Vanna con la clave API y el modelo
        vn = VannaDefault(api_key=api_key, model=model)

        try:
            
            # Extrae los parámetros de la conexión para pasar a Vanna
            conn_info = connection.get_dsn_parameters()
            vn.connect_to_postgres(host=conn_info['host'], dbname=conn_info['dbname'], user=conn_info['user'], password='1234', port=conn_info['port'])
            print("Vanna connected successfully to the database")
            
        except Exception as e:
            print(f"Error connecting Vanna to the database: {e}")
        
        finally:
            connection.close()
        return vn
    
    else:
        print("Failed to connect to PostgreSQL. Vanna aborted.")
        return None


# Genera preguntas de muestra utilizando la instancia de Vanna.
# Cachea los datos generados para optimizar el rendimiento, mostrando un spinner con el mensaje "Generating sample questions ..."

@st.cache_data(show_spinner="Generando preguntas de muestra...")
def generate_questions_cached():
    vn = setup_vanna()
    return vn.generate_questions()


# Entrenamos el modelo de Vanna con una pregunta y una consulta SQL específica.
# Genera una consulta SQL a partir de una pregunta en lenguaje natural.
# También cachea los resultados, mostrando un spinner con el mensaje "Generating SQL query ..."

vn = setup_vanna()
vn.train(ddl="CREATE TABLE productos2 (id int primary key, productoName varchar(255), category varchar(255), price decimal(18,2), ranting decimal(18,2), numreviews int, stockquantity int, ciscount decimal(18,2), sales decimal(18,2), dateadded date);")
vn.train(question="Muestrame detalle de los headphones",sql=f"""SELECT * FROM productos2 WHERE productoname = 'Headphones'""")
vn.train(question="Muestra las laptops añadidas en fecha del 2023", sql=f"""SELECT * FROM productos2 WHERE productname = 'Laptop' AND dateadded >= '2023-01-01' AND dateadded <= '2023-12-31';""")
vn.train(question="Muestra el producto mejor calificado por categoría", sql=f"""SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY ranting DESC) AS rn FROM productos2) ranked WHERE rn = 1;""")


@st.cache_data(show_spinner="Generando consulta SQL...")
def generate_sql_cached(question: str):
    vn = setup_vanna()
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)
    

#Verifica si una consulta SQL es válida.
#Cachea los resultados y muestra un spinner con el mensaje "Checking for valid SQL ...".
@st.cache_data(show_spinner="Chequeando si la consulta SQL es válida...")
def is_sql_valid_cached(sql: str):
    vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)


#Ejecuta una consulta SQL y retorna los resultados.
#Cachea los resultados y muestra un spinner con el mensaje "Running SQL query ...".
@st.cache_data(show_spinner="Corriendo la consulta SQL...")
def run_sql_cached(sql: str):
    vn = setup_vanna()
    return vn.run_sql(sql=sql)


#Determina si se debe generar un gráfico basado en los resultados de una consulta SQL.
#Cachea la decisión y muestra un spinner con el mensaje "Checking if we should generate a chart ...".
@st.cache_data(show_spinner="Chequeando si debemos generar un gráfico...")
def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)


#Genera el código necesario para crear un gráfico con Plotly basado en una consulta SQL y sus resultados.
#Cachea el código generado y muestra un spinner con el mensaje "Generating Plotly code ...".
@st.cache_data(show_spinner="Generando código Plotly...")
def generate_plotly_code_cached(question, sql, df):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


#Ejecuta el código de Plotly para generar un gráfico y retorna la figura resultante.
#Cachea la figura y muestra un spinner con el mensaje "Running Plotly code ...".
@st.cache_data(show_spinner="Corriendo el código Plotly...")
def generate_plot_cached(code, df):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)


#Genera preguntas de seguimiento basadas en la pregunta original, la consulta SQL y los resultados.
#Cachea las preguntas generadas y muestra un spinner con el mensaje "Generating followup questions ...".
#@st.cache_data(show_spinner="Generando preguntas de seguimiento...")
#def generate_followup_cached(question, sql, df):
#    vn = setup_vanna()
#    return vn.generate_followup_questions(question=question, sql=sql, df=df, num_questions=3, language="es")


#Genera un resumen basado en la pregunta original y los resultados de la consulta.
#Cachea el resumen y muestra un spinner con el mensaje "Generating summary ...".
@st.cache_data(show_spinner="Generando resumen...")
def generate_summary_cached(question, df):
    vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)