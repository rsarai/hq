import sys

from PIL import Image
from pathlib import Path

sys.path.append('/home/sarai/github-projects/hq')
from hq.common import get_files
from hq.config import NotionArticles as config
from hq.modules import notion_articles
from hq.views.articles import ArticlesView


images_files = get_files(config.export_path, "*/*/")

for image_path in images_files:
    if '.png' in str(image_path):
        print("PNG, nothing to do here, carrying on...")
        continue

    picture = Image.open(str(image_path))
    picture.save(
        str(image_path),
        "JPEG",
        optimize=True,
        quality=75
    )

