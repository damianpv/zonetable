from redis import Redis
from zonetable.apps.sorl.thumbnail.kvstores.base import KVStoreBase
from zonetable.apps.sorl.thumbnail.conf import settings


class KVStore(KVStoreBase):
    def __init__(self, *args, **kwargs):
        super(KVStore, self).__init__(*args, **kwargs)
        self.connection = Redis(
            host=settings.THUMBNAIL_REDIS_HOST,
            port=settings.THUMBNAIL_REDIS_PORT,
            db=settings.THUMBNAIL_REDIS_DB,
            )

    def _get_raw(self, key):
        return self.connection.get(key)

    def _set_raw(self, key, value):
        return self.connection.set(key, value)

    def _delete_raw(self, *keys):
        return self.connection.delete(*keys)

    def _find_keys_raw(self, prefix):
        pattern = prefix + '*'
        return self.connection.keys(pattern=pattern)

