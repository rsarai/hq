import calendar
import sys
import json
import requests

from pathlib import Path
from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.config import Github as config
from hq.exporters import utils


LIST_OF_PRIVATE_REPOS_TO_FETCH = config.private_repos_notifications


def generate_notifications_report():
    res = requests.get(
        "https://api.github.com/notifications",
        auth=('rsarai', config.api_key)
    )

    if res.status_code == 200:
        today = datetime.today()
        filename = today.strftime('%Y-%m-%d') + '.json'
        export_path = Path(config.export_path + "/notifications/" + filename)
        utils.dumper(res.json(), export_path)
    else:
        print(res.content)

    for repo in LIST_OF_PRIVATE_REPOS_TO_FETCH:
        res = requests.get(
            f"https://api.github.com/repos/{repo}/notifications",
            auth=('rsarai', config.api_key)
        )
        if res.status_code == 200:
            today = datetime.today()
            filename = repo.replace("/", "_") + '_' + today.strftime('%Y-%m-%d') + '.json'
            export_path = Path(config.export_path + "/notifications/" + filename)
            utils.dumper(res.json(), export_path)
        else:
            print(res.content)


generate_notifications_report()
