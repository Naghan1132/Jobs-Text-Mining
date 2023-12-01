import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Ma première application Streamlit")

# Contenu de l'application
st.write("Bienvenue sur ma première application Streamlit!")

# Read the CSV file
df = pd.read_csv("../data/indeed.csv")

# Display the head of the CSV on Streamlit
st.write(df.head())



