import json
import unittest
# https://github.com/googleapis/google-api-python-client/blob/17c8516ba497849945fdabf37ae746b43229d53b/tests/test_mocks.py

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools


import httplib2

import os,sys
import inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from service import Service
from container import Container

from googleapiclient.http import RequestMockBuilder
from googleapiclient.http import HttpMock

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Set path to folder with tagmanager.dat file
os.environ["GTM_API_CONFIG_FOLDER"] = ""

# Set test account and key
account_id = 6004604474
gtm_key = "GTM-T57NB3S"
workspace_name = "Test workspase"

def datafile(filename):
    return os.path.join(DATA_DIR, filename)

def cachefile(filename):
    return os.path.join(os.environ["GTM_API_CONFIG_FOLDER"],'cache', account_id, gtm_key, filename)

def get_dict(path): 
    with open(path) as json_file:
        return json.load(json_file)

        
class TestService(unittest.TestCase):

    def test_cache(self):
        http = HttpMock(datafile("container.json"), {"status": "200"})

        service = Service(http)
        source_container = Container(service, account_id, gtm_key)
        # Check is Container saved to cache folder
        self.assertDictEqual(get_dict(datafile("container.json")), get_dict(cachefile('container.json')))


if __name__ == '__main__':
    unittest.main()