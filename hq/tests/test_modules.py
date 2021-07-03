import mock
from pathlib import Path

from hq.modules import bash


@mock.patch("hq.modules.bash.config")
def test_bash_get_file_paths(_bash_config):
    _bash_config.export_path = "hq/tests/files"

    files = bash.get_file_paths()
    assert files == [
        Path("hq/tests/files/bash.log"),
        Path("hq/tests/files/other_bash.log")
    ]

