import streamlit as st
from scrape import steal
st.title("SQLote")
url = st.text_input("Enter a Website URL: ")

if st.button("Sacame del bolsillo"):
    st.write("El hackeo comienza...")
    result = steal(url)
    print(result)