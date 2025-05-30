import streamlit as st
import pandas as pd
from weather_report import fetch_weather, API_KEY
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def create_and_save_plots(df):
    # Set the style for better-looking plots
    plt.style.use('seaborn-v0_8')  # Using a valid style name
    
    # Set the color palette
    colors = sns.color_palette("husl", len(df))
    
    # Figure 1: Temperature comparison with error bars
    plt.figure(figsize=(12, 6))
    plt.bar(df['city'], df['temperature'], 
            yerr=df['temperature'].std()/2,  # Add error bars
            alpha=0.7,
            color=colors)
    plt.title('Temperature Comparison Across Cities', pad=20)
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('temperature_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Figure 2: Weather metrics comparison
    plt.figure(figsize=(12, 6))
    width = 0.35
    x = range(len(df['city']))
    
    plt.bar([i - width/2 for i in x], df['temperature'], 
            width, label='Temperature (°C)', color='coral')
    plt.bar([i + width/2 for i in x], df['humidity'], 
            width, label='Humidity (%)', color='skyblue')
    
    plt.title('Temperature and Humidity Comparison', pad=20)
    plt.xlabel('City')
    plt.ylabel('Value')
    plt.xticks(x, df['city'], rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig('weather_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Figure 3: Wind speed distribution
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='city', y='wind_speed', palette='husl')
    plt.title('Wind Speed Distribution by City', pad=20)
    plt.xlabel('City')
    plt.ylabel('Wind Speed (m/s)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('wind_speed_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def analyze_and_save_report(df):
    # Create plots first
    create_and_save_plots(df)
    
    # Analyze data
    highest_temp_city = df.loc[df['temperature'].idxmax()]
    lowest_temp_city = df.loc[df['temperature'].idxmin()]
    avg_temp = df['temperature'].mean()
    clear_sky_cities = df[df['description'].str.contains('clear|sunny', case=False, regex=True)]
    
    # Create report
    report = f"""Weather Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

Temperature Analysis:
Highest Temperature: {highest_temp_city['temperature']:.1f}°C in {highest_temp_city['city']}
Lowest Temperature: {lowest_temp_city['temperature']:.1f}°C in {lowest_temp_city['city']}
Average Temperature: {avg_temp:.1f}°C

Weather Conditions:

Cities with clear/sunny weather: {len(clear_sky_cities)}
These cities are: {', '.join(clear_sky_cities['city'].tolist()) if not clear_sky_cities.empty else 'None'}

Detailed City Information:
-----------------------"""

    # Add detailed information for each city
    for _, city_data in df.iterrows():
        report += f"\n\n{city_data['city']}:"
        report += f"\n  Temperature: {city_data['temperature']:.1f}°C"
        report += f"\n  Humidity: {city_data['humidity']}%"
        report += f"\n  Wind Speed: {city_data['wind_speed']} m/s"
        report += f"\n  Weather: {city_data['description']}"

    report += "\n\nNote: Additional visualizations have been saved as:"
    report += "\n- temperature_comparison.png (Temperature comparison across cities)"
    report += "\n- weather_metrics.png (Temperature and humidity comparison)"
    report += "\n- wind_speed_distribution.png (Wind speed distribution)"

    # Save report to file
    with open('summary_report.txt', 'w') as f:
        f.write(report)
    
    return report

st.set_page_config(page_title="Weather Report Dashboard", layout="wide")

st.title("📊 Weather Report Dashboard")

# Sidebar for city input
st.sidebar.header("Add Cities")
new_city = st.sidebar.text_input("Enter a city name")
if st.sidebar.button("Add City"):
    if new_city:
        with open("cities.txt", "a") as f:
            f.write(f"\n{new_city}")
        st.sidebar.success(f"Added {new_city} to the list!")

# Read existing cities
with open("cities.txt", "r") as f:
    cities = [line.strip() for line in f if line.strip()]

st.sidebar.header("Current Cities")
st.sidebar.write(", ".join(cities))

# Fetch weather data for all cities
weather_data = []
for city in cities:
    data = fetch_weather(city)
    if data:
        weather_data.append(data)

if weather_data:
    # Convert to DataFrame
    df = pd.DataFrame(weather_data)
    
    # Generate and save report
    report = analyze_and_save_report(df)
    
    # Display current time
    st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create three columns for key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Highest Temperature", 
                 f"{max(df['temperature']):.1f}°C",
                 f"in {df.loc[df['temperature'].idxmax(), 'city']}")
    
    with col2:
        st.metric("Lowest Temperature", 
                 f"{min(df['temperature']):.1f}°C",
                 f"in {df.loc[df['temperature'].idxmin(), 'city']}")
    
    with col3:
        st.metric("Average Temperature", 
                 f"{df['temperature'].mean():.1f}°C")
    
    with col4:
        clear_sky_count = len(df[df['description'].str.contains('clear|sunny', case=False, regex=True)])
        st.metric("Clear Sky Cities", 
                 f"{clear_sky_count}",
                 f"out of {len(df)} cities")

    # Temperature visualization
    st.subheader("Temperature Comparison")
    fig_temp = px.bar(df, 
                     x='city', 
                     y='temperature',
                     color='temperature',
                     labels={'temperature': 'Temperature (°C)', 'city': 'City'},
                     title="Temperature by City")
    st.plotly_chart(fig_temp, use_container_width=True)

    # Weather details table
    st.subheader("Detailed Weather Information")
    st.dataframe(df.style.format({'temperature': '{:.1f}°C',
                                 'humidity': '{:.0f}%',
                                 'wind_speed': '{:.1f} m/s'}),
                hide_index=True,
                use_container_width=True)

    # Humidity visualization
    st.subheader("Humidity Levels")
    fig_humidity = px.bar(df,
                         x='city',
                         y='humidity',
                         color='humidity',
                         labels={'humidity': 'Humidity (%)', 'city': 'City'},
                         title="Humidity by City")
    st.plotly_chart(fig_humidity, use_container_width=True)

    # Display the report in an expandable section
    with st.expander("View Detailed Analysis Report"):
        st.text(report)

else:
    st.warning("No weather data available. Please check your city list and API key.") 