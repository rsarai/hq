from orger import Mirror
from orger.inorganic import node, link, OrgNode
from orger.common import dt_heading

from hq.kindle import get_highlights_from_book  # TODO


class KindleView(Mirror):
    """
        KindleView.main()
            - https://github.com/karlicoss/orger/blob/928f17947b27648deed7da6105da43cb4208e42d/src/orger/org_view.py#L104
    """

    def _format_book_name(self, highlight):
        pass

    def _format_datetime(self, highlight):
        pass

    def _format_header(self, highlight):
        pass

    def render_highligh(self, highlight):
        pass

    def get_items(self):
        for highlight in get_highlights_from_book():
            yield node(
                heading=dt_heading(
                    self._format_datetime(highlight),
                    self._format_header(highlight)
                ),
                children=[self.render_highligh(highlight)]
            )

