# 🔆 Enhancing Urban Environments: Smart Street Lighting using LSTM-DNN Hybrid AI

A final year capstone project exploring the integration of artificial intelligence with smart city infrastructure to optimize energy usage in urban environments. This study leverages a hybrid model that combines Long Short-Term Memory (LSTM) networks and Deep Neural Networks (DNN) to forecast streetlight energy consumption using real-time weather data.

---

## 📌 Project Summary

- **Goal:** Predict future streetlight energy usage based on weather patterns using deep learning.
- **Model:** Custom-built hybrid AI framework (LSTM → DNN) for sequence learning and integration.
- **Impact:** A step toward intelligent and adaptive street lighting systems for smart cities.
- **Application:** Optimizing public energy systems based on climate-aware predictions.

---

## 💡 Key Features

- 📊 **Data Granularity:** Weather and energy usage data collected every **15 minutes** over 6 years.
- 🧠 **Dual AI Modeling:** Two independent LSTM models (for LED usage & weather), combined through a DNN.
- 🎯 **Bayesian Optimization:** Efficient hyperparameter tuning across thousands of combinations.
- 🌦️ **Climate-Aware Predictions:** Integration of multiple weather features (e.g., temp, humidity, solar radiation).
- 🌍 **Smart City Relevance:** Real-world application for urban sustainability and energy efficiency.

---

## 🧪 Methodology

### 1. Data Collection
- **Streetlight Energy Usage:** Collected from Las Vegas city dataset (15 locations, 2014–2016).
- **Weather Data:** Retrieved via Weatherbit API (2010–2016), aligned with energy usage timestamps.
- ~200,000 datapoints across both datasets.

### 2. Data Preprocessing & EDA
- Feature reduction via correlation analysis (Pearson, Kendall, Mutual Info).
- Interpolation for missing time slices.
- Aligned and normalized both datasets using `MinMaxScaler`.

### 3. LSTM Modelling
- Trained separate LSTM models:
  - `LSTM_1`: Streetlight energy usage
  - `LSTM_2`: Weather sequences
- Forecast horizon: **12 hours (96 timesteps)**

### 4. Hybrid LSTM-DNN Model
- Combined LSTM outputs via `Concatenate + Dense` layers
- Optimized with **Bayesian Hyperparameter Search**
- Evaluated with MSE, MAE, R²

---

## 📊 Results

| Model             | MAE     | MSE     | R²     |
|------------------|---------|---------|--------|
| LSTM (Energy)    | 0.0909  | 0.0190  | 0.63   |
| LSTM (Weather)   | 0.0730  | 0.0163  | 0.86   |
| LSTM-DNN Hybrid  | 0.0328  | 0.0033  | -0.003 |

- **Insight:** While the hybrid model showed low point-wise error (MAE/MSE), it struggled to generalize patterns (low R²), suggesting future improvements are needed in architecture or input engineering.
- **Conclusion:** This work demonstrates that combining sequence-aware models improves short-term accuracy in public energy forecasting.

---

## 📁 Project Structure
```
smart-streetlight-energy/
├── data/                 # Processed LED and weather datasets
├── notebooks/            # EDA and model development notebooks
├── scripts/              # Preprocessing and model training scripts
├── models/               # Saved model weights and tuning results
├── dissertation.pdf      # Final year thesis document
├── requirements.txt      # Dependencies
└── README.md             # You’re here!
```

---

## 🧑‍💻 How to Run the Project
### ✅ Prerequisites
- Python 3.12+
- Install dependencies:
```bash
cd/venv/Scripts
pip install -r requirements.txt
```

### ▶️ Execution Flow
1.	preprocess_led.py, preprocess_weather.py – Clean & align datasets
2.	split_led.py, split_weather.py – Segment into train/val/test
3.	lstm_led.py, lstm_weather.py – Train LSTM models
4.	hybrid_lstm_dnn.py – Combine via DNN and evaluate predictions

---

## 📄 Dataset & License
- **Streetlight Data:** [City of Las Vegas (Data.World)](https://data.world/city-of-las-vegas/las-vegas-streetlights)
- **Weather Data:** [Weatherbit.io API](https://www.weatherbit.io/) – Non-commercial use only
- **License:** This project is for academic and research purposes only.

---

## Documentation
For a detailed explanation of this project, refer to the [Dissertation Document](https://github.com/yenijung/smartcityproject/blob/507c805023b146975f72258de2b13bc41918e333/23%3A24%20final%20year%20project%20.pdf).
