"""

Haystack client.
Includes session and session management and basic get/put operations.
Supports basic authentication.
Supports SkySpark 3.0 SCRAM authentication.

Adapted from pyox project at ox-framework.org

"""

import requests
from cxhs.auth import SS3Auth
#import logging

CONTENT_TYPE_HEADERS_DICT = {
	"json": {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		},
	"zinc": {
		'Content-Type': 'text/zinc',
		'Accept': 'text/zinc',
		},
	"csv": {
		'Content-Type': 'text/csv',
		'Accept': 'text/csv',
		},

	#"zinc":
}

class HSession(object):

	def __init__(self, url, username = None, password = None, basic = True):
		""" Initialize instance, without establishing connection. Provide base URL """
		#  not been invoked yet
		# base URL
		self.url = url
		self.headers = {}
		self.contentTypeHeaders = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			#'Accept-Encoding': 'gzip, deflate',
		}
		self._contentType = 'json'
		self._basic = basic
		self._verbose = False

		self.session = requests.Session()
		# will contains the last response received
		self.response = None
		if username or basic:
			self.session.auth = (username, password)
		if not basic:
			self.session.auth = SS3Auth(username, password)

	@property
	def contentType(self):
		return self._contentType

	@contentType.setter
	def contentType(self, value):
		headers = CONTENT_TYPE_HEADERS_DICT.get(value)
		if not headers:
			raise ValueError("ContentType not supported: " % value)
		self._contentType = value
		self.contentTypeHeaders = headers

	@property
	def basic(self):
		return self._basic

	@basic.setter
	def basic(self, value):
		if type(value) != bool:
			raise ValueError("Basic auth flag must be T/F: %s" % value)
		self._basic = value

	@property
	def verbose(self):
		return self._verbose

	@verbose.setter
	def verbose(self, value):
		if type(value) != bool:
			raise ValueError("Verbose flag must be T/F: %s" % value)
		self._verbose = value

	def addHeader(self, name, value):
		""" Adds header that will be used for requests """
		self.headers[name] = value

	def post(self, url, body, timeout=None):
		""" Perform a POST request.
		TODO: fully implement and test this
		"""
		#import pdb
		#pdb.set_trace()
		if timeout==None:
			timeout = 3
		return self.doUrlRequest(url, body, 'POST', timeout)

	def get(self, url, timeout=None):
		""" Perform a GET request"""
		if timeout==None:
			timeout = 3
		return self.doUrlRequest(url,timeout)

	def put(self, url, body, timeout=None):
		""" Perform a PUT request using href with a body as target of PUT.
		TODO: fully implement and test this
		"""
		#url = obj.href
		#body = obj.toXML()
		if timeout==None:
			timeout = 3
		return self.doUrlRequest(url, body, 'PUT', timeout)

	#def __str__(self):
	#	logging.info('Session: %s' % self.url)

	#************** Private functions **************

	def doUrlRequest(self, url, body = None, method = 'GET', timeout=3):
		"""Perform url request.
		Args:
			url: url to request
			in: HTTP POST body (needed only for POST requests)
			method: HTTP method to use
		"""

		#request.add_header('Connection', 'keep-alive')
		#request.add_header('Content-Length', len(input))
		currentHeaders = self.contentTypeHeaders
		if self._verbose:
			print("%s %s" % (method, url))
		# merge with header set by user
		currentHeaders.update(self.headers)
		#print(method, "headers=", currentHeaders)
		try:
			if method == 'GET':
				res = self.session.get(url, headers=currentHeaders, timeout=timeout)
			elif method == 'POST':
				res = self.session.post(url, data=body, headers=currentHeaders, timeout=timeout)
			else:
				raise ValueError("Method %s is not supported right now." % method)

			self.response = res.status_code
			#print("sc:",res.status_code,"url:",url)
			content = res.text
		except Exception as err:
			raise Exception("Can't perform request to %s: %s" % (url, str(err)))
		#except httplib.BadStatusLine, err:
		#	raise Exception("BadStatusLine for %s: %s" % (url, err))
		#except httplib2.RedirectLimit, err:
		#	self.response = err.response
		#	content = err.content

		return content

