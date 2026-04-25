"""Chain GeoJSON LineString features into a connected path from a start coord
to the start of Dani.gpx, then prepend the resulting points as <trkpt> entries
to Dani.gpx (original is preserved in Dani.gpx.bak)."""
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).parent
GEOJSON = Path(r"c:\Users\toron\AppData\Local\Temp\04c368ee-e9eb-4dab-995a-95c1aa606a51_pasted.zip.a51\pasted1.json")
GPX = HERE / "Dani.gpx"

# user-stated start (lat, lon) — convert to (lon, lat)
START = (8.58102495551904, 47.403485404992445)


def haversine(a, b):
    R = 6371000.0
    lon1, lat1 = a
    lon2, lat2 = b
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    h = math.sin(dp/2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(h))


def main():
    geo = json.loads(GEOJSON.read_text(encoding="utf-8"))
    feats = [f["geometry"]["coordinates"] for f in geo["features"]]

    gpx_text = GPX.read_text(encoding="utf-8")
    m = re.search(r'<trkpt\s+lat="([\d\.\-]+)"\s+lon="([\d\.\-]+)"', gpx_text)
    if not m:
        raise SystemExit("could not find first trkpt in GPX")
    end_pt = (float(m.group(2)), float(m.group(1)))  # (lon, lat)
    print(f"GPX start (target): {end_pt}")
    print(f"User start:         {START}")

    used = [False] * len(feats)
    chain = [START]
    cursor = START

    SNAP_TOL = 60.0
    while True:
        best_i, best_rev, best_d = -1, False, float("inf")
        for i, coords in enumerate(feats):
            if used[i]:
                continue
            d_start = haversine(cursor, tuple(coords[0]))
            d_end = haversine(cursor, tuple(coords[-1]))
            if d_start < best_d:
                best_d, best_i, best_rev = d_start, i, False
            if d_end < best_d:
                best_d, best_i, best_rev = d_end, i, True
        if best_i < 0:
            break

        coords = feats[best_i][:]
        if best_rev:
            coords.reverse()

        d_now = haversine(cursor, end_pt)
        d_after = haversine(tuple(coords[-1]), end_pt)
        if best_d > SNAP_TOL and d_after >= d_now:
            break

        used[best_i] = True
        if haversine(chain[-1], tuple(coords[0])) < 1.0:
            chain.extend(coords[1:])
        else:
            chain.extend(coords)
        cursor = tuple(chain[-1])

        if haversine(cursor, end_pt) < 30.0:
            break

    print(f"Chained: {len(chain)} pts; last={cursor}; "
          f"to GPX start = {haversine(cursor, end_pt):.1f} m")

    # build trkpt block — leave a tiny gap so the original first point still
    # exists; just prepend before the existing first <trkpt>.
    new_pts = "\n".join(
        f'   <trkpt lat="{lat:.7f}" lon="{lon:.7f}">\n    <ele>430.0</ele>\n   </trkpt>'
        for lon, lat in chain
    )

    if "<trkseg>" not in gpx_text:
        raise SystemExit("could not find <trkseg> in GPX")

    backup = GPX.with_suffix(".gpx.bak")
    if not backup.exists():
        backup.write_text(gpx_text, encoding="utf-8")
        print(f"backup: {backup}")

    new_gpx = gpx_text.replace("<trkseg>", "<trkseg>\n" + new_pts, 1)
    GPX.write_text(new_gpx, encoding="utf-8")
    print(f"wrote {GPX} (+{len(chain)} prepended points)")


if __name__ == "__main__":
    main()
