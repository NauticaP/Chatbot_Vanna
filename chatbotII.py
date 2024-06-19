import time
import streamlit as st
#from code_editor import code_editor
from llamadasIII import (
    generate_questions_cached,
    generate_sql_cached,
    run_sql_cached,
    generate_plotly_code_cached,
    generate_plot_cached,
    generate_followup_cached,
    should_generate_chart_cached,
    is_sql_valid_cached,
    generate_summary_cached
)

avatar_url = "S3comLogo.png"


#Configuración de la página de Streamlit para usar un diseño ancho
st.set_page_config(layout="wide")


#Mensaje del asistente con un botón para mostrar preguntas sugeridas
#Se establecen varias opciones de salida que el usuario puede activar o desactivar (mostrar SQL, tabla, código de Plotly, gráfico, resumen y preguntas de seguimiento).
st.sidebar.title("Output Settings")
st.sidebar.checkbox("Show SQL", value=True, key="show_sql")
st.sidebar.checkbox("Show Table", value=True, key="show_table")
st.sidebar.checkbox("Show Plotly Code", value=True, key="show_plotly_code")
st.sidebar.checkbox("Show Chart", value=True, key="show_chart")
st.sidebar.checkbox("Show Summary", value=True, key="show_summary")
st.sidebar.checkbox("Show Follow-up Questions", value=True, key="show_followup")
st.sidebar.button("Reset", on_click=lambda: set_question(None), use_container_width=True)


#Título de la app
st.title("Chatbot con Vanna AI")
# st.sidebar.write(st.session_state)


#Función para establecer la pregunta en el session_state
def set_question(question):
    st.session_state["my_question"] = question


#Muestra un mensaje del asistente con un botón para mostrar preguntas sugeridas.
#Si se presiona el botón, se obtienen y muestran preguntas sugeridas.
assistant_message_suggested = st.chat_message(
    "assistant", avatar=avatar_url
)
if assistant_message_suggested.button("Click to show suggested questions"):
    st.session_state["my_question"] = None
    questions = generate_questions_cached()
    for i, question in enumerate(questions):
        time.sleep(0.05)
        button = st.button(
            question,
            on_click=set_question,
            args=(question,),
        )


#Obtención de la pregunta actual
my_question = st.session_state.get("my_question", default=None)


#Si no hay pregunta, muestra un campo de entrada de chat para ingresar una pregunta
if my_question is None:
    my_question = st.chat_input(
        "Ask me a question about your data",
    )

#Procesa la pregunta
if my_question:
    st.session_state["my_question"] = my_question
    user_message = st.chat_message("user")
    user_message.write(f"{my_question}")

    sql = generate_sql_cached(question=my_question)

    if sql:
        if is_sql_valid_cached(sql=sql): # Verifica si la consulta SQL generada es válida
            if st.session_state.get("show_sql", True):
                assistant_message_sql = st.chat_message(
                    "assistant", avatar=avatar_url
                )
                assistant_message_sql.code(sql, language="sql", line_numbers=True)
        else:
            assistant_message = st.chat_message(
                "assistant", avatar=avatar_url
            )
            assistant_message.write(sql)
            st.stop()


        #Ejecuta la consulta SQL y obtiene los resultados en un DataFrame
        df = run_sql_cached(sql=sql)

        if df is not None:
            st.session_state["df"] = df


        #Muestra la tabla de resultados si está habilitado en la configuración
        if st.session_state.get("df") is not None:
            if st.session_state.get("show_table", True):
                df = st.session_state.get("df")
                assistant_message_table = st.chat_message(
                    "assistant",
                    avatar=avatar_url,
                )
                if len(df) > 10:
                    assistant_message_table.text("First 10 rows of data")
                    assistant_message_table.dataframe(df.head(10))
                else:
                    assistant_message_table.dataframe(df)


            #Verifica si se debe generar un gráfico
            if should_generate_chart_cached(question=my_question, sql=sql, df=df):
                code = generate_plotly_code_cached(question=my_question, sql=sql, df=df)


                #Muestra el código de Plotly si está habilitado en la configuración
                if st.session_state.get("show_plotly_code", False):
                    assistant_message_plotly_code = st.chat_message(
                        "assistant",
                        avatar=avatar_url,
                    )
                    assistant_message_plotly_code.code(
                        code, language="python", line_numbers=True
                    )


                #Genera y muestra el gráfico si el código de Plotly no está vacío
                if code is not None and code != "":
                    if st.session_state.get("show_chart", True):
                        assistant_message_chart = st.chat_message(
                            "assistant",
                            avatar=avatar_url,
                        )
                        fig = generate_plot_cached(code=code, df=df)
                        if fig is not None:
                            assistant_message_chart.plotly_chart(fig)
                        else:
                            assistant_message_chart.error("I couldn't generate a chart")


            #Genera y muestra un resumen de los resultados si está habilitado en la configuración
            if st.session_state.get("show_summary", True):
                assistant_message_summary = st.chat_message(
                    "assistant",
                    avatar=avatar_url,
                )
                summary = generate_summary_cached(question=my_question, df=df)
                if summary is not None:
                    assistant_message_summary.text(summary)


            #Genera y muestra preguntas de seguimiento si está habilitado en la configuración
            if st.session_state.get("show_followup", True):
                assistant_message_followup = st.chat_message(
                    "assistant",
                    avatar=avatar_url,
                )
                followup_questions = generate_followup_cached(
                    question=my_question, sql=sql, df=df
                )
                st.session_state["df"] = None

                if len(followup_questions) > 0:
                    assistant_message_followup.text(
                        "Here are some possible follow-up questions"
                    )
                    #Muestra las primeras 5 preguntas de seguimiento
                    for question in followup_questions[:5]:
                        assistant_message_followup.button(question, on_click=set_question, args=(question,))


    #Si no se puede generar una consulta SQL para la pregunta, muestra un mensaje de error.
    else:
        assistant_message_error = st.chat_message(
            "assistant", avatar=avatar_url
        )
        assistant_message_error.error("I wasn't able to generate SQL for that question")