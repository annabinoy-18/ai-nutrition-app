import streamlit as st
import pickle
import numpy as np

model = pickle.load(open("nutrition_model.pkl","rb"))
le = pickle.load(open("label_encoder.pkl","rb"))

st.set_page_config(page_title="AI Nutrition Advisor", layout="centered")

st.title("🤖 AI Family Nutrition Advisor")

st.markdown("Enter your details below:")

age = st.number_input("Age", 18, 80)
weight = st.number_input("Weight (kg)", 40, 120)
height = st.number_input("Height (m)", 1.4, 2.0)
activity = st.selectbox("Activity Level", ["Low","Moderate","High"])

activity_map = {"Low":1,"Moderate":2,"High":3}
activity_value = activity_map[activity]

if st.button("Get Recommendation"):
    prediction = model.predict([[age,weight,height,activity_value]])
    result = le.inverse_transform(prediction)[0]

    st.success(f"Recommended Calorie Level: {result}")

    if result == "Low":
        st.write("🥗 Light meals: millets, vegetables, fruits, soups")
    elif result == "Moderate":
        st.write("🍛 Balanced diet: rice, dal, vegetables, eggs, paneer")
    else:
        st.write("💪 High calorie: nuts, dairy, whole grains, protein-rich food")
