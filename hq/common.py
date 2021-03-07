import os
from os.path import isfile, join

def get_files(dir_path):
    return [f for f in os.listdir(dir_path) if isfile(join(dir_path, f))]
