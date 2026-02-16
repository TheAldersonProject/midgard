import functools
import threading


def singleton(cls):
    """Make a Singleton object"""

    instances = {}
    lock = threading.Lock()

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper_singleton
