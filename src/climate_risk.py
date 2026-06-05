import pandas as pd

# Load rainfall dataset
rainfall = pd.read_csv("datasets/district wise rainfall normal.csv")

# User Input
district_name = input("Enter District Name: ").strip().upper()

# Find district
district_data = rainfall[
    rainfall["DISTRICT"].str.upper() == district_name
]

if len(district_data) == 0:
    print("District not found.")

else:
    annual_rainfall = district_data.iloc[0]["ANNUAL"]

    print("\nDistrict:", district_name)
    print("Annual Rainfall:", annual_rainfall, "mm")

    # Risk Classification
    if annual_rainfall > 1500:
        risk = "LOW"
    elif annual_rainfall > 800:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    print("Climate Risk Level:", risk)

    # Suggestions
    if risk == "HIGH":
        print("\nRecommended Climate-Resilient Crops:")
        print("- Millet")
        print("- Sorghum")
        print("- Maize")

    elif risk == "MEDIUM":
        print("\nRecommended Crops:")
        print("- Maize")
        print("- Groundnut")
        print("- Pulses")

    else:
        print("\nRecommended Crops:")
        print("- Rice")
        print("- Sugarcane")
        print("- Banana")