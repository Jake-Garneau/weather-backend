from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import engine, get_db
from app.models import Base, Location, CurrentWeather
from app.weather import job
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database tables created.")
    
    # create scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", minutes=5, next_run_time=datetime.now())
    scheduler.start()
    logging.info("Scheduler started: job scheduled now, and every 5 minutes following.")

    # run the app
    yield

    # stop scheduler on shutdown
    scheduler.shutdown()
    logging.info("Scheduler shut down.")

app = FastAPI(lifespan=lifespan, title="Weather Data Service")
    
@app.get("/")
async def read_root():
    return {"message": "init main"}

# health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# manual trigger to run job
@app.get("/fetch_and_store")
async def manual_trigger():
    try:
        await job()
        return {"message": "Weather data fetched and stored."}
    except Exception as e:
        logging.error("Manual weather fetch failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch and store weather data.")

# api endpoint to get current weather, for testing
@app.get("/weather/current/{lat}/{lon}")
async def get_current_weather(lat: float, lon: float, db: AsyncSession = Depends(get_db)):
    # find location
    result = await db.execute(
        select(Location).where(Location.lat == lat, Location.lon == lon)
    )
    location = result.scalars().first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # fetch current weather for lat/lon
    result = await db.execute(
        select(CurrentWeather)
        .where(CurrentWeather.location_id == location.id)
        .order_by(CurrentWeather.dt.desc())
        .limit(1)
    )
    weather = result.scalars().first()

    if not weather:
        raise HTTPException(status_code=404, detail="No weather data found")

    return {
        "location": {
            "lat": location.lat,
            "lon": location.lon,
            "timezone": location.timezone
        },
        "weather": {
            "timestamp": weather.dt,
            "temp": weather.temp,
            "feels_like": weather.feels_like,
            "humidity": weather.humidity,
            "pressure": weather.pressure,
            "uvi": weather.uvi,
            "clouds": weather.clouds,
            "wind_speed": weather.wind_speed,
            "weather_main": weather.weather_main,
            "description": weather.weather_description,
            "icon": weather.weather_icon,
        }
    }
