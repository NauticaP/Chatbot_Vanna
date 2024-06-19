import streamlit as st
from vanna.remote import VannaDefault


#Esta función configura y retorna una instancia de VannaDefault.
#Usa la clave API almacenada en st.secrets para autenticarse.
#Conecta a una base de datos SQLite alojada en una URL específica.
#La función está decorada con @st.cache_resource(ttl=3600), lo que significa que los resultados se cachearán durante una hora para mejorar el rendimiento.
@st.cache_resource(ttl=3600)
def setup_vanna():
    api_key = '0cc56619601643e1b3831519a35abdc5'
    vn = VannaDefault(api_key=api_key, model='nauticap')
    vn.connect_to_postgres(host='localhost', dbname='Crimen_Car_Security', user='postgres', password='1234', port='5432')
    return vn


#Genera preguntas de muestra utilizando la instancia de Vanna.
#Cachea los datos generados para optimizar el rendimiento, mostrando un spinner con el mensaje "Generating sample questions ...".
@st.cache_data(show_spinner="Generating sample questions ...")
def generate_questions_cached():
    vn = setup_vanna()
    return vn.generate_questions()


#Genera una consulta SQL a partir de una pregunta en lenguaje natural.
#También cachea los resultados, mostrando un spinner con el mensaje "Generating SQL query ...".
@st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(question: str):
    vn = setup_vanna()
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)


#Verifica si una consulta SQL es válida.
#Cachea los resultados y muestra un spinner con el mensaje "Checking for valid SQL ...".
@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(sql: str):
    vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)


#Ejecuta una consulta SQL y retorna los resultados.
#Cachea los resultados y muestra un spinner con el mensaje "Running SQL query ...".
@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(sql: str):
    vn = setup_vanna()
    return vn.run_sql(sql=sql)


#Determina si se debe generar un gráfico basado en los resultados de una consulta SQL.
#Cachea la decisión y muestra un spinner con el mensaje "Checking if we should generate a chart ...".
@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)


#Genera el código necesario para crear un gráfico con Plotly basado en una consulta SQL y sus resultados.
#Cachea el código generado y muestra un spinner con el mensaje "Generating Plotly code ...".
@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(question, sql, df):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


#Ejecuta el código de Plotly para generar un gráfico y retorna la figura resultante.
#Cachea la figura y muestra un spinner con el mensaje "Running Plotly code ...".
@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(code, df):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)


#Genera preguntas de seguimiento basadas en la pregunta original, la consulta SQL y los resultados.
#Cachea las preguntas generadas y muestra un spinner con el mensaje "Generating followup questions ...".
@st.cache_data(show_spinner="Generating followup questions ...")
def generate_followup_cached(question, sql, df):
    vn = setup_vanna()
    return vn.generate_followup_questions(question=question, sql=sql, df=df)


#Genera un resumen basado en la pregunta original y los resultados de la consulta.
#Cachea el resumen y muestra un spinner con el mensaje "Generating summary ...".
@st.cache_data(show_spinner="Generating summary ...")
def generate_summary_cached(question, df):
    vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)