from entity import Entity
from utils import camel_case
import logging
logger = logging.getLogger(__name__)

class BuiltInVariable(Entity):
    def __init__(self, data, parent):
        Entity.__init__(self, data, parent)
        self.entity_type = 'built_in_variables'

        self.depended_checks = {
            'tags': ['dependent_built_in_variables'],
            'triggers': ['dependent_built_in_variables'],
            'variables': ['dependent_built_in_variables'],
        }

        self.path_additional_params = {'type': camel_case(self.name)}
