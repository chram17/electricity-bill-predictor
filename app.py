import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI Electricity Bill Predictor", page_icon="💡")
st.title("💡 AI Electricity Bill Predictor")
st.write("Enter your appliance usage, AI will predict your monthly bill!")

data = []
for fans in [1,2,3,4]:
    for ac_hours in [0,2,4,6,8]:
        for fridge_hours in [12,24]:
            units = (fans*75*8 + ac_hours*1500 + fridge_hours*200 + 2*60*6) * 30 / 1000
            bill = units * 7
            data.append([fans, ac_hours, fridge_hours, units, bill])

df = pd.DataFrame(data, columns=['fans','ac_hours','fridge_hours','units','bill'])
X = df[['fans','ac_hours','fridge_hours']]
y = df['bill']
model = LinearRegression()
model.fit(X, y)

st.header("Enter Your Usage")
fans = st.slider("How many Fans?", 0, 10, 2)
lights = st.slider("How many Lights?", 0, 10, 4)
ac_hours = st.slider("AC Usage Hours Per Day?", 0, 24, 4)
fridge_hours = st.selectbox("Fridge Running?", [12, 24])
motor_hours = st.slider("Motor / Pump Hours Per Day?", 0, 5, 1)

if st.button("Predict My Bill"):
    prediction = model.predict([[fans, ac_hours, fridge_hours]])[0]
    extra = (lights*60*6 + motor_hours*750) * 30 / 1000 * 7
    total_bill = prediction + extra
    total_units = total_bill / 7
    st.success(f"Predicted Monthly Units: {total_units:.1f} Units")
    st.success(f"Predicted Monthly Bill: Rs. {total_bill:.0f}")
    if ac_hours > 6:
        st.warning("Tip: Your AC uses 60% power. Reduce 1 hour daily to save Rs. 300+ per month!")
    else:
        st.info("Tip: Your usage is efficient! Use LED lights to save more.")