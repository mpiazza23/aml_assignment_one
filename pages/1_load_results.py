import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from sklearn.metrics import accuracy_score, f1_score
import datetime

st.title("AML Assignment 1")

name = st.text_input("Insert your name:")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if 'df' not in st.session_state:
    st.session_state.df = None

if uploaded_file is not None:
    timestamp = datetime.datetime.now()
    if name == "":
        st.error("Name not inserted!")
        st.rerun()
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df

    st.write("Check CSV file:")
    st.dataframe(df)

    if st.button("Confirm CSV file"):
        conn = st.connection("assignment_one", type=GSheetsConnection)
        true_labels = conn.read()
        if len(true_labels) != len(df):
            st.error("The length of the uploaded file is not correct")
        else:
            accuracy = accuracy_score(true_labels, df)
            f1 = f1_score(true_labels, df)
            col1, col2 = st.columns(2)
            with col1:
                st.info("Accuracy = "+str(accuracy))
                classifica_accuracy = pd.read_csv("classifica_accuracy.csv", index_col=False, header=0)
                classifica_accuracy['Timestamp'] = pd.to_datetime(classifica_accuracy['Timestamp'])
                row = {'Student':name, "Accuracy":accuracy, "Timestamp":timestamp}
                classifica_accuracy = pd.concat([classifica_accuracy, pd.DataFrame([row])], ignore_index=True)
                #classifica_accuracy = classifica_accuracy.append(row, ignore_index=True)
                classifica_accuracy = classifica_accuracy.sort_values(['Accuracy'], ascending=[False])
                classifica_accuracy = classifica_accuracy.sort_values(['Timestamp'], ascending=[True])
                classifica_accuracy = classifica_accuracy.reset_index(drop=True)
                classifica_accuracy.to_csv("classifica_accuracy.csv", index=False)
                st.write("First 10 positions")
                st.dataframe(classifica_accuracy[0:10])
            with col2:
                st.info("F1 = "+str(f1))
                classifica_f1 = pd.read_csv("classifica_f1.csv", index_col=False)
                classifica_f1['Timestamp'] = pd.to_datetime(classifica_f1['Timestamp'])
                row = {'Student':name, "F1":f1, "Timestamp":timestamp}
                classifica_f1 = pd.concat([classifica_f1, pd.DataFrame([row])], ignore_index=True)
                #classifica_f1 = classifica_f1.append(row, ignore_index=True)
                classifica_f1 = classifica_f1.sort_values(['F1'], ascending=[False])
                classifica_f1 = classifica_f1.reset_index(drop=True)
                classifica_f1 = classifica_f1.sort_values(['Timestamp'], ascending=[True])
                classifica_f1.to_csv("classifica_f1.csv", index=False)
                st.write("First 10 positions")
                st.dataframe(classifica_f1)


else:
    if st.session_state.df is not None:
        st.write("You already uploaded a CSV file. Do you want to upload another one?")
        if st.button("Load new file"):
            st.session_state.df = None
            st.rerun()
