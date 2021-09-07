import httplib2
import os, json

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools

from ratelimit import limits, sleep_and_retry

from cache import Cache

import logging
logger = logging.getLogger(__name__)

REQUESTS_PER_PERIOD = 60
REQUESTS_PERIOD = 60
SLEEP_TIME_DEFAULT = 6

class Service:
    def __init__(self, http = None):
        if "GTM_API_CONFIG_FOLDER" in os.environ:
            self.config_folder = os.environ["GTM_API_CONFIG_FOLDER"]
        else:
            self.config_folder = "../configs"

        self.api_name = "tagmanager"
        self.api_version = "v2"
        self.scope = [
            "https://www.googleapis.com/auth/tagmanager.edit.containers"
        ]
        self.client_secrets_path = os.path.join(
            self.config_folder, "client_secrets.json"
        )
        self.sleep_time = SLEEP_TIME_DEFAULT
        self.repository_path = os.path.join(
            self.config_folder, "repository_path"
        )
        self.file_extension = "json"
        self.storage_path = os.path.join(self.config_folder, "tagmanager.dat")
        self.http = http
        self.gtmservice = self.getService()
        self.cache = Cache(self.config_folder)

    def getService(self):
        if not self.http:
            flow = client.flow_from_clientsecrets(
                self.client_secrets_path,
                scope=self.scope,
                message=tools.message_if_missing(self.client_secrets_path),
            )
            storage = file.Storage(self.storage_path)
            credentials = storage.get()
            if credentials is None or credentials.invalid:
                credentials = tools.run_flow(flow, storage, [])
            self.http = credentials.authorize(http=httplib2.Http())

        # Build the service object.
        service = build(self.api_name, self.api_version, http=self.http, cache_discovery=False)
        service.debug = False

        return service

    def get_cache(self, entity, cache = True):
        return self.cache.get_cache(entity, cache)


    def is_workspace_changed(self, workspace, entity_path):
        cache_file_path = self.cache.get_cache_file_path('workspace',entity_path)
        cache_file_folder = self.cache.get_cache_file_folder(entity_path)

        workspace_cache = self.cache.get_cache_file(cache_file_path)
        if workspace_cache and workspace_cache['fingerprint'] == workspace['fingerprint']:
            return True
        self.cache.save(cache_file_folder, cache_file_path, workspace)        
        return False

    def update_cache(self, entity_type, entity_path, data):
        self.cache.update_cache(entity_type, entity_path, data)

    @sleep_and_retry
    @limits(calls=REQUESTS_PER_PERIOD, period=REQUESTS_PERIOD)
    def execute(self, object):
        return object.execute()
