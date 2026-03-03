import streamlit as st
import pickle

# Load trained model
model = pickle.load(open("nutrition_model.pkl","rb"))
le = pickle.load(open("label_encoder.pkl","rb"))

st.set_page_config(page_title="AI Lifestyle Nutrition Advisor", layout="centered")

# Initialize session state
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
    disease = st.selectbox(
    "Health Condition",
    [
        "None",
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

        # Save values in session
        st.session_state.result = result
        st.session_state.disease = disease
        st.session_state.activity = activity
        st.session_state.age = age
        st.session_state.weight = weight

        st.session_state.page = 2
        st.rerun()

# ---------------- PAGE 2 ----------------
elif st.session_state.page == 2:

    st.title("📋 Your Personalized Lifestyle Plan")

    result = st.session_state.result
    disease = st.session_state.disease
    activity = st.session_state.activity
    age = st.session_state.age
    weight = st.session_state.weight

    # ---------------- CALORIE RESULT ----------------
    st.subheader(f"🔥 Predicted Calorie Level: {result}")

    # ---------------- FOOD RECOMMENDATION ----------------
    st.subheader("🍽 Recommended Foods")

    if disease == "Diabetes":
        st.write("✅ Millets, oats, brown rice")
        st.write("✅ Leafy vegetables, bitter gourd")
        st.write("✅ Nuts, seeds, lentils")
        st.write("❌ Avoid sugar, sweets, white bread, soft drinks")

    elif disease == "Kidney Disease":
        st.write("✅ Cabbage, cauliflower, apple, berries")
        st.write("✅ Egg whites, controlled white rice")
        st.write("❌ Avoid banana, potato, spinach, excess salt")

    elif disease == "High BP":
        st.write("✅ Oats, fruits, leafy greens")
        st.write("✅ Garlic, low-salt diet")
        st.write("❌ Avoid pickles, chips, processed foods")

    elif disease == "Heart Disease":
        st.write("✅ Fish, olive oil, nuts")
        st.write("✅ Whole grains, fruits, vegetables")
        st.write("❌ Avoid fried food, red meat, butter")

    else:
        st.write("✅ Balanced diet with vegetables, fruits & protein")
        st.write("✅ Include whole grains and healthy fats")

    # ---------------- ACTIVITY ----------------
    st.subheader("🏃 Activity Recommendation")

    if activity == "Low":
        st.write("🚶 30 minutes walking daily")
        st.write("🧘 Light yoga or stretching")
        st.write("🪑 Reduce sitting time")

    elif activity == "Moderate":
        st.write("🏃 45 minutes brisk walk or jogging")
        st.write("🏋 Strength training 3 times/week")
        st.write("🧘 Flexibility exercises")

    else:
        st.write("💪 Strength training 4–5 times/week")
        st.write("🏃 Cardio + endurance workouts")
        st.write("🔥 Core strengthening exercises")

    # ---------------- WATER CALCULATION ----------------
    st.subheader("💧 Daily Water Intake Recommendation")

    water = weight * 0.033  # basic formula

    if activity == "High":
        water += 0.5
    elif activity == "Moderate":
        water += 0.3

    st.write(f"👉 Recommended Water Intake: **{water:.1f} liters per day**")

    # ---------------- SLEEP RECOMMENDATION ----------------
    st.subheader("😴 Sleep Recommendation")

    if age <= 25:
        sleep = "7–9 hours"
    elif age <= 64:
        sleep = "7–8 hours"
    else:
        sleep = "7 hours"

    if activity == "High":
        sleep = "8 hours (due to high activity level)"

    st.write(f"👉 Recommended Sleep Duration: **{sleep} per night**")

    # ---------------- BACK BUTTON ----------------
    if st.button("⬅ Back"):
        st.session_state.page = 1
        st.rerun()
