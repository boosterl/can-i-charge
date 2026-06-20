from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from asyncio import CancelledError
from click import echo
from can_i_charge.api import get_station, StationNotFoundError

status_icon_map = {
    "occupied": "🚫",
    "available": "✅",
}


async def get_charging_status(stations, api_key, verbose):
    async with ClientSession() as session:
        for station_id in stations:
            try:
                station = await get_station(session, api_key, station_id)
                echo(f"📍 Station: {station['shortAddress']}")
                for charge_point in station["chargePoints"]:
                    status = charge_point["status"].lower()
                    status_icon = status_icon_map.get(status, "❓")
                    echo(
                        f"    - Connector {charge_point['evseId']} is {status} {status_icon}"
                    )
                    for connector in charge_point["connectors"]:
                        print_connector_details(connector, station, verbose)
            except StationNotFoundError:
                echo(
                    f"No data returned for {station_id}, check station id", err=True
                )
            except (CancelledError, ClientError, TimeoutError) as err:
                echo(err, err=True)


def print_connector_details(connector, station, verbose):
    if verbose < 1:
        return
    echo(f"      Connector type: {connector['plugTypeName']}")
    echo(f"      Max power: {connector['maxPowerInKw']}kW")
    if verbose < 2:
        return
    echo(f"      Latitude: {station['lat']}")
    echo(f"      Longitude: {station['lon']}")
