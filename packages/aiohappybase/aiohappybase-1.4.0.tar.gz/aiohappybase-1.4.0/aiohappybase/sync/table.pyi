from contextlib import *
from typing import *

from thriftpy2.transport import *
from thriftpy2.protocol import *
from thriftpy2.thrift import *

from ..table import *
from . import *


class Table:

    def __init__(self, name: bytes, connection: 'Connection'):
        ...

    @property
    def client(self):
        ...

    def __repr__(self):
        ...

    def families(self) -> Dict[bytes, Dict[str, Any]]:
        ...

    def column_family_names(self) -> List[bytes]:
        ...

    def _column_family_descriptors(self) -> Dict[bytes, Any]:
        ...

    def regions(self) -> List[Dict[str, Any]]:
        ...

    def row(self,
            row: bytes,
            columns: Iterable[bytes] = None,
            timestamp: int = None,
            include_timestamp: bool = False) -> Row:
        ...

    def rows(self,
             rows: List[bytes],
             columns: Iterable[bytes] = None,
             timestamp: int = None,
             include_timestamp: bool = False) -> List[Tuple[bytes, Row]]:
        ...

    def cells(self,
              row: bytes,
              column: bytes,
              versions: int = None,
              timestamp: int = None,
              include_timestamp: bool = False) -> ValuesWithTs:
        ...

    def scan(self,
             row_start: bytes = None,
             row_stop: bytes = None,
             row_prefix: bytes = None,
             columns: Iterable[bytes] = None,
             filter: bytes = None,
             timestamp: int = None,
             include_timestamp: bool = False,
             batch_size: int = 1000,
             scan_batching: int = None,
             limit: int = None,
             sorted_columns: bool = False,
             reverse: bool = False) -> Generator[Tuple[bytes, Data], None, None]:
        ...

    def put(self,
            row: bytes,
            data: Data,
            timestamp: int = None,
            wal: bool = True) -> None:
        ...

    def append(self,
               row: bytes,
               data: Dict[bytes, bytes],
               include_timestamp: bool = False) -> Row:
        ...

    def delete(self,
               row: bytes,
               columns: Iterable[bytes] = None,
               timestamp: int = None,
               wal: bool = True) -> None:
        ...

    def batch(self,
              timestamp: int = None,
              batch_size: int = None,
              transaction: bool = False,
              wal: bool = True) -> Batch:
        ...

    def counter_get(self, row: bytes, column: bytes) -> int:
        ...

    def counter_set(self,
                    row: bytes,
                    column: bytes,
                    value: int = 0) -> None:
        ...

    def counter_inc(self,
                    row: bytes,
                    column: bytes,
                    value: int = 1) -> int:
        ...

    def counter_dec(self,
                    row: bytes,
                    column: bytes,
                    value: int = 1) -> int:
        ...
