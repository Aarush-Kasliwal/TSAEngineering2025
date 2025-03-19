import streamlit as st


# Function to calculate required nitrogen
def calculate_nitrogen(soil_moisture, nitrogen, pH, fertility, temp, humidity, wind, rainfall, solar_rad, atm_nitrogen,
                       crop_type, prev_fertilizer):
    # Base nitrogen requirement based on crop type
    crop_nitrogen_req = {"Wheat": 100, "Corn": 120, "Soybean": 80, "Rice": 110}
    base_nitrogen = crop_nitrogen_req.get(crop_type, 100)

    # Adjustments based on environmental conditions
    nitrogen_adjustment = (
            (-5 if soil_moisture < 30 else 5) +
            (-10 if nitrogen > 50 else 10) +
            (-7 if 6.0 <= pH <= 7.5 else 7) +
            (15 if fertility < 50 else -15) +
            (-5 if temp < 15 else 5) +
            (-3 if humidity > 80 else 3) +
            (-5 if wind > 20 else 5) +
            (10 if rainfall < 50 else -10) +
            (-8 if solar_rad > 200 else 8) +
            (-10 if atm_nitrogen > 30 else 10)
    )

    # Final nitrogen requirement per unit area
    final_nitrogen = base_nitrogen + nitrogen_adjustment - prev_fertilizer
    return max(final_nitrogen, 0)  # Ensure nitrogen value is not negative


# Streamlit UI
st.title("Precision Agriculture Nitrogen Calculator")
st.header("Determine Required Nitrogen for Optimal Crop Growth")

# User Inputs
crop_type = st.selectbox("Select Crop Type", ["Wheat", "Corn", "Soybean", "Rice"])
prev_fertilizer = st.number_input("Previous Fertilizer/Nitrogen Deposit (kg/ha)", min_value=0.0, value=0.0)

st.subheader("Soil Sensor Data")
soil_moisture = st.slider("Soil Moisture (%)", 0, 100, 50)
nitrogen = st.slider("Existing Soil Nitrogen (ppm)", 0, 100, 30)
pH = st.slider("Soil pH Level", 4.0, 9.0, 6.5)
fertility = st.slider("Soil Fertility Level (%)", 0, 100, 70)

st.subheader("Weather Balloon Data")
temp = st.slider("Temperature (°C)", -10, 50, 20)
humidity = st.slider("Humidity (%)", 0, 100, 60)
wind = st.slider("Wind Fall (km/h)", 0, 50, 10)
rainfall = st.slider("Rainfall (mm)", 0, 200, 100)
solar_rad = st.slider("Solar Radiation (W/m²)", 0, 500, 250)
atm_nitrogen = st.slider("Atmospheric Nitrogen Levels (ppm)", 0, 100, 40)

# Calculate and display results
if st.button("Calculate Required Nitrogen"):
    required_nitrogen = calculate_nitrogen(soil_moisture, nitrogen, pH, fertility, temp, humidity, wind, rainfall,
                                           solar_rad, atm_nitrogen, crop_type, prev_fertilizer)
    st.success(f"Recommended Nitrogen Application: {required_nitrogen:.2f} kg/ha")

