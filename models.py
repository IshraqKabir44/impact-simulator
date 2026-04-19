import numpy as np
import math
import pandas as pd
import plotly.express as px

## MODEL FOR THE FOOD CRISIS
def calculate_food_security(diameter, days_post_impact):
    # --- 1. Constants from Tanner's Model ---
    S0 = 0.485  # Total Southern Ocean Fishery Yield (Million Tons)
    K_biomass = 60.0  # Initial Krill Biomass (Million Tons)
    recovery_time = 1460  # 48 months in days
    
    # --- 2. Dust/Sunlight Factor (Beta) ---
    # Based on Bennu study: 500m = 28% drop. Scaling for diameter:
    max_sunlight_reduction = 0.28 * (diameter / 500)
    
    # Decay of dust over time (Simple linear recovery for Beta)
    if days_post_impact < recovery_time:
        beta_t = 1 - (max_sunlight_reduction * (1 - days_post_impact / recovery_time))
    else:
        beta_t = 1.0
        
    # --- 3. Krill Carrying Capacity (C) ---
    # C is directly proportional to sunlight (beta)
    C_t = K_biomass * beta_t
    
    # --- 4. Logistic Growth Result ---
    # S(t) = S0 * (Current_Krill / Initial_Krill)
    # This simplifies the trophic cascade to a linear ratio for the UI
    current_supply = S0 * (C_t / K_biomass)
    
    return {
        "supply": round(current_supply, 3),
        "beta": round(beta_t * 100, 1),
        "loss_pct": round((1 - (current_supply/S0)) * 100, 1)}

## MODEL FOR THE FLOODING
def calculate_water_effects(diameter):
    # 1. Ensure units are base SI (meters and kg)
    v_ms = 72000     # 72 km/s -> 72,000 m/s
    rho = 1700       # kg/m^3
    
    # 2. Energy Calculation
    radius = diameter / 2
    volume = (4/3) * math.pi * (radius**3)
    mass_asteroid = volume * rho
    energy_initial = 0.5 * mass_asteroid * (v_ms**2)
    
    # 3. Work lost to atmosphere (W) 
    # Alex's W = 2.1027e19 Joules for a 1000m asteroid. 
    # We scale this by the cross-sectional area (radius squared)
    work_lost = 2.1027e19 * (radius / 500)**2
    energy_final = energy_initial - work_lost
    
    # 4. Melt Logic (95% of energy)
    q_imp = 0.95 * energy_final
    energy_to_melt_ice = 436000 # Joules per kg
    m_ice_melted = q_imp / energy_to_melt_ice
    
    # 5. Sea Level Rise
    # 1 kg ice = 0.001 m^3 water
    v_water = m_ice_melted * 0.001
    ocean_area = 3.61e14 
    delta_h_mm = (v_water / ocean_area) * 1000
    
    return {
        "ice_melted_kg": m_ice_melted,
        "sea_level_mm": round(delta_h_mm, 2),
        "years_equiv": round(delta_h_mm / 4.4, 1)
    }

## VISUALIZATION OF DATA
import pandas as pd
import plotly.express as px

def generate_visual_maps(diameter):
    # 1. Energy-based scaling (Diameter cubed represents Volume/Energy)
    # We use a base size and then scale up.
    impact_magnitude = (diameter / 500) ** 3
    
    data = pd.DataFrame({
        "lat": [-90.0],
        "lon": [0.0],
        "size": [impact_magnitude]
    })
    
    fig = px.scatter_geo(
        data,
        lat="lat",
        lon="lon",
        size="size",
        projection="orthographic",
        # size_max is the key—it sets how many pixels the largest dot can be
        size_max=100, 
        title="NASA Impact Assessment: Primary Strike Zone"
    )
    
    # 2. Add the 'Shockwave' effect (Glow and Transparency)
    fig.update_traces(
        marker=dict(
            color="Red",
            opacity=0.6, # Makes it look like a thermal pulse, not a solid ball
            line=dict(width=2, color="DarkRed") # The "Crater" rim
        )
    )

    fig.update_geos(
        projection_rotation=dict(lat=-90, lon=0, roll=0),
        showland=True, landcolor="#d1d1d1",
        showocean=True, oceancolor="#0e1117",
        lataxis_showgrid=False, lonaxis_showgrid=False
    )
    
    fig.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)")
    
    return fig
