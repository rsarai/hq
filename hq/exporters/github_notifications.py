import calendar
import sys
import json
import requests

from pathlib import Path
from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.config import Github as config
from hq.exporters import utils
from hq.modules import github


LIST_OF_PRIVATE_REPOS_TO_FETCH = config.private_repos_notifications


def generate_notifications_report():
    res = requests.get(
        "https://api.github.com/notifications",
        auth=('rsarai', config.api_key)
    )

    if res.status_code == 200:
        today = datetime.today()
        filename = today.strftime('%Y-%m-%d') + '.json'
        path = config.export_path + "/notifications/" + filename
        export_path = Path(path)
        utils.dumper(res.json(), export_path)

        notification_details = {}
        generator_notifications = github.process_notifications([path], use_details=False)
        for notification in generator_notifications:
            latest_comment_url = notification.subject.get("latest_comment_url")
            if not latest_comment_url:
                latest_comment_url = notification.subject.get("url")

            print("Fetching details for:", latest_comment_url)
            res = requests.get(
                latest_comment_url,
                auth=('rsarai', config.api_key)
            )
            if res.status_code == 200:
                key = notification.github_id + notification.updated_at_str
                notification_details[key] = res.json()
            else:
                print("Error when fetching notification details")
                print(res.content)

        filename = today.strftime('%Y-%m-%d') + '_details.json'
        path = config.export_path + "/notifications/" + filename
        export_path = Path(path)
        utils.dumper(notification_details, export_path)
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
            path = config.export_path + "/notifications/" + filename
            export_path = Path(path)
            utils.dumper(res.json(), export_path)

            notification_details = {}
            generator_notifications = github.process_notifications([path], use_details=False)
            for notification in generator_notifications:
                latest_comment_url = notification.subject.get("latest_comment_url")
                print("Fetching details for:", latest_comment_url)
                if not latest_comment_url:
                    continue

                res = requests.get(
                    latest_comment_url,
                    auth=('rsarai', config.api_key)
                )
                if res.status_code == 200:
                    key = notification.github_id + notification.updated_at_str
                    notification_details[key] = res.json()
                else:
                    print("Error when fetching notification details")
                    print(res.content)

            filename = filename = repo.replace("/", "_") + '_' + today.strftime('%Y-%m-%d') + '_details.json'
            path = config.export_path + "/notifications/" + filename
            export_path = Path(path)
            utils.dumper(notification_details, export_path)
        else:
            print(res.content)


generate_notifications_report()
