import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and description
st.title("Interactive Data Explorer")
st.write("Upload a CSV file to explore your data interactively.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    # Data preview
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    # Summary statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())
    
    # Column selection for visualization
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if numeric_columns:
        selected_column = st.selectbox("Select a numeric column for histogram", numeric_columns)
        
        # Histogram
        st.subheader(f"Histogram of {selected_column}")
        fig, ax = plt.subplots()
        ax.hist(df[selected_column].dropna(), bins=20, edgecolor='black')
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        st.write("No numeric columns found for visualization.")
else:
    st.write("Please upload a CSV file to get started.")
