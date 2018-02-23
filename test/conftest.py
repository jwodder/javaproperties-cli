import time
import pytest

@pytest.fixture(autouse=True)
def use_fixed_time(mocker):
    mocker.patch('time.localtime', return_value=time.localtime(1478550580))
