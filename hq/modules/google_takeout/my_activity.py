import json
import zipfile

from bs4 import BeautifulSoup

from hq.common import get_files
from hq.config import GoogleTakeout as config


def get_file_paths():
    # [max(get_files(config.export_path, "vinta*"))]
    # [max(get_files(config.export_path, "ecomp*"))]
    return [max(get_files(config.export_path, "takeout*"))]


def simplify_my_activities(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    for zip_path in input_files:
        input_files_str = [str(i) for i in input_files]
        if zip_path.replace('.zip', '.json') in input_files_str:
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
                for content in items:
                    new_tag = soup.new_tag("p")
                    new_tag.string = " "
                    content.br.replace_with(new_tag)
                    all_content.append(content.text)

                results += [{'title': a, 'content': b} for a, b in zip(all_titles, all_content)]
                print("Finished", file_name)

        my_custom_file = zip_path.replace('.zip', '.json')
        with open(my_custom_file, 'w') as f:
            json.dump(results, f, indent=4)
