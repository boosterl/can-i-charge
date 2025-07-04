from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from asyncio import CancelledError
from click import echo
from shellrecharge import Api, LocationEmptyError, LocationValidationError

status_icon_map = {
    "occupied": "🚫",
    "available": "✅",
}


async def get_charging_status(stations, verbose):
    async with ClientSession() as session:
        api = Api(session)
        for station_id in stations:
            try:
                location = await api.location_by_id(station_id)
                if not location:
                    echo(f"Error connecting with API")
                    continue
                echo(
                    f"📍 Station: {location.address.streetAndNumber}, {location.address.postalCode} {location.address.city}"
                )
                for evse in location.evses:
                    status_icon = status_icon_map.get(evse.status.lower(), "❓")
                    echo(
                        f"    - Connector {evse.uid} is {evse.status.lower()} {status_icon}"
                    )
                    for connector in evse.connectors:
                        print_connector_details(connector, verbose)
            except LocationEmptyError:
                echo(f"No data returned for {station_id}, check station id", err=True)
            except LocationValidationError as err:
                echo(f"Location validation error {err}, report station id", err=True)
            except (CancelledError, ClientError, TimeoutError) as err:
                echo(err, err=True)


def print_connector_details(connector, verbose):
    if verbose < 1:
        return
    echo(f"      Connector type: {connector.connectorType}")
    echo(f"      Max power: {connector.electricalProperties.maxElectricPower}kW")
    if verbose < 2:
        return
    echo(f"      Power type: {connector.electricalProperties.powerType}")
    echo(f"      Voltage: {connector.electricalProperties.voltage}V")
    echo(f"      Amperage: {connector.electricalProperties.amperage}A")
