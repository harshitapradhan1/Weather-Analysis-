def analyze_data(data):
    temps = [d["temperature"] for d in data]
    clear_skies = [d for d in data if "clear" in d["description"].lower()]

    max_temp = max(data, key=lambda x: x["temperature"])
    min_temp = min(data, key=lambda x: x["temperature"])
    avg_temp = sum(temps) / len(temps)

    summary = f"""
Weather Summary Report
----------------------
City with highest temperature: {max_temp["city"]} ({max_temp["temperature"]}°C)
City with lowest temperature: {min_temp["city"]} ({min_temp["temperature"]}°C)
Average temperature: {avg_temp:.2f}°C
Cities with clear sky or similar: {len(clear_skies)}
    """.strip()
    return summary

def generate_plot(data):
    import matplotlib.pyplot as plt
    cities = [d['city'] for d in data]
    temps = [d['temperature'] for d in data]

    plt.figure(figsize=(10, 5))
    plt.bar(cities, temps, color='skyblue')
    plt.xlabel('Cities')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Comparison')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/temperature_chart.png')
    plt.close()
