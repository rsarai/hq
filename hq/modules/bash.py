import sys
import pytz

from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')

from hq.common import get_files
from hq.config import BashHistory as config


timezone = pytz.timezone("America/Recife")


class Command:

    def __init__(self, raw):
        self.raw = raw

        try:
            # this is buggy
            date_str = raw.split(" ", 1)[0]
            remaining = raw.split(" ", 1)[1]
            self.date = datetime.strptime(
                date_str,
                "%Y-%m-%d.%H:%M:%S"
            )
            self.host = "rsarai"
        except ValueError:
            self.host = date_str

            date_str = remaining.split(" ", 1)[0]
            remaining = remaining.split(" ", 1)[1]
            self.date = datetime.strptime(
                date_str,
                "%Y-%m-%d.%H:%M:%S"
            )
        finally:
            self.folder = remaining.split("  ", 1)[0]
            self.cmd = remaining.split("  ", 1)[1]
            self.date_tz = timezone.localize(self.date)


def process():
    # bash_files = get_files(config.export_path, "*.log")
    bash_files = get_files("~/.logs", "*.log")

    for f_path in bash_files:
        content = f_path.read_text()
        for cmd_str in content.split('\n'):
            yield Command(raw=cmd_str)
