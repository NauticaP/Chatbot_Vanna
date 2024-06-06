# Chatbot con Vanna AI

Este chatbot interactivo permite a los usuarios hacer preguntas sobre sus datos y obtener respuestas utilizando consultas SQL. Puedes configurar qué elementos deseas mostrar en las respuestas, como el código SQL, tablas de datos, código de Plotly para gráficos, gráficos generados, resúmenes de datos y preguntas de seguimiento. La base de datos es enviada a la app mediante una URL.

## Requisitos

- Python 3.7 o superior
- pip

## Instalación

  1. Crea un entorno virtual:
  ```bash
  python -m venv venv
  source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
  ```
  2. Instala las dependencias:
  ```bash
  pip install streamlit
  ```
  ```bash
  pip install vanna
  ```

## Uso

  1. Ejecuta la aplicación:  
  ```bash
  streamlit run chatbot_vanna.py
  ```
  2. Ingresa una pregunta sobre tus datos en el campo de chat.

  3. Personaliza las opciones de salida en la barra lateral según tus preferencias.

  4. Recibe respuestas interactivas que incluyen SQL generado, tablas de datos, gráficos, resúmenes y preguntas de seguimiento.

## Archivos

- `chatbot_vanna.py`: El script principal que configura y ejecuta la aplicación de chatbot.
- `llamadas_vanna.py`: Este código crea el chatbot interactivo que utiliza la librería Vanna para generar preguntas y consultas SQL a partir de preguntas en lenguaje natural sobre datos alojados en una base de datos SQLite.
- `vanna_api_key.py`: Contiene las funciones para invocar la solicitud de la API key.
