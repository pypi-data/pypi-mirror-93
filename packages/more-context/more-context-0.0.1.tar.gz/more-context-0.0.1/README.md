# More Context

Context utilities

## Installation

    pip install more-context


## Usage

### Safe Context Manager

Like `@contextmanager`, but safe.

Code like this:

```python
@safe_context_manager
def my_ctx():
    lock = lock_resource()
    yield
    lock.delete()
```

Is equivalent to:

```python
@contextmanager
def my_ctx():
    lock = lock_resource()
    try:
        yield
    finally:
        lock.delete()
```
