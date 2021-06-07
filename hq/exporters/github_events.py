import sys
import requests

from pathlib import Path
from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.config import Github as config
from hq.exporters import utils


def generate_events_report():
    res = requests.get(
        "https://api.github.com/users/rsarai/events",
        auth=('rsarai', config.api_key)
    )

    if res.status_code == 200:
        today = datetime.today()
        filename = today.strftime('%Y-%m-%d') + '.json'
        export_path = Path(config.export_path + "/events/" + filename)
        utils.dumper(res.json(), export_path)
    else:
        print(res.content)


generate_events_report()
