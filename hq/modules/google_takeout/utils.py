
from hq.common import get_files


def get_file_paths(export_path):
    return [
        max(get_files(export_path, "takeout*.json")),
        max(get_files(export_path, "takeout*.zip")),
        max(get_files(export_path, "vinta*.json")),
        max(get_files(export_path, "vinta*.zip")),
        max(get_files(export_path, "ecomp*.json")),
        max(get_files(export_path, "ecomp*.zip")),
    ]


def get_zip_file_paths(export_path):
    return [
        max(get_files(export_path, "takeout*.zip")),
        max(get_files(export_path, "vinta*.zip")),
        max(get_files(export_path, "ecomp*.zip")),
    ]
