from pathlib import Path
import time
import pytest


@pytest.fixture(autouse=True)
def use_fixed_time(mocker):
    mocker.patch("time.localtime", return_value=time.localtime(1478550580))


@pytest.fixture
def defaults_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    with open("defaults.properties", "wb") as fp:
        fp.write(b"key = lock\nlost = found\n")
