import time
from   click.testing import CliRunner
import pytest

@pytest.fixture(autouse=True)
def use_fixed_time(mocker):
    mocker.patch('time.localtime', return_value=time.localtime(1478550580))

@pytest.fixture
def defaults_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('defaults.properties', 'wb') as fp:
            fp.write(
                b'key = lock\n'
                b'lost = found\n'
            )
        yield
