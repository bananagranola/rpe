#!/usr/bin/python
# ravelry api retrieval
# get() and url_to_string()

import base64
import logging
try: import simplejson as json
except ImportError: import json
import urllib2

logging.basicConfig()
logger = logging.getLogger('ravpatt')
logger.setLevel(logging.DEBUG)

class Ravelry:
	def __init__(self, accesskey, personalkey):
		self.accesskey = accesskey
		self.personalkey = personalkey

	def get_json(self, json_url):

		request = urllib2.Request(json_url)
		base64string = base64.encodestring('%s:%s' % (self.accesskey, self.personalkey)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % base64string)

		try: 
			requested = urllib2.urlopen(request)
		except urllib2.HTTPError, e:
			logger.error ('HTTPError: %s. URL: %s', str(e.args), json_url)
			return None

		try: 
			loaded = json.load(requested)
		except ValueError, e:
			logger.error ('ValueError: %s. URL: %s', str(e.args), json_url)
			return None
	
		return loaded

