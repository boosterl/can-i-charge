import requests

class ShellRechargeApi:
    base_url = "https://ui-map.shellrecharge.com/api/map/v2"

    def get_station_info(self, station_id):
        return requests.get(f"{self.base_url}/locations/{station_id}").json()

    def get_station_connectors(self, station_id):
        station = self.get_station_info(station_id)
        return station.get("evses", [])

    def get_station_connectors_statuses(self, station_id):
        connectors = self.get_station_connectors(station_id)
        return [connector.get("status", "unknown").lower() for connector in connectors]
