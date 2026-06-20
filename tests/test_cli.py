from click.testing import CliRunner
from unittest.mock import AsyncMock, patch
from can_i_charge.__main__ import main
from can_i_charge.api import StationNotFoundError


def test_cli_verbose_flag():
    runner = CliRunner()
    result = runner.invoke(main, ["-v", "--api-key", "test-key"])
    assert result.exit_code == 0


def test_cli_station_flag():
    runner = CliRunner()
    with patch("can_i_charge.cli.get_station", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = StationNotFoundError()
        result = runner.invoke(
            main, ["-s", "NON_EXISTING_STATION", "--api-key", "test-key"]
        )
        assert (
            result.output
            == "No data returned for NON_EXISTING_STATION, check station id\n"
        )
        assert result.exit_code == 0


def test_cli_non_existing_argument():
    runner = CliRunner()
    result = runner.invoke(main, ["--no"])
    assert result.exit_code == 2
