"""
All the habit tracking extracted from the habits android app

Export Format:
"SELECT * FROM Habits;"
['Id', *
 'archived',
 'color',
 'description', *
 'freq_den',
 'freq_num',
 'highlight',
 'name', *
 'position',
 'reminder_days',
 'reminder_hour',
 'reminder_min',
 'type',
 'target_type',
 'target_value',
 'unit']

"SELECT * FROM Repetitions;"
['id', 'habit', 'timestamp', 'value']

"""
import pytz

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from hq.common import get_files
from hq.sqlite_db import get_readonly_connection
from hq.config import Habits as config


timezone = pytz.timezone("America/Recife")


def get_file_paths():
    """
        As of now, the export file has all the dataset history,
        so the processing of the latest file should be enough
    """
    return [max(get_files(config.export_path, "*.db"))]


_QUERY = """
SELECT DISTINCT r.id, r.timestamp, r.value, h.description, h.name
FROM Repetitions AS r
JOIN Habits AS h
ON r.habit = h.id;
"""

class Habit(BaseModel):
    raw: list
    date_tz: Optional[datetime]
    description: Optional[str]
    name: Optional[str]

    def __init__(self, raw):
        data = {"raw": raw}

        timestamp = raw[1]
        # https://stackoverflow.com/a/31548402/7537918
        data["date_tz"] = datetime.fromtimestamp(timestamp/1000, timezone)
        data["description"] = raw[3]
        data["name"] = raw[4]

        super().__init__(**data)


def process(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    for db_path in input_files:
        with get_readonly_connection(db_path) as conn:
            cur = conn.cursor()
            cur.execute(_QUERY)
            for res in cur.fetchall():
                yield Habit(res)
