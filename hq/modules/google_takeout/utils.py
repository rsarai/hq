
from hq.common import get_files


def get_file_paths(export_path):
    return [
        max(get_files(export_path, "takeout*")),
        max(get_files(export_path, "vinta*")),
        max(get_files(export_path, "ecomp*")),
    ]

