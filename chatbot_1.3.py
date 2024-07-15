import time
import streamlit as st
import vanna as vn
from vanna.remote import VannaDefault
import psycopg2
from psycopg2 import OperationalError

# Configuración de la página de Streamlit para usar un diseño ancho
st.set_page_config(layout="wide")

from llamadas_1_3 import (
    create_connection,
    generate_questions_cached,
    generate_sql_cached,
    run_sql_cached,
    generate_plotly_code_cached,
    generate_plot_cached,
    #generate_followup_cached,
    should_generate_chart_cached,
    is_sql_valid_cached,
    generate_summary_cached, setup_vanna
)

avatar_url = "S3comLogo.png"

# Inicialización del historial de mensajes
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola! Puedes hacerme una pregunta", "avatar": avatar_url}]

# Sidebar de configuración de salida
st.sidebar.title("Configuración de salida")
st.sidebar.checkbox("Mostrar código SQL", value=True, key="show_sql")
st.sidebar.checkbox("Mostrar tabla", value=True, key="show_table")
st.sidebar.checkbox("Mostrar código Plotly", value=True, key="show_plotly_code")
st.sidebar.checkbox("Mostrar cuadro", value=True, key="show_chart")
st.sidebar.checkbox("Mostrar resumen", value=True, key="show_summary")
st.sidebar.button("Limpiar opciones", on_click=lambda: set_question(None), use_container_width=True)

# Título de la app
st.title("Chatbot con Vanna.AI")

# Función para establecer la pregunta en el session_state
def set_question(question):
    st.session_state["my_question"] = question

# Mostrar el historial de mensajes
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        message_slot = st.chat_message("assistant", avatar=msg["avatar"])
        if isinstance(msg["content"], str):
            message_slot.write(msg["content"])
        elif isinstance(msg["content"], dict):
            if msg["content"].get("type") == "table":
                message_slot.dataframe(msg["content"]["data"])
            elif msg["content"].get("type") == "plot":
                message_slot.plotly_chart(msg["content"]["data"])
            elif msg["content"].get("type") == "code":
                message_slot.code(msg["content"]["data"], language=msg["content"].get("language", "python"))
    else:
        message_slot = st.chat_message(msg["role"])
        message_slot.write(msg["content"])

# Obtención de la pregunta actual
my_question = st.session_state.get("my_question", default=None)

# Si no hay pregunta, muestra un campo de entrada de chat para ingresar una pregunta
if my_question is None:
    my_question = st.chat_input("Házme una pregunta ...")

# Procesa la pregunta
if my_question:
    st.session_state["my_question"] = my_question
    user_message = st.chat_message("user")
    user_message.write(f"{my_question}")
    st.session_state.messages.append({"role": "user", "content": my_question})

    vn = setup_vanna()    

    sql = generate_sql_cached(question=my_question)

    if sql:
        if is_sql_valid_cached(sql=sql): # Verifica si la consulta SQL generada es válida
            if st.session_state.get("show_sql", True):
                assistant_message_sql = st.chat_message("assistant", avatar=avatar_url)
                assistant_message_sql.code(sql, language="sql", line_numbers=True)
                st.session_state.messages.append({"role": "assistant", "content": {"type": "code", "data": sql, "language": "sql"}, "avatar": avatar_url})
            # Ejecuta la consulta SQL y obtiene los resultados en un DataFrame
            connection = create_connection()
            df = run_sql_cached(sql=sql)

            if df is not None:
                st.session_state["df"] = df
            
            # Muestra la tabla de resultados si está habilitado en la configuración
            if st.session_state.get("df") is not None:
                if st.session_state.get("show_table", True):
                    df = st.session_state.get("df")
                    assistant_message_table = st.chat_message("assistant", avatar=avatar_url)
                    if len(df) > 10:
                        assistant_message_table.text("First 10 rows of data")
                        assistant_message_table.dataframe(df.head(10))
                        st.session_state.messages.append({"role": "assistant", "content": {"type": "table", "data": df.head(10)}, "avatar": avatar_url})
                    else:
                        assistant_message_table.dataframe(df)
                        st.session_state.messages.append({"role": "assistant", "content": {"type": "table", "data": df}, "avatar": avatar_url})

                # Verifica si se debe generar un gráfico
                if should_generate_chart_cached(question=my_question, sql=sql, df=df):
                    code = generate_plotly_code_cached(question=my_question, sql=sql, df=df)

                    # Muestra el código de Plotly si está habilitado en la configuración
                    if st.session_state.get("show_plotly_code", False):
                        assistant_message_plotly_code = st.chat_message("assistant", avatar=avatar_url)
                        assistant_message_plotly_code.code(code, language="python", line_numbers=True)
                        st.session_state.messages.append({"role": "assistant", "content": {"type": "code", "data": code, "language": "python"}, "avatar": avatar_url})

                    # Genera y muestra el gráfico si el código de Plotly no está vacío
                    if code is not None and code != "":
                        if st.session_state.get("show_chart", True):
                            assistant_message_chart = st.chat_message("assistant", avatar=avatar_url)
                            fig = generate_plot_cached(code=code, df=df)
                            if fig is not None:
                                assistant_message_chart.plotly_chart(fig)
                                st.session_state.messages.append({"role": "assistant", "content": {"type": "plot", "data": fig}, "avatar": avatar_url})
                            else:
                                assistant_message_chart.error("No puedo generar el gráfico")
                                st.session_state.messages.append({"role": "assistant", "content": "No puedo generar el gráfico", "avatar": avatar_url})

                # Genera y muestra un resumen de los resultados si está habilitado en la configuración
                if st.session_state.get("show_summary", True):
                    assistant_message_summary = st.chat_message("assistant", avatar=avatar_url)
                    summary = generate_summary_cached(question=my_question, df=df)
                    if summary is not None:
                        assistant_message_summary.text(summary)
                        st.session_state.messages.append({"role": "assistant", "content": summary, "avatar": avatar_url})
     
        else:
            assistant_message = st.chat_message("assistant", avatar=avatar_url)
            assistant_message.write(sql)
            st.session_state.messages.append({"role": "assistant", "content": sql, "avatar": avatar_url})

    else:
        assistant_message_error = st.chat_message("assistant", avatar=avatar_url)
        assistant_message_error.error("No puedo responder a esa pregunta. Por favor, intenta con otra pregunta.")
        st.session_state.messages.append({"role": "assistant", "content": "No puedo responder a esa pregunta. Por favor, intenta con otra pregunta.", "avatar": avatar_url})

# Asegurarse de que el usuario pueda ingresar nuevas preguntas
st.session_state["my_question"] = None
