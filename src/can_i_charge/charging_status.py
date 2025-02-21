from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from asyncio import CancelledError
from click import echo
from shellrecharge import Api, LocationEmptyError, LocationValidationError

status_icon_map = {
    "occupied": "🚫",
    "available": "✅",
}


async def get_charging_status(location_ids):
    async with ClientSession() as session:
        api = Api(session)
        for location_id in location_ids:
            try:
                location = await api.location_by_id(location_id)
                echo(
                    f"📍 Station: {location.address.streetAndNumber}, {location.address.postalCode} {location.address.city}"
                )
                for evses in location.evses:
                    status_icon = status_icon_map.get(evses.status.lower(), "❓")
                    echo(
                        f"    - Connector {evses.uid} is {evses.status.lower()} {status_icon}"
                    )
            except LocationEmptyError:
                echo(f"No data returned for {location_id}, check location id")
            except LocationValidationError as err:
                echo(f"Location validation error {err}, report location id")
            except (CancelledError, ClientError, TimeoutError) as err:
                echo(err)
