import requests
from datetime import datetime

def get_sky_condition(code):
    conditions = {
        0:  "☀️  Clear Sky",
        1:  "🌤️  Mainly Clear",
        2:  "⛅  Partly Cloudy",
        3:  "☁️  Overcast",
        45: "🌫️  Foggy",
        48: "🌫️  Icy Fog",
        51: "🌦️  Light Drizzle",
        53: "🌦️  Moderate Drizzle",
        55: "🌧️  Dense Drizzle",
        61: "🌧️  Slight Rain",
        63: "🌧️  Moderate Rain",
        65: "🌧️  Heavy Rain",
        71: "🌨️  Slight Snow",
        73: "🌨️  Moderate Snow",
        75: "❄️  Heavy Snow",
        80: "🌦️  Slight Showers",
        81: "🌧️  Moderate Showers",
        82: "⛈️  Violent Showers",
        95: "⛈️  Thunderstorm",
        99: "⛈️  Thunderstorm + Hail",
    }
    return conditions.get(code, "🌡️ Unknown")


def get_coordinates(city):
    url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1&language=en&format=json"
    )
    response = requests.get(url)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return None

    result = data["results"][0]
    return (
        result["latitude"],
        result["longitude"],
        result["name"],
        result.get("country", "")
    )


def get_wind_direction(degree):
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degree / 45) % 8
    return dirs[index]


def get_weather(city):
    print(f"\n⏳ Fetching weather data for '{city}'...")

    coords = get_coordinates(city)
    if coords is None:
        print(f"\n❌ City '{city}' not found. Please enter a valid city name.")
        return

    lat, lon, city_name, country = coords

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,"
        f"relative_humidity_2m,weather_code,"
        f"wind_speed_10m,wind_direction_10m,"
        f"precipitation,precipitation_probability"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,"
        f"precipitation_probability_max,precipitation_sum,"
        f"wind_speed_10m_max"
        f"&timezone=auto&forecast_days=7"
    )

    response = requests.get(url)
    data = response.json()

    if "current" not in data:
        print("❌ Failed to retrieve weather data. Please try again.")
        return

    c = data["current"]
    d = data["daily"]

    print("\n" + "═" * 52)
    print(f"   🌍  {city_name}, {country}".center(52))
    print(f"   🕐  Updated: {c['time'].replace('T', '  ')}".center(52))
    print("═" * 52)

    print(f"\n  {'─' * 46}")
    print(f"   📍  Current Weather")
    print(f"  {'─' * 46}")

    temp       = c["temperature_2m"]
    feels      = c["apparent_temperature"]
    humidity   = c["relative_humidity_2m"]
    sky        = get_sky_condition(c["weather_code"])
    wind_speed = c["wind_speed_10m"]
    wind_dir   = get_wind_direction(c["wind_direction_10m"])
    rain_prob  = c.get("precipitation_probability", 0)
    rain_mm    = c.get("precipitation", 0.0)

    print(f"   🌡️  Temperature       : {temp}°C  (Feels like {feels}°C)")
    print(f"   {sky.split()[0]}  Sky Condition     : {' '.join(sky.split()[1:])}")
    print(f"   🌧️  Chance of Rain    : {rain_prob}%")
    print(f"   💧  Rainfall Amount   : {rain_mm} mm")
    print(f"   💨  Wind              : {wind_speed} km/h  Direction: {wind_dir}")
    print(f"   💦  Humidity          : {humidity}%")

    print(f"\n  {'─' * 46}")
    print(f"   📅  7-Day Forecast")
    print(f"  {'─' * 46}\n")

    for i in range(7):
        date_str  = d["time"][i]
        date_obj  = datetime.strptime(date_str, "%Y-%m-%d")
        day_label = date_obj.strftime("%A, %d %b")

        max_t  = d["temperature_2m_max"][i]
        min_t  = d["temperature_2m_min"][i]
        sky_d  = get_sky_condition(d["weather_code"][i])
        r_prob = d["precipitation_probability_max"][i]
        r_sum  = d["precipitation_sum"][i]
        wind_d = d["wind_speed_10m_max"][i]

        print(f"   📆  {day_label}")
        print(f"       {sky_d}")
        print(f"       🌡️  {min_t}°C ~ {max_t}°C  |  🌧️ {r_prob}% ({r_sum}mm)  |  💨 {wind_d} km/h")
        print()

    print("═" * 52 + "\n")


if __name__ == "__main__":
    print("╔══════════════════════════════════════╗")
    print("║      🌤️  Weather Forecast Terminal      ║")
    print("╚══════════════════════════════════════╝")
    city_input = input("\n🏙️  Enter city name: ")
    get_weather(city_input.strip())