"""Main module."""

import time
import threading


class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance


class Counter(SingletonMixin):
    counter = 0
    __lock = threading.Lock()

    def incr(self):
        with self.__lock:
            self.counter += 1

        return self.counter


counter = Counter()


def gen_guid(shard_id=1):
    incr = counter.incr()

    guid = (int(time.time() * 1000) << (64 - 41))
    guid |= (shard_id << (64 - 41 - 13))
    guid |= incr % 1024

    return guid
