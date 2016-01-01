#!/usr/bin/python

import base64
import logging
import signal
try: import simplejson as json
except ImportError: import json
import StringIO
import sys
import urllib2

from auth_my import *
from ravelry import *
from unicodewriter import *

URL="https://api.ravelry.com/projects/{}/list.json"

logging.basicConfig()
logger = logging.getLogger('ravelry_pattern_exporter')
logger.setLevel(logging.DEBUG)

def signal_handler(signal, frame):
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def export(username):

    ravelry = Ravelry (ravelry_accesskey, ravelry_personalkey)
    
    data = ravelry.get_json(URL.format(username))

    try:
    	projects_data = data.get('projects', '-')
    except AttributeError, e:
			logger.error('AttributeError: %s.', str(e.args))
			return None

    projects_file = None

    try:
				si = StringIO.StringIO()
				csvwriter = UnicodeWriter(si)
    except IOError, e:
        logger.error('IOError: %s.', str(e.args))
        return None

    headed = False
    for project in projects_data:
        if headed == False:
            header = project.keys()
            csvwriter.writerow(header)
            headed = True

        try:
            csvwriter.writerow(project.values())
        except UnicodeEncodeError, e:
            logger.error('UnicodeEncodeError: %s.', str(e.args))

    return si.getvalue()

if __name__ == '__main__':
	try:
		username = sys.argv[1]
	except IndexError, e:
		username = "bananagranola"
	
	export(username)
