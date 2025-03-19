import requests
import os
from dotenv import load_dotenv

load_dotenv('../.env')
api_key = os.getenv('WEATHER_API_KEY')


def current_weather(location: str, unit: str = "celsius") -> str:
    if not api_key:
        return "Error: WEATHER_API_KEY not found in environment variables"

    response = requests.get(
        'https://api.weatherapi.com/v1/current.json',
        params={
            'key': api_key,
            'q': location,
            'aqi': 'no',
        }
    )

    if response.status_code != 200:
        return f"Error: API request failed with status code {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
        current = data['current']
        
        temp = current['temp_c'] if unit == 'celsius' else current['temp_f']
        feels_like = current['feelslike_c'] if unit == 'celsius' else current['feelslike_f']
        temp_unit = '°C' if unit == 'celsius' else '°F'
        
        condition = current['condition']['text']
        wind_kph = current['wind_kph']
        wind_dir = current['wind_dir']
        humidity = current['humidity']
        cloud = current['cloud']
        uv = current['uv']
        

        weather_report = f"""
Current weather in {location}:
Temperature: {temp}{temp_unit}
Feels like: {feels_like}{temp_unit}
Condition: {condition}
Wind: {wind_kph} km/h, direction {wind_dir}
Humidity: {humidity}%
Cloud cover: {cloud}%
UV index: {uv}
"""
        return weather_report.strip()
    
    except requests.exceptions.JSONDecodeError:
        return f"Error: Unable to parse JSON response. Response content: {response.text}"
    except KeyError as e:
        return f"Error: Unexpected response format. Missing key: {str(e)}. Response: {data}"


def forecast_weather(location: str, days, unit: str = 'celsius'):
    if not api_key:
        return "Error: WEATHER_API_KEY not found in environment variables"

    response = requests.get(
        'https://api.weatherapi.com/v1/forecast.json',
        params={
            'key': api_key,
            'q': location,
            'days': days,
            'aqi': 'no',
        }
    )

    if response.status_code != 200:
        return f"Error: API request failed with status code {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
        forecast = data['forecast']['forecastday']

        temp_unit = '°C' if unit == 'celsius' else '°F'
        forecast_report = f"Weather Forecast for {location} for the next {days} days:\n"

        for day in forecast:
            date = day['date']
            condition = day['day']['condition']['text']
            high_temp = day['day']['maxtemp_c'] if unit == 'celsius' else day['day']['maxtemp_f']
            low_temp = day['day']['mintemp_c'] if unit == 'celsius' else day['day']['mintemp_f']

            forecast_report += (
                f"\nDate: {date}\n"
                f"Condition: {condition}\n"
                f"High: {high_temp}{temp_unit}\n"
                f"Low: {low_temp}{temp_unit}\n"
                "-------------------------"
            )

        return forecast_report.strip()
    except requests.exceptions.JSONDecodeError:
        return f"Error: Unable to parse JSON response. Response content: {response.text}"
    except KeyError as e:
        return f"Error: Unexpected response format. Missing key: {str(e)}. Response: {data}"
    except requests.exceptions.JSONDecodeError:
        return f"Error: Unable to parse JSON response. Response content: {response.text}"


if __name__ == "__main__":
    result = forecast_weather("thessaloniki", 3)
    print(result)