import streamlit as st
from PIL import Image

# ---- Load your logo ----
logo = Image.open("logo.png")
st.image(logo, width=180)
st.markdown("<h1 style='text-align: center;'>Norbert's Free Iron Dog Calculator</h1>", unsafe_allow_html=True)

# ---- Your lookup tables from your GUI script (shortened for this sample; you should paste the full tables) ----
BIG_AIR_POINTS = {
    (16, 1): 908.11, (18, 6): 908.11, (31, 3): 1063.6, (40, 0): 1127.15,  # ...and so on...
}
EXTREME_VERTICAL_POINTS = {
    (4, 6): 788.13, (5, 8): 929.86, (8, 4): 1072.13, (13, 0): 1263.75,  # ...and so on...
}
SPEED_RETRIEVE_POINTS = [
    (2.5, 1133.47), (3.832, 1090.22), (7.436, 951.57), (20.0, 17.07)  # ...and so on...
]

def get_big_air_points(feet, inches):
    possible = [(f, i) for (f, i) in BIG_AIR_POINTS if (f < feet) or (f == feet and i <= inches)]
    if not possible:
        return 0.0
    max_ft_in = max(possible)
    return BIG_AIR_POINTS[max_ft_in]

def get_extreme_vertical_points(feet, inches):
    possible = [(f, i) for (f, i) in EXTREME_VERTICAL_POINTS if (f < feet) or (f == feet and i <= inches)]
    if not possible:
        return 0.0
    max_ft_in = max(possible)
    return EXTREME_VERTICAL_POINTS[max_ft_in]

def get_speed_retrieve_points(seconds):
    for sec, pts in SPEED_RETRIEVE_POINTS:
        if seconds <= sec:
            return pts
    return SPEED_RETRIEVE_POINTS[-1][1]

with st.form("iron_dog_form"):
    st.subheader("Big Air")
    ba_feet = st.number_input("Feet", min_value=0, max_value=40, value=0, step=1)
    ba_inches = st.number_input("Inches", min_value=0, max_value=11, value=0, step=1)

    st.subheader("Extreme Vertical")
    ev_feet = st.number_input("Feet ", min_value=0, max_value=13, value=0, step=1, key="ev_ft")
    ev_inches = st.number_input("Inches ", min_value=0, max_value=11, value=0, step=1, key="ev_in")

    st.subheader("Speed Retrieve")
    sr_time = st.number_input("Time (seconds)", min_value=2.5, max_value=20.0, value=0, step=0.001, format="%.3f")

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
    st.write(f"## **Total Iron Dog Score: {total:.2f} points**")
