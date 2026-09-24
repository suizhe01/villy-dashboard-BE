"""MySQL named locks, for work that must never run twice at the same time.

GET_LOCK belongs to the database session, not to a table, so it blocks nothing
but a second request asking for the same name. MySQL releases it by itself
when the session ends, and Django closes the session at the end of every
request, so a request that crashes mid-way cannot leave the lock held.
"""
from contextlib import contextmanager

from django.db import connection


class LockNotAcquired(Exception):
    pass


@contextmanager
def named_lock(name, timeout):
    """Hold the MySQL lock `name` for the duration of the block.

    Waits up to `timeout` seconds for another holder to finish, then raises
    LockNotAcquired. GET_LOCK returns NULL rather than 0 when it errors, which
    is treated as not acquired too.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT GET_LOCK(%s, %s)", [name, timeout])
        acquired = cursor.fetchone()[0] == 1

    if not acquired:
        raise LockNotAcquired(name)

    try:
        yield
    finally:
        with connection.cursor() as cursor:
            cursor.execute("SELECT RELEASE_LOCK(%s)", [name])


def is_lock_held(name):
    """Whether any session currently holds the MySQL lock `name`."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT IS_USED_LOCK(%s)", [name])
        return cursor.fetchone()[0] is not None
