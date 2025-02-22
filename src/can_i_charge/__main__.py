from asyncio import run
from can_i_charge.cli import get_charging_status
from click import command, option


@command()
@option("-s", "--station", envvar="STATIONS", multiple=True)
def main(station):
    run(get_charging_status(station))


if __name__ == "__main__":
    main()
