import asyncio
import click

from can_i_charge.charging_status import get_charging_status


@click.command()
@click.option("-s", "--station", envvar="STATIONS", multiple=True)
def main(station):
    asyncio.run(get_charging_status(station))


if __name__ == "__main__":
    main()
