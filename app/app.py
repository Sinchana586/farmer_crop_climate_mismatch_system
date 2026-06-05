import streamlit as st
import pandas as pd
import joblib

# ==========================
# Load Models & Datasets
# ==========================

# Language Selection


TEXT = {
    "title": {
        "English": "🌾 Smart Farming Assistant",
        "Kannada": "🌾 ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ",
        "Hindi": "🌾 स्मार्ट कृषि सहायक"
    },
    "description": {
        "English": "Enter your farm details to find the best crop and get simple farming advice.",
        "Kannada": "ನಿಮ್ಮ ಜಮೀನಿನ ವಿವರಗಳನ್ನು ನೀಡಿ ಉತ್ತಮ ಬೆಳೆ ಮತ್ತು ಕೃಷಿ ಸಲಹೆ ಪಡೆಯಿರಿ.",
        "Hindi": "अपनी खेती की जानकारी दर्ज करें और सबसे अच्छी फसल तथा सरल कृषि सलाह प्राप्त करें।"
    },
    "best_crop": {
        "English": "🌱 Best Crop to Grow",
        "Kannada": "🌱 ಬೆಳೆಸಲು ಉತ್ತಮ ಬೆಳೆ",
        "Hindi": "🌱 उगाने के लिए सबसे अच्छी फसल"
    },
    "weather": {
        "English": "☁️ Weather Condition",
        "Kannada": "☁️ ಹವಾಮಾನ ಸ್ಥಿತಿ",
        "Hindi": "☁️ मौसम की स्थिति"
    },
    "district": {
        "English": "District",
        "Kannada": "ಜಿಲ್ಲೆ",
        "Hindi": "जिला"
    },
    "rain": {
        "English": "Yearly Rain",
        "Kannada": "ವಾರ್ಷಿಕ ಮಳೆ",
        "Hindi": "वार्षिक वर्षा"
    },
    "weather_safety": {
        "English": "Weather Safety",
        "Kannada": "ಹವಾಮಾನ ಸುರಕ್ಷತೆ",
        "Hindi": "मौसम सुरक्षा"
    },
    "crop_production": {
        "English": "🌾 Crop Production",
        "Kannada": "🌾 ಬೆಳೆ ಉತ್ಪಾದನೆ",
        "Hindi": "🌾 फसल उत्पादन"
    },
    "avg_yield": {
        "English": "Average Yield",
        "Kannada": "ಸರಾಸರಿ ಉತ್ಪಾದನೆ",
        "Hindi": "औसत उत्पादन"
    },
    "water": {
        "English": "💧 Water Needed",
        "Kannada": "💧 ನೀರಿನ ಅಗತ್ಯ",
        "Hindi": "💧 पानी की आवश्यकता"
    },
    "good_harvest": {
        "English": "Good Harvest Expected",
        "Kannada": "ಉತ್ತಮ ಇಳುವರಿ ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ",
        "Hindi": "अच्छी पैदावार की उम्मीद"
    },
    "average_harvest": {
        "English": "Average Harvest Expected",
        "Kannada": "ಸರಾಸರಿ ಇಳುವರಿ ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ",
        "Hindi": "औसत पैदावार की उम्मीद"
    },
    "low_harvest": {
        "English": "Harvest May Be Lower",
        "Kannada": "ಇಳುವರಿ ಕಡಿಮೆ ಇರಬಹುದು",
        "Hindi": "पैदावार कम हो सकती है"
    },
    "more_water": {
        "English": "This crop may need more water.",
        "Kannada": "ಈ ಬೆಳೆಗೆ ಹೆಚ್ಚು ನೀರು ಬೇಕಾಗಬಹುದು.",
        "Hindi": "इस फसल को अधिक पानी की आवश्यकता हो सकती है।"
    },
    "medium_water": {
        "English": "This crop needs a medium amount of water.",
        "Kannada": "ಈ ಬೆಳೆಗೆ ಮಧ್ಯಮ ಪ್ರಮಾಣದ ನೀರು ಬೇಕಾಗುತ್ತದೆ.",
        "Hindi": "इस फसल को मध्यम मात्रा में पानी चाहिए।"
    },
    "less_water": {
        "English": "This crop needs less water.",
        "Kannada": "ಈ ಬೆಳೆಗೆ ಕಡಿಮೆ ನೀರು ಸಾಕಾಗುತ್ತದೆ.",
        "Hindi": "इस फसल को कम पानी की आवश्यकता है।"
    }
    ,
    "weather_good": {
        "English": "Good",
        "Kannada": "ಉತ್ತಮ",
        "Hindi": "अच्छा"
    },
    "weather_moderate": {
        "English": "Moderate",
        "Kannada": "ಮಧ್ಯಮ",
        "Hindi": "मध्यम"
    },
    "weather_care": {
        "English": "Needs Care",
        "Kannada": "ಎಚ್ಚರಿಕೆ ಅಗತ್ಯ",
        "Hindi": "सावधानी आवश्यक"
    },
    "alt_high": {
        "English": "Other Crops You Can Grow: Millet, Sorghum, Maize",
        "Kannada": "ನೀವು ಬೆಳೆಸಬಹುದಾದ ಇತರ ಬೆಳೆಗಳು: ಸಜ್ಜೆ, ಜೋಳ, ಮೆಕ್ಕೆಜೋಳ",
        "Hindi": "आप उगा सकते हैं अन्य फसलें: बाजरा, ज्वार, मक्का"
    },
    "alt_medium": {
        "English": "Other Crops You Can Grow: Groundnut, Pulses, Maize",
        "Kannada": "ನೀವು ಬೆಳೆಸಬಹುದಾದ ಇತರ ಬೆಳೆಗಳು: ಕಡಲೆಕಾಯಿ, ಬೇಳೆಗಳು, ಮೆಕ್ಕೆಜೋಳ",
        "Hindi": "आप उगा सकते हैं अन्य फसलें: मूंगफली, दालें, मक्का"
    },
    "weather_favorable": {
        "English": "Weather is suitable for farming.",
        "Kannada": "ಕೃಷಿಗೆ ಹವಾಮಾನ ಅನುಕೂಲಕರವಾಗಿದೆ.",
        "Hindi": "खेती के लिए मौसम अनुकूल है।"
    },
    "select_district": {
        "English": "Select District",
        "Kannada": "ಜಿಲ್ಲೆ ಆಯ್ಕೆಮಾಡಿ",
        "Hindi": "जिला चुनें"
    },
    "market_price": {
        "English": "💰 Market Price",
        "Kannada": "💰 ಮಾರುಕಟ್ಟೆ ಬೆಲೆ",
        "Hindi": "💰 बाजार मूल्य"
    },
    "income_estimate": {
        "English": "💵 Income Estimate",
        "Kannada": "💵 ಆದಾಯ ಅಂದಾಜು",
        "Hindi": "💵 आय का अनुमान"
    },
    "avg_market_price": {
        "English": "Average Market Price",
        "Kannada": "ಸರಾಸರಿ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ",
        "Hindi": "औसत बाजार मूल्य"
    },
    "min_market_price": {
        "English": "Minimum Market Price",
        "Kannada": "ಕನಿಷ್ಠ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ",
        "Hindi": "न्यूनतम बाजार मूल्य"
    },
    "max_market_price": {
        "English": "Maximum Market Price",
        "Kannada": "ಗರಿಷ್ಠ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ",
        "Hindi": "अधिकतम बाजार मूल्य"
    },
    "income_estimate": {
        "English": "💵 Income Estimate",
        "Kannada": "💵 ಆದಾಯ ಅಂದಾಜು",
        "Hindi": "💵 आय का अनुमान"
    },
    "estimated_income": {
        "English": "Estimated Income",
        "Kannada": "ಅಂದಾಜು ಆದಾಯ",
        "Hindi": "अनुमानित आय"
    },
    "market_not_available": {
        "English": "Market price data not available for this crop.",
        "Kannada": "ಈ ಬೆಳೆಗೆ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ.",
        "Hindi": "इस फसल के लिए बाजार मूल्य डेटा उपलब्ध नहीं है।"
    }
}

