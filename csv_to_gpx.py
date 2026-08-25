import csv, sys
from xml.sax.saxutils import escape

def convert(csv_path, gpx_path):
    columns = [
        "loc_id", "country_code", "subnational1_code", "subnational2_code",
        "latitude", "longitude", "locality", "latest_obs_date",
        "num_species_all_time", "num_species_last_30"
    ]
    waypoints = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0].strip():
                continue
            rec = dict(zip(columns, row + [""] * (len(columns) - len(row))))
            try:
                lat = float(rec["latitude"])
                lon = float(rec["longitude"])
            except ValueError:
                continue
            name = rec["locality"].strip() or rec["loc_id"]
            desc_parts = []
            if rec.get("num_species_all_time"):
                desc_parts.append(f"{rec['num_species_all_time']} species all-time")
            if rec.get("num_species_last_30"):
                desc_parts.append(f"{rec['num_species_last_30']} species last 30 days")
            if rec.get("latest_obs_date"):
                desc_parts.append(f"latest obs {rec['latest_obs_date']}")
            desc_parts.append(f"eBird ID {rec['loc_id']}")
            desc = " | ".join(desc_parts)
            waypoints.append((lat, lon, name, desc))

    with open(gpx_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<gpx version="1.1" creator="ebird-hotspot-converter" '
                'xmlns="http://www.topografix.com/GPX/1/1" '
                'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 '
                'http://www.topografix.com/GPX/1/1/gpx.xsd">\n')
        for lat, lon, name, desc in waypoints:
            f.write(f'  <wpt lat="{lat:.7f}" lon="{lon:.7f}">\n')
            f.write(f'    <name>{escape(name)}</name>\n')
            f.write(f'    <desc>{escape(desc)}</desc>\n')
            f.write(f'    <sym>Bird</sym>\n')
            f.write('  </wpt>\n')
        f.write('</gpx>\n')
    return len(waypoints)

if __name__ == "__main__":
    n = convert(sys.argv[1], sys.argv[2])
    print(f"Wrote {n} waypoints to {sys.argv[2]}")
