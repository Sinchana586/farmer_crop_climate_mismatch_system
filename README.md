# 🌾 Farmer Crop-Climate Mismatch Early Warning System

A multilingual smart farming assistant designed to help farmers make informed agricultural decisions through machine learning, climate analysis, irrigation prediction, market insights, and income estimation.

## 🚀 Features

- 🌱 Crop Recommendation using Machine Learning
- 🌦 Climate Risk Analysis based on district rainfall data
- 🌾 Yield Estimation
- 💰 Market Price Analysis
- 💵 Income Estimation
- 💧 Irrigation Requirement Prediction
- 🌍 Multilingual Support
  - English
  - Kannada
  - Hindi
- 👨‍🌾 Simple Farmer Mode (No soil test required)
- 🔬 Advanced Mode (Soil test based recommendations)
- 🗄 SQLite Database for Prediction History
- 📊 Interactive Streamlit Dashboard

---

## 🛠 Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- SQLite
- Joblib
- Machine Learning
- Data Analytics

---

## 📂 Project Structure

```text
farmer_crop_climate_mismatch_system/
│
├── app/
│   └── app.py
│
├── datasets/
│   ├── Crop_recommendation.csv
│   ├── district wise rainfall normal.csv
│   ├── India Agriculture Crop Production.csv
│   └── Price_Agriculture_commodities_Week.csv
│
├── models/
│   ├── random_forest_model.pkl
│   ├── irrigation_model.pkl
│   ├── irrigation_target_encoder.pkl
│   └── irrigation_feature_columns.pkl
│
├── screenshots/
├── farmer_data.db
├── requirements.txt
└── README.md
```

---

## 🎯 Application Modes

### 🔬 Advanced Mode

Suitable for users with soil test reports.

Inputs:
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

### 👨‍🌾 Simple Farmer Mode

Suitable for farmers without soil test reports.

Inputs:
- District
- Soil Type
- Season
- Water Availability

---

## 🤖 Machine Learning Models

| Model | Purpose |
|---------|---------|
| Random Forest | Crop Recommendation |
| Random Forest | Irrigation Prediction |

---

## 📊 System Outputs

The application provides:

- Recommended Crop
- Climate Risk Assessment
- Alternative Crop Suggestions
- Yield Estimation
- Market Price Analysis
- Income Estimation
- Irrigation Requirement Prediction

---

## ▶️ Installation & Execution

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/farmer_crop_climate_mismatch_system.git
cd farmer_crop_climate_mismatch_system
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app/app.py
```

---

## 🌍 Multilingual Support

The system supports:

- English
- Kannada (ಕನ್ನಡ)
- Hindi (हिन्दी)

All major inputs, outputs, recommendations, and alerts are available in the selected language.

---

## 🗄 Database Support

Prediction history is stored using SQLite.

Stored Information:
- Language
- District
- Recommended Crop
- Weather Status
- Irrigation Requirement
- Timestamp

---

## 📸 Screenshots

Add screenshots of:

- Home Dashboard
- Advanced Mode Prediction
- Simple Farmer Mode Prediction
- Climate Analysis
- Market Price Analysis
- Irrigation Prediction
- Prediction History

---

## 💡 Future Enhancements

- Live Weather API Integration
- Real-Time Market Price Updates
- Mobile Application
- Voice-Based Farmer Assistance
- AI Agricultural Chatbot
- Satellite-Based Crop Monitoring

---

## 👩‍💻 Author

**Sinchana L Gowda**

Aspiring AI/ML Engineer | Data Analytics Enthusiast | Smart Agriculture Solutions Developer

---

⭐ If you found this project useful, consider giving it a star.