model = joblib.load("models/random_forest_model.pkl")

rainfall_df = pd.read_csv(
    "datasets/district wise rainfall normal.csv"
)

production_df = pd.read_csv(
    "datasets/India Agriculture Crop Production.csv"
)

market_df = pd.read_csv(
    "datasets/Price_Agriculture_commodities_Week.csv"
)

irrigation_model = joblib.load(
    "models/irrigation_model.pkl"
)

target_encoder = joblib.load(
    "models/irrigation_target_encoder.pkl"
)

feature_columns = joblib.load(
    "models/irrigation_feature_columns.pkl"
)

# ==========================
# Page Configuration
# ==========================

st.set_page_config(
    page_title="Farmer Crop-Climate Mismatch System",
    page_icon="🌾",
    layout="centered"
)

language = st.selectbox(
    "Choose Language / ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ / भाषा चुनें",
    ["English", "Kannada", "Hindi"]
)

st.title(TEXT["title"][language])
st.write(TEXT["description"][language])

# ==========================
# User Inputs
# ==========================

N = st.number_input(
    {
        "English":"Nitrogen (N)",
        "Kannada":"ನೈಟ್ರೋಜನ್ (N)",
        "Hindi":"नाइट्रोजन (N)"
    }[language],
    min_value=0.0,
    value=90.0
)

