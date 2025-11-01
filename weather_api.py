from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Any, Dict

app = FastAPI(title="RT-TAR Weather Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def _geocode_city(name: str) -> Dict[str, Any] | None:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={httpx.utils.quote(name)}&count=1"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results")
        if not results:
            return None
        return results[0]


@app.get("/v1/geocode")
async def geocode(city: str):
    res = await _geocode_city(city)
    if not res:
        raise HTTPException(status_code=404, detail="City not found")
    return res


@app.post("/v1/weather")
async def weather_proxy(payload: Dict[str, Any]):
    city = payload.get("city")
    date = payload.get("date")
    lat = payload.get("lat")
    lon = payload.get("lon")

    if not date:
        raise HTTPException(status_code=400, detail="`date` is required")

    if city and (lat is None or lon is None):
        geo = await _geocode_city(str(city))
        if not geo:
            raise HTTPException(status_code=404, detail="City not found")
        lat = geo.get("latitude")
        lon = geo.get("longitude")

    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="Provide either `city` or both `lat` and `lon`")

    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&start_date={date}&end_date={date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=auto"
    )

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

        daily = data.get("daily", {})
        if not daily or not daily.get("time"):
            raise HTTPException(status_code=404, detail="No data available for that date/location")

        idx = 0
        return {
            "date": daily.get("time")[idx],
            "temperature_max": daily.get("temperature_2m_max")[idx],
            "temperature_min": daily.get("temperature_2m_min")[idx],
            "precipitation_sum": daily.get("precipitation_sum")[idx],
            "weathercode": daily.get("weathercode")[idx] if daily.get("weathercode") else None,
            "latitude": lat,
            "longitude": lon,
        }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))
