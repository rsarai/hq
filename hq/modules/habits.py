"""
All the habit tracking extracted from the habits android app
"""
from zipfile import ZipFile

from datetime import datetime, date

sys.path.append('/home/sarai/github-projects/hq')

from hq.common import get_files
from hq.config import Habits as config
