from service import Service
import os

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools


import logging
logger = logging.getLogger(__name__)


class Container():
    def __init__(self, service, account_id, gtm_key, cache=True):
        self.account_id = account_id
        self.gtm_key = gtm_key

        self.service = service
        self.gtmservice = service.gtmservice

        self.containers = []
        self.entity_type = 'container'
        self.get_entities = self.get_containers

        self.containers = self.service.get_cache(
            {
                "path": os.path.join(str(account_id), self.gtm_key),
                "type": self.entity_type,
                "get": self.get_entities
            }, cache
        )
        self.container = self.get_by_gtm_key()
        logger.info('Container ready')

    def get_containers(self):
        logger.info('get_containers')
        account_path = "accounts/{}".format(self.account_id)
        result = (
            self.service.execute(self.gtmservice.accounts()
                         .containers()
                         .list(parent=account_path)
                         )
        )
        return result

    def get_workspaces(self):
        return (
            self.service.execute(self.gtmservice.accounts()
            .containers()
            .workspaces()            
            .list(parent=self.container["path"])
            )
        )

    def get_workspace_by_name(self,name):
        workspace = self.get_workspaces()
        return [w for w in workspace['workspace'] if w['name']==name]

    def get_by_gtm_key(self):
        for container in self.containers["container"]:
            if container["publicId"] == self.gtm_key:
                return container
        raise Exception("Cant find '{}' container".format(self.gtm_key))

    def create_workspace(self, name):
        try:
            self.service.execute(self.gtmservice.accounts().containers().workspaces().create(
                parent=self.container["path"], body={"name": name, }
            ))
        except:
            raise Exception("Can not create workspace: '{}'".format(name))
