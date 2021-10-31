import sys
import logging
logger = logging.getLogger(__name__)

from .entity import Entity

class Template(Entity):
    def __init__(self, data, parent):
        Entity.__init__(self, data, parent)
        self.entity_type ='templates'
        self.id_name = "templateId"

        self.depended_checks = {
            'tags':[],
        }

