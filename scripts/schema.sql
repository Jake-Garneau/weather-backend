DROP TABLE IF EXISTS daily_weather CASCADE; -- reset tables on startup
DROP TABLE IF EXISTS hourly_weather CASCADE;
DROP TABLE IF EXISTS current_weather CASCADE;
DROP TABLE IF EXISTS locations CASCADE;

-- tables based on json response from openweather current/forecasts api, exclude minutely and alerts
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    timezone TEXT NOT NULL,
    timezone_offset INTEGER NOT NULL,
    UNIQUE(lat, lon)  -- prevents duplicate locations
);

CREATE TABLE current_weather (
    id SERIAL PRIMARY KEY,
    dt TIMESTAMP NOT NULL,
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    temp FLOAT,
    feels_like FLOAT,
    pressure INTEGER,
    humidity INTEGER,
    dew_point FLOAT,
    uvi FLOAT,
    clouds INTEGER,
    visibility INTEGER,
    wind_speed FLOAT,
    wind_deg INTEGER,
    wind_gust FLOAT,
    weather_id INTEGER,
    weather_main TEXT,
    weather_description TEXT,
    weather_icon TEXT,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE
);

CREATE TABLE hourly_weather (
    id SERIAL PRIMARY KEY,
    dt TIMESTAMP NOT NULL,
    temp FLOAT,
    feels_like FLOAT,
    pressure INTEGER,
    humidity INTEGER,
    dew_point FLOAT,
    uvi FLOAT,
    clouds INTEGER,
    visibility INTEGER,
    wind_speed FLOAT,
    wind_deg INTEGER,
    wind_gust FLOAT,
    pop FLOAT,
    weather_id INTEGER,
    weather_main TEXT,
    weather_description TEXT,
    weather_icon TEXT,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE
);

CREATE TABLE daily_weather (
    id SERIAL PRIMARY KEY,
    dt TIMESTAMP NOT NULL,
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    moonrise TIMESTAMP,
    moonset TIMESTAMP,
    moon_phase FLOAT,
    summary TEXT,
    temp_day FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    temp_night FLOAT,
    temp_eve FLOAT,
    temp_morn FLOAT,
    feels_like_day FLOAT,
    feels_like_night FLOAT,
    feels_like_eve FLOAT,
    feels_like_morn FLOAT,
    pressure INTEGER,
    humidity INTEGER,
    dew_point FLOAT,
    wind_speed FLOAT,
    wind_deg INTEGER,
    wind_gust FLOAT,
    clouds INTEGER,
    pop FLOAT,
    rain FLOAT,
    snow FLOAT,
    uvi FLOAT,
    weather_id INTEGER,
    weather_main TEXT,
    weather_description TEXT,
    weather_icon TEXT,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE
);