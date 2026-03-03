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
disease = st.selectbox(
    "Select Health Condition",
    ["None", "Diabetes", "Kidney Disease", "High BP", "Heart Disease"]
)

if st.button("Get Recommendation"):
    prediction = model.predict([[age,weight,height,activity_value]])
    result = le.inverse_transform(prediction)[0]

    st.success(f"Recommended Calorie Level: {result}")
    st.subheader("🍽 Recommended Foods")

if disease == "Diabetes":
    st.write("✅ Whole grains, millets, green vegetables, nuts, lentils")
    st.write("❌ Avoid white rice, sugar, sweets, sugary drinks")

elif disease == "Kidney Disease":
    st.write("✅ Cabbage, cauliflower, apple, white rice (limited), egg whites")
    st.write("❌ Avoid high potassium foods like banana, potato, spinach")

elif disease == "High BP":
    st.write("✅ Oats, leafy greens, fruits, low-salt diet")
    st.write("❌ Avoid salty snacks, pickles, processed food")

elif disease == "Heart Disease":
    st.write("✅ Olive oil, nuts, fish, whole grains")
    st.write("❌ Avoid fried food, red meat, butter")

else:
    st.write("✅ Balanced diet with vegetables, protein, whole grains")

    if result == "Low":
        st.write("🥗 Light meals: millets, vegetables, fruits, soups")
    elif result == "Moderate":
        st.write("🍛 Balanced diet: rice, dal, vegetables, eggs, paneer")
    else:
        st.write("💪 High calorie: nuts, dairy, whole grains, protein-rich food")
