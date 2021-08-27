import sys
import logging
logger = logging.getLogger(__name__)

from entity import Entity

class Folder(Entity):
    def __init__(self, data, parent):
        Entity.__init__(self, data, parent)
        self.entity_type ='folders'

        self.depended_checks = {
            'tags':[],
            'triggers':[],
            'variables':[],
        }

    def get_id(self):
        return self.data['folderId']