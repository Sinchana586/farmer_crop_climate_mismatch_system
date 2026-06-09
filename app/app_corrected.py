
import streamlit as st
import pandas as pd
import joblib
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(
    crop,
    weather,
    market_price,
    income,
    irrigation
):

    pdf_file = "farmer_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Farmer Recommendation Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Recommended Crop: {crop}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Weather Status: {weather}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Market Price: ₹{market_price}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Estimated Income: ₹{income}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Irrigation Need: {irrigation}",
            styles["Normal"]
        )
    )

    doc.build(content)

    return pdf_file


st.set_page_config(
    page_title="Farmer Crop-Climate Mismatch System",
    page_icon="🌾",
    layout="wide"
)
st.markdown("""
<style>

/* Metric Cards */
div[data-testid="stMetric"]{
    border:1px solid rgba(128,128,128,0.3);
    border-radius:15px;
    padding:15px;
    transition:all 0.3s ease;
}

div[data-testid="stMetric"]:hover{
    transform:translateY(-3px);
}

/* Buttons */
.stButton button{
    border-radius:12px;
    font-weight:600;
    transition:all 0.3s ease;
}

.stButton button:hover{
    transform:scale(1.03);
}

/* Smooth Page Load */
@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(10px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

.block-container{
    animation:fadeIn 0.6s ease-in-out;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

div[data-testid="stMetric"] {
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(128,128,128,0.3);
    transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
}

div[data-testid="stMetricLabel"] {
    font-size: 16px;
    font-weight: bold;
}

h1 {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------- LANGUAGE ----------

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
    },
    "mode_selection": {
        "English": "Choose Recommendation Mode",
        "Kannada": "ಶಿಫಾರಸು ವಿಧಾನವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "Hindi": "सिफारिश मोड चुनें"
    },

    "advanced": {
        "English": "Advanced (Soil Test Available)",
        "Kannada": "ಸುಧಾರಿತ (ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ ಲಭ್ಯವಿದೆ)",
        "Hindi": "उन्नत (मिट्टी परीक्षण उपलब्ध)"
    },

    "simple_mode": {
        "English": "Simple Farmer Mode",
        "Kannada": "ಸರಳ ರೈತ ವಿಧಾನ",
        "Hindi": "सरल किसान मोड"
    },
    "soil_type": {
        "English": "Soil Type",
        "Kannada": "ಮಣ್ಣಿನ ವಿಧ",
        "Hindi": "मिट्टी का प्रकार"
    },

    "season": {
        "English": "Season",
        "Kannada": "ಋತು",
        "Hindi": "मौसम"
    },

    "water_availability": {
        "English": "Water Availability",
        "Kannada": "ನೀರಿನ ಲಭ್ಯತೆ",
        "Hindi": "पानी की उपलब्धता"
    },

    "district_select": {
        "English": "District",
        "Kannada": "ಜಿಲ್ಲೆ",
        "Hindi": "जिला"
    },
    "irrigation_info": {
        "English": "💧 Irrigation Information",
        "Kannada": "💧 ನೀರಾವರಿ ಮಾಹಿತಿ",
        "Hindi": "💧 सिंचाई जानकारी"
    },

    "soil_moisture": {
        "English": "Soil Moisture (%)",
        "Kannada": "ಮಣ್ಣಿನ ತೇವಾಂಶ (%)",
        "Hindi": "मिट्टी की नमी (%)"
    },

    "irrigation_soil": {
        "English": "Soil Type for Irrigation",
        "Kannada": "ನೀರಾವರಿಗಾಗಿ ಮಣ್ಣಿನ ವಿಧ",
        "Hindi": "सिंचाई हेतु मिट्टी का प्रकार"
    },
    "predict": {
        "English": "Predict",
        "Kannada": "ಭವಿಷ್ಯ ನುಡಿಸಿ",
        "Hindi": "भविष्यवाणी करें"
    },
    "climate_analysis": {
    "English": "☁️ Climate Analysis",
    "Kannada": "☁️ ಹವಾಮಾನ ವಿಶ್ಲೇಷಣೆ",
    "Hindi": "☁️ मौसम विश्लेषण"
    },

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
        "English": "Suggested Alternatives: Millet, Sorghum, Maize",
        "Kannada": "ಪರ್ಯಾಯ ಬೆಳೆಗಳು: ಸಜ್ಜೆ, ಜೋಳ, ಮೆಕ್ಕೆಜೋಳ",
        "Hindi": "वैकल्पिक फसलें: बाजरा, ज्वार, मक्का"
    },

    "alt_medium": {
        "English": "Suggested Alternatives: Groundnut, Pulses, Maize",
        "Kannada": "ಪರ್ಯಾಯ ಬೆಳೆಗಳು: ಕಡಲೆಕಾಯಿ, ಬೇಳೆ, ಮೆಕ್ಕೆಜೋಳ",
        "Hindi": "वैकल्पिक फसलें: मूंगफली, दालें, मक्का"
    },

    "weather_favorable": {
        "English": "Weather is suitable for farming.",
        "Kannada": "ಕೃಷಿಗೆ ಹವಾಮಾನ ಅನುಕೂಲಕರವಾಗಿದೆ.",
        "Hindi": "खेती के लिए मौसम अनुकूल है।"
    },
    "yield_analysis": {
        "English": "🌾 Yield Analysis",
        "Kannada": "🌾 ಇಳುವರಿ ವಿಶ್ಲೇಷಣೆ",
        "Hindi": "🌾 उपज विश्लेषण"
    },

    "avg_yield": {
        "English": "Average Yield",
        "Kannada": "ಸರಾಸರಿ ಇಳುವರಿ",
        "Hindi": "औसत उपज"
    },

    "good_harvest": {
        "English": "Good Harvest Expected",
        "Kannada": "ಉತ್ತಮ ಇಳುವರಿ ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ",
        "Hindi": "अच्छी उपज की उम्मीद"
    },

    "average_harvest": {
        "English": "Average Harvest Expected",
        "Kannada": "ಸರಾಸರಿ ಇಳುವರಿ ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ",
        "Hindi": "औसत उपज की उम्मीद"
    },

    "low_harvest": {
        "English": "Harvest May Be Lower",
        "Kannada": "ಇಳುವರಿ ಕಡಿಮೆ ಇರಬಹುದು",
        "Hindi": "उपज कम हो सकती है"
    },
    "market_price": {
        "English": "💰 Market Price Analysis",
        "Kannada": "💰 ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ವಿಶ್ಲೇಷಣೆ",
        "Hindi": "💰 बाजार मूल्य विश्लेषण"
    },

    "current_price": {
        "English": "Current Market Price",
        "Kannada": "ಪ್ರಸ್ತುತ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ",
        "Hindi": "वर्तमान बाजार मूल्य"
    },

    "price_unit": {
        "English": "per Quintal",
        "Kannada": "ಪ್ರತಿ ಕ್ವಿಂಟಲ್",
        "Hindi": "प्रति क्विंटल"
    },

    "price_not_found": {
        "English": "Market price data not available.",
        "Kannada": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ.",
        "Hindi": "बाजार मूल्य डेटा उपलब्ध नहीं है।"
    },
    "income_estimation": {
        "English": "💵 Income Estimation",
        "Kannada": "💵 ಆದಾಯ ಅಂದಾಜು",
        "Hindi": "💵 आय अनुमान"
    },

    "estimated_income": {
        "English": "Estimated Income",
        "Kannada": "ಅಂದಾಜು ಆದಾಯ",
        "Hindi": "अनुमानित आय"
    },

    "income_note": {
        "English": "Estimated based on average yield and market price.",
        "Kannada": "ಸರಾಸರಿ ಇಳುವರಿ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಬೆಲೆಯ ಆಧಾರದ ಮೇಲೆ ಅಂದಾಜಿಸಲಾಗಿದೆ.",
        "Hindi": "औसत उपज और बाजार मूल्य के आधार पर अनुमानित।"
    },
    "irrigation_prediction": {
        "English": "💧 Irrigation Prediction",
        "Kannada": "💧 ನೀರಾವರಿ ಮುನ್ಸೂಚನೆ",
        "Hindi": "💧 सिंचाई पूर्वानुमान"
    },

    "irrigation_need": {
        "English": "Irrigation Need",
        "Kannada": "ನೀರಾವರಿ ಅಗತ್ಯ",
        "Hindi": "सिंचाई आवश्यकता"
    },
    "saved": {
        "English": "Prediction saved successfully.",
        "Kannada": "ಮುನ್ಸೂಚನೆ ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ.",
        "Hindi": "पूर्वानुमान सफलतापूर्वक सहेजा गया।"
    },
    "farm_summary": {
        "English": "📊 Farm Summary",
        "Kannada": "📊 ಕೃಷಿ ಸಾರಾಂಶ",
        "Hindi": "📊 कृषि सारांश"
    },
    "top_crops": {
        "English": "🏆 Top Crop Recommendations",
        "Kannada": "🏆 ಅತ್ಯುತ್ತಮ ಬೆಳೆ ಶಿಫಾರಸುಗಳು",
        "Hindi": "🏆 सर्वोत्तम फसल सिफारिशें"
    },
    "download_report": {
        "English": "📄 Download Report",
        "Kannada": "📄 ವರದಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
        "Hindi": "📄 रिपोर्ट डाउनलोड करें"
    },
    "expected_income": {
        "English": "Expected Income",
        "Kannada": "ಅಂದಾಜು ಆದಾಯ",
        "Hindi": "अनुमानित आय"
    },
    "voice_assistant": {
        "English": "🔊 Voice Assistant",
        "Kannada": "🔊 ಧ್ವನಿ ಸಹಾಯಕ",
        "Hindi": "🔊 वॉयस असिस्टेंट"
    },
    "negotiation_assistant": {
        "English": "💰 Farmer Negotiation Assistant",
        "Kannada": "💰 ರೈತ ಬೆಲೆ ಮಾತುಕತೆ ಸಹಾಯಕ",
        "Hindi": "💰 किसान मूल्य वार्ता सहायक"
    },
    "why_crop": {
    "English": "🧠 Why BhoomiAI Recommended This Crop",
    "Kannada": "🧠 BhoomiAI ಈ ಬೆಳೆಯನ್ನು ಏಕೆ ಶಿಫಾರಸು ಮಾಡಿದೆ?",
    "Hindi": "🧠 BhoomiAI ने इस फसल की सिफारिश क्यों की?"
    },

    "positive_outlook": {
    "English": "🟢 Positive Outlook",
    "Kannada": "🟢 ಧನಾತ್ಮಕ ದೃಷ್ಟಿಕೋನ",
    "Hindi": "🟢 सकारात्मक दृष्टिकोण"
    },

    "neutral_outlook": {
    "English": "🟡 Neutral Outlook",
    "Kannada": "🟡 ತಟಸ್ಥ ದೃಷ್ಟಿಕೋನ",
    "Hindi": "🟡 तटस्थ दृष्टिकोण"
    },

    "negative_outlook": {
    "English": "🔴 Negative Outlook",
    "Kannada": "🔴 ಋಣಾತ್ಮಕ ದೃಷ್ಟಿಕೋನ",
    "Hindi": "🔴 नकारात्मक दृष्टिकोण"
    },

    "reason_rainfall_low": {
    "English": "✓ Suitable for low rainfall conditions",
    "Kannada": "✓ ಕಡಿಮೆ ಮಳೆಯ ಪರಿಸ್ಥಿತಿಗಳಿಗೆ ಸೂಕ್ತವಾಗಿದೆ",
    "Hindi": "✓ कम वर्षा की परिस्थितियों के लिए उपयुक्त"
    },

    "reason_rainfall_good": {
    "English": "✓ Suitable for available rainfall",
    "Kannada": "✓ ಲಭ್ಯವಿರುವ ಮಳೆಯ ಪ್ರಮಾಣಕ್ಕೆ ಸೂಕ್ತವಾಗಿದೆ",
    "Hindi": "✓ उपलब्ध वर्षा के लिए उपयुक्त"
    },

    "reason_simple": {
    "English": "✓ Selected based on soil and seasonal conditions",
    "Kannada": "✓ ಮಣ್ಣು ಮತ್ತು ಋತುಮಾನ ಪರಿಸ್ಥಿತಿಗಳ ಆಧಾರದ ಮೇಲೆ ಆಯ್ಕೆ ಮಾಡಲಾಗಿದೆ",
    "Hindi": "✓ मिट्टी और मौसम की स्थिति के आधार पर चयनित"
    },

    "reason_advanced": {
    "English": "✓ Selected using soil nutrient analysis",
    "Kannada": "✓ ಮಣ್ಣಿನ ಪೋಷಕಾಂಶ ವಿಶ್ಲೇಷಣೆಯ ಆಧಾರದ ಮೇಲೆ ಆಯ್ಕೆ ಮಾಡಲಾಗಿದೆ",
    "Hindi": "✓ मिट्टी पोषक तत्व विश्लेषण के आधार पर चयनित"
    },

    "reason_weather_good": {
    "English": "✓ Favorable climate conditions",
    "Kannada": "✓ ಅನುಕೂಲಕರ ಹವಾಮಾನ ಪರಿಸ್ಥಿತಿಗಳು",
    "Hindi": "✓ अनुकूल जलवायु परिस्थितियाँ"
    },

    "reason_weather_moderate": {
    "English": "✓ Moderate climate conditions",
    "Kannada": "✓ ಮಧ್ಯಮ ಹವಾಮಾನ ಪರಿಸ್ಥಿತಿಗಳು",
    "Hindi": "✓ मध्यम जलवायु परिस्थितियाँ"
    },

    "reason_weather_risk": {
    "English": "⚠ Climate risk detected",
    "Kannada": "⚠ ಹವಾಮಾನ ಅಪಾಯ ಪತ್ತೆಯಾಗಿದೆ",
    "Hindi": "⚠ जलवायु जोखिम पाया गया"
    },
    "fair_range": {
    "English": "Fair Selling Range",
    "Kannada": "ನ್ಯಾಯಸಮ್ಮತ ಮಾರಾಟ ಶ್ರೇಣಿ",
    "Hindi": "उचित बिक्री सीमा"
    },

    "avoid_below": {
    "English": "Avoid selling below",
    "Kannada": "ಇದಕ್ಕಿಂತ ಕಡಿಮೆ ಬೆಲೆಗೆ ಮಾರಾಟ ಮಾಡಬೇಡಿ",
    "Hindi": "इससे कम मूल्य पर बिक्री न करें"
    },

    "market_favorable": {
    "English": "Market conditions are favorable. Consider selling now.",
    "Kannada": "ಮಾರುಕಟ್ಟೆ ಪರಿಸ್ಥಿತಿಗಳು ಅನುಕೂಲಕರವಾಗಿವೆ. ಈಗ ಮಾರಾಟ ಮಾಡುವುದನ್ನು ಪರಿಗಣಿಸಿ.",
    "Hindi": "बाज़ार की स्थिति अनुकूल है। अभी बेचने पर विचार करें।"
    },

    "market_low": {
    "English": "Market prices are relatively low. Consider waiting if storage is available.",
    "Kannada": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು ತುಲನಾತ್ಮಕವಾಗಿ ಕಡಿಮೆಯಿವೆ. ಸಂಗ್ರಹಣೆ ಸೌಲಭ್ಯ ಇದ್ದರೆ ಕಾಯುವ ಬಗ್ಗೆ ಪರಿಗಣಿಸಿ.",
    "Hindi": "बाज़ार मूल्य अपेक्षाकृत कम हैं। यदि भंडारण उपलब्ध है तो प्रतीक्षा करने पर विचार करें।"
    },
    "summary": {
    "English": "📊 BhoomiAI Summary",
    "Kannada": "📊 BhoomiAI ಸಾರಾಂಶ",
    "Hindi": "📊 BhoomiAI सारांश"
    },
    "price": {
    "English": "💰 Price",
    "Kannada": "💰 ಬೆಲೆ",
    "Hindi": "💰 मूल्य"
    },

    "income": {
    "English": "💵 Income",
    "Kannada": "💵 ಆದಾಯ",
    "Hindi": "💵 आय"
    }

}


language = st.selectbox(
    "Choose Language / ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ / भाषा चुनें",
    ["English","Kannada","Hindi"]
)

titles = {
    "English": "Smart Farming & Agricultural Decision Support System",
    "Kannada": "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಮತ್ತು ಕೃಷಿ ನಿರ್ಧಾರ ಬೆಂಬಲ ವ್ಯವಸ್ಥೆ",
    "Hindi": "स्मार्ट कृषि एवं कृषि निर्णय सहायता प्रणाली"
}

st.markdown(f"""
<div style="
padding:20px;
border-radius:15px;
border:1px solid rgba(128,128,128,0.3);
text-align:center;
margin-bottom:20px;
">
    <h1>🌾 BhoomiAI</h1>
    <h4>{titles[language]}</h4>
</div>
""", unsafe_allow_html=True)

# ---------- LOAD ----------
model = joblib.load(
    "models/random_forest_model.pkl"
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
rainfall_df = pd.read_csv(
    "datasets/district wise rainfall normal.csv"
)

production_df = pd.read_csv(
    "datasets/India Agriculture Crop Production.csv"
)

market_df = pd.read_csv(
    "datasets/Price_Agriculture_commodities_Week.csv"
)

conn = sqlite3.connect(
    "farmer_data.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    language TEXT,
    district TEXT,
    recommended_crop TEXT,
    weather_status TEXT,
    irrigation_need TEXT
)
""")

