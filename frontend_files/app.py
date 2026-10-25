
import streamlit as st
import requests

st.title("SuperKart Sales Prediction")

st.write("Enter product and store information to predict product sales.")

product_weight = st.number_input("Product Weight")
product_allocated_area = st.number_input("Product Allocated Area")
product_mrp = st.number_input("Product MRP")
store_establishment_year = st.number_input(
    "Store Establishment Year",
    step=1
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

product_type = st.text_input("Product Type")
store_id = st.text_input("Store ID")
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)
store_type = st.text_input("Store Type")

if st.button("Predict Sales"):

    data = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_Type": product_type,
        "Product_MRP": product_mrp,
        "Store_Id": store_id,
        "Store_Establishment_Year": store_establishment_year,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location,
        "Store_Type": store_type
    }

    response = requests.post(
        "http://backend:5000/predict",
        json=data
    )

    prediction = response.json()["prediction"]

    st.success(f"Predicted Sales: {prediction:.2f}")