P = st.number_input(
    {
        "English":"Phosphorus (P)",
        "Kannada":"ಫಾಸ್ಫರಸ್ (P)",
        "Hindi":"फॉस्फोरस (P)"
    }[language],
    min_value=0.0,
    value=42.0
)

K = st.number_input(
    {
        "English":"Potassium (K)",
        "Kannada":"ಪೊಟಾಸಿಯಂ (K)",
        "Hindi":"पोटैशियम (K)"
    }[language],
    min_value=0.0,
    value=43.0
)

temperature = st.number_input(
    {
        "English":"Temperature (°C)",
        "Kannada":"ತಾಪಮಾನ (°C)",
        "Hindi":"तापमान (°C)"
    }[language],
    value=25.0
)

humidity = st.number_input(
    {
        "English":"Humidity (%)",
        "Kannada":"ಆರ್ದ್ರತೆ (%)",
        "Hindi":"नमी (%)"
    }[language],
    value=80.0
)

ph = st.number_input(
    {
        "English":"pH",
        "Kannada":"pH",
        "Hindi":"pH"
    }[language],
    value=6.5
)

rainfall = st.number_input(
    {
        "English":"Rainfall (mm)",
        "Kannada":"ವರ್ಷಾವಸರ (ಮಿಮೀ)",
        "Hindi":"वर्षा (मिमी)"
    }[language],
    value=220.0
)

districts = sorted(
    rainfall_df["DISTRICT"].dropna().unique()
)

district = st.selectbox(
    TEXT["select_district"][language],
    districts
)

st.subheader("💧 Irrigation Information")

soil_type = st.selectbox(
    "Soil Type",
    ["Sandy", "Loamy", "Clay"]
)

soil_moisture = st.slider(
    "Soil Moisture (%)",
    0.0,
    100.0,
    50.0
)

# ==========================
# Prediction Button
# ==========================

button_text = {
    "English": "Predict",
    "Kannada": "ಭವಿಷ್ಯ ನುಡಿಸಿ",
    "Hindi": "भविष्यवाणी करें"
}

