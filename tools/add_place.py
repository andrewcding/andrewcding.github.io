"""Add a place to jsons/Places_Visited.geojson (shown on the travel map).

Usage:
    python tools/add_place.py "Lucerne"                    # geocodes via OpenStreetMap
    python tools/add_place.py "Lucerne" --lived            # mark as a place lived in
    python tools/add_place.py "Springfield" --country "United States"

Coordinates pasted from Google Maps (lat, lng — skips geocoding):
    python tools/add_place.py "Somewhere" --coords "44.90394354001831, 15.611562943579703"
    python tools/add_place.py "Somewhere" --coords 44.9039 15.6115

Multiple places at once:
    python tools/add_place.py "Lucerne" "Zug" "Bern"

The Country field is taken from the geocoder result unless --country is given.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEOJSON = os.path.join(ROOT, "jsons", "Places_Visited.geojson")

NOMINATIM = "https://nominatim.openstreetmap.org/search?{}"
HEADERS = {"User-Agent": "andrewding.ca-places-tool/1.0 (personal travel map)"}


def geocode(query):
    params = urllib.parse.urlencode({
        "q": query,
        "format": "jsonv2",
        "limit": 5,
        "addressdetails": 1,
        "accept-language": "en",
    })
    req = urllib.request.Request(NOMINATIM.format(params), headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def pick_result(name, results):
    if not results:
        print(f"  no geocoding results for '{name}'")
        return None
    for i, r in enumerate(results, 1):
        print(f"  [{i}] {r['display_name']}  ({float(r['lat']):.4f}, {float(r['lon']):.4f})")
    choice = input(f"  pick 1-{len(results)} (enter=1, s=skip): ").strip().lower()
    if choice == "s":
        return None
    idx = int(choice) - 1 if choice.isdigit() else 0
    return results[idx] if 0 <= idx < len(results) else results[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("names", nargs="+", help="place name(s) to add")
    ap.add_argument("--country", help="override the country name")
    ap.add_argument("--lived", action="store_true", help="mark as lived (star on the map)")
    ap.add_argument("--coords", nargs="+", metavar="LAT,LNG",
                    help="coordinates as given by Google Maps (lat, lng); "
                         "used instead of geocoding (single place only)")
    args = ap.parse_args()

    coords = None
    if args.coords:
        try:
            nums = [float(x) for x in re.split(r"[,\s]+", " ".join(args.coords).strip()) if x]
            lat, lng = nums
        except ValueError:
            sys.exit(f"could not parse --coords {' '.join(args.coords)!r}: "
                     "expected two numbers (lat, lng)")
        if not (-90 <= lat <= 90):
            sys.exit(f"latitude {lat} out of range — did you swap lat/lng?")
        coords = (lng, lat)

    if coords and len(args.names) > 1:
        sys.exit("--coords only works with a single place name")

    data = json.load(open(GEOJSON, encoding="utf-8"))
    features = data["features"]
    next_id = max(f["id"] for f in features) + 1
    existing = {(f["properties"]["PlaceName"], f["properties"]["Country"]) for f in features}

    added = 0
    for name in args.names:
        print(f"\n{name}:")
        if coords:
            lng, lat = coords
            country = args.country or input("  country: ").strip()
        else:
            result = pick_result(name, geocode(name))
            if result is None:
                continue
            lng, lat = float(result["lon"]), float(result["lat"])
            country = args.country or result.get("address", {}).get("country", "")
            if not country:
                country = input("  country: ").strip()
            time.sleep(1)  # Nominatim usage policy: max 1 request/second

        if (name, country) in existing:
            print(f"  already in the map ({name}, {country}) — skipped")
            continue

        features.append({
            "type": "Feature",
            "id": next_id,
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {
                "OBJECTID": next_id,
                "PlaceName": name,
                "Country": country,
                "Lived": 1 if args.lived else 0,
            },
        })
        print(f"  added: {name}, {country} ({lng:.5f}, {lat:.5f})"
              + (" [lived]" if args.lived else ""))
        next_id += 1
        added += 1

    if added:
        with open(GEOJSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\nsaved {added} place(s) -> jsons/Places_Visited.geojson "
              f"({len(features)} total)")
    else:
        print("\nnothing added")


if __name__ == "__main__":
    main()
