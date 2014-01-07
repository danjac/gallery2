from ..models import DBSession


class ModelResource(object):

    model = None

    @classmethod
    def for_model(cls, model):
        def _create_instance(request):
            return cls(request, model)
        return _create_instance

    def __init__(self, request, model=None):

        self.request = request
        self.model = model or self.model

    def __getitem__(self, key):
        obj = self.get_instance(key)
        if obj is None:
            raise KeyError(key)

        obj.__name__ = key
        obj.__parent__ = self

        return obj

    def get_instance(self, key):
        return DBSession.query(self.model).get(key)
