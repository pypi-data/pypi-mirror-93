from contextlib import *
from typing import *

from thriftpy2.transport import *
from thriftpy2.protocol import *
from thriftpy2.thrift import *

from ..connection import *
from . import *


class Connection:

    THRIFT_TRANSPORTS = dict(
        buffered=TBufferedTransportFactory(),
        framed=TFramedTransportFactory(),
    )
    THRIFT_PROTOCOLS = dict(
        binary=TBinaryProtocolFactory(decode_response=False),
        compact=TCompactProtocolFactory(decode_response=False),
    )
    THRIFT_CLIENTS = dict(
        socket=make_client,
        http=make_http_client,
    )

    def __init__(self,
                 host: str = DEFAULT_HOST,
                 port: int = DEFAULT_PORT,
                 timeout: int = None,
                 autoconnect: bool = False,
                 table_prefix: AnyStr = None,
                 table_prefix_separator: AnyStr = b'_',
                 compat: str = DEFAULT_COMPAT,
                 transport: str = DEFAULT_TRANSPORT,
                 protocol: str = DEFAULT_PROTOCOL,
                 client: str = DEFAULT_CLIENT,
                 **client_kwargs: Any):
        ...

    def _autoconnect(self):
        ...

    def _table_name(self, name: AnyStr) -> bytes:
        ...

    def open(self) -> None:
        ...

    def close(self) -> None:
        ...

    def table(self, name: AnyStr, use_prefix: bool = True) -> Table:
        ...

    def tables(self) -> List[bytes]:
        ...

    def create_table(self,
                     name: AnyStr,
                     families: Dict[str, Dict[str, Any]]) -> Table:
        ...

    def delete_table(self, name: AnyStr, disable: bool = False) -> None:
        ...

    def enable_table(self, name: AnyStr) -> None:
        ...

    def disable_table(self, name: AnyStr) -> None:
        ...

    def is_table_enabled(self, name: AnyStr) -> None:
        ...

    def compact_table(self, name: AnyStr, major: bool = False) -> None:
        ...

    def __enter__(self) -> 'Connection':
        ...

    def __exit__(self, *_exc) -> None:
        ...

    def __del__(self) -> None:
        ...
