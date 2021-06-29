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
            self.date_str = raw.split(" ", 1)[0]
            remaining = raw.split(" ", 1)[1]
            self.date = datetime.strptime(
                self.date_str,
                "%Y-%m-%d.%H:%M:%S"
            )
            self.host = "Avell G1711: rsarai"
            self.folder = remaining.split("  ", 1)[0]
            self.cmd = remaining.strip().split("  ", 1)[1]
            self.date_tz = timezone.localize(self.date)
        except ValueError:
            self.host = "Avell G1711: rsarai"
            remaining = raw.split(" ", 1)[1]

            self.date_str = remaining.split(" ", 1)[0]
            remaining = remaining.split(" ", 1)[1]
            try:
                self.date = datetime.strptime(
                    self.date_str,
                    "%Y-%m-%d.%H:%M:%S"
                )
                self.folder = remaining.split("  ", 1)[0]
                self.cmd = remaining.strip().split("  ", 1)[1]
                self.date_tz = timezone.localize(self.date)
            except ValueError:
                self.cmd =  "    " + raw
                self.folder = ""
                self.date_tz = None
                self.date = None

        strip_cmd = self.cmd.strip()
        try:
            int(strip_cmd[:4])
            self.cmd = strip_cmd[4:].strip()
        except Exception:
            pass


def get_file_paths():
    return get_files(config.export_path, "*.log")


def process(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    handled = set()
    for f_path in input_files:
        content = f_path.read_text()
        for cmd_str in content.split('\n'):
            if not cmd_str:
                continue

            cmd_object = Command(raw=cmd_str)
            unique_set = f"""{cmd_object.cmd}, {cmd_object.date_str}, {cmd_object.folder}"""
            if unique_set in handled:
                # ids are reseted and are not consisted through different devices
                # uniqueness validation should be achieved by content
                continue
            else:
                handled.add(unique_set)
                yield cmd_object


process()
