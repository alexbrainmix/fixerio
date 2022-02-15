Test python client for fixer.io
============
JSON API for historical exchange rates published by the European Central Bank.

Free plan API usage: 100 requests per month

Edit get_cur.py, insert API_KEY for fixer.io

.. code:: python
	fixer = Fixerio(API_KEY)
	fixer.historical('2021-05-01','USD,MXN')