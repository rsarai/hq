import os
import re
import sys
import shutil

from pathlib import Path

sys.path.append('/home/sarai/github-projects/hq')
from hq.modules import notion_articles
from hq.common import SimpleOrgNode, Replica, dt_heading
from hq.common import get_files
from hq.settings import IMAGES_FOLDER


from hq.config import NotionArticles as config
from hq.config import SecondBrain as second_brain


class ArticlesView(Replica):
    DEFAULT_HEADER = '''
#+title: Saved Articles
# This file is AUTOGENERATED by {tool}
# It's deliberately read-only, because it will be overwritten next time Orger is run.
# If you want to edit it anyway, you can use chmod +w in your terminal, or M-x toggle-read-only in Emacs.
'''.lstrip()

    def get_items(self):
        for article in notion_articles.process():
            yield article.uuid, SimpleOrgNode(
                heading='',
                children=[SimpleOrgNode(i) for i in article.raw.split('\n')]
            )

    def _run(self, to):
        super()._run(to)
        notion_files = get_files(config.export_path, "*.md")
        all_files = get_files(config.export_path, "*")
        images_folders = set(all_files) - set(notion_files)
        destination = Path(second_brain.export_path + '/' + IMAGES_FOLDER)

        for f in images_folders:
            destination_str = str(destination) + '/' + f.stem + '/'
            destination_str = destination_str.replace(' ', '+')
            if os.path.exists(destination_str):
                shutil.rmtree(destination_str)
            shutil.copytree(f, destination_str)


if __name__ == '__main__':
    ArticlesView.main()
