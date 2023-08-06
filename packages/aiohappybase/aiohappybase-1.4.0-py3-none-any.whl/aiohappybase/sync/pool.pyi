from contextlib import *
from typing import *

from thriftpy2.transport import *
from thriftpy2.protocol import *
from thriftpy2.thrift import *

from ..pool import *
from . import *


class ConnectionPool:

    QUEUE_TYPE = aio.LifoQueue

    def __init__(self, size: int, **kwargs):
        ...

    def close(self):
        ...

    def _queue_get(self, timeout: Real = None) -> Connection:
        ...

    def _acquire_connection(self, timeout: Real = None) -> Connection:
        ...

    def _return_connection(self, connection: Connection) -> None:
        ...

    @contextmanager
    def connection(self, timeout: Real = None) -> Connection:
        ...

    def __enter__(self) -> 'ConnectionPool':
        ...

    def __exit__(self, *_exc) -> None:
        ...

    def __del__(self) -> None:
        ...
