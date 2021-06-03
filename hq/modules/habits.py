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
import sys
import pytz

from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')

from hq.common import get_files
from hq.sqlite_db import get_readonly_connection
from hq.config import Habits as config


timezone = pytz.timezone("America/Recife")


def get_file_paths():
    """
        As of now, the export file has all the dataset history,
        so the processing of the latest file should be enough
    """
    return max(get_files(config.export_path, "*.db"))


_QUERY = """
SELECT DISTINCT r.id, r.timestamp, r.value, h.description, h.name
FROM Repetitions AS r
JOIN Habits AS h
ON r.habit = h.id;
"""

class Habit:

    def __init__(self, raw):
        self.raw = raw
        self.timestamp = raw[1]

        # https://stackoverflow.com/a/31548402/7537918
        self.date_tz = datetime.fromtimestamp(self.timestamp/1000, timezone)

        self.description = raw[3]
        self.name = raw[4]


def process():
    db_path = get_file_paths()
    with get_readonly_connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(_QUERY)
        for res in cur.fetchall():
            yield Habit(res)
