import csv
import json
import zipfile
import locale
from io import TextIOWrapper
from bs4 import BeautifulSoup

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from hq.common import parse_datetime, get_files
from hq.config import GoogleTakeout as config
from hq.modules.google_takeout.utils import get_file_paths


FOLDER_PREFIX = "YouTube e YouTube Music"

"""
Content: https://developers.google.com/youtube/v3/quickstart/python

Folders:
    - playlists
    - inscrições
    - histórico de pesquisa
    - histórico-de-visualização
"""

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def get_file_paths_by_prefix(prefix):
    return [
        max(get_files(config.export_path, f"*{prefix}.json")),
    ]


class Playlist(BaseModel):
    raw: dict
    code: Optional[str] = None
    title: Optional[str] = None
    is_visible: Optional[bool] = None
    date_tz: Optional[datetime] = None
    update_date_tz: Optional[datetime] = None
    url: Optional[str] = None
    playlist_items: Optional[list] = None

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
    id: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    def __init__(self, raw):
        data = {"raw": raw}
        data["id"] = raw.get("ID do canal")
        data["url"] = raw.get("URL do canal")
        data["title"] = raw.get("Título do canal")
        data["description"] = "YouTube: Subscriptions"
        super().__init__(**data)


class Search(BaseModel):
    raw: dict
    search: str
    product: Optional[str] = None
    date_tz: datetime

    def __init__(self, raw):
        data = {"raw": raw}
        search = raw.get("search").replace("Searched for\xa0", "")

        try:
            val = int(search[-31:][:2])
            if val > 31:
                raise ValueError

            date_str = search[-31:]
        except ValueError:
            date_str = search[-30:]

        search = search.replace(date_str, "")

        date_tz = datetime.strptime(date_str, "%d de %b. de %Y %H:%M:%S BRT")
        data["search"] = search
        data["date_tz"] = date_tz
        super().__init__(**data)


class View(BaseModel):
    raw: dict
    title: str
    link: str
    date_tz: datetime

    def __init__(self, raw):
        data = {"raw": raw}
        title = raw.get("title")
        link = raw.get("link")
        REPLACE_LIST = ["Gilvan Rodrigues 32"]

        date_str = raw.get("views")
        if "Watched at" in date_str:
            index = date_str.find("Watched at")
            # The goal here is to remove ocurrences of "Watched at 18:32"
            # this causes wrong watch dates
            date_str = date_str.replace(date_str[index:index+16], " ")

        for replace_str in REPLACE_LIST:
            # replace string because it was messing with the dates
            # "ValueError: day is out of range for month"
            if replace_str in date_str:
                date_str = date_str.replace(replace_str, " ")

        try:
            # This is required to account for numbers of one digit such as:
            # "...Daily Stoic9 de fev. de 2022 18:33:02 BRT"
            val = int(date_str[-31:][:2])
            if val > 31:
                raise ValueError

            date_str = date_str[-31:]
        except ValueError:
            date_str = date_str[-30:]

        date_str = date_str.replace("+", "")
        date_str = date_str.replace("-", "")
        date_tz = datetime.strptime(date_str, "%d de %b. de %Y %H:%M:%S BRT")

        data["title"] = title
        data["link"] = link
        data["date_tz"] = date_tz
        super().__init__(**data)


def process_view_history(input_files=None):
    ENTITY_PREFIX = "histórico-de-visualização"
    if not input_files:
        input_files = get_file_paths_by_prefix(ENTITY_PREFIX)

    for file in input_files:
        with open(file, 'r') as json_file:
            activity_list = json.load(json_file)
            for activity in activity_list:
                if "Watched" in activity["views"]:
                    yield View(activity)


def process_search_history(input_files=None):
    ENTITY_PREFIX = "histórico de pesquisa"
    if not input_files:
        input_files = get_file_paths_by_prefix(ENTITY_PREFIX)

    for file in input_files:
        with open(file, 'r') as json_file:
            activity_list = json.load(json_file)
            for activity in activity_list:
                if "Searched" in activity["search"]:
                    yield Search(activity)


def process_subscriptions(input_files=None):
    ENTITY_PREFIX = "inscrições"
    if not input_files:
        input_files = get_file_paths(config.export_path)

    for zip_path in input_files:
        zf = zipfile.ZipFile(zip_path)

        youtube_files = [i for i in zf.filelist if FOLDER_PREFIX in str(i) and ENTITY_PREFIX in str(i)]
        print("Found ", len(input_files), "youtube files")

        # for each one of the found files
        for file_name in youtube_files:
            with zf.open(file_name) as csvfile:
                reader = csv.DictReader(TextIOWrapper(csvfile, 'utf-8'))
                for row in reader:
                    yield Subscriptions(row)


