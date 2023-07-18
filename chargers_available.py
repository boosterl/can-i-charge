import requests

status_icon_map = {
    "occupied": "🚫",
    "available": "✅",
}

charging_stations = {
    "Overzet": "3039876",
    "Einde Were": "3595319",
    "Krijgsgasthuisstraat": "3456460",
    "Johannes Schranstraat": "2593755",
    "Groenevalleilaan": "3459060",
}

for station_name, station_id in charging_stations.items():
    api_response = requests.get(f"https://ui-map.shellrecharge.com/api/map/v2/locations/{station_id}").json()
    print(f"Status of charging stations {station_name}")
    connector_count = 1
    for connector in api_response.get("evses", []):
        status = connector.get("status", "unknown").lower()
        status_icon = status_icon_map.get(status, "❓")
        print(f"Connector {connector_count} is {status} {status_icon}")
        connector_count += 1

