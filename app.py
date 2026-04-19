import streamlit as st
import models
import plotly.graph_objects as go

st.set_page_config(page_title="Project A.S.P.I.", layout="wide")

# --- CUSTOM CSS FOR NASA THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0f14; color: #e0e6ed; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1e26; border-radius: 5px; color: #a1a9b8; }
    .stTabs [aria-selected="true"] { background-color: #313a4d; color: #ffffff; }
    .stMetric { border: 1px solid #333; padding: 15px; border-radius: 10px; background-color: #1a1e26; color: #ffffff !important; }
    [data-testid="stMetricLabel"] {
        color: #a1a9b8 !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ Project A.S.P.I. (Antarctic South Pole Impact)")
st.caption("National Aeronautics and Space Administration (NASA) - Consequence Assessment Dashboard")

# --- Sidebar ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e5/NASA_logo.svg", width=120)
    st.header("Simulation Settings")
    st.markdown("Adjust the initial impactor variables:")
    dia = st.slider("Asteroid Diameter (m)", 500, 5000, 1000)
    t_days = st.select_slider("Timeline (Days)", options=[0, 30, 90, 180, 365, 550,  730, 915, 1100, 1275, 1460], value=180)
    st.divider()
    st.info("**Model Boundary:** Antarctica bedrock target, 72 km/s impact.")

# --- Execute Models ---
# Tanner
res_food = models.calculate_food_security(dia, t_days)
# Alex
res_water = models.calculate_water_effects(dia)
# Maps (Using Alex's data for scaling)
map_viz = models.generate_visual_maps(dia)

# --- Create Tabs ---
tab1, tab2 = st.tabs(["🌾 Tanner: Trophic Collapse", "💧 Alex: Cryosphere Melt"])

with tab1:
    # 1. Data Metrics
    col1, col2, col3 = st.columns(3)
    # Calculate the actual drop
    sun_drop = res_food['beta'] - 100

    col1.metric(
        "Sunlight Levels", 
        f"{res_food['beta']}%", 
        delta=f"{sun_drop:.1f}% vs Pre-Impact"
    )
    col2.metric("Fishery Yield (Area 48/58)", f"{res_food['supply']}M Tons")
    col3.metric("Global Food Deficit", f"{res_food['loss_pct']}%", delta_color="inverse")

    # 2. Visual Sunlight Intensity (The "Regular Day" idea)
    st.markdown("---")
    st.subheader("Visual Sunlight Intensity")
    st.caption(f"Comparing a baseline clear day at the South Pole vs. T+{t_days} days post-impact.")
    
    sun_intensity = res_food['beta'] / 100 # Convert to 0.0-1.0
    
    # We can use CSS to dynamically color a box based on the intensity
    # 0% = black, 100% = bright yellow
    hex_intensity = int(sun_intensity * 255)
    sun_color = f"#{hex_intensity:02x}{hex_intensity:02x}{0:02x}" # Shades of Yellow/Black

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f'<div style="width:100%;height:150px;background-color:#ffff00;border-radius:10px;border:3px solid #FFD700;display:flex;justify-content:center;align-items:center;color:#000;"><strong>PRE-IMPACT: 100%</strong></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div style="width:100%;height:150px;background-color:{sun_color};border-radius:10px;border:3px solid #a1a9b8;display:flex;justify-content:center;align-items:center;color:#fff;"><strong>CURRENT (T+{t_days}): {res_food["beta"]}%</strong></div>', unsafe_allow_html=True)

    # 3. Critical Status
    if res_food['loss_pct'] > 15:
        st.error(f"⚠️ SEVERE FOOD SHORTAGE ALERT: Global deficit exceeds 15% due to krill biomass suppression.")

with tab2:
    # 1. Data Metrics
    c1, c2 = st.columns(2)
    c1.metric(
        label="Instant Sea Level Rise", 
        value=f"{res_water['sea_level_mm']} mm", 
        delta=f"{res_water['years_equiv']} years eq.", 
        delta_color="inverse"
    )
    c2.metric("Melt Volume (Cryosphere)", f"{res_water['ice_melted_kg']:.2e} kg")

    # 2. Dynamic Red Zone Map
    st.markdown("---")
    st.subheader("3D Polar Visualization")
    st.caption("The red circle indicates the immediate 'Zone of Vaporization' where Antarctic ice is converted directly into liquid water and steam upon impact. Move the Diameter slider to see the zone scale.")
    
    if dia > 1800:
        st.warning("☄️ EXTINCTION LIMIT: Energy exceeds regional scaling model, displaying max blast zone.")

    # Show the Map!
    st.plotly_chart(map_viz, use_container_width=True)
    
    # 3. Impact Summary
    st.divider()
    st.write("**Assessment:**")
    st.write(f"Thermal pulse converts ~95% of final kinetic energy into latent heat, driving a global sea level rise of {res_water['sea_level_mm']}mm. Impact on South Pole landmass prevents direct displacement tsunamis; however, a Richter Magnitude ~9.0 seismic quake is projected.")
