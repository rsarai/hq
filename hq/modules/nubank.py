import sys

sys.path.append('/home/sarai/github-projects/hq')
from hq.common import get_files
from hq.config import Nubank as config


def process():
    print(config.export_path)
    first = min(get_files(config.export_path, "*.json"))
    last = max(get_files(config.export_path, "*.json"))
    print("first", first)
    print("last", last)


process()
