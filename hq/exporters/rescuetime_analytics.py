import calendar
import sys
import json
import requests

from pathlib import Path
from datetime import datetime, timedelta

sys.path.append('/home/sarai/github-projects/hq')
from hq.config import RescueTime as config
from hq.exporters import utils


def _retroactive_export():
    months = list(range(1, 5))
    for m in months:
        zero_padded_month = str(m).zfill(2)
        start = datetime.strptime(f'2021-{zero_padded_month}-01', '%Y-%m-%d')

        last_day_of_month = calendar.monthrange(2021, m)[1]
        end = datetime.strptime(f'2021-{zero_padded_month}-{last_day_of_month}', '%Y-%m-%d')
        generate_analytics_export(beg=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))


def generate_analytics_export(beg=None, end=None):
    if beg is None or end is None:
        beg, end = utils.get_start_and_end_date_of_last_month()

    res = requests.get(
        "https://www.rescuetime.com/anapi/data",
        dict(
            key=config.api_key,
            format='json',
            perspective='interval',
            interval='minute',
            restrict_begin=beg,
            restrict_end=end,
        )
    )

    if res.status_code == 200:
        filename = beg + '__' + end + '.json'
        export_path = Path(config.export_path + "/analytic_data/" + filename)
        utils.dumper(res.json(), export_path)
    else:
        print(res.content)


generate_analytics_export()
