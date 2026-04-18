import streamlit as st
import models
import pandas as pd

st.set_page_config(layout="wide")
st.title("NASA Asteroid Impact: Global Food Security")

# --- Sidebar ---
dia = st.sidebar.slider("Asteroid Diameter (m)", 500, 5000, 1000)
t_days = st.sidebar.select_slider("Timeline", options=[0, 30, 90, 180, 365, 730, 1460], value=180)

# --- Execute Tanner's Model ---
results = models.calculate_food_security(dia, t_days)

# --- Display Results ---
col1, col2, col3 = st.columns(3)
col1.metric("Sunlight Levels", f"{results['beta']}%", delta="-28% vs Pre-Impact")
col2.metric("Fishery Yield", f"{results['supply']}M Tons")
col3.metric("Global Food Deficit", f"{results['loss_pct']}%", delta_color="inverse")

# --- The "Action" Visualization ---
st.subheader("Trophic Cascade Impact")

# We can show a simple progress bar or a custom graphic
st.write(f"**Krill Population Status at T+{t_days} days:**")
st.progress(results['beta'] / 100) 

if results['loss_pct'] > 20:
    st.error("⚠️ CRITICAL FOOD SHORTAGE DETECTED IN SOUTHERN HEMISPHERE")