conn.commit()

st.write(TEXT["description"][language])

st.sidebar.title("Database")

if st.sidebar.button("View Saved Records"):

    records = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY id DESC",
        conn
    )

    st.dataframe(records)


mode = st.radio(
    TEXT["mode_selection"][language],
    [
        TEXT["advanced"][language],
        TEXT["simple_mode"][language]
    ]
)
districts = sorted(
    rainfall_df["DISTRICT"].dropna().unique()
)

# ---------- INPUTS ----------


if mode == TEXT["advanced"][language]:

    st.info(
        {
            "English": "Use this mode if you have a soil test report.",
            "Kannada": "ನಿಮ್ಮ ಬಳಿ ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ವರದಿ ಇದ್ದರೆ ಈ ವಿಧಾನವನ್ನು ಬಳಸಿ.",
            "Hindi": "यदि आपके पास मिट्टी परीक्षण रिपोर्ट है तो इस मोड का उपयोग करें।"
        }[language]
    )

    N = st.number_input(
        {
            "English": "Nitrogen (N)",
            "Kannada": "ನೈಟ್ರೋಜನ್ (N)",
            "Hindi": "नाइट्रोजन (N)"
        }[language],
        min_value=0.0,
        max_value=140.0,
        value=90.0
    )

    P = st.number_input(
        {
            "English": "Phosphorus (P)",
            "Kannada": "ಫಾಸ್ಫರಸ್ (P)",
            "Hindi": "फॉस्फोरस (P)"
        }[language],
        min_value=0.0,
        max_value=145.0,
        value=42.0
    )

    K = st.number_input(
        {
            "English": "Potassium (K)",
            "Kannada": "ಪೊಟ್ಯಾಸಿಯಮ್ (K)",
            "Hindi": "पोटैशियम (K)"
        }[language],
        min_value=0.0,
        max_value=205.0,
        value=43.0
    )

    temperature = st.slider(
        {
            "English": "Temperature (°C)",
            "Kannada": "ತಾಪಮಾನ (°C)",
            "Hindi": "तापमान (°C)"
        }[language],
        min_value=0.0,
        max_value=50.0,
        value=25.0
    )

    humidity = st.slider(
        {
            "English": "Humidity (%)",
            "Kannada": "ಆರ್ದ್ರತೆ (%)",
            "Hindi": "आर्द्रता (%)"
        }[language],
        min_value=0.0,
        max_value=100.0,
        value=80.0
    )

    ph = st.slider(
        {
            "English": "Soil pH",
            "Kannada": "ಮಣ್ಣಿನ pH",
            "Hindi": "मिट्टी का pH"
        }[language],
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )

    rainfall = st.number_input(
        {
            "English": "Rainfall (mm)",
            "Kannada": "ಮಳೆ (ಮಿಮೀ)",
            "Hindi": "वर्षा (मिमी)"
        }[language],
        min_value=0.0,
        max_value=5000.0,
        value=220.0
    )

    district = st.selectbox(
        TEXT["district_select"][language],
        districts
    )

