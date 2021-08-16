import requests

from requests.auth import HTTPBasicAuth
from pathlib import Path
from enum import Enum

from hq.config import Wakatime as config
from hq.exporters import utils


BASE_URL = "https://wakatime.com/api/v1/"
ENDPOINT_STATS = "users/current/summaries"


def _retroactive_export():
    generate_exports(
        start_date='2019-12-05',
        end_date='2020-12-05'
    )
    generate_exports(
        start_date='2020-12-06',
        end_date='2021-08-15'
    )


def generate_exports(start_date=None, end_date=None):
    if start_date is None or end_date is None:
        start_date, end_date = utils.get_start_and_end_date_of_last_month()

    res = requests.get(
        BASE_URL + ENDPOINT_STATS,
        dict(
            start=start_date,
            end=end_date,
        ),
        auth=HTTPBasicAuth("", config.api_key)
    )

    if res.status_code != 200:
        print(res.content)
        return

    json_response = res.json()["data"]
    filename = start_date + "__" + end_date + '.json'
    export_path = Path(config.export_path + "/" + filename)
    utils.dumper(json_response, export_path)


generate_exports()
