ENBW_API_URL = (
    "https://enbw-emp.azure-api.net/emobility-public-api/api/v1/chargestations/{}"
)


class StationNotFoundError(Exception):
    pass


async def get_station(session, api_key, station_id):
    url = ENBW_API_URL.format(station_id)
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Accept": "application/json",
        "Origin": "https://www.enbw.com",
        "Referer": "https://www.enbw.com/",
    }
    async with session.get(url, headers=headers) as response:
        if response.status == 404:
            raise StationNotFoundError(station_id)
        response.raise_for_status()
        return await response.json()