else:

    st.info(
        {
            "English": "Use this mode if you do not have a soil test report.",
            "Kannada": "ನಿಮ್ಮ ಬಳಿ ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ವರದಿ ಇಲ್ಲದಿದ್ದರೆ ಈ ವಿಧಾನವನ್ನು ಬಳಸಿ.",
            "Hindi": "यदि आपके पास मिट्टी परीक्षण रिपोर्ट नहीं है तो इस मोड का उपयोग करें।"
        }[language]
    )

    district = st.selectbox(
        TEXT["district_select"][language],
        districts
    )

    soil_type = st.selectbox(
        TEXT["soil_type"][language],
        {
            "English": [
                "Black Soil",
                "Red Soil",
                "Loamy Soil",
                "Clay Soil",
                "Sandy Soil"
            ],
            "Kannada": [
                "ಕರಿ ಮಣ್ಣು",
                "ಕೆಂಪು ಮಣ್ಣು",
                "ಲೋಮಿ ಮಣ್ಣು",
                "ಜೇಡಿಮಣ್ಣು",
                "ಮರಳು ಮಣ್ಣು"
            ],
            "Hindi": [
                "काली मिट्टी",
                "लाल मिट्टी",
                "दोमट मिट्टी",
                "चिकनी मिट्टी",
                "रेतीली मिट्टी"
            ]
        }[language]
    )

    season = st.selectbox(
        TEXT["season"][language],
        {
            "English": ["Kharif", "Rabi", "Summer"],
            "Kannada": ["ಖರೀಫ್", "ರಬಿ", "ಬೇಸಿಗೆ"],
            "Hindi": ["खरीफ", "रबी", "ग्रीष्म"]
        }[language]
    )

    water_availability = st.selectbox(
        TEXT["water_availability"][language],
        {
            "English": ["Low", "Medium", "High"],
            "Kannada": ["ಕಡಿಮೆ", "ಮಧ್ಯಮ", "ಹೆಚ್ಚು"],
            "Hindi": ["कम", "मध्यम", "अधिक"]
        }[language]
    )