if st.button(button_text[language]):

    # Crop Prediction
    features = pd.DataFrame([{
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])

    predicted_crop = model.predict(features)[0]

    st.success(
        f"{TEXT['best_crop'][language]}: {predicted_crop.upper()}"
    )

    # Climate Risk Analysis
    district_data = rainfall_df[
        rainfall_df["DISTRICT"] == district
    ]

    if not district_data.empty:

        annual_rainfall = district_data.iloc[0]["ANNUAL"]

        if annual_rainfall > 1500:
            weather_status = "Good"

        elif annual_rainfall > 800:
            weather_status = "Moderate"

        else:
            weather_status = "Needs Care"

        st.subheader(TEXT["weather"][language])

        st.write(
            f"**{TEXT['district'][language]}:** {district}"
        )

        st.write(
            f"**{TEXT['rain'][language]}:** {annual_rainfall:.1f} mm"
        )

        if weather_status == "Good":
            display_status = TEXT["weather_good"][language]

        elif weather_status == "Moderate":
            display_status = TEXT["weather_moderate"][language]

        else:
            display_status = TEXT["weather_care"][language]

        st.write(
            f"**{TEXT['weather_safety'][language]}:** {display_status}"
        )

# Weather Suggestions

        if weather_status == "Needs Care":

            st.warning(
                TEXT["alt_high"][language]
         )

        elif weather_status == "Moderate":

         st.info(
                 TEXT["alt_medium"][language]
         )

        else:

            st.success(
                TEXT["weather_favorable"][language]
    )

    # Yield Analysis
    crop_data = production_df[
        production_df["Crop"]
        .astype(str)
        .str.lower()
        == predicted_crop.lower()
    ]

    if not crop_data.empty:

        avg_yield = crop_data["Yield"].mean()

        st.subheader(TEXT["crop_production"][language])

        st.write(
            f"{TEXT['avg_yield'][language]}: {avg_yield:.2f}"
        )

        if avg_yield > 5:
            st.success(TEXT["good_harvest"][language])

        elif avg_yield > 3:
            st.info(TEXT["average_harvest"][language])

        else:
            st.warning(TEXT["low_harvest"][language])


# ==========================
# Market Price Analysis
# ==========================

    crop_price_data = market_df[
        market_df["Commodity"]
        .astype(str)
        .str.lower()
        .str.contains(predicted_crop.lower(), na=False)
    ]

    if not crop_price_data.empty:

        avg_price = crop_price_data["Modal Price"].mean()

        min_price = crop_price_data["Min Price"].mean()

        max_price = crop_price_data["Max Price"].mean()

        st.subheader(
        TEXT["market_price"][language]
        )

        st.write(
            f"{TEXT['avg_market_price'][language]}: ₹{avg_price:.0f}"
        )

        st.write(
            f"{TEXT['min_market_price'][language]}: ₹{min_price:.0f}"
        )

        st.write(
            f"{TEXT['max_market_price'][language]}: ₹{max_price:.0f}"
        )

        if 'avg_yield' in locals():

            estimated_income = avg_yield * avg_price

            st.subheader(
                TEXT["income_estimate"][language]
            )

            st.success(
                f"{TEXT['estimated_income'][language]}: ₹{estimated_income:,.0f}"
            )

    else:

        st.warning(
        TEXT["market_not_available"][language]
        )

# Water Assessment


   # ==========================
# Irrigation Prediction
# ==========================

    st.subheader("💧 Irrigation Prediction")

    irrigation_input = pd.DataFrame([{
        "Soil_Type": soil_type,
        "Soil_pH": ph,
        "Soil_Moisture": soil_moisture,
        "Organic_Carbon": 0.8,
        "Electrical_Conductivity": 0.5,
        "Temperature_C": temperature,
        "Humidity": humidity,
        "Rainfall_mm": rainfall,
        "Sunlight_Hours": 8,
        "Wind_Speed_kmh": 10,
        "Crop_Type": predicted_crop,
        "Crop_Growth_Stage": "Vegetative",
        "Season": "Kharif",
        "Irrigation_Type": "Drip",
        "Water_Source": "Groundwater",
        "Field_Area_hectare": 1,
        "Mulching_Used": "Yes",
        "Previous_Irrigation_mm": 20,
        "Region": "South"
    }])

    irrigation_input = pd.get_dummies(
        irrigation_input
    )

    irrigation_input = irrigation_input.reindex(
        columns=feature_columns,
        fill_value=0
    )

    prediction = irrigation_model.predict(
        irrigation_input
    )

    irrigation_need = target_encoder.inverse_transform(
        prediction
    )[0]

    irrigation_text = {
        "English": "Irrigation Need",
        "Kannada": "ನೀರಾವರಿ ಅಗತ್ಯ",
        "Hindi": "सिंचाई आवश्यकता"
    }

    st.success(
        f"{irrigation_text[language]}: {irrigation_need}"
    )