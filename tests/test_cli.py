from click.testing import CliRunner
from can_i_charge.__main__ import main

def test_cli_verbose_flag():
    runner = CliRunner()
    result = runner.invoke(main, ["-v"])
    assert result.exit_code == 0

def test_cli_station_flag():
    runner = CliRunner()
    result = runner.invoke(main, ["-s", "NON_EXISTING_STATION"])
    assert result.output == "No data returned for NON_EXISTING_STATION, check station id\n"
    assert result.exit_code == 0

def test_cli_non_existing_argument():
    runner = CliRunner()
    result = runner.invoke(main, ["--no"])
    assert result.exit_code == 2
    
