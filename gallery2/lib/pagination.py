import paginate

from sqlalchemy.orm import Query


class SqlAlchemyWrapper(object):
    """Wrapper class to access elements of a collection."""
    def __init__(self, collection):
        self.collection = collection

    def __getitem__(self, range):
        return self.collection[range]

    def __len__(self):
        if isinstance(self.collection, Query):
            return self.collection.count()
        return len(self.collection)


class Page(paginate.Page):
        """A pagination page that deals with SQLAlchemy ORM objects."""

        def __init__(self, request, collection, *args, **kwargs):
            try:
                page_number = int(request.params['page'])
            except (TypeError, KeyError, ValueError):
                page_number = 1

            def url_maker(page):
                params = request.params.copy()
                params['page'] = page
                return request.current_route_url(_query=params)

            self.window_size = kwargs.pop('window_size', 10)

            super(Page, self).__init__(
                collection, page_number,
                *args, wrapper_class=SqlAlchemyWrapper,
                url_maker=url_maker, **kwargs)

            leftmost_page = max((self.page - (self.window_size // 2)),
                                self.first_page or 1)
            rightmost_page = min((self.page + (self.window_size // 2)),
                                 self.last_page or 1)
            self.window = range(leftmost_page, rightmost_page + 1)
