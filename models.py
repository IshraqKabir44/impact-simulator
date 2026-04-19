import numpy as np

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
def calculate_water_effects(energy_joules):
    # Alex's constants
    heat_conversion_rate = 0.95
    energy_to_melt_1kg_ice = 436000 # Joules (436 kJ/kg)
    ocean_surface_area = 3.61e14    # m^2
    
    # 1. Energy converted to heat
    q_imp = energy_joules * heat_conversion_rate
    
    # 2. Mass of ice melted
    m_ice_melted = q_imp / energy_to_melt_1kg_ice
    
    # 3. Volume of water (1kg ice = 1L water = 0.001 m^3)
    v_water = m_ice_melted * 0.001
    
    # 4. Sea level rise (meters)
    delta_h_meters = v_water / ocean_surface_area
    delta_h_mm = delta_h_meters * 1000
    
    return {
        "ice_melted_kg": m_ice_melted,
        "sea_level_mm": round(delta_h_mm, 2),  # <--- Check this spelling!
        "years_equiv": round(delta_h_mm / 4.4, 1)}

