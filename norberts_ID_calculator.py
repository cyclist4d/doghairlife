import streamlit as st
import pandas as pd

# ------------------------------
# Load scoring tables from Excel
# ------------------------------
@st.cache_data
def load_scores():
    # Ensure the Excel file is in the same directory (2025 ID scores.xlsx)
    xls = pd.ExcelFile("2025 ID scores.xlsx")
    bigair = pd.read_excel(xls, sheet_name="Big Air")
    extreme = pd.read_excel(xls, sheet_name="Extreme Vertical")
    speed = pd.read_excel(xls, sheet_name="Speed Retrieve")
    return bigair, extreme, speed

bigair_df, extreme_df, speed_df = load_scores()

# ------------------------------
# Page configuration
# ------------------------------
st.set_page_config(
    page_title="Norbert's Free Iron Dog Calculator",
    page_icon="logo.png"
)

# Display the logo at the top
st.image("logo.png", width=200)

# norberts_ID_calculator.py title
st.title("Norbert's Free Iron Dog Calculator")

# ------------------------------
# User inputs
# ------------------------------
st.header("Enter Your Measurements")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Big Air")
    ba_ft = st.number_input(
        "Feet (ft)", 
        min_value=int(bigair_df['ft'].min()), 
        max_value=int(bigair_df['ft'].max()),
        step=1
    )
    ba_in = st.number_input(
        "Inches (in)", 
        min_value=0, 
        max_value=11,
        step=1
    )
with col2:
    st.subheader("Extreme Vertical")
    ev_ft = st.number_input(
        "Feet (ft)", 
        min_value=int(extreme_df['ft'].min()), 
        max_value=int(extreme_df['ft'].max()),
        step=1
    )
    ev_in = st.number_input(
        "Inches (in)", 
        min_value=0, 
        max_value=11,
        step=1
    )

st.subheader("Speed Retrieve")
sr_secs = st.number_input(
    "Time (seconds)", 
    min_value=float(speed_df['secs'].min()),
    max_value=float(speed_df['secs'].max()),
    format="%.3f",
    step=0.001
)

# ------------------------------
# Calculate and display scores
# ------------------------------
if st.button("Calculate Scores"):
    # Lookup Big Air score
    ba_match = bigair_df[(bigair_df['ft'] == ba_ft) & (bigair_df['in'] == ba_in)]
    ba_score = ba_match['Points'].iloc[0] if not ba_match.empty else None

    # Lookup Extreme Vertical score
    ev_match = extreme_df[(extreme_df['ft'] == ev_ft) & (extreme_df['in'] == ev_in)]
    ev_score = ev_match['Points'].iloc[0] if not ev_match.empty else None

    # Lookup Speed Retrieve score (rounded match)
    sr_match = speed_df[speed_df['secs'].round(3) == round(sr_secs, 3)]
    sr_score = sr_match['Points'].iloc[0] if not sr_match.empty else None

    # Display individual event results
    st.subheader("Results")
    if ba_score is not None:
        st.write(f"**Big Air:** {ba_ft} ft {ba_in} in → {ba_score:.2f} points")
    else:
        st.write(f"**Big Air:** {ba_ft} ft {ba_in} in → **No score found**")

    if ev_score is not None:
        st.write(f"**Extreme Vertical:** {ev_ft} ft {ev_in} in → {ev_score:.2f} points")
    else:
        st.write(f"**Extreme Vertical:** {ev_ft} ft {ev_in} in → **No score found**")

    if sr_score is not None:
        st.write(f"**Speed Retrieve:** {sr_secs:.3f} s → {sr_score:.2f} points")
    else:
        st.write(f"**Speed Retrieve:** {sr_secs:.3f} s → **No score found**")

    # Calculate and display total score
    if None not in (ba_score, ev_score, sr_score):
        total_score = ba_score + ev_score + sr_score
        st.markdown(f"### Total Iron Dog Score: **{total_score:.2f} points**")
    else:
        st.markdown("### Total Iron Dog Score: _Unable to calculate due to missing scores_")
