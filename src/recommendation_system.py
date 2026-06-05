import pandas as pd
import joblib

# Load model
model = joblib.load("models/random_forest_model.pkl")

# Load rainfall dataset
rainfall = pd.read_csv("/workspaces/farmer_crop_climate_mismatch_system/datasets/district wise rainfall normal.csv")

# User Inputs
N = float(input("Enter Nitrogen (N): "))
P = float(input("Enter Phosphorus (P): "))
K = float(input("Enter Potassium (K): "))
temperature = float(input("Enter Temperature: "))
humidity = float(input("Enter Humidity: "))
ph = float(input("Enter pH: "))
rainfall_input = float(input("Enter Rainfall: "))
district = input("Enter District Name: ").strip().upper()

# Predict crop
features = pd.DataFrame([{
    "N": N,
    "P": P,
    "K": K,
    "temperature": temperature,
    "humidity": humidity,
    "ph": ph,
    "rainfall": rainfall_input
}])

predicted_crop = model.predict(features)[0]

# Climate Risk Analysis
district_data = rainfall[
    rainfall["DISTRICT"].str.upper() == district
]

print("\n" + "="*40)
print("FARMER CROP-CLIMATE REPORT")
print("="*40)

print("Recommended Crop:", predicted_crop)

if len(district_data) > 0:

    annual_rainfall = district_data.iloc[0]["ANNUAL"]

    print("District:", district)
    print("Annual Rainfall:", annual_rainfall)

    if annual_rainfall > 1500:
        risk = "LOW"
    elif annual_rainfall > 800:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    print("Climate Risk Level:", risk)

    if risk == "HIGH":
        print("\nSuggested Alternatives:")
        print("- Millet")
        print("- Sorghum")
        print("- Maize")

    elif risk == "MEDIUM":
        print("\nSuggested Alternatives:")
        print("- Groundnut")
        print("- Pulses")
        print("- Maize")

else:
    print("District not found in rainfall database.")

print("="*40)