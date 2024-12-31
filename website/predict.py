import http.client
import json
import csv
from datetime import datetime, timedelta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
import pdb
from urllib.parse import urlencode


def fetch_weather_data(city):
    # Get today's date and the date 7 days ago
    today = datetime.today()
    seven_days_ago = today - timedelta(days=6)
    
    # Format dates to strings
    today_str = today.strftime('%Y-%m-%d')
    seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d')

    # API Connection to RapidAPI Weather API
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")
    params =urlencode({"q": city})
    headers = {
           'x-rapidapi-key': "4765efd0e4msh0e6f4310f441125p115acdjsnc5b407e62f78",
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }

    # API URL to fetch historical weather data
    url = f"/history.json?{params}&lang=en&dt={seven_days_ago_str}&end_dt={today_str}"

    # Make the API request
    conn.request("GET", url, headers=headers)

    # Get the response
    res = conn.getresponse()
    data = res.read()
    

    # Parse the JSON response
 
    weather_data = json.loads(data.decode("utf-8"))
   
    return weather_data



def convert_to_csv(weather_data, city):
    header = ["Date", "AvgTemp", "Humidity", "WindSpeed", "Precipitation", "Condition"]
    rows = []

    # Loop through the forecast data and add each day's weather information
    for day in weather_data['forecast']['forecastday']:
        rows.append([
            day['date'],  # Date
            day['day']['avgtemp_c'],  # Average Temperature (Celsius)
            day['day']['avghumidity'],  # Average Humidity
            day['day']['maxwind_kph'],  # Max Wind Speed (kph)
            day['day']['totalprecip_mm'],  # Precipitation (mm)
            day['day']['condition']['text']  # Weather Condition (text)
        ])
    
    # Write the data to a CSV file using the csv module
    csv_filename = f"{city}_weather_data.csv"
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header row
        writer.writerows(rows)  # Write the weather data

    print(f"CSV file '{csv_filename}' created successfully.")


def preprocess_data(csv_filename):
     # Load the CSV data into a DataFrame
    df = pd.read_csv(csv_filename)
    print(df)
    
    df['Date'] = pd.to_datetime(df['Date'])

    # Drop the 'Date' column as it's not useful for prediction
    df = df.drop(columns=["Date"])
    df = df.drop(columns=['Condition'])
  

    # Handle missing values (simple imputation strategy)
    # imputer = SimpleImputer(strategy="mean")
    # df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    # Feature columns (excluding the target column 'AvgTemp')
    print(df)
  
    X = df.drop(columns=["AvgTemp"])
    print('x is',X)
   
    print(f"Shape of X input after scaling: {X.shape}")

    # Target column (assuming you're predicting 'AvgTemp')
    y = df["AvgTemp"]
    print('y is',y)
    
    X = X.values

    # Normalize the features (optional)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Shape of X_scaled:", X_scaled.shape)
    
    return X_scaled, y,scaler


def split_data(X, y):
    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test



def train_model(X_train, y_train):
    # Initialize the XGBoost model
    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, random_state=42)
    
    # Train the model
    print('xtrain is ',X_train)
    print('ytrain is ',y_train)
    
    print(X_train.shape[1])
    model.fit(X_train, y_train)
    
    return model


def evaluate_model(model, X_test, y_test):
    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model using Mean Absolute Error (MAE)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error: {mae:.2f}")

    # You can also print predicted vs actual values if needed
    comparison = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
    print(comparison.head())
    


def predict_next_day_temperature(model, input_data):
    # Make a prediction for the next day's temperature
   
    
    print(input_data)
    
    predicted_temp = model.predict(input_data)
   
    print(f"Predicted temperature for next day: {predicted_temp[0]:.2f}°C")
    



import random
import numpy as np
def predict_next_7_days(model, last_known_data, scaler, days=7):
    print(last_known_data)
    

    predictions = []
    
    # Get the last known input data (scaled and encoded)
    current_input = last_known_data
    
    
    last_known_humidity = current_input[0, 0]  # Assuming 2nd column is Humidity
    last_known_windspeed = current_input[0, 1]  # Assuming 3rd column is WindSpeed
    last_known_precipitation = current_input[0, 2]  # Assuming 4th column is Precipitation
   
    for day in range(days):
       
        print('current data is ',current_input)
        
        prediction = model.predict(current_input)
        
        print('first data prediction is ',prediction)
        predictions.append(prediction[0]) 

        
        # Simulate small random changes in weather features
        next_day_humidity = last_known_humidity + np.random.normal(0, 100)  
        next_day_windspeed = last_known_windspeed + np.random.normal(0, 50)  
        next_day_precipitation = last_known_precipitation + np.random.normal(0, 0.9)  

    
        
       
        new_data_point = np.array([[ next_day_humidity, next_day_windspeed, next_day_precipitation]])
       
        print('data shape ',new_data_point)
        current_input = scaler.transform(new_data_point) 
       
        
    return predictions

def predictcity(city):
    
    # weather_data=fetch_weather_data(city)
    # convert_to_csv(weather_data,city)
    X_scaled, y,scaler = preprocess_data(f"{city}_weather_data.csv")
    X_train, X_test, y_train, y_test = split_data(X_scaled, y)
    print(X_train.shape[1])
    
    model = train_model(X_train, y_train)
    
    evaluate_model(model, X_test, y_test)
    input_data = [[26.4, 81, 22]] 
    
    predict_next_day_temperature(model, input_data)
    
    
    X_scaled, y, scaler = preprocess_data(f"{city}_weather_data.csv")
   

# Assume the model is already trained, and we have the last known data point (e.g., the last row from the dataset)
    last_known_data = X_scaled[-1:]  # Use the last row as the input for prediction
    
# Make predictions for the next 7 days
    predictions = predict_next_7_days(model, last_known_data, scaler, days=7)
    
# Print or display the predictions for the next 7 days
    for i, prediction in enumerate(predictions, 1):
        print(f"Day {i}: Predicted AvgTemp = {prediction:.2f}°C")
    predictions = [float(prediction) for prediction in predictions]
    return predictions
