import re
import sys

sys.path.append('/home/sarai/github-projects/hq')
from hq.modules import notion_articles
from hq.common import SimpleOrgNode, Replica, dt_heading


class ArticlesView(Replica):

    def get_items(self):
        for article in notion_articles.process():
            yield article.uuid, SimpleOrgNode(
                heading=dt_heading(
                    article.datetime(),
                    article.title(),
                ),
                children=[SimpleOrgNode(i) for i in article.raw.split('\n')]
            )




if __name__ == '__main__':
    ArticlesView.main()
