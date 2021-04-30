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
            date_str = raw.split(" ", 1)[0]
            remaining = raw.split(" ", 1)[1]
            self.date = datetime.strptime(
                date_str,
                "%Y-%m-%d.%H:%M:%S"
            )
            self.host = "rsarai"
            self.folder = remaining.split("  ", 1)[0]
            self.cmd = remaining.split("  ", 1)[1]
            self.date_tz = timezone.localize(self.date)
        except ValueError:
            self.host = raw.split(" ", 1)[0]
            remaining = raw.split(" ", 1)[1]

            date_str = remaining.split(" ", 1)[0]
            remaining = remaining.split(" ", 1)[1]
            self.date = datetime.strptime(
                date_str,
                "%Y-%m-%d.%H:%M:%S"
            )
            self.folder = remaining.split("  ", 1)[0]
            self.cmd = remaining.split("  ", 1)[1]
            self.date_tz = timezone.localize(self.date)


def process():
    """
        # bash_files = get_files("~/.logs", "*.log")
        Today exports are centered in a single file, however,
        I use them in multiple computers.
        The following deals with two files on the correct folder.
    """
    bash_files = get_files(config.export_path, "*.log")

    for f_path in bash_files:
        content = f_path.read_text()
        for cmd_str in content.split('\n'):
            if not cmd_str:
                continue

            yield Command(raw=cmd_str)
