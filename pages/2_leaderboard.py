import streamlit as st
import pandas as pd


st.title("AML Assignment 1")
col1, col2 = st.columns(2)
with col1:
    st.info("Accuracy")
    classifica_accuracy = pd.read_csv("classifica_accuracy.csv", index_col=False, header=0)
    st.dataframe(classifica_accuracy)

with col2:
    st.info("F1-Score")
    classifica_f1 = pd.read_csv("classifica_f1.csv", index_col=False, header=0)
    st.dataframe(classifica_f1)
