"""
Yango ride/delivery widget link builder — no API key required for this mode.
Docs: https://yango.com/en_int/partner-program/documentation/
"""
from urllib.parse import urlencode

YANGO_WIDGET_BASE = "https://yango.go.link/route"

def build_ride_widget_link(
    *, start_lat: float, start_lon: float, end_lat: float, end_lon: float,
    ref: str = "ananse-mcp", lang: str = "en",
) -> str:
    params = {
        "start-lat": start_lat, "start-lon": start_lon,
        "end-lat": end_lat, "end-lon": end_lon,
        "ref": ref, "lang": lang,
    }
    return f"{YANGO_WIDGET_BASE}?{urlencode(params)}"
