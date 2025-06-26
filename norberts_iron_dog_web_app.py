import streamlit as st
from PIL import Image

# ---- Load your logo ----
logo = Image.open("logo.png")
st.image(logo, width=180)
st.markdown("<h1 style='text-align: center;'>Norbert's Free Iron Dog Calculator</h1>", unsafe_allow_html=True)

# ---- Full lookup tables ----
BIG_AIR_POINTS = {(0, 0): 0.0, (0, 1): 0.0, (0, 2): 0.0, (0, 3): 0.0, (0, 4): 0.0, (0, 5): 0.0, (0, 6): 0.0, (0, 7): 0.0, (0, 8): 0.0, (0, 9): 0.0, (0, 10): 0.0, (0, 11): 0.0, (3, 0): 1.52, (3, 1): 12.89, (3, 2): 24.26, (16, 1): 908.11, (18, 6): 908.11, (31, 3): 1063.6, (39, 11): 1126.16, (40, 0): 1127.15}
EXTREME_VERTICAL_POINTS = {(4, 6): 788.13, (5, 8): 929.86, (8, 4): 1072.13, (13, 0): 1263.75}
SPEED_RETRIEVE_POINTS = [(2.5, 1133.47), (3.832, 1090.22), (7.436, 951.57), (20.0, 17.07)]

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
    st.write(f"**Big Air:** {int(ba_feet)}' {int(ba_inches)}" → {ba_pts} points")
    st.write(f"**Extreme Vertical:** {int(ev_feet)}' {int(ev_inches)}" → {ev_pts} points")
    st.write(f"**Speed Retrieve:** {sr_time:.3f} sec → {sr_pts} points")
    st.markdown(f"<h2>Total Iron Dog Score: {total:.2f} points</h2>", unsafe_allow_html=True)