st.subheader(
    TEXT["irrigation_info"][language]
)



irrigation_soil_type = st.selectbox(
    TEXT["irrigation_soil"][language],
    {
        "English": ["Sandy", "Loamy", "Clay"],
        "Kannada": ["ಮರಳು", "ಲೋಮಿ", "ಜೇಡಿಮಣ್ಣು"],
        "Hindi": ["रेतीली", "दोमट", "चिकनी"]
    }[language]
)

soil_moisture = st.slider(
    TEXT["soil_moisture"][language],
    0.0,
    100.0,
    50.0
)

# ---------- PREDICT ----------
if st.button(TEXT["predict"][language]):

    if mode == TEXT["advanced"][language]:
        features = pd.DataFrame([{
            "N":N,
            "P":P,
            "K":K,
            "temperature":temperature,
            "humidity":humidity,
            "ph":ph,
            "rainfall":rainfall
        }])
        predicted_crop = model.predict(features)[0]
    else:
    # English
        if language == "English":

            if soil_type == "Black Soil":

                if water_availability == "High":
                    predicted_crop = "Cotton"
                else:
                    predicted_crop = "Jowar"

            elif soil_type == "Red Soil":

                if season == "Kharif":
                    predicted_crop = "Groundnut"
                else:
                    predicted_crop = "Ragi"

            elif soil_type == "Loamy Soil":

                if water_availability == "High":
                    predicted_crop = "Rice"
                else:
                    predicted_crop = "Maize"

            elif soil_type == "Clay Soil":
                predicted_crop = "Rice"

            else:
                predicted_crop = "Bajra"

    # Kannada
        elif language == "Kannada":

            if soil_type == "ಕರಿ ಮಣ್ಣು":

                if water_availability == "ಹೆಚ್ಚು":
                    predicted_crop = "Cotton"
                else:
                    predicted_crop = "Jowar"

            elif soil_type == "ಕೆಂಪು ಮಣ್ಣು":

                if season == "ಖರೀಫ್":
                    predicted_crop = "Groundnut"
                else:
                    predicted_crop = "Ragi"

            elif soil_type == "ಲೋಮಿ ಮಣ್ಣು":

                if water_availability == "ಹೆಚ್ಚು":
                    predicted_crop = "Rice"
                else:
                    predicted_crop = "Maize"

            elif soil_type == "ಜೇಡಿಮಣ್ಣು":
                predicted_crop = "Rice"

            else:
                predicted_crop = "Bajra"

    # Hindi
        else:

            if soil_type == "काली मिट्टी":

                if water_availability == "अधिक":
                    predicted_crop = "Cotton"
                else:
                    predicted_crop = "Jowar"

            elif soil_type == "लाल मिट्टी":

                if season == "खरीफ":
                    predicted_crop = "Groundnut"
                else:
                    predicted_crop = "Ragi"

            elif soil_type == "दोमट मिट्टी":

                if water_availability == "अधिक":
                    predicted_crop = "Rice"
                else:
                    predicted_crop = "Maize"

            elif soil_type == "चिकनी मिट्टी":
                predicted_crop = "Rice"

            else:
                predicted_crop = "Bajra"
    # ==========================
    # Crop Recommendation
    # ==========================

    st.success(
        f"{TEXT['best_crop'][language]}: {predicted_crop.upper()}"
    )
    st.divider()
    # ==========================
    # Climate Analysis
    # ==========================

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

    st.subheader(
        TEXT["climate_analysis"][language]
    )

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

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label=TEXT["best_crop"][language],
            value=predicted_crop.upper()
        )

    with col2:
        st.metric(
            label=TEXT["weather_safety"][language],
            value=locals().get("display_status", "N/A")
        )

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

    st.divider()
    # ==========================
    # Why BhoomiAI Recommended This Crop
    # ==========================

    st.subheader(
    TEXT["why_crop"][language]
    )

    reasons = []
    outlook_score = 0

    if mode == TEXT["simple_mode"][language]:

        reasons.append(
        TEXT["reason_simple"][language]
        )

        outlook_score += 30

    else:

        reasons.append(
        TEXT["reason_advanced"][language]
        )

        outlook_score += 30

    if weather_status == "Good":

        reasons.append(
        TEXT["reason_weather_good"][language]
        )

        outlook_score += 40

    elif weather_status == "Moderate":

        reasons.append(
        TEXT["reason_weather_moderate"][language]
        )

        outlook_score += 20

    else:

        reasons.append(
        TEXT["reason_weather_risk"][language]
        )

    if weather_status == "Good":

        reasons.append(
        TEXT["reason_weather_good"][language]
        )

        outlook_score += 30

    elif weather_status == "Moderate":

        reasons.append(
        TEXT["reason_weather_moderate"][language]
        )

        outlook_score += 15

    else:

        reasons.append(
        TEXT["reason_weather_risk"][language]
        )

    outlook_score = min(outlook_score, 100)

    if outlook_score >= 70:

        st.success(
        f"{TEXT['positive_outlook'][language]} ({outlook_score}/100)"
        )

    elif outlook_score >= 40:

        st.warning(
        f"{TEXT['neutral_outlook'][language]} ({outlook_score}/100)"
        )

    else:

        st.error(
        f"{TEXT['negative_outlook'][language]} ({outlook_score}/100)"
        )

    for reason in reasons:

        st.write(reason)
    st.divider()
    # ==========================
    # Yield Analysis
    # ==========================

    crop_data = production_df[
        production_df["Crop"]
        .astype(str)
        .str.lower()
        == predicted_crop.lower()
    ]

    if not crop_data.empty:

        avg_yield = crop_data["Yield"].mean()

        st.subheader(
            TEXT["yield_analysis"][language]
        )

        st.write(
            f"{TEXT['avg_yield'][language]}: {avg_yield:.2f}"
        )

        if avg_yield > 5:

            st.success(
            TEXT["good_harvest"][language]
            )

        elif avg_yield > 3:

            st.info(
                TEXT["average_harvest"][language]
            )

        else:

            st.warning(
                TEXT["low_harvest"][language]
            )
    st.divider()
    # ==========================
    # Market Price Analysis
    # ==========================

    st.subheader(
        TEXT["market_price"][language]
    )

    crop_price_data = market_df[
        market_df["Commodity"]
        .astype(str)
        .str.lower()
        .str.contains(
            predicted_crop.lower(),
            na=False
        )
    ]

    if not crop_price_data.empty:

        market_price = crop_price_data.iloc[0]["Modal Price"]

        st.success(
            f"{TEXT['current_price'][language]}: ₹{market_price:.2f} {TEXT['price_unit'][language]}"
        )

    else:

        st.warning(
            TEXT["price_not_found"][language]
        )
    st.divider()

    st.subheader(
        TEXT["negotiation_assistant"][language]
    )
    minimum_price = market_price * 0.90
    ideal_price = market_price
    premium_price = market_price * 1.10

    st.info(
    f"{TEXT['fair_range'][language]}: ₹{minimum_price:.0f} - ₹{premium_price:.0f}"
    )

    st.warning(
    f"{TEXT['avoid_below'][language]} ₹{minimum_price:.0f}"
    )

    if market_price > 3000:

        st.success(
        TEXT["market_favorable"][language]
        )

    else:

        st.warning(
        TEXT["market_low"][language]
        )
    st.divider()
    # ==========================
    # Income Estimation
    # ==========================

    if not crop_data.empty and not crop_price_data.empty:

        estimated_income = avg_yield * market_price

        st.subheader(
            TEXT["income_estimation"][language]
        )

        st.success(
            f"{TEXT['estimated_income'][language]}: ₹{estimated_income:,.2f}"
        )

        st.info(
            TEXT["income_note"][language]
        )
        st.divider()
        st.subheader(
            TEXT["top_crops"][language]
        )

        crop_rankings = []

        crop_rankings.append(
            (predicted_crop, estimated_income)
        )
    

    
    if mode == TEXT["simple_mode"][language]:

        temperature = 25.0
        humidity = 70.0
        ph = 6.5
        rainfall = 800.0
    
    # ==========================
    # Crop Ranking
    # ==========================

    # Alternative crops from weather analysis

    if weather_status == "Needs Care":

        crop_rankings.extend([
            ("Millet", estimated_income * 0.90),
            ("Maize", estimated_income * 0.85)
        ])

    elif weather_status == "Moderate":

        crop_rankings.extend([
            ("Groundnut", estimated_income * 0.95),
            ("Maize", estimated_income * 0.90)
        ])

    else:

        crop_rankings.extend([
            ("Rice", estimated_income * 0.95),
            ("Maize", estimated_income * 0.90)
        ])

    crop_rankings = sorted(
        crop_rankings,
        key=lambda x: x[1],
        reverse=True
    )

    col1, col2, col3 = st.columns(3)

    for col, (crop, income) in zip(
        [col1, col2, col3],
        crop_rankings[:3]
    ):

        with col:

            st.metric(
                crop.upper(),
                f"₹{income:,.0f}"
            )
    

    st.metric(
        crop.upper(),
        f"₹{income:,.0f}",
        help=TEXT["expected_income"][language]
    )
    st.divider()
    # ==========================
    # Irrigation Prediction
    # ==========================

    st.subheader(
        TEXT["irrigation_prediction"][language]
    )

    irrigation_input = pd.DataFrame([{
        "Soil_Type": irrigation_soil_type,
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


    irrigation_levels = {
    "Low": {
        "English": "Low",
        "Kannada": "ಕಡಿಮೆ",
        "Hindi": "कम"
    },
    "Medium": {
        "English": "Medium",
        "Kannada": "ಮಧ್ಯಮ",
        "Hindi": "मध्यम"
    },
    "High": {
        "English": "High",
        "Kannada": "ಹೆಚ್ಚು",
        "Hindi": "अधिक"
    }
    }

    display_irrigation = irrigation_levels.get(
        irrigation_need,
        {}
    ).get(language, irrigation_need)

    st.success(
        f"{TEXT['irrigation_need'][language]}: {display_irrigation}"
    )
    st.divider()
    # ==========================
    # Save Prediction
    # ==========================
    st.success(
        TEXT["saved"][language]
    )
    pdf_file = generate_report(
        predicted_crop,
        display_status,
        market_price,
        estimated_income,
        irrigation_need
    )

    st.download_button(
        label=TEXT["download_report"][language],
        data=open(pdf_file, "rb"),
        file_name="farmer_report.pdf",
        mime="application/pdf"
    )

    cursor.execute("""
    INSERT INTO predictions (
    language,
    district,
    recommended_crop,
    weather_status,
    irrigation_need
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
    language,
    district,
    predicted_crop,
    weather_status,
    irrigation_need
    ))

    conn.commit()   
   
    st.divider()

    
    st.subheader(
    TEXT["summary"][language]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
        TEXT["best_crop"][language],
        predicted_crop.upper()
        )

    with col2:
        st.metric(
        TEXT["weather_safety"][language],
        display_status
        )

    with col3:
        st.metric(
        TEXT["price"][language],
        f"₹{market_price:.0f}"
        )

    with col4:
        st.metric(
        TEXT["income"][language],
        f"₹{estimated_income:.0f}"
        )
    st.divider()

   