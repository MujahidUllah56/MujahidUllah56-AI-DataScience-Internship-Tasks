import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load model
model = joblib.load("churn_model.pkl")

# Load dataset
df = pd.read_csv("Churn_Modelling (1).csv")

# Remove unnecessary columns
df = df.drop(["RowNumber","CustomerId","Surname"],axis=1)

st.title("Customer Churn Prediction System")

st.write("Enter customer information")

# Sidebar inputs
st.sidebar.header("Customer Details")

credit_score = st.sidebar.slider("Credit Score",300,850,600)
age = st.sidebar.slider("Age",18,90,35)
tenure = st.sidebar.slider("Tenure",0,10,3)
balance = st.sidebar.number_input("Balance",0.0,250000.0,50000.0)
products = st.sidebar.slider("Number of Products",1,4,1)
credit_card = st.sidebar.selectbox("Has Credit Card",[0,1])
active_member = st.sidebar.selectbox("Is Active Member",[0,1])
salary = st.sidebar.number_input("Estimated Salary",0.0,200000.0,50000.0)

geography = st.sidebar.selectbox("Geography",["France","Spain","Germany"])
gender = st.sidebar.selectbox("Gender",["Male","Female"])

# Encoding
geo_germany = 1 if geography=="Germany" else 0
geo_spain = 1 if geography=="Spain" else 0
gender_male = 1 if gender=="Male" else 0

# Correct input dataframe
input_data = pd.DataFrame({
"CreditScore":[credit_score],
"Age":[age],
"Tenure":[tenure],
"Balance":[balance],
"NumOfProducts":[products],
"HasCrCard":[credit_card],
"IsActiveMember":[active_member],
"EstimatedSalary":[salary],
"Geography_Germany":[geo_germany],
"Geography_Spain":[geo_spain],
"Gender_Male":[gender_male]
})

st.subheader("Input Data")
st.write(input_data)

# Prediction
if st.button("Predict"):

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    st.subheader("Prediction Result")

    if prediction[0] == 1:
        st.error("Customer will churn")
    else:
        st.success("Customer will stay with the bank")

    st.subheader("Prediction Probability")

    st.write("Stay Probability:", round(probability[0][0]*100,2),"%")
    st.write("Churn Probability:", round(probability[0][1]*100,2),"%")


# Dataset preview
st.subheader("Dataset Preview")
st.dataframe(df.head())


# Churn distribution
st.subheader("Churn Distribution")

fig, ax = plt.subplots()

sns.countplot(x="Exited",data=df)

st.pyplot(fig)