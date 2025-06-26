import streamlit as st
import pandas as pd
from PIL import Image

# --- Load the logo ---
logo = Image.open("logo.png")
st.image(logo, width=180)
st.markdown("<h1 style='text-align: center;'>Norbert's Free Iron Dog Calculator</h1>", unsafe_allow_html=True)

# --- Load the Excel tables ---
excel = pd.ExcelFile("2025 Iron Dog scores.xlsx")
big_air_df = pd.read_excel(excel, sheet_name="Big Air")
extreme_vertical_df = pd.read_excel(excel, sheet_name="Extreme Vertical")
speed_retrieve_df = pd.read_excel(excel, sheet_name="Speed Retrieve")

# --- Create lookup tables ---
def get_big_air_points(feet, inches):
    row = big_air_df[(big_air_df['BIG AIR'] == feet) & (big_air_df['Unnamed: 1'] == inches)]
    if row.empty:
        # fallback: find closest lower value
        subset = big_air_df[(big_air_df['BIG AIR'] < feet) | ((big_air_df['BIG AIR'] == feet) & (big_air_df['Unnamed: 1'] <= inches))]
        if subset.empty:
            return 0.0
        row = subset.iloc[[-1]]
    return float(row['Unnamed: 2'].values[0])

def get_extreme_vertical_points(feet, inches):
    row = extreme_vertical_df[(extreme_vertical_df['EXTREME VERTICAL'] == feet) & (extreme_vertical_df['Unnamed: 1'] == inches)]
    if row.empty:
        subset = extreme_vertical_df[(extreme_vertical_df['EXTREME VERTICAL'] < feet) | ((extreme_vertical_df['EXTREME VERTICAL'] == feet) & (extreme_vertical_df['Unnamed: 1'] <= inches))]
        if subset.empty:
            return 0.0
        row = subset.iloc[[-1]]
    return float(row['Unnamed: 2'].values[0])

def get_speed_retrieve_points(seconds):
    row = speed_retrieve_df[speed_retrieve_df['SPEED RETRIEVE'] >= seconds].head(1)
    if row.empty:
        return float(speed_retrieve_df.iloc[-1]['Unnamed: 1'])
    return float(row['Unnamed: 1'].values[0])

# --- Streamlit form UI ---
with st.form("iron_dog_form"):
    st.subheader("Big Air")
    ba_feet = st.number_input("Feet (Big Air)", min_value=0, max_value=40, value=0, step=1)
    ba_inches = st.number_input("Inches (Big Air)", min_value=0, max_value=11, value=0, step=1)

    st.subheader("Extreme Vertical")
    ev_feet = st.number_input("Feet (Extreme Vertical)", min_value=0, max_value=13, value=0, step=1)
    ev_inches = st.number_input("Inches (Extreme Vertical)", min_value=0, max_value=11, value=0, step=1)

    st.subheader("Speed Retrieve")
    sr_time = st.number_input("Time (seconds)", min_value=2.5, max_value=20.0, value=7.0, step=0.001, format="%.3f")

    submitted = st.form_submit_button("Calculate Iron Dog Score")

if submitted:
    ba_pts = get_big_air_points(int(ba_feet), int(ba_inches))
    ev_pts = get_extreme_vertical_points(int(ev_feet), int(ev_inches))
    sr_pts = get_speed_retrieve_points(sr_time)
    total = ba_pts + ev_pts + sr_pts

    st.success("Results")
    st.write(f"**Big Air:** {int(ba_feet)}' {int(ba_inches)}\" → {ba_pts} points")
    st.write(f"**Extreme Vertical:** {int(ev_feet)}' {int(ev_inches)}\" → {ev_pts} points")
    st.write(f"**Speed Retrieve:** {sr_time:.3f} sec → {sr_pts} points")
    st.markdown(f"<h2>Total Iron Dog Score: {total:.2f} points</h2>", unsafe_allow_html=True)
