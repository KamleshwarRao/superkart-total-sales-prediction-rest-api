import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Total Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
Product_Id = st.text_input("Product_Id")
#Product_Id_Char = st.selectbox("Product_Id_char", ["FD", "DR", "NC"])
Product_Type_Category = st.selectbox("Product_Type_Category", ["Perishables", "Non Perishables"])
Product_Weight = st.number_input("Product_Weight")
Product_Sugar_Content = st.selectbox("Product_Sugar_Content", ["Low Sugar", "Regular", "No Sugar"])
Store_Location_City_Type = st.selectbox("Store_Location_City_Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store_Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Food Mart", "Departmental Store"])
Store_Size = st.selectbox("Store_Size", ["Small", "Medium", "High"])
Product_Allocated_Area = st.number_input("Product_Allocated_Area")
Product_MRP = st.number_input("Product_MRP")
Store_Opening_Year = st.number_input("Store_Opening_Year")
Store_Age_Years = Now( ) - Store_Opening_Year

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Id': Product_Id,
    'Product_Type_Category': Product_Type_Category,
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Store_Size': Store_Size,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Age_Years': Store_Age_Years
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/totalsales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Price (in dollars)']
        st.success(f"Predicted Total Sales (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/totalsalesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
