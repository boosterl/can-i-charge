import json
from api import Api

status_icon_map = {
    "occupied": "🚫",
    "available": "✅",
}

with open("config.json") as config:
    config = json.load(config)

def init_api():
    api_name = config.get("api_name")
    return Api().get_api(api_name)

def print_charging_station_statuses(api):
    for station_name, station_id in config.get("charging_stations").items():
        print(f"Status of charging stations {station_name}")
        connector_count = 1
        for status in api.get_station_connectors_statuses(station_id):
            status_icon = status_icon_map.get(status, "❓")
            print(f"Connector {connector_count} is {status} {status_icon}")
            connector_count += 1

if __name__ == "__main__":
    api = init_api()
    if api:
        print_charging_station_statuses(api)
    else:
        print(f"{config.get('api_name')} is not a valid charging station API")
