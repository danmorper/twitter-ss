import streamlit as st
import pandas as pd
import openai
import os
import time

# Inicializar OpenAI con la API KEY
# Load API key from environment variable
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]
# Initialize the OpenAI client with your API key
openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=openai.api_key)

st.title("Bot información Semana Santa")

# Corregir 'assitant' a 'assistant'
if "assistant" not in st.session_state:
    st.session_state.assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
    
if "thread" not in st.session_state:
    st.session_state.thread = client.beta.threads.create()
    # Create initial message
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content="Hola, preguntame algo sobre la Semana Santa 😁"
    )

if prompt := st.chat_input("Escribe tu pregunta"):
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )
    # Get assistant response
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant.id
    )

    with st.spinner("Pensando..."):
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            time.sleep(1)
    
    # Retrieve messages from the thread
try:
    messages = client.beta.threads.messages.list(thread_id=st.session_state.thread.id).data
    for message in reversed(messages):
        role = message.role  # 'user' o 'assistant'
        content = message.content[0].text.value  # El contenido del mensaje
        with st.chat_message(role):
            st.markdown(content)
except Exception as e:
    st.error("Error al recuperar mensajes: {}".format(e))

# Quién toca en Jerez de la Frontera?