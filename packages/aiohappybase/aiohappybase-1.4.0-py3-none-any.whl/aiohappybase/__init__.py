"""
AIOHappyBase, a developer-friendly Python library to interact asynchronously
with Apache HBase.
"""

__all__ = [
    'DEFAULT_HOST',
    'DEFAULT_PORT',
    'Connection',
    'Table',
    'Batch',
    'ConnectionPool',
    'NoConnectionsAvailable',
]

from . import _load_hbase_thrift  # noqa

from .connection import DEFAULT_HOST, DEFAULT_PORT, Connection
from .table import Table
from .batch import Batch
from .pool import ConnectionPool, NoConnectionsAvailable

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
