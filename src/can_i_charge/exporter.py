import logging

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from asyncio import CancelledError
from prometheus_client import Enum, Gauge
from can_i_charge.api import get_station, StationNotFoundError
from time import sleep

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

evse_status_map = {
    "AVAILABLE": "Available",
    "OCCUPIED": "Occupied",
    "OUT_OF_SERVICE": "Unavailable",
}

metrics = {
    "address": Gauge(
        "cic_address",
        "Address information",
        ["station_id", "address", "latitude", "longitude"],
    ),
    "evse_status": Enum(
        "cic_evse_status",
        "Status of evse",
        ["station_id", "address", "latitude", "longitude", "evse_id"],
        states=["Available", "Unavailable", "Occupied", "Unknown"],
    ),
    "evse_updated": Gauge(
        "cic_evse_updated",
        "Evse last updated time",
        ["station_id", "address", "latitude", "longitude", "evse_id"],
    ),
    "operator_name": Gauge(
        "cic_operator_name",
        "Operator name",
        ["station_id", "address", "latitude", "longitude", "operator_name"],
    ),
    "station_exists": Gauge("cic_station_exists", "Station Exists", ["station_id"]),
    "connector_power": Gauge(
        "cic_connector_power",
        "Connector power",
        ["station_id", "address", "latitude", "longitude", "evse_id", "connector_id"],
    ),
}

logger = logging.getLogger(__name__)


def set_metrics(station, found):
    if not found:
        metrics["station_exists"].labels(station_id=station).set(0)
        return
    station_id = str(station["stationId"])
    address = station["shortAddress"]
    latitude = station["lat"]
    longitude = station["lon"]
    metrics["address"].labels(
        station_id=station_id,
        address=address,
        latitude=latitude,
        longitude=longitude,
    ).set(1)
    metrics["operator_name"].labels(
        station_id=station_id,
        address=address,
        latitude=latitude,
        longitude=longitude,
        operator_name=station["operator"],
    ).set(1)
    metrics["station_exists"].labels(station_id=station_id).set(1)
    for evse in station["chargePoints"]:
        evse_id = evse["evseId"]
        status = evse_status_map.get(evse["status"], "Unknown")
        metrics["evse_status"].labels(
            station_id=station_id,
            address=address,
            latitude=latitude,
            longitude=longitude,
            evse_id=evse_id,
        ).state(status)
        metrics["evse_updated"].labels(
            station_id=station_id,
            address=address,
            latitude=latitude,
            longitude=longitude,
            evse_id=evse_id,
        ).set(evse["state"]["updatedAt"] / 1000)
        for i, connector in enumerate(evse["connectors"]):
            connector_id = str(i + 1)
            metrics["connector_power"].labels(
                station_id=station_id,
                address=address,
                latitude=latitude,
                longitude=longitude,
                evse_id=evse_id,
                connector_id=connector_id,
            ).set(connector["maxPowerInKw"] * 1000)


async def run_metrics_loop(stations, api_key, interval):
    async with ClientSession() as session:
        while True:
            for station_id in stations:
                try:
                    station = await get_station(session, api_key, station_id)
                    set_metrics(station, True)
                except StationNotFoundError:
                    set_metrics(station_id, False)
                except (CancelledError, ClientError, TimeoutError) as err:
                    logger.error(
                        f"An exception occured while connecting with the API: {err}"
                    )
            sleep(interval)
