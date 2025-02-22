from asyncio import get_event_loop, run
from can_i_charge.cli import get_charging_status
from can_i_charge.exporter import run_metrics_loop
from click import command, option
from prometheus_client import start_http_server


@command()
@option("-e", "--exporter", envvar="EXPORTER", is_flag=True)
@option("-i", "--interval", envvar="EXPORTER_INTERVAL", type=int)
@option("-p", "--port", envvar="EXPORTER_PORT", type=int)
@option("-s", "--station", envvar="STATIONS", multiple=True)
def main(exporter, interval, port, station):
    if exporter:
        start_http_server(port if port else 9041)
        metrics_loop = run_metrics_loop(station, interval if interval else 60)
        get_event_loop().run_until_complete(metrics_loop)
    else:
        run(get_charging_status(station))


if __name__ == "__main__":
    main()
