"""
We need to check whether LED dataset and Weather dataset have a correlation or not.
Following methods will be used:
1. Pearson Correlation Coefficient
2. Spearman Correlation Coefficient
3. Kendall Correlation Coefficient
4. Mutual Information
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the datasets
led = pd.read_csv('Datasets/preprocessed_led.csv', index_col='Start Date Time', parse_dates=True)
weather = pd.read_csv('Datasets/preprocessed_weather.csv', index_col='Start Date Time', parse_dates=True)
# Check if the start date time range is the same and if it is not, drop the rows that are not in the intersection
led.index = pd.to_datetime(led.index, format='%d/%m/%Y %H:%M:%S')
weather.index = pd.to_datetime(weather.index, format='%d/%m/%Y %H:%M:%S')
common_start = max(led.index.min(), weather.index.min())
common_end = min(led.index.max(), weather.index.max())
led_filtered = led[(led.index >= common_start) & (led.index <= common_end)]
weather_filtered = weather[(weather.index >= common_start) & (weather.index <= common_end)]
# Pivot the LED dataset and handle the NaN values
led_filtered = led_filtered.pivot_table(values='Usage', index=led_filtered.index, columns='Loc')

# As both dataset has seasonal pattern, correlation will be checked after differencing both datasets
# According to the analysis_led.py, the seasonal pattern is not shown through the decomposition
# but it was visible through daily plots. Therefore, the seasonal pattern is assumed to be daily.
def led_seasonal_diff(data, period=24*4):
    differenced = data.diff(periods=period)
    differenced = differenced.dropna()
    return differenced


# According to the analysis_weather.py, there is clear yearly pattern in the dataset.
# Therefore, the seasonal pattern is assumed to be yearly.
def weather_seasonal_diff(data, period=4*24*365):
    differenced = data.diff(periods=period)
    differenced = differenced.dropna()
    return differenced


# Seasonal differencing for both datasets
led_filtered = led_seasonal_diff(led_filtered)
weather_filtered = weather_seasonal_diff(weather_filtered)

# Combine the datasets
combined = led_filtered.join(weather_filtered, how='inner')
combined = combined.fillna(0)
usage_cols = combined.columns[:15].tolist()
weather_cols = combined.columns[15:].tolist()


# Pearson Correlation Coefficient
def pearson_corr(usage, weather, combined):
    usage_weather_df = combined[usage + weather]
    pearson_corr = usage_weather_df.corr(method='pearson')
    filtered = pearson_corr.loc[usage, weather]
    plt.figure(figsize=(12, 14))
    sns.heatmap(filtered, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Pearson Correlation Coefficient Heatmap between Usage and Weather Parameters')
    plt.xlabel('Weather Parameters')
    plt.ylabel('LED Locations')
    plt.savefig('Images/correlations_integrated/pearson_corr.png')
    plt.show()
    return pearson_corr


# Kendall Correlation Coefficient
def kendall_corr(usage, weather, combined):
    usage_weather_df = combined[usage + weather]
    kendall_corr = usage_weather_df.corr(method='kendall')
    filtered = kendall_corr.loc[usage, weather]
    plt.figure(figsize=(12, 14))
    sns.heatmap(filtered, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Kendall Correlation Coefficient Heatmap between Usage and Weather Parameters')
    plt.xlabel('Weather Parameters')
    plt.ylabel('LED Locations')
    plt.savefig('Images/correlations_integrated/kendall_corr.png')
    plt.show()
    return kendall_corr


# Mutual Information
def mutual_info(combined, usage, weather):
    from sklearn.feature_selection import mutual_info_regression
    mi_results = pd.DataFrame(index=weather, columns=usage)
    for param in weather:
        for loc in usage:
            X = combined[[param]].values.ravel()
            y = combined[loc].values.ravel()
            mi_score = mutual_info_regression(X.reshape(-1, 1), y)
            mi_results.loc[param, loc] = float(mi_score[0])
    plt.figure(figsize=(12, 14))
    sns.heatmap(mi_results.astype(float), annot=True, cmap='viridis', fmt='.2f')
    plt.title('Mutual Information Heatmap between Usage and Weather Parameters')
    plt.xlabel('Usage of Locations')
    plt.ylabel('Weather Parameters')
    plt.savefig('Images/correlations_integrated/mutual_info.png')
    plt.show()
    return mi_results


pearson_corr = pearson_corr(usage_cols, weather_cols, combined)
kendall_corr = kendall_corr(usage_cols, weather_cols, combined)
mi_results = mutual_info(combined, usage_cols, weather_cols)
print(pearson_corr)
print(kendall_corr)
print(mi_results)
