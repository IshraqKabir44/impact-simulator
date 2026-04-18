import numpy as np

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
        "loss_pct": round((1 - (current_supply/S0)) * 100, 1)
