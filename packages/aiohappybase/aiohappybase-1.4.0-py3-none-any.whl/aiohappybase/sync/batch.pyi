from contextlib import *
from typing import *

from thriftpy2.transport import *
from thriftpy2.protocol import *
from thriftpy2.thrift import *

from ..batch import *
from . import *


class Batch:

    def __init__(self,
                 table: 'Table',
                 timestamp: int = None,
                 batch_size: int = None,
                 transaction: bool = False,
                 wal: bool = True):
        ...

    def send(self) -> None:
        ...

    def close(self) -> None:
        ...

    def __enter__(self):
        raise RuntimeError("Use with")

    def __exit__(self, *_exc):
        raise RuntimeError("Use with")
