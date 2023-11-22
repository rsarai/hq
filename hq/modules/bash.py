import pytz

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from hq.common import get_files, parse_datetime
from hq.config import BashHistory as config


timezone = pytz.timezone("America/Recife")


class Command(BaseModel):
    raw: str
    host: Optional[str] = None
    folder: Optional[str] = None
    cmd: Optional[str] = None
    date_tz: Optional[datetime] = None

    def __init__(self, raw):
        raw = raw
        data = {"raw": raw}

        try:
            date_str = raw.split(" ", 1)[0]
            remaining = raw.split(" ", 1)[1]
            data["date_tz"] = parse_datetime(date_str, "%Y-%m-%d.%H:%M:%S")
            data["host"] = "Avell G1711: rsarai"
            data["folder"] = remaining.split("  ", 1)[0]
            data["cmd"] = remaining.strip().split("  ", 1)[1]
        except ValueError:
            data["host"] = "Avell G1711: rsarai"
            remaining = raw.split(" ", 1)[1]

            date_str = remaining.split(" ", 1)[0]
            remaining = remaining.split(" ", 1)[1]
            try:
                data["date_tz"] = parse_datetime(date_str, "%Y-%m-%d.%H:%M:%S")
                data["folder"] = remaining.split("  ", 1)[0]
                data["cmd"] = remaining.strip().split("  ", 1)[1]
            except ValueError:
                data["cmd"] =  "    " + raw
                data["folder"] = ""
                data["date_tz"] = None

        strip_cmd = data["cmd"].strip()
        try:
            int(strip_cmd[:4])
            data["cmd"] = strip_cmd[4:].strip()
        except Exception:
            pass

        super().__init__(**data)


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
            unique_set = f"""{cmd_object.cmd}, {cmd_object.date_tz}, {cmd_object.folder}"""
            if unique_set in handled:
                # ids are reseted and are not consisted through different devices
                # uniqueness validation should be achieved by content
                continue
            else:
                handled.add(unique_set)
                yield cmd_object


process()
