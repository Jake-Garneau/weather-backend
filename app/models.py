from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# models created to match schema script
class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    timezone = Column(String, nullable=False)
    timezone_offset = Column(Integer, nullable=False)
    
    __table_args__ = (UniqueConstraint('lat', 'lon', name='_lat_lon_uc'),)

class CurrentWeather(Base):
    __tablename__ = "current_weather"

    id = Column(Integer, primary_key=True, index=True)
    dt = Column(DateTime(timezone=True), nullable=False)
    sunrise = Column(DateTime(timezone=True))
    sunset = Column(DateTime(timezone=True))
    temp = Column(Float)
    feels_like = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)
    dew_point = Column(Float)
    uvi = Column(Float)
    clouds = Column(Integer)
    visibility = Column(Integer)
    wind_speed = Column(Float)
    wind_deg = Column(Integer)
    wind_gust = Column(Float)
    weather_id = Column(Integer)
    weather_main = Column(String)
    weather_description = Column(String)
    weather_icon = Column(String)
    location_id = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), nullable=False)

class HourlyWeather(Base):
    __tablename__ = "hourly_weather"

    id = Column(Integer, primary_key=True, index=True)
    dt = Column(DateTime(timezone=True), nullable=False)
    temp = Column(Float)
    feels_like = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)
    dew_point = Column(Float)
    uvi = Column(Float)
    clouds = Column(Integer)
    visibility = Column(Integer)
    wind_speed = Column(Float)
    wind_deg = Column(Integer)
    wind_gust = Column(Float)
    pop = Column(Float)
    weather_id = Column(Integer)
    weather_main = Column(String)
    weather_description = Column(String)
    weather_icon = Column(String)
    location_id = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), nullable=False)

class DailyWeather(Base):
    __tablename__ = "daily_weather"

    id = Column(Integer, primary_key=True, index=True)
    dt = Column(DateTime(timezone=True), nullable=False)
    sunrise = Column(DateTime(timezone=True))
    sunset = Column(DateTime(timezone=True))
    moonrise = Column(DateTime(timezone=True))
    moonset = Column(DateTime(timezone=True))
    moon_phase = Column(Float)
    summary = Column(String)
    temp_day = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    temp_night = Column(Float)
    temp_eve = Column(Float)
    temp_morn = Column(Float)
    feels_like_day = Column(Float)
    feels_like_night = Column(Float)
    feels_like_eve = Column(Float)
    feels_like_morn = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)
    dew_point = Column(Float)
    wind_speed = Column(Float)
    wind_deg = Column(Integer)
    wind_gust = Column(Float)
    clouds = Column(Integer)
    pop = Column(Float)
    rain = Column(Float)
    snow = Column(Float)
    uvi = Column(Float)
    weather_id = Column(Integer)
    weather_main = Column(String)
    weather_description = Column(String)
    weather_icon = Column(String)
    location_id = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), nullable=False)