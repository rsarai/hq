import locale
import json
import zipfile

from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from hq.common import get_files
from hq.config import GoogleTakeout as config


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def get_file_paths():
    return [
        max(get_files(config.export_path, "takeout*")),
        max(get_files(config.export_path, "vinta*")),
        max(get_files(config.export_path, "ecomp*")),
    ]


def get_my_activities_file_paths():
    return [
        max(get_files(config.export_path, "*.json")),
    ]


def simplify_my_activities(input_files=None, force_override=False):
    if not input_files:
        input_files = get_file_paths()

    for zip_path in input_files:
        input_files_str = [str(i) for i in input_files]
        my_custom_file = str(zip_path).replace('.zip', '.json')
        if not force_override and my_custom_file in input_files_str:
            continue

        zf = zipfile.ZipFile(zip_path)
        my_activities_files = [
            f.filename for f in zf.filelist if f.filename.endswith("Minhaatividade.html")
        ]

        results = []
        for file_name in my_activities_files:
            print("Started", file_name)
            with zf.open(file_name) as html_doc:
                soup = BeautifulSoup(html_doc, 'html.parser')
                titles = soup.find_all(class_="mdl-typography--title")
                all_titles = [t.text for t in titles]

                items = soup.find_all(class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
                all_content = []
                all_activity = []
                for content in items:
                    all_activity.append(content.text.split("\xa0")[0])
                    new_tag = soup.new_tag("p")
                    new_tag.string = " "
                    content.br.replace_with(new_tag)
                    all_content.append(content.text)

                results += [
                    {'title': a, 'content': b, "activity": c}
                    for a, b, c in zip(all_titles, all_content, all_activity)
                ]
                print("Finished", file_name)

        with open(my_custom_file, 'w') as f:
            json.dump(results, f, indent=4)


class Activity(BaseModel):
    raw: dict
    title: str
    content: str
    date_tz: datetime

    def __init__(self, raw):
        data = {"raw": raw}
        data["title"] = raw.get("title")

        content = raw.get("content").replace("\xa0", " ")

        try:
            val = int(content[-31:][:2])
            if val > 31:
                raise ValueError

            activity = content[:-31]
            date_str = content[-31:]
        except ValueError:
            activity = content[:-30]
            date_str = content[-30:]

        date_tz = datetime.strptime(date_str, "%d de %b. de %Y %H:%M:%S BRT")
        data["content"] = activity
        data["date_tz"] = date_tz
        super().__init__(**data)


def process_my_activities(input_files=None):
    if not input_files:
        input_files = get_my_activities_file_paths()

    for file in input_files:
        with open(file, 'r') as json_file:
            activity_list = json.load(json_file)
            for activity in activity_list:
                yield Activity(activity)
