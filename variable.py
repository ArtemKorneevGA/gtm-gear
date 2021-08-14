import sys
import logging
logger = logging.getLogger(__name__)

from entity import Entity

class Variable(Entity):
    def __init__(self, data, parent):
        Entity.__init__(self, data, parent)
        self.entity_type ='variables'

        self.depended_checks = {
            'tags':['dependent_variables'],
            'triggers':['dependent_variables'],
            'variables':['dependent_variables'],
        }