def process_playlists(input_files=None):
    ENTITY_PREFIX = "playlists"
    if not input_files:
        input_files = get_file_paths(config.export_path)

    print("Found ", len(input_files), "files, accross all accounts")
    for zip_path in input_files:
        zf = zipfile.ZipFile(zip_path)

        youtube_files = [i for i in zf.filelist if FOLDER_PREFIX in str(i) and ENTITY_PREFIX in str(i)]
        print("Found ", len(input_files), "youtube files, accross all accounts")
        # for each one of the found files
        for file_name in youtube_files:
            with zf.open(file_name) as csvfile:
                reader = csv.DictReader(TextIOWrapper(csvfile, 'utf-8'))
                playlist_name = file_name.filename.split("/")[-1].split('.')[0]

                index = 0
                header_values = None
                items = []
                for row in reader:
                    if index == 0:
                        index += 1
                        continue

                    if index == 1:
                        header_values = row
                        index += 1
                        continue

                    if index > 3:
                        items.append(row)

                    index += 1

                yield Playlist(header_values, items)


def simplify_research_historic(input_files=None, force_override=False):
    ENTITY_PREFIX = "histórico de pesquisa"
    if not input_files:
        input_files = get_file_paths(config.export_path)

    for zip_path in input_files:
        input_files_str = [str(i) for i in input_files]
        my_custom_file = str(zip_path).replace('.zip', f'{ENTITY_PREFIX}.json')
        if not force_override and my_custom_file in input_files_str:
            continue

        zf = zipfile.ZipFile(zip_path)
        my_files = [
            f.filename for f in zf.filelist if f.filename.endswith(f"{ENTITY_PREFIX}.html")
        ]

        if len(my_files) == 0:
            continue

        results = []
        for file_name in my_files:
            print("Started", file_name)
            with zf.open(file_name) as html_doc:
                soup = BeautifulSoup(html_doc, 'html.parser')
                searches = soup.find_all(class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
                all_searches = [t.text for t in searches]

                products = soup.find_all(class_="content-cell mdl-cell mdl-cell--12-col mdl-typography--caption")
                all_products = [t.text for t in products]

            results += [
                {'search': a, 'product': b}
                for a, b in zip(all_searches, all_products)
            ]
            print("Finished", file_name)

        my_custom_file = str(zip_path).replace('.zip', f'{ENTITY_PREFIX}.json')
        with open(f"{my_custom_file}", 'w') as f:
            json.dump(results, f, indent=4)


def simplify_view_historic(input_files=None, force_override=False):
    ENTITY_PREFIX = "histórico-de-visualização"
    if not input_files:
        input_files = get_file_paths(config.export_path)

    for zip_path in input_files:
        print("Analysing", zip_path)
        input_files_str = [str(i) for i in input_files]
        my_custom_file = str(zip_path).replace('.zip', f'{ENTITY_PREFIX}.json')
        if not force_override and my_custom_file in input_files_str:
            print("Early exit. File already generated.")
            continue

        zf = zipfile.ZipFile(zip_path)
        my_files = [
            f.filename for f in zf.filelist if f.filename.endswith(f"{ENTITY_PREFIX}.html")
        ]

        if len(my_files) == 0:
            continue

        results = []
        for file_name in my_files:
            print("Started", file_name)
            with zf.open(file_name) as html_doc:
                soup = BeautifulSoup(html_doc, 'html.parser')
                views = soup.find_all(class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")

                all_views = [t.text for t in views]
                all_views_link = [t.find('a')["href"] if t.find('a') else "Watched a video that has been removed" for t in views]
                all_views_text = [t.find('a').get_text() if t.find('a') else "Watched a video that has been removed" for t in views]

                products = soup.find_all(class_="content-cell mdl-cell mdl-cell--12-col mdl-typography--caption")
                all_products = [t.text for t in products]

            results += [
                {'views': a, 'title': b, 'link': c, 'product': d}
                for a, b, c, d in zip(all_views, all_views_text, all_views_link, all_products)
            ]
            print("Finished", file_name)

        my_custom_file = str(zip_path).replace('.zip', f'{ENTITY_PREFIX}.json')
        with open(f"{my_custom_file}", 'w') as f:
            json.dump(results, f, indent=4)
