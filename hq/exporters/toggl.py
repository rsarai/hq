import sys
import json
import requests

from pathlib import Path
from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.config import Toggl as config
from hq.exporters import utils


TIME_ENTRIES = "https://www.toggl.com/api/v8/time_entries"
DOCS = "https://github.com/toggl/toggl_api_docs/blob/master/chapters/time_entries.md"


def _retroactive_export():
    import calendar

    year = 2021
    months = list(range(1, 6))
    for m in months:
        zero_padded_month = str(m).zfill(2)
        start = datetime.strptime(f'{year}-{zero_padded_month}-01', '%Y-%m-%d')

        last_day_of_month = calendar.monthrange(year, m)[1]
        end = datetime.strptime(f'{year}-{zero_padded_month}-{last_day_of_month}', '%Y-%m-%d')
        generate_monthly_exports(
            beg=start.strftime('%Y-%m-%dT%H:%M:%S%z') + "-00:00",
            end=end.strftime('%Y-%m-%dT%H:%M:%S%z') + "-00:00",
        )


def generate_monthly_exports(beg=None, end=None):
    if beg is None or end is None:
        beg, end = utils.get_start_and_end_date_of_last_month(iso_format=True)

    res = requests.get(
        TIME_ENTRIES,
        dict(
            start_date=beg,
            end_date=end,
        ),
        auth=(config.api_key, 'api_token'),
    )

    if res.status_code == 200:
        filename = beg.split("T")[0] + "__" + end.split("T")[0] + '.json'
        export_path = Path(config.export_path + "/" + filename)
        utils.dumper(res.json(), export_path)
    else:
        print(res.content)


generate_monthly_exports()
