import streamlit as st
import models
import pandas as pd

st.set_page_config(layout="wide")
st.title("NASA Asteroid Impact: Global Food Security")

# --- Sidebar ---
dia = st.sidebar.slider("Asteroid Diameter (m)", 500, 5000, 1000)
t_days = st.sidebar.select_slider("Timeline", options=[0, 30, 90, 180, 365, 730, 1460], value=180)

# --- Execute Models ---
results_food = models.calculate_food_security(dia, t_days)
results_water = models.calculate_water_effects(dia)

# --- Create Tabs ---
tab1, tab2 = st.tabs(["🦐 Food Security", "🌊 Water Effects"])

with tab1:
    # --- Tanner's Model Display (Your Original Code) ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Sunlight Levels", f"{results_food['beta']}%", delta="-28% vs Pre-Impact")
    col2.metric("Fishery Yield", f"{results_food['supply']}M Tons")
    col3.metric("Global Food Deficit", f"{results_food['loss_pct']}%", delta_color="inverse")

    st.subheader("Trophic Cascade Impact")
    st.write(f"**Krill Population Status at T+{t_days} days:**")
    safe_beta = max(0.0, results_food['beta'])
    st.progress(safe_beta / 100)

    if results_food['loss_pct'] > 20:
        st.error("⚠️ CRITICAL FOOD SHORTAGE DETECTED IN SOUTHERN HEMISPHERE")

with tab2:
    # --- Alex's Model Display ---
    if dia > 1800:
        st.warning("☄️ GLOBAL EXTINCTION LEVEL EVENT: The energy release exceeds the bounds of this regional model.")
         
    st.subheader("South Pole Ice Melt & Sea Level Rise")
    
    if results_water['ice_melted_kg'] > 0:
        c1, c2 = st.columns(2)
        c1.metric("Global Sea Level Rise", f"{results_water['sea_level_mm']} mm")
        c2.metric("Climate Acceleration", f"{results_water['years_equiv']} Years", delta="of normal rise")
        st.info(f"Total Ice Melted: {results_water['ice_melted_kg']:.2e} kg")
    else:
        # If mass is 0 or negative due to atmospheric drag calculation
        st.error("Kinetic energy fully dissipated by atmospheric drag. No surface melting occurred.")
    
    st.markdown("---")
    st.write("**Impact Analysis:**")
    st.write(f"Because the impact occurs at the **South Pole landmass**, there is no direct displacement tsunami. However, the thermal pulse creates an instantaneous melt equivalent to {results_water['years_equiv']} years of current global warming.")
   
