from django.utils.functional import LazyObject
from zonetable.apps.sorl.thumbnail.conf import settings
from zonetable.apps.sorl.thumbnail.helpers import get_module_class


class Backend(LazyObject):
    def _setup(self):
        self._wrapped = get_module_class(settings.THUMBNAIL_BACKEND)()


class KVStore(LazyObject):
    def _setup(self):
        self._wrapped = get_module_class(settings.THUMBNAIL_KVSTORE)()


class Engine(LazyObject):
    def _setup(self):
        self._wrapped = get_module_class(settings.THUMBNAIL_ENGINE)()


class Storage(LazyObject):
    def _setup(self):
        self._wrapped = get_module_class(settings.THUMBNAIL_STORAGE)()


backend = Backend()
kvstore = KVStore()
engine = Engine()
storage = Storage()

