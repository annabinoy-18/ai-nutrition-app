st.markdown("""
    <style>
    .stApp {
        background-color: #F9FBFD;
    }
    h1 {
        color: #2E7D32;
        text-align: center;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)
import streamlit as st
import pickle
import pandas as pd

# Load trained model
model = pickle.load(open("nutrition_model.pkl","rb"))
le = pickle.load(open("label_encoder.pkl","rb"))

st.set_page_config(page_title="AI Lifestyle Nutrition Advisor", layout="centered")

# Session state
if "page" not in st.session_state:
    st.session_state.page = 1

# ---------------- PAGE 1 ----------------
if st.session_state.page == 1:

    st.title("🤖 AI Lifestyle Nutrition Advisor")

    st.subheader("Enter Your Details")

    age = st.number_input("Age", 18, 80)
    weight = st.number_input("Weight (kg)", 40, 120)
    height = st.number_input("Height (m)", 1.4, 2.0)
    activity = st.selectbox("Activity Level", ["Low","Moderate","High"])

    diseases = st.multiselect(
        "Select Health Conditions (You can choose multiple)",
        [
            "Diabetes",
            "Kidney Disease",
            "High BP",
            "Heart Disease",
            "PCOS",
            "Thyroid",
            "Obesity",
            "Anemia",
            "Gastric / Acidity",
            "Arthritis"
        ]
    )

    activity_map = {"Low":1,"Moderate":2,"High":3}
    activity_value = activity_map[activity]

    if st.button("Generate My Plan"):

        prediction = model.predict([[age,weight,height,activity_value]])
        result = le.inverse_transform(prediction)[0]

        # Save values
        st.session_state.result = result
        st.session_state.diseases = diseases
        st.session_state.activity = activity
        st.session_state.age = age
        st.session_state.weight = weight

        st.session_state.page = 2
        st.rerun()

# ---------------- PAGE 2 ----------------
elif st.session_state.page == 2:

    st.title("📋 Your Personalized Lifestyle Plan")

    result = st.session_state.result
    diseases = st.session_state.diseases
    activity = st.session_state.activity
    age = st.session_state.age
    weight = st.session_state.weight

    # ---------------- CALORIE ----------------
    st.subheader(f"🔥 Predicted Calorie Level: {result}")

    # ---------------- FOOD ----------------
    st.subheader("🍽 Recommended Foods")

    if not diseases:
        st.write("✅ Balanced diet with vegetables, fruits & protein.")
    else:
        for disease in diseases:
            st.markdown(f"### 🔹 {disease}")

            if disease == "Diabetes":
                st.write("• Millets, oats, brown rice")
                st.write("• Avoid sugar & refined carbs")

            elif disease == "Kidney Disease":
                st.write("• Cabbage, cauliflower, apple")
                st.write("• Avoid banana, potato, excess salt")

            elif disease == "High BP":
                st.write("• Oats, fruits, leafy greens")
                st.write("• Avoid pickles & processed foods")

            elif disease == "Heart Disease":
                st.write("• Fish, olive oil, nuts")
                st.write("• Avoid fried food & red meat")

            elif disease == "PCOS":
                st.write("• High fiber diet, lean protein")
                st.write("• Avoid sugary drinks")

            elif disease == "Thyroid":
                st.write("• Iodized salt, eggs, nuts")

            elif disease == "Obesity":
                st.write("• High protein, vegetables")
                st.write("• Avoid high sugar foods")

            elif disease == "Anemia":
                st.write("• Spinach, beetroot, dates")
                st.write("• Vitamin C rich fruits")

            elif disease == "Gastric / Acidity":
                st.write("• Oats, banana, yogurt")
                st.write("• Avoid spicy & caffeine")

            elif disease == "Arthritis":
                st.write("• Omega-3 foods, walnuts")
                st.write("• Avoid inflammatory fried food")

    # ---------------- ACTIVITY ----------------
    st.subheader("🏃 Activity Recommendation")

    if activity == "Low":
        activity_text = "30 mins walking + light yoga daily"
    elif activity == "Moderate":
        activity_text = "45 mins brisk walk + strength training 3x/week"
    else:
        activity_text = "Cardio + strength training 4–5x/week"

    st.write(activity_text)

    # ---------------- WATER ----------------
    st.subheader("💧 Daily Water Intake")

    water = weight * 0.033
    if activity == "High":
        water += 0.5
    elif activity == "Moderate":
        water += 0.3

    st.write(f"Recommended: **{water:.1f} liters/day**")

    # ---------------- SLEEP ----------------
    st.subheader("😴 Sleep Recommendation")

    if age <= 25:
        sleep = "7–9 hours"
    elif age <= 64:
        sleep = "7–8 hours"
    else:
        sleep = "7 hours"

    if activity == "High":
        sleep = "8 hours"

    st.write(f"Recommended: **{sleep} per night**")

    # ---------------- WEEKLY ROUTINE ----------------
    st.subheader("📅 Suggested Weekly Routine")

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    for day in days:
        st.write(f"**{day}**")
        st.write(f"- 🥗 Follow recommended diet")
        st.write(f"- 🏃 {activity_text}")
        st.write(f"- 💧 Drink {water:.1f}L water")
        st.write(f"- 😴 Sleep {sleep}")

    # ---------------- CHART ----------------
    st.subheader("📊 Lifestyle Overview")

    chart_data = pd.DataFrame({
        "Category": ["Water (L)", "Activity Level"],
        "Value": [water, 1 if activity=="Low" else 2 if activity=="Moderate" else 3]
    })

    st.bar_chart(chart_data.set_index("Category"))

    # ---------------- DOWNLOAD REPORT ----------------
    st.subheader("📄 Download Your Health Report")

    disease_text = ", ".join(diseases) if diseases else "None"

    report = f"""
AI Lifestyle Nutrition Report

Calorie Level: {result}
Health Conditions: {disease_text}
Activity: {activity_text}
Water: {water:.1f} L/day
Sleep: {sleep}

Disclaimer: This report is for educational purposes only.
"""

    st.download_button(
        label="Download Report",
        data=report,
        file_name="health_report.txt",
        mime="text/plain"
    )

    # ---------------- DISCLAIMER ----------------
    st.markdown("---")
    st.caption("⚠️ Disclaimer: This application provides general health guidance and is not a substitute for professional medical advice.")

    # ---------------- BACK BUTTON ----------------
    if st.button("⬅ Back"):
        st.session_state.page = 1
        st.rerun()
