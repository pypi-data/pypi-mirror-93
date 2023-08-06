============
AIOHappyBase
============

.. py:currentmodule:: aiohappybase

**AIOHappyBase** is a developer-friendly Python__ library to interact with `Apache
HBase`__. AIOHappyBase is designed for use in standard HBase setups, and offers
application developers a Pythonic API to interact with HBase. Below the surface,
AIOHappyBase uses the `Python ThriftPy2 library`__ to connect to HBase using
its Thrift__ gateway, which is included in the standard HBase 0.9x releases.

__ http://python.org/
__ http://hbase.apache.org/
__ http://pypi.python.org/pypi/thriftpy2
__ http://thrift.apache.org/


.. note::

    **From the original HappyBase author, Wouter Bolsterlee:**

    **Do you enjoy HappyBase?** Great! You should know that I don't use HappyBase
    myself anymore, but still maintain it because it's quite popular. Please
    consider making a small donation__ to let me know you appreciate my work.
    Thanks!

    __ https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZJ9U8DNN6KZ9Q


Example
=======

The example below illustrates basic usage of the library. The :doc:`user guide
<user>` contains many more examples.

::

    from aiohappybase import Connection

    async def main():

        async with Connection('hostname') as connection:
            table = connection.table('table-name')

            await table.put(b'row-key', {
                b'family:qual1': b'value1',
                b'family:qual2': b'value2',
            })

            row = await table.row(b'row-key')
            print(row[b'family:qual1'])  # prints 'value1'

            for key, data in await table.rows([b'row-key-1', b'row-key-2']):
               print(key, data)  # prints row key and data for each row

            async for key, data in table.scan(row_prefix=b'row'):
               print(key, data)  # prints 'value1' and 'value2'

            await table.delete(b'row-key')


Core documentation
==================

.. toctree::
    :maxdepth: 2

    installation
    user
    api
    sync_api


Additional documentation
========================

.. toctree::
    :maxdepth: 1

    news
    development
    todo
    faq
    license


External links
==============

* `Online Documentation <https://aiohappybase.readthedocs.io/>`_ (Read the Docs)
* `Downloads <http://pypi.python.org/pypi/aiohappybase/>`_ (PyPI)
* `Source Code <https://github.com/python-happybase/aiohappybase>`_ (Github)

* `HappyBase Online Documentation <https://happybase.readthedocs.io/>`_ (Read the Docs)
* `HappyBase Downloads <http://pypi.python.org/pypi/happybase/>`_ (PyPI)
* `HappyBase Source Code <https://github.com/python-happybase/happybase>`_ (Github)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. vim: set spell spelllang=en:
