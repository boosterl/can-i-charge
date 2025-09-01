import logging

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from asyncio import CancelledError
from datetime import datetime
from prometheus_client import start_http_server, Enum, Gauge
from random import randrange
from shellrecharge import Api, LocationEmptyError, LocationValidationError
from time import sleep

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

connector_properties = {
    "connector_amperage": "amperage",
    "connector_power": "maxElectricPower",
    "connector_voltage": "voltage",
}

metrics = {
    "address": Gauge(
        "cic_address",
        "Address information",
        ["station_id", "address", "street", "postal_code", "city", "country"],
    ),
    "evse_status": Enum(
        "cic_evse_status",
        "Status of evse",
        ["station_id", "address", "evse_id"],
        states=["Available", "Unavailable", "Occupied", "Unknown"],
    ),
    "evse_updated": Gauge(
        "cic_evse_updated",
        "Evse last updated time",
        ["station_id", "address", "evse_id"],
    ),
    "operator_name": Gauge(
        "cic_operator_name", "Operator name", ["station_id", "address", "operator_name"]
    ),
    "station_exists": Gauge("cic_station_exists", "Station Exists", ["station_id"]),
}

logger = logging.getLogger(__name__)

for connector_property in connector_properties:
    metrics[connector_property] = Gauge(
        f"cic_{connector_property}",
        connector_property.replace("_", " ").capitalize(),
        ["station_id", "address", "evse_id", "connector_id"],
    )


def iso_to_epoch(iso_string):
    return datetime.fromisoformat(iso_string.replace("Z", "+00:00")).timestamp()


def set_metrics(station, found):
    if not found:
        metrics["station_exists"].labels(station_id=station).set(0)
        return
    address = f"{station.address.streetAndNumber}, {station.address.postalCode} {station.address.city}"
    metrics["address"].labels(
        station_id=station.externalId,
        address=address,
        street=station.address.streetAndNumber,
        postal_code=station.address.postalCode,
        city=station.address.city,
        country=station.address.country,
    ).set(1)
    metrics["operator_name"].labels(
        station_id=station.externalId,
        address=address,
        operator_name=station.operatorName,
    ).set(1)
    metrics["station_exists"].labels(station_id=station.externalId).set(1)
    for evse in station.evses:
        metrics["evse_status"].labels(
            station_id=station.externalId, address=address, evse_id=evse.externalId
        ).state(evse.status)
        metrics["evse_updated"].labels(
            station_id=station.externalId, address=address, evse_id=evse.externalId
        ).set(iso_to_epoch(evse.updated))
        for connector in evse.connectors:
            for connector_property, attr_name in connector_properties.items():
                value = getattr(connector.electricalProperties, attr_name)
                if connector_property == "connector_power":
                    value *= 1000
                metrics[connector_property].labels(
                    station_id=station.externalId,
                    address=address,
                    evse_id=evse.externalId,
                    connector_id=connector.externalId,
                ).set(value)


async def run_metrics_loop(stations, interval):
    async with ClientSession() as session:
        api = Api(session)
        while True:
            for station_id in stations:
                try:
                    station = await api.location_by_id(station_id)
                    if not station:
                        logger.error("Error connecting with API")
                        cooldown_period = randrange(30,60)
                        logger.info(f"Cooling down communication with API for {cooldown_period}s")
                        sleep(cooldown_period)
                        continue
                    set_metrics(station, True)
                except (LocationEmptyError, LocationValidationError):
                    set_metrics(station_id, False)
                except (CancelledError, ClientError, TimeoutError) as err:
                    logger.error(
                        f"An exception occured while connecting with the API: {err}"
                    )
            sleep(interval)
