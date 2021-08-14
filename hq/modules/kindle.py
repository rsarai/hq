from hq.common import get_files
from hq.config import Kindle as config


SEPARATOR = "=========="

def get_file_paths():
    """
        As of now, the export file has all the dataset history,
        so the processing of the latest file should be enough
    """
    return [max(get_files(config.export_path, "*.txt"))]


def get_formated_title(title):
    title = title.replace(u'\ufeff', '')
    return title.rstrip()


def get_highlights(kindle_paths=None):
    if not kindle_paths:
        kindle_paths = get_file_paths()

    kindle_path = kindle_paths[0]
    with open(kindle_path, encoding='utf-8-sig') as f:
        title = line = f.readline()
        title = line = get_formated_title(title)
        content = dict()
        content[title] = []
        while line:
            if SEPARATOR in line:
                title = line = f.readline()
                title = line = get_formated_title(title)
                if title not in content.keys():
                    content[title] = []
                continue

            if "Seu destaque" in line:
                line = f.readline()
                continue

            if line == title:
                line = f.readline()
                continue

            content[title] += [line]
            line = f.readline()
    return content

