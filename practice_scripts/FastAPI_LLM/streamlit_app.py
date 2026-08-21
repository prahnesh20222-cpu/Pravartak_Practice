import streamlit as st
import httpx

endpoint = 'http://localhost:8000/chat'
params = {}

message_input = st.text_input("Enter your message: ")
temperature = st.text_input("Enter required temperature: ")
retries = st.text_input("Enter Retries: ")
timeout = st.text_input("Enter timeout: ")


if st.button("Run query"):
    body = {
  "query": message_input,
  "temp": float(temperature),
  "retries": int(retries),
  "timeout": int(timeout)
}

    try:
        #We are calling an API endpoint we created. This might call an llm in the backend. It can also be a simple python tool
        with httpx.Client() as client:
            response = client.post(endpoint, params=params, json=body)
            st.write(response.json())

    except Exception as e:
        st.write(f"Error occured as {e}")