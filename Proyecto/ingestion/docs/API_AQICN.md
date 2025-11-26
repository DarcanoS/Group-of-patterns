# Copilot instructions – AQICN / WAQI JSON API ingestion in Python

You are helping to implement a Python 3 ingestion component for a university project called **“Air Quality Platform”**.

Your main goal is to generate clean, well-structured Python code that **reads real-time air quality data** from the World Air Quality Index (AQICN / WAQI) JSON API and exposes it through a small, reusable client module. This client will later be used by a separate ingestion pipeline to persist data into PostgreSQL / TimescaleDB, so focus here on **HTTP calls and parsing**, not on database code.

---

## General guidelines

- Use **Python 3.11+** compatible code.
- Use the **`requests`** library for HTTP calls (or `httpx` only if it is already imported in the project).
- Do **not** hard-code secrets:
  - Read the API token from an environment variable, preferably `AQICN_TOKEN`.
  - Optionally accept the token as an explicit constructor argument.
- Write **small, composable functions** and one small client class instead of a single monolithic script.
- Add **type hints**, `@dataclass` models where useful, and clear docstrings.
- Prefer returning **parsed Python objects** instead of raw untyped JSON dictionaries.

---

## API overview (read-only JSON API)

Implement a client for the **AQICN / WAQI JSON API**:

- **Base URL**: `https://api.waqi.info`
- All requests must include a **`token` query parameter** with a valid API key.
- Every response is JSON with a top-level structure similar to:

  ```json
  {
    "status": "ok" | "error",
    "data": ...
  }
````

* For simple tests you may support the public `demo` token, but clearly document that it only works for Shanghai and should never be used in production.

The client you generate must only use **read-only endpoints** (no upload APIs).

---

## Endpoints the client MUST support

Design a class `AqicnClient` that encapsulates all HTTP access to the API.

### 1. Search stations / cities

* HTTP: `GET /search/?keyword={keyword}&token={token}`
* Purpose: find monitoring stations or cities by free-text keyword (e.g. `"london"`).
* Typical response: a list of station summaries with fields like `uid`, `aqi`, `time`, and `station` (name, geo, url).
* Add a method with a clear signature, for example:

```python
def search_stations(self, keyword: str) -> list[StationSearchResult]:
    """Search AQICN stations by free-text keyword (city or station name)."""
```

Where `StationSearchResult` is a `@dataclass` that holds at least:

* `uid: int`
* `aqi: int | None`
* `name: str`
* `latitude: float`
* `longitude: float`
* `url_slug: str`
* `timezone: str | None`
* `last_update: datetime | None`

---

### 2. City / station feed by slug

* HTTP: `GET /feed/{station_slug}/?token={token}`
* `station_slug` is typically the `station.url` field from the search endpoint (e.g. `"london"`).
* Purpose: get the **current AQI, pollutants, weather and metadata** for a given city/station.
* The response includes fields like:

  * `data.aqi` (overall AQI)
  * `data.dominentpol`
  * `data.iaqi` (per-pollutant values: `pm25`, `pm10`, `no2`, `o3`, `so2`, `co`, etc.)
  * `data.city` (name, geo, url)
  * `data.time` (timestamp, timezone)
  * `data.forecast` (if available)
* Add a method, for example:

```python
def get_station_feed(self, slug: str) -> AqiStationFeed:
    """
    Fetch AQI data for a station using its slug (e.g. 'london').

    Returns a parsed AqiStationFeed object with overall AQI, per-pollutant indices,
    timestamps and basic station metadata.
    Raises AqicnApiError on API or HTTP errors.
    """
```

Define an `AqiStationFeed` dataclass that exposes at least:

* `aqi: int | None`
* `dominant_pollutant: str | None`
* `city_name: str`
* `city_geo: tuple[float, float] | None`
* `time: datetime | None`
* `timezone: str | None`
* `pollutants: dict[str, float]` (parsed from `iaqi`, keyed by pollutant code)
* Optional: `forecast` and `attributions` as structured fields.

---

### 3. Station feed by numeric UID

* HTTP: `GET /feed/@{uid}/?token={token}`
* `uid` is the numeric station identifier returned by the search endpoint.
* Purpose: fetch the same kind of feed as in (2), but using a numeric ID.
* Add a convenience method that internally calls the same parsing logic as `get_station_feed`:

```python
def get_station_feed_by_uid(self, uid: int) -> AqiStationFeed:
    """Fetch AQI data for a station using its numeric UID."""
