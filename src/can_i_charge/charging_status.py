import aiohttp
import click
import shellrecharge

from asyncio import CancelledError
from aiohttp.client_exceptions import ClientError
from shellrecharge import LocationEmptyError, LocationValidationError


status_icon_map = {
    "occupied": "🚫",
    "available": "✅",
}


async def get_charging_status(location_ids):
    async with aiohttp.ClientSession() as session:
        api = shellrecharge.Api(session)
        for location_id in location_ids:
            try:
                location = await api.location_by_id(location_id)
                click.echo(f"Status for station {location.address.streetAndNumber}, {location.address.postalCode} {location.address.city}")
                for evses in location.evses:
                    status_icon = status_icon_map.get(evses.status.lower(), "❓")
                    click.echo(
                        f"Connector {evses.uid} is {evses.status.lower()} {status_icon}"
                    )
            except LocationEmptyError:
                click.echo(f"No data returned for {location_id}, check location id")
            except LocationValidationError as err:
                click.echo(
                    "Location validation error {}, report location id".format(err)
                )
            except (ClientError, TimeoutError, CancelledError) as err:
                click.echo(err)
