import csv
from hq.modules.google_takeout.play_store import Subscription
import zipfile
from io import TextIOWrapper

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from hq.common import parse_datetime
from hq.config import GoogleTakeout as config
from hq.modules.google_takeout.utils import get_file_paths


FOLDER_PREFIX = "YouTube e YouTube Music"

"""
Content: https://developers.google.com/youtube/v3/quickstart/python
"""


class Playlist(BaseModel):
    raw: dict
    code: Optional[str]
    title: Optional[str]
    is_visible: Optional[bool]
    date_tz: Optional[datetime]
    update_date_tz: Optional[datetime]
    url: Optional[str]
    playlist_items: Optional[list]

    def __init__(self, header, items):
        data = {"raw": {"header": header, "items": items}}
        data['code'] = header.get("Código da playlist")
        data['title'] = header.get("Título")
        data['is_visible'] = header.get("Visibilidade") == 'Particular'
        data['url'] = self._get_url(data['code'])

        date = header.get("Horário da criação")
        if date:
            data["date_tz"] = parse_datetime(date, '%Y-%m-%d %H:%M:%S %Z')

        date = header.get("Horário da atualização")
        if date:
            data["update_date_tz"] = parse_datetime(date, '%Y-%m-%d %H:%M:%S %Z')

        playlist_items = []
        for row in items:
            id = row["Código da playlist"]
            added_at = row["ID do canal"]
            playlist_items.append({
                "url": f"https://www.youtube.com/watch?v={id}",
                "code": id,
                "added_at": parse_datetime(added_at, '%Y-%m-%d %H:%M:%S %Z')
            })
        data['playlist_items'] = playlist_items
        super().__init__(**data)

    def _get_url(self, id):
        return f"https://www.youtube.com/playlist?list={id}"


class Subscriptions(BaseModel):
    raw: dict
    id: Optional[str]
    url: Optional[str]
    title: Optional[str]
    description: Optional[str]

    def __init__(self, raw):
        data = {"raw": raw}
        data["id"] = raw.get("ID do canal")
        data["url"] = raw.get("URL do canal")
        data["title"] = raw.get("Título do canal")
        data["description"] = "YouTube: Subscriptions"
        super().__init__(**data)


def process_subscriptions(input_files=None):
    ENTITY_PREFIX = "inscrições"
    if not input_files:
        input_files = get_file_paths(config.export_path)

    for zip_path in input_files:
        zf = zipfile.ZipFile(zip_path)

        youtube_files = [i for i in zf.filelist if FOLDER_PREFIX in str(i) and ENTITY_PREFIX in str(i)]

        # for each one of the found files
        for file_name in youtube_files:
            with zf.open(file_name) as csvfile:
                reader = csv.DictReader(TextIOWrapper(csvfile, 'utf-8'))
                for row in reader:
                    yield Subscription(row)


def process_playlists(input_files=None):
    ENTITY_PREFIX = "playlists"
    if not input_files:
        input_files = get_file_paths(config.export_path)

    for zip_path in input_files:
        zf = zipfile.ZipFile(zip_path)

        youtube_files = [i for i in zf.filelist if FOLDER_PREFIX in str(i) and ENTITY_PREFIX in str(i)]

        # for each one of the found files
        for file_name in youtube_files:
            with zf.open(file_name) as csvfile:
                reader = csv.DictReader(TextIOWrapper(csvfile, 'utf-8'))
                playlist_name = file_name.filename.split("/")[-1].split('.')[0]

                index = 0
                header = None
                items = []
                for row in reader:
                    if index == 0:
                        header = row

                    if index == 1:
                        continue

                    items.append(row)
                    index += 1
