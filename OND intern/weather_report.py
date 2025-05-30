import requests
import argparse
import json
import csv
from utils.helpers import analyze_data, generate_plot

API_KEY = 'a992a9688302dd6127082cfc3e97f9dc'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def read_cities(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def fetch_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    else:
        print(f"[!] Failed to fetch data for: {city}")
        return None

def save_data(data, output_file):
    if output_file.endswith(".json"):
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)
    elif output_file.endswith(".csv"):
        keys = data[0].keys()
        with open(output_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="Weather Data Analysis Tool")
    parser.add_argument('--input', type=str, default='cities.txt', help='Path to cities.txt')
    parser.add_argument('--output', type=str, default='weather_data.json', help='Output data file')
    parser.add_argument('--summary', type=str, default='summary_report.txt', help='Summary report file')
    parser.add_argument('--plot', action='store_true', help='Generate temperature plot')
    
    args = parser.parse_args()

    cities = read_cities(args.input)
    results = []

    for city in cities:
        data = fetch_weather(city)
        if data:
            results.append(data)

    if results:
        save_data(results, args.output)

        summary = analyze_data(results)
        with open(args.summary, 'w') as f:
            f.write(summary)
        print(summary)

        if args.plot:
            generate_plot(results)

if __name__ == "__main__":
    main()
