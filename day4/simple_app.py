import streamlit as st
st.title("Welcome to my first app")
st.header("Information")
name=st.text_input("Enter your first name")
surname=st.text_input("Enter your last name")
gender=st.radio("Select your gender",["Male","Female"])
if st.button("submit"):
    st.write("Hello", name, surname, "You are", gender)

if st.chat_message(""):
    st.chat_message("assistant").write("Hello! How can I assist you today?")