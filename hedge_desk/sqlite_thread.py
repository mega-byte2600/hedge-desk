"""Thread-safety helpers for the SQLite-backed stores.

The web console serves requests from a thread pool (``ThreadingWSGIServer``)
while each store holds one ``sqlite3`` connection. A ``sqlite3`` connection is
bound to the thread that created it unless ``check_same_thread=False`` is
passed, so a store built while handling one request raised
``ProgrammingError: SQLite objects created in a thread can only be used in that
same thread`` as soon as another thread touched it — surfacing as an HTTP 500
on sign-in under any real concurrency.

One connection with ``check_same_thread=False`` plus one re-entrant lock per
store keeps access correct and bounded. The lock serializes access the way
SQLite would anyway, and no connections are leaked the way a per-thread
connection would be under a thread-per-request server.
"""

from __future__ import annotations

import functools
import sqlite3
import threading
from typing import Callable, TypeVar

T = TypeVar("T")


def new_lock() -> threading.RLock:
    """A re-entrant lock, so a guarded method may call another guarded one."""
    return threading.RLock()


def open_connection(db_path: str) -> sqlite3.Connection:
    """Open a connection that may be used from any thread."""
    return sqlite3.connect(db_path, check_same_thread=False)


def serialized(method: Callable) -> Callable:
    """Run ``method`` while holding the instance's ``_lock``."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)

    return wrapper


def thread_safe(cls: type) -> type:
    """Guard every public method of ``cls`` with the instance's ``_lock``.

    ``__init__`` and other private helpers are left alone: they either run
    before the lock exists or are only ever reached from an already-guarded
    public method.
    """
    for name, attr in list(vars(cls).items()):
        if name.startswith("_") or isinstance(attr, (property, staticmethod, classmethod)):
            continue
        if callable(attr):
            setattr(cls, name, serialized(attr))
    return cls


__all__ = ["new_lock", "open_connection", "serialized", "thread_safe"]
