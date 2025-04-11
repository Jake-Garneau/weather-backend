import os
import logging
import httpx
from datetime import datetime, timezone
from sqlalchemy import select
from app.db import async_session
from app.models import Location, CurrentWeather, HourlyWeather, DailyWeather

# weather API call
async def fetch_weather(lat: float, lon: float) -> dict:
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely, alerts",
        "appid": os.getenv("WEATHER_KEY"),
        "units": "imperial",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.openweathermap.org/data/3.0/onecall", params=params)
    if response.status_code != 200:
        logging.error("Weather fetch failed: %s", response.text)
        return {}
    return response.json()

# store json response
async def store_weather(data: dict):
    if not data:
        logging.error("No weather data to store.")
        return

    async with async_session() as session:
        async with session.begin():
            lat = data.get("lat")
            lon = data.get("lon")
            timezone_name = data.get("timezone")
            timezone_offset = data.get("timezone_offset")
            # get location from lat/lon
            result = await session.execute(select(Location).where(Location.lat == lat, Location.lon == lon))
            location = result.scalars().first()
            # make location if can't find
            if not location:
                location = Location(
                    lat=lat,
                    lon=lon,
                    timezone=timezone_name,
                    timezone_offset=timezone_offset
                )
                session.add(location)
                await session.flush()  # send location to db to use for other entries
            
            # convert timestamp to datetime (utc)
            def ts_to_utc(ts):
                return datetime.fromtimestamp(ts, tz=timezone.utc) if ts is not None else None
            
            # store current weather
            current = data.get("current", {})
            current_weather_info = current.get("weather", [{}])[0]
            current_weather = CurrentWeather(
                dt=ts_to_utc(current.get("dt")),
                sunrise=ts_to_utc(current.get("sunrise")),
                sunset=ts_to_utc(current.get("sunset")),
                temp=current.get("temp"),
                feels_like=current.get("feels_like"),
                pressure=current.get("pressure"),
                humidity=current.get("humidity"),
                dew_point=current.get("dew_point"),
                uvi=current.get("uvi"),
                clouds=current.get("clouds"),
                visibility=current.get("visibility"),
                wind_speed=current.get("wind_speed"),
                wind_deg=current.get("wind_deg"),
                wind_gust=current.get("wind_gust"),
                weather_id=current_weather_info.get("id"),
                weather_main=current_weather_info.get("main"),
                weather_description=current_weather_info.get("description"),
                weather_icon=current_weather_info.get("icon"),
                location_id=location.id
            )
            session.add(current_weather)

            # store hourly weather
            hourly_list = data.get("hourly", [])
            for hour in hourly_list:
                hour_weather_info = hour.get("weather", [{}])[0]
                hourly_weather = HourlyWeather(
                    dt=ts_to_utc(hour.get("dt")),
                    temp=hour.get("temp"),
                    feels_like=hour.get("feels_like"),
                    pressure=hour.get("pressure"),
                    humidity=hour.get("humidity"),
                    dew_point=hour.get("dew_point"),
                    uvi=hour.get("uvi"),
                    clouds=hour.get("clouds"),
                    visibility=hour.get("visibility"),
                    wind_speed=hour.get("wind_speed"),
                    wind_deg=hour.get("wind_deg"),
                    wind_gust=hour.get("wind_gust"),
                    pop=hour.get("pop"),
                    weather_id=hour_weather_info.get("id"),
                    weather_main=hour_weather_info.get("main"),
                    weather_description=hour_weather_info.get("description"),
                    weather_icon=hour_weather_info.get("icon"),
                    location_id=location.id
                )
                session.add(hourly_weather)

            # store daily weather
            daily_list = data.get("daily", [])
            for day in daily_list:
                day_weather_info = day.get("weather", [{}])[0]
                temp = day.get("temp", {})
                feels_like = day.get("feels_like", {})
                daily_weather = DailyWeather(
                    dt=ts_to_utc(day.get("dt")),
                    sunrise=ts_to_utc(day.get("sunrise")),
                    sunset=ts_to_utc(day.get("sunset")),
                    moonrise=ts_to_utc(day.get("moonrise")),
                    moonset=ts_to_utc(day.get("moonset")),
                    moon_phase=day.get("moon_phase"),
                    summary=day.get("summary"),
                    temp_day=temp.get("day"),
                    temp_min=temp.get("min"),
                    temp_max=temp.get("max"),
                    temp_night=temp.get("night"),
                    temp_eve=temp.get("eve"),
                    temp_morn=temp.get("morn"),
                    feels_like_day=feels_like.get("day"),
                    feels_like_night=feels_like.get("night"),
                    feels_like_eve=feels_like.get("eve"),
                    feels_like_morn=feels_like.get("morn"),
                    pressure=day.get("pressure"),
                    humidity=day.get("humidity"),
                    dew_point=day.get("dew_point"),
                    wind_speed=day.get("wind_speed"),
                    wind_deg=day.get("wind_deg"),
                    wind_gust=day.get("wind_gust"),
                    clouds=day.get("clouds"),
                    pop=day.get("pop"),
                    rain=day.get("rain"),
                    snow=day.get("snow"),
                    uvi=day.get("uvi"),
                    weather_id=day_weather_info.get("id"),
                    weather_main=day_weather_info.get("main"),
                    weather_description=day_weather_info.get("description"),
                    weather_icon=day_weather_info.get("icon"),
                    location_id=location.id
                )
                session.add(daily_weather)
        logging.info("Weather data stored successfully.")

async def job():
    cities = ["1","2","3"]
    
    for city in cities:
        lat = os.getenv(f"CITY{city}_LAT")
        lon = os.getenv(f"CITY{city}_LON")

        if not lat or not lon:
            logging.warning(f"Skipping CITY{city} — missing lat/lon in env")
            continue

        logging.info(f"Fetching weather for CITY{city} at {lat}, {lon}")
        try:
            data = await fetch_weather(lat,lon)
            if data:
                await store_weather(data)
        except Exception as e:
            logging.error(f"Failed to fetch/store weather for CITY{city}: {e}")