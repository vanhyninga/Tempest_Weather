import requests
import pandas as pd
import pytz
from datetime import datetime

# Provided endpoint
url = 'https://swd.weatherflow.com/swd/rest/observations/station/83925?token={}'

response = requests.get(url)

def celsius_to_fahrenheit(temp):
    """Convert Celsius temperature to Fahrenheit."""
    return (temp * 9/5) + 32

if response.status_code == 200:
    data = response.json()

   
    if 'obs' in data:
        df = pd.DataFrame(data['obs'])

        
        required_columns = ['air_temperature', 'timestamp', 'feels_like', 'heat_index', 'relative_humidity', 'wind_chill']
        df_filtered = df[[col for col in required_columns if col in df.columns]]

        
        for column in ['air_temperature', 'feels_like', 'heat_index', 'wind_chill']:
            if column in df_filtered.columns:
                df_filtered.loc[:, column] = df_filtered[column].apply(celsius_to_fahrenheit)
        
        
        if 'timestamp' in df_filtered.columns:
         df_filtered.loc[:, 'timestamp'] = df_filtered['timestamp'].apply(
        lambda x: datetime.utcfromtimestamp(x).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Pacific')).replace(tzinfo=None)
    )


        
        file_path = 'C:/Users/vanhy/OneDrive/Documents/filtered_weather_data.xlsx'
        df_filtered.to_excel(file_path, index=False, engine='openpyxl')
        print(f"Filtered data saved to {file_path}")

    else:
        print("The 'obs' key was not found in the returned data.")

else:
    print("Error fetching data:", response.status_code)
    print(response.text)

