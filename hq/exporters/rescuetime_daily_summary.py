import sys
import json
import requests

from pathlib import Path
from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.config import RescueTime as config
from hq.exporters import utils


def generate_daily_summary_export():
    res = requests.get(
        "https://www.rescuetime.com/anapi/daily_summary_feed",
        dict(
            key=config.api_key,
            format='json',
        )
    )

    if res.status_code == 200:
        today = datetime.today()
        filename = today.strftime('%Y-%m-%d') + '.json'
        export_path = Path(config.export_path + "/daily_summary/" + filename)
        utils.dumper(res.json(), export_path)
    else:
        print(res.content)


generate_daily_summary_export()
