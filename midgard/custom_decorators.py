"""
A module providing a decorator to enforce singleton behavior on classes.

This module defines a utility to apply the singleton design pattern to a Python
class. The included decorator ensures that only one instance of a class is
created during the program’s execution. Thread safety is maintained to handle
multithreaded environments where multiple threads might try to create the class
instance simultaneously.
"""

import functools
import threading


def singleton(cls):
    """
    A decorator to enforce the singleton design pattern on a class. This ensures that only one instance
    of the specified class is created during the runtime of the application. Subsequent calls to create
    the class instance will return the same previously created instance. Thread safety is guaranteed
    using a locking mechanism to prevent race conditions in multithreaded environments.

    :param cls: The class to be decorated as a singleton.
    :type cls: type
    :return: A wrapper function that enforces the singleton behavior on the provided class.
    :rtype: Callable[..., Any]
    """

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
