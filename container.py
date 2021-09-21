import os
from version import Version

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

        self.versions_headers = {}
        self.versions = []

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
        return self.service.get_containers(self.account_id)

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

    def init_versions(self):
        self.versions_headers = self.get_versions_list()
        self.versions = [Version(self, version['path']) for version in self.versions_headers['containerVersionHeader']]

    def get_versions_stat(self,from_version=None,to_version=None):
        stat = []
        self.init_versions()

        from_version = 1 if (from_version is None or from_version>to_version or to_version>len(self.versions)) else from_version
        to_version = to_version if to_version is not None and (to_version> from_version and from_version<= len(self.versions)) else len(self.versions)
        
        for version_num in range(from_version-1,to_version):
            self.versions[version_num].init()
  

        for version_num in range(from_version,to_version):
             version_stat = self.versions[version_num].compare(self.versions[version_num-1])
             stat.append(version_stat)
        return stat

    def get_versions_list(self):
        return (self.service.execute(getattr(self.gtmservice.accounts().containers(), 'version_headers')()
                .list(parent=self.container["path"])
        ))

    def get_versions(self, version_path):
        return (self.service.execute(getattr(self.gtmservice.accounts().containers(), 'versions')()
                .get(path=version_path)
        ))

