"""
Safe Context Manager
"""

from contextlib import _GeneratorContextManager
from functools import wraps

# pylint: disable=too-few-public-methods
class _SafeGeneratorContextManager(_GeneratorContextManager):
    def __exit__(self, exc_type, value, traceback):
        try:
            next(self.gen)
        except StopIteration:
            pass
        else:
            raise RuntimeError("generator didn't stop")
        if exc_type is None:
            return False
        return super().__exit__(exc_type, value, traceback)


def safe_context_manager(func):
    """
    Like @contextmanager, but safe.

    Code like this:

        @safe_context_manager
        def my_ctx():
            lock = lock_resource()
            yield
            lock.delete()

    Is equivalent to:

        @contextmanager
        def my_ctx():
            lock = lock_resource()
            try:
                yield
            finally:
                lock.delete()
    """

    @wraps(func)
    def helper(*args, **kwds):
        return _SafeGeneratorContextManager(func, args, kwds)

    return helper