```

---

### 4. Feed by geographic coordinates

* HTTP: `GET /feed/geo:{lat};{lon}/?token={token}`
* Purpose: get AQI from the **nearest** station to a given latitude/longitude.
* Add a method:

```python
def get_geo_feed(self, lat: float, lon: float) -> AqiStationFeed:
    """Fetch AQI data for the station nearest to the given latitude/longitude."""
```

Internally reuse the same parsing code as for the other feed methods.

---

### 5. Stations within map bounds (optional but useful)

* HTTP: `GET /map/bounds/?latlng={box}&token={token}`
* `box` is a comma-separated bounding box string (e.g. `"lon1,lat1,lon2,lat2"`).
* Purpose: list stations and their AQI inside a geographic bounding box (for heatmaps and coverage checks).
* Add a dataclass and method, for example:

```python
@dataclass
class BoundedStation:
    name: str
    latitude: float
    longitude: float
    aqi: int | None

def get_stations_in_bounds(self, box: str) -> list[BoundedStation]:
    """Return stations and AQI values within the given bounding box."""
```

---

## Client structure and helper methods

Implement `AqicnClient` roughly like this:

```python
class AqicnClient:
    def __init__(self, token: str | None = None, base_url: str = "https://api.waqi.info", timeout: float = 10.0):
        # Load token from env if not provided
        ...

    def _request(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Internal helper: perform a GET request to `base_url + path`,
        always adding the `token` query param, handling:
        - HTTP errors (non-2xx)
        - Network errors (timeouts, connection issues)
        - API-level errors where JSON['status'] != 'ok'
        Returns the decoded JSON's 'data' field on success.
        """

    # Public methods:
    # - search_stations(...)
    # - get_station_feed(...)
    # - get_station_feed_by_uid(...)
    # - get_geo_feed(...)
    # - get_stations_in_bounds(...)
```

Implementation requirements:

* Always raise a custom exception class like `AqicnApiError(Exception)` when:

  * HTTP status is not 2xx,
  * or the JSON `status` field is `"error"`,
  * or the response is malformed.
* Parse integers and floats safely:

  * Convert AQI strings to integers when needed.
  * Use `.get()` and sensible defaults when fields are missing.
* Support a configurable `timeout` for all HTTP calls.
* Optionally support a simple retry mechanism (e.g. 1–3 retries on timeouts or 5xx responses).

---

## Rate limiting and acceptable usage

Even though the public documentation mentions a high default quota, treat the API as a shared public resource:

* Add a simple, optional **client-side delay** between requests for batch jobs (e.g. configurable `min_interval_seconds`).
* Do **not** generate code that:

  * re-sells AQICN data,
  * uses it for paid services,
  * or caches and redistributes historical data beyond what is needed for this educational project.

Document clearly in comments that this client is intended for **non-commercial, educational use**.

---

## Coding style and examples

* Follow **PEP 8** naming and formatting.
* Add concise docstrings explaining:

  * what each method does,
  * its arguments,
  * its return type,
  * and when it raises `AqicnApiError`.
* Include a small usage example in a guarded main block:

```python
if __name__ == "__main__":
    # Example: quick manual test
    client = AqicnClient()
    results = client.search_stations("Bogota")
    if results:
        feed = client.get_station_feed(results[0].url_slug)
        print(f"City: {feed.city_name}, AQI: {feed.aqi}, dominant pollutant: {feed.dominant_pollutant}")
```

---

## What NOT to do

* Do **not** hard-code the API token.
* Do **not** create database models, ORM code or SQL here; keep this module strictly focused on HTTP access and JSON parsing.
* Do **not** implement any of the data-upload APIs; this client is strictly **read-only**.

When I ask you to *"create or update the AQICN ingestion client"*, generate or modify the `aqicn_client.py` module accordingly, following all the rules, endpoints and design constraints described above.



[1]: https://aqicn.org/api/?utm_source=chatgpt.com "Air Quality Programmatic APIs"
[2]: https://aqicn.org/data-platform/api/A378508/es/?utm_source=chatgpt.com "API de plataforma de datos abiertos sobre calidad del aire"
[3]: https://developer.vonage.com/ja/blog/build-an-air-quality-reporting-service-with-messages-api?utm_source=chatgpt.com "Build an Air Quality Reporting Service With Messages API"
[4]: https://stackoverflow.com/questions/71767603/retrieving-data-from-the-air-quality-index-aqi-website-through-the-api-and-onl?utm_source=chatgpt.com "Retrieving data from the Air Quality Index (AQI) website ..."
