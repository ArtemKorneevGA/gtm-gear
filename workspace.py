import os, sys, json

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools

from datetime import date, timedelta
from time import sleep


import logging
logger = logging.getLogger(__name__)

from service import Service
from container import Container
from tag import Tag
from trigger import Trigger
from variable import Variable
from built_in_variable import BuiltInVariable

ENTITY_CONFIG = {
    'tags':{
        'className':'Tag',
        'key':'tag'
    }
    ,'triggers':{
        'className':'Trigger',
        'key':'trigger'
    }
    ,'variables':{
        'className':'Variable',
        'key':'variable'
    }
    ,'built_in_variables':{
        'className':'BuiltInVariable',
        'key':'builtInVariable'
    }
}

ENTITY_TYPES = list(ENTITY_CONFIG.keys())

class Workspace():
    def __init__(self, container, workspace_name="Default Workspace", cache=True, deps =['tags','triggers','variables','built_in_variables','folders','dependencies_for_tags','dependencies_for_triggers']):
        self.service = container.service
        self.gtmservice = container.gtmservice

        self.container = container.container
        self.gtm_key = container.gtm_key
        self.workspace_name = workspace_name
        self.cache = cache
        
        self.workspaces = []
        self.entity_type = 'workspace'
        self.get_entities = container.get_workspaces
        self.workspaces = self.service.get_cache(
            {
                "path": os.path.join(str(self.container['accountId']), self.gtm_key,workspace_name),
                "type": self.entity_type,
                "get": self.get_entities
            }, cache
        )


        self.workspace = self.get_by_name()

        logger.info('Worspace ready')

        self.tags = []
        self.triggers = []
        self.built_in_variables = []
        self.variables = []
        self.folders = []

        self.init()
        logger.info(f"tags: {len(self.tags)}")
        logger.info(f"triggers: {len(self.triggers)}")
        logger.info(f"variables: {len(self.variables)}")
        logger.info(f"built_in_variables: {len(self.built_in_variables)}")
        logger.info(f"Worspace deps loaded")

        logger.info('Worspace inited')




  

    def get_list(self, entity_type):
        return (self.service.execute(getattr(self.gtmservice.accounts().containers().workspaces(), entity_type)()
                .list(parent=self.workspace["path"])
                ))
 

    def get_entities_list(self, entity_type):
        def h():
            return self.get_list(entity_type)
        return h


    def get_by_name(self):
        if not self.workspace_name:
            self.workspace_name = "Default Workspace"
        for workspace in self.workspaces["workspace"]:
            if workspace["name"] == self.workspace_name:
                return workspace
        raise Exception("Cant find '{}' workspace".format(self.workspace_name))


    def init(self):
        for entity_type in ENTITY_TYPES:
            entities= self.service.get_cache(
                {
                    "path": os.path.join(str(self.container['accountId']), self.gtm_key,self.workspace_name),
                    "type": entity_type,
                    "get": self.get_entities_list(entity_type)
                }, self.cache
            )



            object = globals()[ENTITY_CONFIG[entity_type]['className']]
            key = ENTITY_CONFIG[entity_type]['key']
            setattr(self,entity_type, [object(entity, self) for entity in entities[key]])
            logger.info(f"{entity_type} inited")

    def get_tag(self, tag_name):
        for tag in self.tags:
            if tag.name == tag_name:
                return tag

    def delete(self,entity_type, entity_name):
        self.check_entity(entity_type)     
        entities = getattr(self, entity_type)
        setattr(self, entity_type,[entity for entity in entities if entity.name != entity_name])
        self.update_cache(entity_type)


    def update_cache(self,entity_type):
        self.check_entity(entity_type)
        entity_path = os.path.join(self.container['accountId'], self.gtm_key, self.workspace_name)

        data = {
           ENTITY_CONFIG[entity_type]['key']: [tag.data for tag in getattr(self, entity_type)]
        }
        self.service.update_cache(entity_type, entity_path, data)

    def get_depended(self,entity_type, entity_id, checks):
        self.check_entity(entity_type)

        result ={}
        result_len = 0

        for check_entity_type in checks.keys():
            result[check_entity_type]={}
            for check_property in checks[check_entity_type]:
                depended = [entity.name for entity in getattr(self, check_entity_type) if str(entity_id) in getattr(entity,check_property,[])]
                result_len += len(depended)
                result[check_entity_type][check_property] = depended
            result['len'] = result_len
        return result

    def check_entity(self,entity_type):
        if entity_type not in ENTITY_TYPES:
            raise ValueError(f"Can't update cach for entity: {entity_type}")   
