# Enhancing Urban Environments: The Smart Street Lighting Project using LSTM-DNN Hybrid Model 🔆

## Overview
This project explores the integration of artificial intelligence (AI) and urban planning to improve energy efficiency in smart city infrastructure. By utilizing a hybrid AI model that combines Long Short-Term Memory (LSTM) and Deep Neural Networks (DNN), this research predicts streetlight energy consumption based on weather patterns. The aim is to optimize energy usage while maintaining sustainability in urban lighting systems. 

### Key Features:
- **Advanced AI Models:** Implementation of LSTM and DNN hybrid models for accurate energy consumption prediction.
- **Data-Driven Insights:** Utilizes datasets on streetlight energy usage and weather conditions.
- **Energy Optimization:** Predicts future energy demands to enhance urban planning and energy efficiency.
- **Smart City Application:** Contributes to sustainable development of urban environments by optimizing streetlight operations.

## Methodology
- **Data Collection:** Streetlight energy usage data and weather data were collected at 15-minute intervals.
- **Data Preprocessing:** Extensive cleaning and feature selection to ensure accurate model input.
- **Model Development:** Separate LSTM models were created for energy usage and weather data, which were later combined into a DNN for integrated predictions.
- **Bayesian Optimization:** Hyperparameter tuning to ensure optimal model performance.

## Results
The hybrid LSTM-DNN model was able to predict streetlight energy usage based on weather patterns, providing a framework for smart energy management in urban environments. Future work involves improving model scalability and incorporating additional data types for even greater accuracy.

## Documentation
For a detailed explanation of this project, refer to the [Dissertation Document](https://github.com/yenijung/smartcityproject/blob/507c805023b146975f72258de2b13bc41918e333/23%3A24%20final%20year%20project%20.pdf)

## How to Run the Project
### Prerequisites
1. Install the latest version of pip.
2. Check your python version. (python 3.12.0)
3. Clone the git repository.
4. Navigate to the path.
```bash
cd/venv/Scripts
```  
5. Run the following command to install the libraries. The project will NOT run with these libraries.
```bash
pip install -r requirements.txt
```
### Code running order
1. preprocess_led.py, preprocess2_led.py
2. preprocess_weather.py
3. preprocess_length_both.py
4. split_led.py, split_weather.py
5. lstm_led.py, lstm_weather.py
6. hybrid_lstm_dnn.py

## License
This project is for academic and non-commercial purposes only, as specified in the dataset usage terms.
