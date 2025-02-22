from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from asyncio import CancelledError
from click import echo
from shellrecharge import Api, LocationEmptyError, LocationValidationError

status_icon_map = {
    "occupied": "🚫",
    "available": "✅",
}


async def get_charging_status(stations):
    async with ClientSession() as session:
        api = Api(session)
        for station_id in stations:
            try:
                location = await api.location_by_id(station_id)
                echo(
                    f"📍 Station: {location.address.streetAndNumber}, {location.address.postalCode} {location.address.city}"
                )
                for evses in location.evses:
                    status_icon = status_icon_map.get(evses.status.lower(), "❓")
                    echo(
                        f"    - Connector {evses.uid} is {evses.status.lower()} {status_icon}"
                    )
            except LocationEmptyError:
                echo(f"No data returned for {station_id}, check station id")
            except LocationValidationError as err:
                echo(f"Location validation error {err}, report station id")
            except (CancelledError, ClientError, TimeoutError) as err:
                echo(err)
