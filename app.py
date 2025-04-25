import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load("credit_risk_model.pkl")

st.title("Credit Risk Prediction App")

st.sidebar.header("Applicant Information")

age = st.sidebar.slider("Age", 18, 75, 30)
job = st.sidebar.selectbox("Job Type", [0, 1, 2, 3])
credit_amount = st.sidebar.number_input("Credit Amount", min_value=0, step=100)
duration = st.sidebar.slider("Duration (in months)", 4, 72, 12)

sex_male = st.sidebar.radio("Sex", ['Male', 'Female']) == 'Male'
housing = st.sidebar.radio("Housing", ['Own', 'Free', 'Rent'])
housing_own = 1 if housing == 'Own' else 0
housing_rent = 1 if housing == 'Rent' else 0

saving_acc = st.sidebar.selectbox("Saving Account", ['Unknown', 'Little', 'Moderate', 'Quite Rich', 'Rich'])
saving_moderate = 1 if saving_acc == 'Moderate' else 0
saving_quite_rich = 1 if saving_acc == 'Quite Rich' else 0
saving_rich = 1 if saving_acc == 'Rich' else 0

checking_acc = st.sidebar.selectbox("Checking Account", ['Unknown', 'Little', 'Moderate', 'Rich'])
checking_moderate = 1 if checking_acc == 'Moderate' else 0
checking_rich = 1 if checking_acc == 'Rich' else 0

purpose = st.sidebar.selectbox("Loan Purpose", [
    'Car', 'Domestic Appliances', 'Education', 'Furniture/Equipment',
    'Radio/TV', 'Repairs', 'Vacation/Others'
])


purposes = {
    'Purpose_car': 0,
    'Purpose_domestic appliances': 0,
    'Purpose_education': 0,
    'Purpose_furniture/equipment': 0,
    'Purpose_radio/TV': 0,
    'Purpose_repairs': 0,
    'Purpose_vacation/others': 0
}
if f"Purpose_{purpose.lower()}" in purposes:
    purposes[f"Purpose_{purpose.lower()}"] = 1
elif purpose == 'Furniture/Equipment':
    purposes['Purpose_furniture/equipment'] = 1

input_data = np.array([[
    age, job, credit_amount, duration, int(sex_male), 
    housing_own, housing_rent,
    saving_moderate, saving_quite_rich, saving_rich,
    checking_moderate, checking_rich,
    purposes['Purpose_car'], purposes['Purpose_domestic appliances'], purposes['Purpose_education'],
    purposes['Purpose_furniture/equipment'], purposes['Purpose_radio/TV'], purposes['Purpose_repairs'],
    purposes['Purpose_vacation/others']
]])


if st.button("Predict Credit Risk"):
    prediction = model.predict(input_data)[0]
    result = "Good Credit Risk" if prediction == 1 else "Bad Credit Risk"
    st.success(f"Prediction: {result}")

