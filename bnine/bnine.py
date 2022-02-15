import os
import logging
import requests
import datetime
from dateutil import parser


# Enter API key for fixer.io
API_KEY = None

logging.basicConfig(filename=os.path.basename(__file__) + ".log",
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")
logging.getLogger("Fixerio").setLevel(logging.DEBUG)
logging.getLogger("Fixerio").addHandler(logging.StreamHandler())


class FixerioException(Exception):
   """ General Fixerio exception """

   def __init__(self, *args, **kwargs):
      Exception.__init__(self, *args, **kwargs)


class Fixerio(object):
	""" Class for Fixer.io """

	BASE_URL = "http://data.fixer.io/api/"
	LATEST = 'latest'
	SYMBOLS = 'symbols'
	CONVERT = 'convert'
	TIMESERIES = 'timeseries'
	FLUCTUATION = 'fluctuation'

	ACCESS_KEY = '?access_key='
	FORMAT = "%Y-%m-%d"

	def __init__(self, access_key=None):
		"""
		:param access_key: your API Key.
		:type access_key: str.
		"""
		if access_key is None:
			raise FixerioException('Get API KEY at https://fixer.io')
		self.key_str = self.ACCESS_KEY + access_key
		self.is_connection = self._ping()
	
	def _ping(self):
		""" 
		Test connectivity to API.
		:raises: FixerioException
		"""
		return self._request_api(self._create_api_uri())

	def _request_api(self, url):
		logging.debug(url)
		response = requests.get(url)
		return response.json()

	def _create_api_uri(self, method=LATEST, **kwargs):
		param = ""
		if kwargs:
			param = '&'+'&'.join('%s=%s' % item for item in kwargs.items())
		url = self.BASE_URL + method + self.key_str + param
		return url

	def timeseries(self, start_date, end_date, symbols, base='EUR'):
		start_date_str = parser.parse(start_date).strftime(self.FORMAT)
		end_date_str = parser.parse(end_date).strftime(self.FORMAT)
		url = self._create_api_uri(self.TIMESERIES, start_date=start_date, end_date=end_date, symbols=symbols, base=base)
		return self._request_api(url)

	def historical(self, date, symbols, base='EUR'):
		date_str = parser.parse(date).strftime(self.FORMAT)
		url = self._create_api_uri(date_str, symbols=symbols, base=base)
		return self._request_api(url)


def main():
	fixer = Fixerio(API_KEY)
	logging.info(fixer.is_connection)
	r = fixer.historical('2021-05-01','USD,MXN')
	logging.info(r)

if __name__ == '__main__':
    main()