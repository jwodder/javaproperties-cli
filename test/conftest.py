import time
import pytest

@pytest.fixture(autouse=True)
def use_fixed_time(mocker):
    mocker.patch(
        'time.localtime',
        return_value=time.struct_time((2016, 11, 7, 15, 29, 40, 0, 312, 0)),
    )
