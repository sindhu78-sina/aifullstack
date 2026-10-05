import ollama
import streamlit as st
st.title("Welcome To My UiBot!")
st.markdown("This is a simple chatbot built with Streamlit and Ollama.")
if "messages" not in st.session_state:
    st.session_state.messages=[]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
question=st.chat_input("Send a chat:")
if question:
    with st.chat_message("user"):
        st.write("You:",question)
    st.session_state.messages.append(
            {
                "role":"user",
                "content":question
            }
            )
    response=ollama.chat(
        model="llama3.2:3b",
        messages=st.session_state.messages
        )
    st.session_state.messages.append(
            {
            "role":"assistant",
            "content":response["message"]["content"]
            }
        )
    with st.chat_message("assistant"):
        st.write("AI:",response["message"]["content"])
        