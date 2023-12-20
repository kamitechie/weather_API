import requests
import smtplib
import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()

# ----------NOW TIME-------- #

time_now = dt.datetime.now()
hour_now = time_now.hour

# ---------- API ---------- #

my_email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
LAT = 69.623380
LON = 18.764940
api_key = os.getenv("API_KEY")

parameters = {
    "lat": LAT,
    "lon": LON,
    "key": api_key,
    "days": 2
}

response = requests.get("http://api.weatherapi.com/v1/forecast.json?key=24ef4a1521424ea3b5942824232202&q=69.623380,18.764940&days=2&aqi=no&alerts=no")
response.raise_for_status()

data = response.json()
day_forecast = data["forecast"]["forecastday"]
hourly_forecast = data["forecast"]["forecastday"][0]["hour"]

print(day_forecast[0]["day"]["daily_will_it_rain"])
rain_list = []
for every in hourly_forecast[7:18]:
    time = every["time"]
    rain = every["will_it_rain"]
    rain_list.append(rain)

print(rain_list)
if 1 in rain_list:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=os.getenv("TO_EMAIL"),
                            msg=f"Subject:Rain Warning!\n\nBring an umbrella.")